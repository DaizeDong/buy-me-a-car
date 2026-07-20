#!/usr/bin/env python3
"""
Dossier Generator — fill {{PLACEHOLDER}} in an HTML template using a YAML/JSON config.

Usage:
  python generate_dossier.py --config my_dossier.yaml --output my_dossier.html
  python generate_dossier.py --config my_dossier.yaml --output my_dossier.html --to-pdf my_dossier.pdf
  python generate_dossier.py --config my_dossier.yaml --output my_dossier_cn.html --template ../assets/dossier_template_cn.html
  python generate_dossier.py --config my_dossier.yaml --output my_dossier_es.html --template ../assets/dossier_template_es.html

The template uses {{KEY}} placeholders; keys are resolved from the config file's top-level dict.
The EN / CN / ES templates share an identical {{KEY}} placeholder set, so the same config
drives all three (default: dossier_template.html; --template selects the CN or ES variant).

By default the script fails loudly if:
  (a) the config is missing any LOAD_BEARING_KEYS (buyer address, year, target OTD, state,
      tax rate, plus >=2 dealer competing offers); or
  (b) any {{KEY}} present in the template is absent from the config.

Pass --allow-missing to downgrade (b) to warnings (kept for back-compat).
Load-bearing-field failures cannot be downgraded — they always exit non-zero.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def load_config(path):
    """Load YAML (preferred) or JSON config. Always reads as UTF-8 explicitly."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            sys.exit("Error: PyYAML required for YAML configs. pip install pyyaml")
        return yaml.safe_load(text)
    elif path.endswith(".json"):
        return json.loads(text)
    else:
        # Best-effort: try YAML first, fall back to JSON
        try:
            import yaml
            return yaml.safe_load(text)
        except Exception:
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


def extract_template_keys(template):
    """Return the set of all {{KEY}} placeholders referenced in the template."""
    return set(PLACEHOLDER_PATTERN.findall(template))


def validate_config_sanity(flat_config):
    """Check load-bearing-field invariants. Returns list of human-readable errors (empty if all OK)."""
    errors = []

    # Required scalar fields
    for k in LOAD_BEARING_KEYS:
        val = flat_config.get(k)
        if val is None or (isinstance(val, str) and not val.strip()):
            errors.append(f"missing or empty load-bearing field: {k}")

    # Required: >= MIN_DEALER_QUOTES competing offer entries (COMP_VEH_1..N)
    comp_indices = []
    for k, v in flat_config.items():
        m = re.match(r"^COMP_VEH_(\d+)$", k)
        if m and isinstance(v, str) and v.strip():
            comp_indices.append(int(m.group(1)))
    if len(comp_indices) < MIN_DEALER_QUOTES:
        errors.append(
            f"need at least {MIN_DEALER_QUOTES} competing dealer offers "
            f"(COMP_VEH_1, COMP_VEH_2, ...); found {len(comp_indices)}"
        )

    return errors


def _strip_dashes(text):
    """The no-dash house rule covers the rendered dossier (buyer-facing prose). dash_guard does
    not scan .html, so normalize en/em/horizontal-bar dashes out of the final output at generation
    time as a backstop, leaving ASCII hyphens (VINs, price ranges) untouched."""
    for d in ("–", "—", "―"):
        text = text.replace(" %s " % d, ", ").replace(d, ",")
    return text


def substitute(template, config):
    """Substitute {{KEY}} placeholders with config values."""
    flat = flatten_dict(config)

    missing = set()
    used = set()

    def repl(m):
        key = m.group(1)
        if key in flat:
            used.add(key)
            return flat[key]
        # Try UPPERCASE variant (template uses {{TITLE}}, config has title)
        if key.lower() in flat:
            used.add(key.lower())
            return flat[key.lower()]
        # Try lowercase variant
        if key.upper() in flat:
            used.add(key.upper())
            return flat[key.upper()]
        missing.add(key)
        return m.group(0)  # leave unchanged

    result = PLACEHOLDER_PATTERN.sub(repl, template)
    return _strip_dashes(result), missing, used


def main():
    p = argparse.ArgumentParser(description="Generate a dossier HTML from a YAML/JSON config and HTML template")
    p.add_argument("--config", required=True, help="Path to YAML or JSON config file")
    p.add_argument("--template", default=None,
                   help="Path to HTML template (default: ../assets/dossier_template.html relative to this script; "
                        "use ../assets/dossier_template_cn.html for CN or ../assets/dossier_template_es.html for ES)")
    p.add_argument("--output", required=True, help="Path to output HTML file")
    p.add_argument("--to-pdf", default=None,
                   help="If set, also convert output HTML to PDF at this path (uses html_to_pdf.sh)")
    p.add_argument("--strict", action="store_true",
                   help="(Deprecated alias) Default behavior now fails on missing template keys; "
                        "use --allow-missing to downgrade to warnings.")
    p.add_argument("--allow-missing", action="store_true",
                   help="Downgrade 'template placeholder not in config' from error to warning. "
                        "Load-bearing-field failures still always error.")
    args = p.parse_args()

    script_dir = Path(__file__).parent.resolve()
    template_path = Path(args.template) if args.template else (script_dir.parent / "assets" / "dossier_template.html")

    if not template_path.exists():
        sys.exit(f"Error: template not found at {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    config = load_config(args.config)
    if not isinstance(config, dict):
        sys.exit(f"Error: config at {args.config} did not parse to a dict (got {type(config).__name__})")

    # ---- Validator 1: config sanity (load-bearing fields) ----
    flat_config = flatten_dict(config)
    sanity_errors = validate_config_sanity(flat_config)
    if sanity_errors:
        msg_lines = [
            "Error: dossier config is missing load-bearing fields. A dealer-facing dossier",
            "without these will mislead negotiation. Fix the YAML and retry:",
        ]
        for err in sanity_errors:
            msg_lines.append(f"  - {err}")
        sys.exit("\n".join(msg_lines))

    # ---- Validator 2: every template {{KEY}} must be resolvable from config ----
    template_keys = extract_template_keys(template_text)
    unresolvable = []
    for tk in sorted(template_keys):
        if tk in flat_config:
            continue
        if tk.lower() in flat_config or tk.upper() in flat_config:
            continue
        unresolvable.append(tk)

    if unresolvable:
        header = f"Template references {len(unresolvable)} placeholder(s) not present in config:"
        body = "\n".join(f"  - {k}" for k in unresolvable)
        full_msg = header + "\n" + body
        if args.allow_missing:
            print(full_msg, file=sys.stderr)
            print("(--allow-missing set, continuing with literal {{KEY}} fallback)", file=sys.stderr)
        else:
            sys.exit(full_msg + "\n\nPass --allow-missing to override (placeholders will appear as literal {{KEY}} in output).")

    # ---- Substitution ----
    result, missing, used = substitute(template_text, config)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Wrote {len(result):,} bytes to {output_path}")
    print(f"Substituted {len(used)} unique placeholders")

    if missing and args.allow_missing:
        # Print again post-substitute for parity with old behavior
        msg = f"Note: {len(missing)} placeholder(s) left as literal {{KEY}} in output:"
        for k in sorted(missing):
            msg += f"\n  - {k}"
        print(msg, file=sys.stderr)

    if args.to_pdf:
        print(f"\nConverting to PDF: {args.to_pdf}")
        html_to_pdf(output_path.absolute(), Path(args.to_pdf).absolute())


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
    if env_override and Path(env_override).exists():
        return env_override, "chromium"

    for path in _chrome_candidates():
        if path.exists():
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


def html_to_pdf(html_path, pdf_path):
    """Convert HTML to PDF using Chrome/Edge headless. Falls back to wkhtmltopdf."""
    chrome, _ = find_chrome()
    if chrome:
        print(f"Using browser: {chrome}")

        # Build a file:// URL that Chrome can parse on all platforms
        file_url = html_path.as_uri()

        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-margins=0",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            file_url,
        ]

        # Use bytes mode + decode with errors='replace' so Chinese-locale stderr does not crash
        result = subprocess.run(cmd, capture_output=True)
        stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
        if result.returncode != 0:
            sys.exit(f"Chrome conversion failed (exit {result.returncode}):\n{stderr}")

        if Path(pdf_path).exists():
            size = Path(pdf_path).stat().st_size
            print(f"PDF written: {size:,} bytes to {pdf_path}")
            return
        else:
            sys.exit(f"PDF output not created at {pdf_path}")

    # Fallback: wkhtmltopdf
    wk = find_wkhtmltopdf()
    if wk:
        print(f"No Chromium browser found; falling back to wkhtmltopdf: {wk}")
        cmd = [wk, "--enable-local-file-access", str(html_path), str(pdf_path)]
        result = subprocess.run(cmd, capture_output=True)
        stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
        if result.returncode != 0:
            sys.exit(f"wkhtmltopdf conversion failed (exit {result.returncode}):\n{stderr}")
        if Path(pdf_path).exists():
            size = Path(pdf_path).stat().st_size
            print(f"PDF written: {size:,} bytes to {pdf_path}")
            return
        sys.exit(f"PDF output not created at {pdf_path}")

    sys.exit(_no_browser_error_message())


if __name__ == "__main__":
    main()
