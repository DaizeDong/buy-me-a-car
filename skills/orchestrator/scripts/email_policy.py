#!/usr/bin/env python3
"""Render and verify constrained dealer drafts from private, approved inputs.

An arbitrary model-written email is not a verified draft. The model selects IDs;
this module renders approved asks and evidence-backed anchor records. Evidence
hashes prove local artifact integrity, not that a dealer or listing is authentic.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


class PolicyError(ValueError):
    """A draft cannot be verified against its approved inputs."""


def _amount(value) -> Decimal:
    if isinstance(value, bool):
        raise PolicyError("invalid_amount")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PolicyError("invalid_amount") from exc
    if not result.is_finite() or result <= 0 or result > Decimal("1000000000"):
        raise PolicyError("invalid_amount")
    if result != result.quantize(Decimal("0.01")):
        raise PolicyError("invalid_amount")
    return result


def _text(value, code="invalid_text") -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise PolicyError(code)
    if not value.isascii() or re.search(r"[\x00-\x1f\x7f`]|\*\*|\[[^]]+\]\(", value):
        raise PolicyError(code)
    return value


def _date(value) -> datetime:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError, TypeError) as exc:
        raise PolicyError("invalid_evidence_time") from exc
    if result.tzinfo is None:
        raise PolicyError("invalid_evidence_time")
    return result


def _indexed(items, code):
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        raise PolicyError(code)
    result = {}
    for item in items:
        ident = _text(item.get("id"), code)
        if ident in result:
            raise PolicyError(code)
        result[ident] = item
    return result


def _anchor(record: dict, vehicle_class: str, now: datetime) -> str:
    if record.get("vehicle_class") != vehicle_class:
        raise PolicyError("anchor_vehicle_class_mismatch")
    dealer = _text(record.get("dealer"))
    vehicle = _text(record.get("vehicle"))
    basis = record.get("basis")
    if basis not in {"listing", "written_otd"}:
        raise PolicyError("unsupported_anchor_basis")
    amount = _amount(record.get("amount"))
    evidence = record.get("evidence")
    if not isinstance(evidence, dict) or evidence.get("confirmed_by_user") is not True:
        raise PolicyError("anchor_evidence_unconfirmed")
    source_id = _text(evidence.get("source_id"), "anchor_source_missing")
    source_text = evidence.get("text")
    if not isinstance(source_text, str) or not source_text.strip():
        raise PolicyError("anchor_source_missing")
    digest = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    if evidence.get("sha256") != digest:
        raise PolicyError("anchor_evidence_hash_mismatch")
    observed = _date(evidence.get("observed_at"))
    expires = _date(evidence.get("expires_at"))
    if not observed <= now <= expires:
        raise PolicyError("anchor_evidence_stale")
    # The confirmed extract must identify the same seller, vehicle, price basis,
    # and amount. The source ID is retained in the private record, never the mail.
    del source_id
    label = "OTD" if basis == "written_otd" else "ask"
    required = [dealer, vehicle, label, f"${amount:,.2f}"]
    if any(term.casefold() not in source_text.casefold() for term in required):
        raise PolicyError("anchor_evidence_fields_mismatch")
    return f"{dealer} lists {vehicle} at ${amount:,.2f} {label}." if basis == "listing" else (
        f"{dealer} quoted ${amount:,.2f} out-the-door (OTD) for {vehicle} in writing."
    )


def _privacy(body: str, policy: dict) -> None:
    walk = _amount(policy.get("walk_away"))
    for token in re.findall(r"(?<![\w.])\$?(\d[\d,]*(?:\.\d+)?\s*[kK]?)(?![\w.])", body):
        numeric = token.strip().replace(",", "")
        amount = Decimal(numeric[:-1]) * 1000 if numeric.lower().endswith("k") else Decimal(numeric)
        if amount == walk:
            raise PolicyError("private_ceiling_disclosed")
    compact = re.sub(r"\W", "", body.casefold())
    values = policy.get("private_values")
    if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
        raise PolicyError("private_values_required")
    for value in values:
        normalized = re.sub(r"\W", "", value.casefold())
        if value.casefold() in body.casefold() or (normalized and normalized in compact):
            raise PolicyError("private_value_disclosed")
    if re.search(r"walk[ _-]?away|hard cap|budget (?:cap|ceiling)|maximum budget", body, re.I):
        raise PolicyError("private_budget_language")


def render_draft(plan: dict, policy: dict, *, now: datetime | None = None) -> str:
    """Render approved content; unknown keys and unapproved offers fail closed."""
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        raise PolicyError("unsupported_policy")
    if not isinstance(plan, dict) or set(plan) != {"ask_ids", "anchor_ids", "include_offer"}:
        raise PolicyError("invalid_plan")
    ask_ids, anchor_ids = plan["ask_ids"], plan["anchor_ids"]
    if (not isinstance(ask_ids, list) or not 1 <= len(ask_ids) <= 3
            or any(not isinstance(item, str) for item in ask_ids)
            or len(set(ask_ids)) != len(ask_ids)):
        raise PolicyError("invalid_ask_selection")
    if (not isinstance(anchor_ids, list) or len(anchor_ids) > 1
            or any(not isinstance(item, str) for item in anchor_ids)):
        raise PolicyError("invalid_anchor_selection")
    if type(plan["include_offer"]) is not bool:
        raise PolicyError("invalid_offer_selection")
    if policy.get("vehicle_class") not in {"new", "used"}:
        raise PolicyError("invalid_vehicle_class")
    asks = _indexed(policy.get("approved_asks"), "invalid_approved_asks")
    anchors = _indexed(policy.get("anchors"), "invalid_anchors")
    body = [f"Hi {_text(policy.get('rep_name'))},", ""]
    for index, ident in enumerate(ask_ids, 1):
        ask = asks.get(ident)
        if not ask or ask.get("approved_by_user") is not True:
            raise PolicyError("ask_not_approved")
        body.append(f"{index}) {_text(ask.get('text'))}")
    if plan["include_offer"]:
        offer = policy.get("authorized_offer")
        if not isinstance(offer, dict) or offer.get("authorized_by_user") is not True:
            raise PolicyError("offer_not_authorized")
        amount = _amount(offer.get("amount"))
        if amount >= _amount(policy.get("walk_away")):
            raise PolicyError("offer_reaches_private_ceiling")
        body += ["", f"My offer is ${amount:,.2f} out-the-door (OTD), subject to the written terms and inspection."]
    for ident in anchor_ids:
        if ident not in anchors:
            raise PolicyError("anchor_not_found")
        body += ["", _anchor(anchors[ident], policy["vehicle_class"], now or datetime.now(timezone.utc))]
    body += ["", "If that does not work, I will continue my search.", "", "Thanks,", _text(policy.get("buyer_name"))]
    rendered = "\n".join(body) + "\n"
    _privacy(rendered, policy)
    return rendered


def validate_draft(body: str, plan: dict, policy: dict, *, now: datetime | None = None) -> dict:
    """A successful result verifies only this exact rendered body and input policy."""
    try:
        expected = render_draft(plan, policy, now=now)
        if not isinstance(body, str):
            raise PolicyError("invalid_body")
        _privacy(body, policy)
        if body != expected:
            raise PolicyError("body_differs_from_approved_plan")
    except PolicyError as exc:
        return {"status": "blocked", "errors": [str(exc)], "send_authorized": False}
    return {"status": "verified", "errors": [], "sha256": hashlib.sha256(body.encode()).hexdigest(),
            "send_authorized": False, "qualitative_review": "unavailable"}


def main() -> int:
    from tools.runtime_paths import DataBoundaryError, data_path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True, help="private data-relative JSON policy")
    parser.add_argument("--plan", required=True, help="private data-relative JSON draft plan")
    parser.add_argument("--output", required=True, help="private data-relative rendered draft file")
    args = parser.parse_args()
    try:
        policy_path, plan_path = data_path(args.policy), data_path(args.plan)
        if policy_path is None or plan_path is None:
            raise PolicyError("private_data_uninitialized")
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        body = render_draft(plan, policy)
        result = validate_draft(body, plan, policy)
        data_path(args.output, for_write=True).write_text(body, encoding="utf-8")
        print(json.dumps(result))
        return 0
    except (DataBoundaryError, PolicyError, OSError, ValueError) as exc:
        print(json.dumps({"status": "blocked", "error_type": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
