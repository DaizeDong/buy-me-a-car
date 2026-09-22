#!/usr/bin/env python3
"""Generate a validated synthetic demonstration or private evidence-based dossier.

Use --mode demo with a generated dossier_config_template YAML, or --mode live
with config/evidence/output paths inside the proven private companion DATA.
The live path uses tools.runtime_paths; there is no public-worktree fallback.
All config text is escaped. Shipped EN/CN/ES templates supply the markup.
PDF output is staged, parsed, and checked before replacing an existing file.
"""
import argparse
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def load_config(path):
    """Load YAML (preferred) or JSON config. Always reads as UTF-8 explicitly."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if str(path).endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            sys.exit("Error: PyYAML required for YAML configs. pip install pyyaml")
        return yaml.safe_load(text)
    elif str(path).endswith(".json"):
        return json.loads(text)
    else:
        # Best-effort: try YAML first, fall back to JSON
        try:
            import yaml
            return yaml.safe_load(text)
        except ImportError:
            return json.loads(text)


def flatten_dict(d, parent_key="", sep="."):
    """Flatten nested dict so YAML structure like {buyer: {name: X}} becomes {buyer.name: X}."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # For lists, expand to indexed keys: comps -> comps.0, comps.1, ...
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}.{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}.{i}", str(item)))
            # Also keep the joined version
            items.append((new_key, ", ".join(str(x) for x in v if not isinstance(x, dict))))
        else:
            items.append((new_key, "" if v is None else str(v)))
    return dict(items)


PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")


# Fields that must be present and non-empty for a dossier to be dealer-actionable.
# Distinct from "any {{KEY}} not filled", these are dossier-correctness invariants.
LOAD_BEARING_KEYS = [
    "BUYER_NAME",
    "BUYER_ADDRESS",   # zip-bearing, sets registering-state context
    "DATE",
    "YEAR",
    "MAKE_MODEL",
    "TARGET_OTD",
    "STATE",
    "TAX_RATE",
]

# At minimum the dossier must show this many dealer comparison rows
MIN_DEALER_QUOTES = 2  # COMP_VEH_1 .. COMP_VEH_N

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "skills/orchestrator/assets"
CENT = Decimal("0.01")
MONEY_KEYS = ("PROPOSED_SALES", "TARGET_OTD", "ASK_OTD", "TAX_BASE", "TAX_AMOUNT",
              "REG_AMOUNT", "TITLE_AMOUNT", "DOC_AMOUNT", "OTHER_FEES",
              "TRADE_IN_CREDIT", "REBATE_AMOUNT")
RESERVED_KEYS = {"QUOTE_ROWS", "EVIDENCE_ROWS", "NUM_COMPETING_OFFERS", "DOSSIER_NOTICE", "PAGE_NOTICE_CSS"}
PROPOSAL_KEYS = {"TITLE", "DATE", "DOSSIER_MODE", "SYNTHETIC", "LANGUAGE", "TARGET_OTD", "PROPOSED_SALES"}
EVIDENCE_KINDS = {"dealer_quote", "listing", "official", "buyer_statement"}
ANALYSIS_KEYS = ("EXEC_SUMMARY_PARAGRAPH_1", "EXEC_SUMMARY_PARAGRAPH_2",
                 "SUPPORT_POINT_1", "SUPPORT_POINT_2", "SUPPORT_POINT_3", "SUPPORT_POINT_4",
                 "TRIM_ANALYSIS_PARA", "INTERNAL_ANCHOR_PARA", "CLOSING_PARAGRAPH")


def _private_path(path, *, for_write=False):
    """Use the shared private companion boundary for every live dossier path."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from tools.runtime_paths import validate_data_path
    return validate_data_path(path, for_write=for_write)


def _demo_configs():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from tools.fixture_recipes.dossier import demo_config
    return [demo_config(language) for language in ("en", "cn", "es")]


def _decimal(value, field, *, signed=False, money=True):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{field}: expected a decimal amount")
    text = str(value).strip()
    pattern = r"-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?" if signed else r"(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?"
    if not re.fullmatch(pattern, text):
        raise ValueError(f"{field}: invalid decimal amount")
    try:
        amount = Decimal(text.replace(",", ""))
        if not amount.is_finite() or abs(amount) > Decimal("1000000000"):
            raise ValueError(f"{field}: amount outside supported range")
        if money and amount != amount.quantize(CENT):
            raise ValueError(f"{field}: amounts must have at most two decimal places")
    except InvalidOperation as exc:
        raise ValueError(f"{field}: invalid decimal amount") from exc
    return amount


def _iso_date(value, field):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{field}: expected YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field}: invalid date") from exc


def extract_template_keys(template):
    """Return the set of all {{KEY}} placeholders referenced in the template."""
    return set(PLACEHOLDER_PATTERN.findall(template))


def validate_config_sanity(config, *, today=None):
    """Validate arithmetic and dated evidence; this does not fact-check source contents."""
    errors = []
    if not isinstance(config, dict):
        return ["config must be an object"]
    if any(not isinstance(key, str) for key in config):
        return ["config keys must be strings"]
    mode = config.get("DOSSIER_MODE")
    if mode not in ("demo", "live"):
        errors.append("DOSSIER_MODE must be demo or live")
    if config.get("SYNTHETIC") is not (mode == "demo"):
        errors.append("SYNTHETIC must be true only in demo mode")
    for k in LOAD_BEARING_KEYS:
        val = config.get(k)
        if val is None or not str(val).strip():
            errors.append(f"missing or empty load-bearing field: {k}")
    for key in ANALYSIS_KEYS:
        value = config.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing or empty analysis: {key}")
    for key in config:
        if key in RESERVED_KEYS or key.startswith("COMP_") or key.startswith("SOURCE_LINK_"):
            errors.append(f"{key} is derived; use QUOTES and EVIDENCE")
    if not re.fullmatch(r"[A-Z]{2}", str(config.get("STATE", ""))):
        errors.append("STATE must be a two-letter registration jurisdiction")
    numbers = {}
    for key in MONEY_KEYS + ("TAX_ADJUSTMENT", "TAX_RATE"):
        try:
            numbers[key] = _decimal(config.get(key), key, signed=key == "TAX_ADJUSTMENT", money=key != "TAX_RATE")
        except ValueError as exc:
            errors.append(str(exc))
    if all(key in numbers for key in MONEY_KEYS):
        total = sum(numbers[key] for key in ("PROPOSED_SALES", "TAX_AMOUNT", "REG_AMOUNT", "TITLE_AMOUNT", "DOC_AMOUNT", "OTHER_FEES"))
        total -= numbers["TRADE_IN_CREDIT"] + numbers["REBATE_AMOUNT"]
        if total != numbers["TARGET_OTD"]:
            errors.append(f"offer components total {total:.2f}, not TARGET_OTD {numbers['TARGET_OTD']:.2f}")
        if numbers["TARGET_OTD"] <= 0 or numbers["PROPOSED_SALES"] <= 0 or numbers["ASK_OTD"] <= 0:
            errors.append("sales price, asking OTD, and target OTD must be positive")
    if all(key in numbers for key in ("TAX_BASE", "TAX_RATE", "TAX_ADJUSTMENT", "TAX_AMOUNT")):
        rate = numbers["TAX_RATE"]
        if rate > 100:
            errors.append("TAX_RATE must be a percentage from 0 to 100")
        tax = (numbers["TAX_BASE"] * rate / 100).quantize(CENT, rounding=ROUND_HALF_UP) + numbers["TAX_ADJUSTMENT"]
        if tax < 0 or tax != numbers["TAX_AMOUNT"]:
            errors.append(f"TAX_AMOUNT must equal rounded TAX_BASE * TAX_RATE / 100 + TAX_ADJUSTMENT ({tax:.2f})")
    current = today or date.today()
    try:
        dossier_date = _iso_date(config.get("DATE"), "DATE")
        if dossier_date > current:
            errors.append("DATE cannot be in the future")
        if mode == "live" and dossier_date != current:
            errors.append("live DATE must be today's date; refresh evidence before generating")
    except ValueError as exc:
        errors.append(str(exc))
        dossier_date = current
    evidence = config.get("EVIDENCE")
    if not isinstance(evidence, list) or not evidence:
        errors.append("EVIDENCE must contain structured source records")
        evidence = []
    sources = {}
    supported = set()
    for record in evidence:
        if not isinstance(record, dict):
            errors.append("each EVIDENCE entry must be an object")
            continue
        ident = record.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", ident) or ident in sources:
            errors.append("evidence IDs must be nonempty, unique letters/digits/hyphens/underscores")
            continue
        sources[ident] = record
        kind = record.get("kind")
        if not isinstance(kind, str) or kind not in ({"synthetic"} if mode == "demo" else EVIDENCE_KINDS):
            errors.append(f"evidence {ident}: kind is invalid for {mode} mode")
        source = record.get("source")
        if not isinstance(source, str) or not source.strip():
            errors.append(f"evidence {ident}: source is required")
        elif kind != "buyer_statement" and not re.fullmatch(r"https://[^\s]+", source):
            errors.append(f"evidence {ident}: public source must be an https URL")
        try:
            observed = _iso_date(record.get("source_date"), f"evidence {ident} source_date")
            age = ((current if mode == "live" else dossier_date) - observed).days
            if age < 0 or (mode == "live" and age > (14 if kind in ("dealer_quote", "listing") else 90)):
                errors.append(f"evidence {ident}: source date is future or stale")
        except ValueError as exc:
            errors.append(str(exc))
        supports = record.get("supports")
        if not isinstance(supports, list) or not supports or any(not isinstance(item, str) or not item.strip() for item in supports):
            errors.append(f"evidence {ident}: supports must list fields or quote:<id>")
        else:
            supported.update(supports)
        if mode == "live":
            artifact = record.get("artifact")
            digest = record.get("sha256")
            if not isinstance(artifact, str) or not artifact.strip() or not isinstance(digest, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
                errors.append(f"evidence {ident}: private artifact path and SHA-256 are required")
            else:
                try:
                    artifact_path = _private_path(artifact)
                    if not artifact_path.is_file() or hashlib.sha256(artifact_path.read_bytes()).hexdigest() != digest.lower():
                        errors.append(f"evidence {ident}: artifact is missing or SHA-256 does not match")
                except (OSError, ValueError, RuntimeError) as exc:
                    errors.append(f"evidence {ident}: private artifact unavailable ({exc})")
    quotes = config.get("QUOTES")
    if not isinstance(quotes, list) or len(quotes) < MIN_DEALER_QUOTES:
        errors.append(f"QUOTES must contain at least {MIN_DEALER_QUOTES} complete competing offers")
        quotes = []
    quote_ids = set()
    quote_vehicles = set()
    for quote in quotes:
        if not isinstance(quote, dict):
            errors.append("each QUOTES entry must be an object")
            continue
        ident = quote.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", ident) or ident in quote_ids:
            errors.append("quote IDs must be nonempty and unique")
            continue
        quote_ids.add(ident)
        for key in ("vehicle", "vehicle_id", "dealer", "mileage", "source_id", "conditions", "registration_state"):
            if not isinstance(quote.get(key), str) or not quote[key].strip():
                errors.append(f"quote {ident}: {key} is required")
        if quote.get("registration_state") != config.get("STATE"):
            errors.append(f"quote {ident}: OTD registration_state must match the buyer's STATE")
        try:
            expires = _iso_date(quote.get("expires_on"), f"quote {ident} expires_on")
            if expires < (current if mode == "live" else dossier_date):
                errors.append(f"quote {ident}: offer has expired")
        except ValueError as exc:
            errors.append(str(exc))
        signature = (str(quote.get("vehicle", "")).casefold(), str(quote.get("dealer", "")).casefold())
        if signature in quote_vehicles:
            errors.append(f"quote {ident}: duplicate dealer/vehicle comparison")
        quote_vehicles.add(signature)
        try:
            if _decimal(quote.get("otd"), f"quote {ident} otd") <= 0:
                errors.append(f"quote {ident}: OTD must be positive")
        except ValueError as exc:
            errors.append(str(exc))
        if quote.get("status") != ("synthetic" if mode == "demo" else "written_quote"):
            errors.append(f"quote {ident}: status must match {mode} evidence")
        source_id = quote.get("source_id")
        record = sources.get(source_id) if isinstance(source_id, str) else None
        if not record or not isinstance(record.get("supports"), list) or f"quote:{ident}" not in record["supports"]:
            errors.append(f"quote {ident}: source_id must reference evidence supporting this quote")
        elif mode == "live" and record.get("kind") != "dealer_quote":
            errors.append(f"quote {ident}: written OTD requires dealer_quote evidence")
    if mode == "live":
        for key, value in config.items():
            if isinstance(value, (str, int, float)) and key not in PROPOSAL_KEYS and str(value).strip() and key not in supported:
                errors.append(f"{key}: live claim requires EVIDENCE.supports")
        # Demonstration content is deliberately identifiable in every language.
        content = [value for value in config.values() if isinstance(value, str)]
        content.extend(value for quote in quotes if isinstance(quote, dict) for value in quote.values() if isinstance(value, str))
        content.extend(record.get("source", "") for record in evidence if isinstance(record, dict))
        inherited = {value.casefold() for example in _demo_configs()
                     for value in flatten_dict(example).values()
                     if re.search(r"synthetic|fictional|ficticio|sintétic|虚构|合成|example\.com|AcmeCorp", value, re.I)}
        explicit_marker = r"fictional|ficticio|demostración sintética|synthetic (?:demo|example|quote|buyer|dealer|source|comparison)|虚构|合成演示|合成示例|example\.com|AcmeCorp"
        if any(isinstance(value, str) and value.casefold() in inherited for value in content) or re.search(explicit_marker, json.dumps(content, ensure_ascii=False, default=str), re.I):
            errors.append("live config contains inherited synthetic demonstration content")
    return errors


def _strip_dashes(text):
    """The no-dash house rule covers the rendered dossier (buyer-facing prose). dash_guard does
    not scan .html, so normalize en/em/horizontal-bar dashes out of the final output at generation
    time as a backstop, leaving ASCII hyphens (VINs, price ranges) untouched."""
    for d in ("–", "—", "―"):
        text = text.replace(" %s " % d, ", ").replace(d, ",")
    return text


def substitute(template, config, trusted_markup=None):
    """Escape all config text; only renderer-owned table rows may contain markup."""
    flat = flatten_dict(config)
    trusted_markup = trusted_markup or {}

    missing = set()
    used = set()

    def repl(m):
        key = m.group(1)
        if key in trusted_markup:
            used.add(key)
            return trusted_markup[key]
        if key in flat:
            used.add(key)
            return html.escape(flat[key], quote=True)
        # Try UPPERCASE variant (template uses {{TITLE}}, config has title)
        if key.lower() in flat:
            used.add(key.lower())
            return html.escape(flat[key.lower()], quote=True)
        # Try lowercase variant
        if key.upper() in flat:
            used.add(key.upper())
            return html.escape(flat[key.upper()], quote=True)
        missing.add(key)
        return m.group(0)  # leave unchanged

    result = PLACEHOLDER_PATTERN.sub(repl, template)
    return _strip_dashes(result), missing, used


def _render_tables(config):
    def cells(values):
        return "<tr>" + "".join(f"<td>{html.escape(str(v), quote=True)}</td>" for v in values) + "</tr>"

    sources = {record["id"]: record for record in config["EVIDENCE"]}
    rows = []
    language = config.get("LANGUAGE", "en")
    for quote in config["QUOTES"]:
        source = sources[quote["source_id"]]
        statuses = {"en": ("Synthetic quote", "Written quote; evidence recorded"),
                    "cn": ("合成报价", "书面报价；已记录证据"),
                    "es": ("Cotización sintética", "Cotización escrita; fuente registrada")}
        status = statuses.get(language, statuses["en"])[config["DOSSIER_MODE"] != "demo"]
        rows.append(cells((f"{quote['vehicle']} ({quote['vehicle_id']})", quote["dealer"], f"${_decimal(quote['otd'], 'otd'):,.2f}",
                           quote["mileage"], f"{status}; {source['source_date']}; [{source['id']}]")))
        prefixes = {"en": "{state} registration; expires {expires}. ",
                    "cn": "{state} 登记；有效至 {expires}。",
                    "es": "Registro en {state}; vence {expires}. "}
        terms = prefixes.get(language, prefixes["en"]).format(state=quote["registration_state"], expires=quote["expires_on"]) + quote["conditions"]
        rows.append(f'<tr><td colspan="5">{html.escape(terms, quote=True)}</td></tr>')
    evidence_rows = [cells((source["id"], source["kind"], source["source"], source["source_date"]))
                     for source in config["EVIDENCE"]]
    return {"QUOTE_ROWS": "\n".join(rows), "EVIDENCE_ROWS": "\n".join(evidence_rows)}


def render_dossier(template, config):
    """Render only validated data, including visible provenance and mode labeling."""
    errors = validate_config_sanity(config)
    if errors:
        raise ValueError("Invalid dossier config:\n  - " + "\n  - ".join(errors))
    rendered_config = dict(config)
    notices = {
        "en": "SYNTHETIC DEMO. All figures and identities are fictional. Do not present this document as a real quote or purchase proposal.",
        "cn": "合成演示。人物、车辆和金额均为虚构，不能作为真实报价或购车提案使用。",
        "es": "DEMOSTRACIÓN SINTÉTICA. Todos los datos e identidades son ficticios. No presentar como cotización o propuesta real.",
    }
    rendered_config["DOSSIER_NOTICE"] = (notices.get(config.get("LANGUAGE"), notices["en"])
                                          if config["DOSSIER_MODE"] == "demo" else
                                          "Proposal based on dated evidence recorded below. Arithmetic and artifact integrity checked; verify the source contents and current terms before sharing.")
    rendered_config["NUM_COMPETING_OFFERS"] = str(len(config["QUOTES"]))
    for key in MONEY_KEYS + ("TAX_ADJUSTMENT",):
        rendered_config[key] = f"{_decimal(config[key], key, signed=key == 'TAX_ADJUSTMENT'):,.2f}"
    markup = _render_tables(config)
    # The notice is renderer-owned fixed prose, serialized as a CSS string for
    # Chromium's page-margin box. No caller-supplied text enters this CSS.
    markup["PAGE_NOTICE_CSS"] = json.dumps(rendered_config["DOSSIER_NOTICE"], ensure_ascii=False)
    result, missing, _ = substitute(template, rendered_config, markup)
    if missing:
        raise ValueError("Missing template fields: " + ", ".join(sorted(missing)))
    return result


def _demo_config_allowed(config):
    if config not in _demo_configs():
        raise ValueError("demo mode accepts only generated synthetic fixtures; use live mode and private DATA for your own inputs")


def _demo_output(path):
    resolved = Path(path).resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise ValueError("demo artifacts must be written outside the public tool repository")
    return resolved


def main():
    parser = argparse.ArgumentParser(description="Validate and render an evidence-based dossier or a synthetic demonstration")
    parser.add_argument("--mode", choices=("demo", "live"), required=True)
    parser.add_argument("--config", required=True, help="Generated demo fixture or private DATA config")
    parser.add_argument("--template", help="One of the shipped EN/CN/ES templates")
    parser.add_argument("--output", required=True, help="HTML path (live: private DATA only)")
    parser.add_argument("--to-pdf", help="Optional PDF path (live: private DATA only)")
    parser.add_argument("--pdf-timeout", type=float, default=60, help="Renderer timeout in seconds (default 60)")
    parser.add_argument("--strict", action="store_true", help="Compatibility flag; validation is always strict")
    args = parser.parse_args()
    try:
        config_path = _private_path(args.config) if args.mode == "live" else Path(args.config).resolve()
        config = load_config(config_path)
        if not isinstance(config, dict) or config.get("DOSSIER_MODE") != args.mode:
            raise ValueError("--mode must match config DOSSIER_MODE")
        if args.mode == "demo":
            _demo_config_allowed(config)
        language = config.get("LANGUAGE", "en")
        if language not in ("en", "cn", "es"):
            raise ValueError("LANGUAGE must be en, cn, or es")
        suffix = {"en": "", "cn": "_cn", "es": "_es"}[language]
        template_path = Path(args.template).resolve() if args.template else ASSETS / f"dossier_template{suffix}.html"
        if template_path not in [ASSETS / f"dossier_template{s}.html" for s in ("", "_cn", "_es")]:
            raise ValueError("use a shipped EN/CN/ES template; arbitrary templates are not supported")
        result = render_dossier(template_path.read_text(encoding="utf-8"), config)
        if args.mode == "live":
            output_path = _private_path(args.output, for_write=True)
            pdf_path = _private_path(args.to_pdf, for_write=True) if args.to_pdf else None
        else:
            output_path = _demo_output(args.output)
            pdf_path = _demo_output(args.to_pdf) if args.to_pdf else None
        if output_path in (config_path, template_path) or pdf_path in (output_path, config_path, template_path):
            raise ValueError("config, template, HTML, and PDF paths must be different")
        if output_path.suffix.lower() != ".html" or (pdf_path and pdf_path.suffix.lower() != ".pdf"):
            raise ValueError("output extensions must be .html and .pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
        print(f"HTML written ({args.mode}): {output_path}")
        if pdf_path:
            html_to_pdf(output_path, pdf_path, timeout=args.pdf_timeout)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


def _chrome_candidates():
    """Return ordered list of likely Chromium-family browser paths across Win/Mac/Linux.

    Includes Google Chrome, Microsoft Edge, Chromium, Brave, Vivaldi (all Chromium-based,
    all honor --headless=new --print-to-pdf).
    """
    import os
    home = Path.home()
    localappdata = os.environ.get("LOCALAPPDATA")
    programfiles = os.environ.get("ProgramFiles", r"C:\Program Files")
    programfiles_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

    paths = []

    # ---- Windows ----
    # Google Chrome (system + user)
    paths += [
        Path(programfiles) / "Google/Chrome/Application/chrome.exe",
        Path(programfiles_x86) / "Google/Chrome/Application/chrome.exe",
    ]
    if localappdata:
        paths.append(Path(localappdata) / "Google/Chrome/Application/chrome.exe")
    # Microsoft Edge (system + user), both Program Files and (x86)
    paths += [
        Path(programfiles) / "Microsoft/Edge/Application/msedge.exe",
        Path(programfiles_x86) / "Microsoft/Edge/Application/msedge.exe",
    ]
    if localappdata:
        paths.append(Path(localappdata) / "Microsoft/Edge/Application/msedge.exe")
    # Brave (system + user)
    paths += [
        Path(programfiles) / "BraveSoftware/Brave-Browser/Application/brave.exe",
        Path(programfiles_x86) / "BraveSoftware/Brave-Browser/Application/brave.exe",
    ]
    if localappdata:
        paths.append(Path(localappdata) / "BraveSoftware/Brave-Browser/Application/brave.exe")
    # Vivaldi
    paths += [
        Path(programfiles) / "Vivaldi/Application/vivaldi.exe",
        Path(localappdata) / "Vivaldi/Application/vivaldi.exe" if localappdata else None,
    ]
    # Chromium (rare on Windows but possible)
    if localappdata:
        paths.append(Path(localappdata) / "Chromium/Application/chrome.exe")

    # ---- macOS ----
    paths += [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        home / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        home / "Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
        home / "Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        Path("/Applications/Vivaldi.app/Contents/MacOS/Vivaldi"),
    ]

    # ---- Linux ----
    paths += [
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/google-chrome-stable"),
        Path("/opt/google/chrome/google-chrome"),
        Path("/opt/google/chrome/chrome"),
        Path("/usr/bin/chromium"),
        Path("/usr/bin/chromium-browser"),
        Path("/snap/bin/chromium"),
        Path("/snap/bin/google-chrome"),
        Path("/usr/lib/chromium/chromium"),
        Path("/usr/lib64/chromium-browser/chromium-browser"),
        Path("/var/lib/flatpak/exports/bin/com.google.Chrome"),
        Path("/var/lib/flatpak/exports/bin/com.microsoft.Edge"),
        Path("/usr/bin/microsoft-edge"),
        Path("/usr/bin/microsoft-edge-stable"),
        Path("/usr/bin/brave-browser"),
        Path("/usr/bin/brave"),
        Path("/usr/bin/vivaldi"),
        Path("/usr/bin/vivaldi-stable"),
    ]

    return [p for p in paths if p is not None]


def find_chrome():
    """Return (binary_path, kind) for the first Chromium-family browser found.

    kind is 'chromium' for Chrome/Edge/Chromium/Brave/Vivaldi (any --headless=new
    --print-to-pdf-capable binary).

    Returns (None, None) if nothing usable is found.
    """
    import shutil

    # Allow explicit override
    env_override = os.environ.get("CHROME_BIN")
    if env_override:
        if not Path(env_override).is_file():
            raise ValueError("CHROME_BIN does not name a browser executable")
        return env_override, "chromium"

    for path in _chrome_candidates():
        if path.is_file():
            return str(path), "chromium"

    # PATH lookup as last resort
    for name in (
        "google-chrome", "google-chrome-stable",
        "chromium", "chromium-browser", "chrome",
        "msedge", "microsoft-edge", "microsoft-edge-stable",
        "brave", "brave-browser",
        "vivaldi", "vivaldi-stable",
    ):
        found = shutil.which(name)
        if found:
            return found, "chromium"

    return None, None


def find_wkhtmltopdf():
    """Return path to wkhtmltopdf if installed, else None."""
    import shutil
    found = shutil.which("wkhtmltopdf")
    if found:
        return found
    # Common install locations
    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "wkhtmltopdf/bin/wkhtmltopdf.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "wkhtmltopdf/bin/wkhtmltopdf.exe",
        Path("/usr/bin/wkhtmltopdf"),
        Path("/usr/local/bin/wkhtmltopdf"),
        Path("/opt/homebrew/bin/wkhtmltopdf"),
    ]
    for p in candidates:
        try:
            if p.exists():
                return str(p)
        except Exception:
            continue
    return None


def _no_browser_error_message():
    """Build a human-readable diagnostic listing every path probed."""
    lines = [
        "Error: no Chromium-family browser (Chrome / Edge / Chromium / Brave / Vivaldi) found",
        "and no wkhtmltopdf fallback available.",
        "",
        "Probed paths (none existed):",
    ]
    for p in _chrome_candidates():
        lines.append(f"  - {p}")
    lines.append("")
    lines.append("Fixes:")
    lines.append("  1. Install Google Chrome: https://www.google.com/chrome/")
    lines.append("  2. Or install Microsoft Edge (already on Windows 10/11 by default)")
    lines.append("  3. Or install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
    lines.append("  4. Or set CHROME_BIN env var to point at your Chromium binary")
    return "\n".join(lines)


def _verify_pdf(path, *, expected_notice=None):
    if not path.is_file() or path.stat().st_size < 100:
        raise RuntimeError("renderer did not create a new PDF")
    data = path.read_bytes()
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-1024:]:
        raise RuntimeError("renderer output is not a complete PDF")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF verification requires pypdf; install with: python -m pip install pypdf") from exc
    try:
        reader = PdfReader(path, strict=True)
        if not reader.pages:
            raise RuntimeError("renderer created an empty PDF")
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if "file:///" in page_text.lower():
                raise RuntimeError("PDF contains a local file URL; print headers/footers were not suppressed")
            if expected_notice and re.sub(r"\s+", "", expected_notice) not in re.sub(r"\s+", "", page_text):
                raise RuntimeError("PDF page is missing the required dossier mode notice; use Chromium 131 or newer")
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError("renderer output could not be parsed as a PDF") from exc
    return len(reader.pages)


def html_to_pdf(html_path, pdf_path, *, timeout=60):
    """Render to a fresh staging file and publish only a verified PDF."""
    html_path, pdf_path = Path(html_path).resolve(), Path(pdf_path).resolve()
    if not html_path.is_file():
        raise ValueError("input HTML does not exist")
    if html_path == pdf_path:
        raise ValueError("HTML and PDF paths must be different")
    if not 0 < timeout <= 300:
        raise ValueError("PDF timeout must be greater than zero and at most 300 seconds")
    chrome, _ = find_chrome()
    wk = None if chrome else find_wkhtmltopdf()
    if not chrome and not wk:
        raise RuntimeError(_no_browser_error_message())
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dossier-render-", dir=pdf_path.parent) as staging:
        new_pdf = Path(staging) / "rendered.pdf"
        if chrome:
            cmd = [chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                   "--no-pdf-header-footer", f"--user-data-dir={Path(staging) / 'profile'}",
                   f"--print-to-pdf={new_pdf}", html_path.as_uri()]
        else:
            cmd = [wk, "--disable-javascript", "--disable-local-file-access", str(html_path), str(new_pdf)]
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=timeout,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"PDF renderer timed out after {timeout:g} seconds; existing output was preserved") from exc
        if result.returncode != 0:
            stderr = (result.stderr or b"").decode("utf-8", errors="replace")
            raise RuntimeError(f"PDF renderer failed (exit {result.returncode}): {stderr[-2000:]}")
        notice = re.search(r'<div class="document-mode">(.*?)</div>', html_path.read_text(encoding="utf-8"), re.S)
        pages = _verify_pdf(new_pdf, expected_notice=html.unescape(notice.group(1)) if notice else None)
        os.replace(new_pdf, pdf_path)
    print(f"PDF verified: {pages} page(s), {pdf_path.stat().st_size:,} bytes: {pdf_path}")
    return pages


if __name__ == "__main__":
    main()
