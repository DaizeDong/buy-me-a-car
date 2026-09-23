#!/usr/bin/env python3
"""Durable inbox import/export ledger. This module does not connect to Gmail.

Providers import complete message pages and reconcile draft receipts by stable
operation ID. Export durably marks an operation uncertain before releasing its
payload. Neither a timeout nor a process restart authorizes replay.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Protocol

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from email_policy import render_draft, validate_draft
from tools.runtime_paths import DataBoundaryError, data_path


class StateError(ValueError):
    """Invalid input or a ledger conflict; no side effect is authorized."""


class StateBusy(StateError):
    """Another process owns this ledger's exclusive lock."""


class DraftAdapter(Protocol):
    """A host adapter must deduplicate operation_id and return a verified receipt.

    On uncertain provider execution, reconcile by operation ID; never invoke
    create_draft again just because the local call did not return a receipt.
    """

    def create_draft(self, operation: dict) -> dict: ...


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(value) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _id(value) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 1024:
        raise StateError("invalid_identifier")
    return value


@contextmanager
def _locked(path: Path):
    # OS locks are released if the process dies; a stale lock file is harmless.
    with path.open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise StateBusy("ledger_locked") from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, value: dict) -> None:
    """Replace one complete JSON state; fsync data before committing the name."""
    payload = (_json(value) + "\n").encode("utf-8")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if os.name != "nt":
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class InboxState:
    def __init__(self, account_id: str, relative: str = "inbox/state.json"):
        self.account_id = _id(account_id)
        self.relative = relative

    @contextmanager
    def _transaction(self):
        # Resolve on every operation so a changed junction/config is rechecked.
        path = data_path(self.relative, for_write=True)
        lock = data_path(self.relative + ".lock", for_write=True)
        with _locked(lock):
            if path.exists():
                state = json.loads(path.read_text(encoding="utf-8"))
                if (state.get("schema_version") != 1 or state.get("account_id") != self.account_id
                        or not isinstance(state.get("messages"), dict)
                        or not isinstance(state.get("operations"), dict)):
                    raise StateError("invalid_or_wrong_account_ledger")
            else:
                state = {"schema_version": 1, "account_id": self.account_id, "revision": 0,
                         "cursor": None, "messages": {}, "operations": {}}
            before = _json(state)
            yield state
            if _json(state) != before:
                state["revision"] += 1
                atomic_write(path, state)

    def snapshot(self) -> dict:
        path = data_path(self.relative)
        if path is None or not path.exists():
            return {"schema_version": 1, "account_id": self.account_id, "revision": 0,
                    "cursor": None, "messages": {}, "operations": {}, "initialized": False}
        with self._transaction() as state:
            return json.loads(_json(state))

    def import_batch(self, batch: dict) -> dict:
        if not isinstance(batch, dict) or batch.get("account_id") != self.account_id:
            raise StateError("account_mismatch")
        if batch.get("complete") is not True:
            raise StateError("incomplete_provider_page")
        before, after = batch.get("cursor_before"), _id(batch.get("cursor_after"))
        if before is not None:
            _id(before)
        messages = batch.get("messages")
        if not isinstance(messages, list):
            raise StateError("invalid_messages")
        incoming = {}
        for message in messages:
            if not isinstance(message, dict):
                raise StateError("invalid_message")
            ident = _id(message.get("message_id"))
            _id(message.get("thread_id"))
            _id(message.get("sender"))
            if not isinstance(message.get("text"), str) or message.get("body_complete") is not True:
                raise StateError("message_body_incomplete")
            if ident in incoming and incoming[ident] != message:
                raise StateError("conflicting_message_id")
            incoming[ident] = message
        with self._transaction() as state:
            for ident, message in incoming.items():
                existing = state["messages"].get(ident)
                if existing and existing["payload_sha256"] != _hash(message):
                    raise StateError("conflicting_message_id")
            if state["cursor"] != before:
                if state["cursor"] == after and all(ident in state["messages"] for ident in incoming):
                    return {"status": "duplicate", "imported": 0, "cursor": after}
                raise StateError("cursor_conflict")
            added = 0
            for ident, message in incoming.items():
                if ident not in state["messages"]:
                    state["messages"][ident] = {"payload": message, "payload_sha256": _hash(message),
                                                "status": "received", "triage": None, "operation_id": None}
                    added += 1
            state["cursor"] = after
            return {"status": "imported", "imported": added, "cursor": after}

    def record_triage(self, message_id: str, category: str) -> dict:
        if category not in {"real_reply", "ooo", "crm", "spam", "needs_review"}:
            raise StateError("invalid_triage")
        with self._transaction() as state:
            message = state["messages"].get(message_id)
            if not message:
                raise StateError("unknown_message")
            if message["triage"] is not None:
                if message["triage"] != category:
                    raise StateError("triage_already_recorded")
                return {"status": message["status"]}
            message["triage"] = category
            message["status"] = "needs_draft" if category == "real_reply" else "review" if category == "needs_review" else "processed"
            return {"status": message["status"]}

    def prepare_draft(self, message_id: str, plan: dict, policy: dict) -> dict:
        body = render_draft(plan, policy)
        verification = validate_draft(body, plan, policy)
        if verification["status"] != "verified":
            raise StateError("draft_validation_failed")
        with self._transaction() as state:
            message = state["messages"].get(message_id)
            if not message or message["triage"] != "real_reply":
                raise StateError("message_not_ready_for_draft")
            previous = message["operation_id"]
            if previous:
                operation = state["operations"][previous]
                if operation["body_sha256"] != verification["sha256"]:
                    raise StateError("existing_draft_requires_reconciliation")
                return {"operation_id": previous, "status": operation["status"]}
            thread_id = message["payload"]["thread_id"]
            if any(op["thread_id"] == thread_id and op["status"] in {"prepared", "uncertain"}
                   for op in state["operations"].values()):
                raise StateError("thread_has_pending_draft")
            operation_id = _hash([self.account_id, message_id, verification["sha256"]])
            state["operations"][operation_id] = {
                "operation_id": operation_id, "account_id": self.account_id,
                "message_id": message_id, "reply_to_message_id": message_id, "thread_id": thread_id,
                "recipient": message["payload"]["sender"], "body": body,
                "body_sha256": verification["sha256"], "status": "prepared", "receipt": None,
                "action": "create_draft", "send_authorized": False,
            }
            message["operation_id"] = operation_id
            message["status"] = "draft_prepared"
            return {"operation_id": operation_id, "status": "prepared"}

    def export_operation(self, operation_id: str) -> dict:
        with self._transaction() as state:
            operation = state["operations"].get(operation_id)
            if not operation or operation["status"] != "prepared":
                raise StateError("operation_not_exportable_reconcile_instead")
            operation["status"] = "uncertain"
            state["messages"][operation["message_id"]]["status"] = "draft_uncertain"
            exported = json.loads(_json(operation))
        # The transaction has committed before a provider sees the payload.
        return exported

    def import_receipt(self, receipt: dict) -> dict:
        if not isinstance(receipt, dict) or receipt.get("account_id") != self.account_id:
            raise StateError("receipt_account_mismatch")
        operation_id = _id(receipt.get("operation_id"))
        if receipt.get("status") not in {"draft_saved", "not_created"}:
            raise StateError("invalid_receipt_status")
        if receipt["status"] == "draft_saved":
            _id(receipt.get("external_draft_id"))
        _id(receipt.get("provider_receipt_id"))
        with self._transaction() as state:
            operation = state["operations"].get(operation_id)
            if not operation or receipt.get("body_sha256") != operation["body_sha256"]:
                raise StateError("receipt_does_not_match_operation")
            if operation["receipt"] is not None:
                if operation["receipt"] != receipt:
                    raise StateError("conflicting_receipt")
                return {"status": operation["status"], "duplicate": True}
            if operation["status"] != "uncertain":
                raise StateError("receipt_before_export")
            operation["receipt"] = receipt
            operation["status"] = receipt["status"]
            state["messages"][operation["message_id"]]["status"] = receipt["status"]
            return {"status": receipt["status"], "duplicate": False}

    def execute_once(self, operation_id: str, adapter: DraftAdapter) -> dict:
        operation = self.export_operation(operation_id)
        # Propagate errors. The durable uncertain state must survive a timeout.
        return self.import_receipt(adapter.create_draft(operation))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["import", "status", "triage", "prepare", "export", "receipt"])
    parser.add_argument("--account-id", required=True, help="provider's stable account ID")
    parser.add_argument("--state", default="inbox/state.json", help="private data-relative ledger")
    parser.add_argument("--input", help="private data-relative JSON payload")
    parser.add_argument("--output", help="private data-relative operation export (required for export)")
    args = parser.parse_args()
    try:
        store = InboxState(args.account_id, args.state)
        payload = None
        if args.input:
            path = data_path(args.input)
            if path is None:
                raise StateError("private_data_uninitialized")
            payload = json.loads(path.read_text(encoding="utf-8"))
        if args.action == "status":
            snapshot = store.snapshot()
            counts = {}
            for message in snapshot["messages"].values():
                counts[message["status"]] = counts.get(message["status"], 0) + 1
            result = {"status": "offline_ledger" if snapshot.get("initialized", True) else "uninitialized",
                      "revision": snapshot["revision"], "counts": counts, "live_gmail": False}
        elif args.action == "import":
            result = store.import_batch(payload)
        elif args.action == "triage":
            result = store.record_triage(**payload)
        elif args.action == "prepare":
            result = store.prepare_draft(**payload)
        elif args.action == "receipt":
            result = store.import_receipt(payload)
        else:
            if not args.output:
                raise StateError("private_output_required")
            output = data_path(args.output, for_write=True)
            if output.exists() or output in {
                    data_path(args.state, for_write=True), data_path(args.state + ".lock", for_write=True)}:
                raise StateError("export_output_must_be_new_and_separate")
            operation = store.export_operation(payload["operation_id"])
            atomic_write(output, operation)
            result = {"status": "uncertain", "operation_id": operation["operation_id"]}
        print(json.dumps(result))
        return 0
    except (DataBoundaryError, StateError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "blocked", "error_type": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
