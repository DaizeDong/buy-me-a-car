#!/usr/bin/env python3
"""
Dossier Generator — fill {{PLACEHOLDER}} in an HTML template using a YAML/JSON config.

Usage:
  python generate_dossier.py --config my_dossier.yaml --output my_dossier.html
  python generate_dossier.py --config my_dossier.yaml --output my_dossier.html --to-pdf my_dossier.pdf
  python generate_dossier.py --config my_dossier.yaml --output my_dossier_cn.html --template ../assets/dossier_template_cn.html

The template uses {{KEY}} placeholders; keys are resolved from the config file's top-level dict.
Missing keys are left as-is and reported as warnings. Empty-string keys are replaced silently.
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


def substitute(template, config):
    """Substitute {{KEY}} placeholders with config values."""
    flat = flatten_dict(config)
    pattern = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")

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

    result = pattern.sub(repl, template)
    return result, missing, used


def main():
    p = argparse.ArgumentParser(description="Generate a dossier HTML from a YAML/JSON config and HTML template")
    p.add_argument("--config", required=True, help="Path to YAML or JSON config file")
    p.add_argument("--template", default=None,
                   help="Path to HTML template (default: ../assets/dossier_template.html relative to this script)")
    p.add_argument("--output", required=True, help="Path to output HTML file")
    p.add_argument("--to-pdf", default=None,
                   help="If set, also convert output HTML to PDF at this path (uses html_to_pdf.sh)")
    p.add_argument("--strict", action="store_true",
                   help="Exit non-zero if any placeholder is missing in the config")
    args = p.parse_args()

    script_dir = Path(__file__).parent.resolve()
    template_path = Path(args.template) if args.template else (script_dir.parent / "assets" / "dossier_template.html")

    if not template_path.exists():
        sys.exit(f"Error: template not found at {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    config = load_config(args.config)

    result, missing, used = substitute(template_text, config)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Wrote {len(result):,} bytes to {output_path}")
    print(f"Substituted {len(used)} unique placeholders")

    if missing:
        msg = f"Missing config values for {len(missing)} placeholders:"
        for k in sorted(missing):
            msg += f"\n  - {k}"
        if args.strict:
            sys.exit(msg)
        else:
            print(msg, file=sys.stderr)

    if args.to_pdf:
        print(f"\nConverting to PDF: {args.to_pdf}")
        html_to_pdf(output_path.absolute(), Path(args.to_pdf).absolute())


def find_chrome():
    """Locate Chrome or Edge binary across Windows / macOS / Linux."""
    candidates = [
        # Windows
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        # macOS
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        # Linux
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    # PATH lookup
    import shutil
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def html_to_pdf(html_path, pdf_path):
    """Convert HTML to PDF using Chrome/Edge headless. Cross-platform."""
    chrome = find_chrome()
    if not chrome:
        sys.exit("Error: Chrome or Edge not found. Install one and retry.")

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
    stdout = result.stdout.decode("utf-8", errors="replace") if result.stdout else ""
    stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
    if result.returncode != 0:
        sys.exit(f"Chrome conversion failed (exit {result.returncode}):\n{stderr}")

    if Path(pdf_path).exists():
        size = Path(pdf_path).stat().st_size
        print(f"PDF written: {size:,} bytes to {pdf_path}")
    else:
        sys.exit(f"PDF output not created at {pdf_path}")


if __name__ == "__main__":
    main()
