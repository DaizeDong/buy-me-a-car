#!/usr/bin/env python3
"""Render an internal buyer research report, with zero written quotes allowed.

JSON and YAML use the same schema; quote YYYY-MM-DD values in YAML. Required
top-level keys: document_type='buyer_research', synthetic (bool), date, language
('cn'), title, decision_summary, criteria, sources, coverage, candidates, sections.
Optional costs and written_quotes default to empty lists. The generated fixture
research_report_config_template.json documents a complete example.

criteria: id, label, value (text/null), status (confirmed/assumed/unknown),
source_ids, notes. sources: id, title, url (HTTPS), observed_date, status
(captured/blocked/unavailable), kind (listing/official/guide/dealer_quote/
buyer_statement), limitations. Captured live sources also require artifact
(private DATA path) and sha256. coverage: id, label, status (complete/partial/
blocked/not_searched), source_ids, query, limitations. candidates: id, vehicle,
configuration, asking_price (nonnegative decimal/null), currency='USD', location,
source_id, limitations; optional vin (17 characters) and stock. A VIN identifies
a vehicle group; each candidate ID retains its original observed offer.

Each section has id, topic, title, blocks. All REQUIRED_TOPICS must occur at least
once; core tables appear once per topic. Blocks are paragraph {text}, bullets
{items:[text]}, or table {columns:[text], rows:[[text/number/null]]}. Optional refs
on each block resolve source:ID, candidate:ID or section:ID. Raw HTML is forbidden.

costs: candidate_id, tax, title_registration, dealer_fees, transport, inspection,
other (all decimal/null), source_ids, limitations. These are comparison scenarios,
not written quotes; no missing amount becomes zero. written_quotes: id,
candidate_id, otd, currency='USD', source_id, conditions. A quote requires a
captured dealer_quote source. No quote count is required for research.

Use generate_report(config_path, output, mode='live'|'demo', to_pdf=None) as the
production writing API. Every live input, artifact and output is resolved through
tools.runtime_paths. In-memory live rendering also requires config_path and an
exact match to that private file. Demo inputs must equal the generated recipe.
Privacy mode is separate from document purpose: both modes are buyer research,
never an outward dealer proposal. PDF rendering reuses the dossier renderer.
"""
from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import html
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.runtime_paths import validate_data_path
from tools.fixture_recipes.research_report import demo_config
from skills.orchestrator.scripts.generate_dossier import html_to_pdf, load_config

REQUIRED_TOPICS = ("requirements", "coverage", "alternatives", "listings", "costs", "suitability",
                   "winter", "ownership", "recommendation", "next_actions", "sources")
COST_KEYS = ("tax", "title_registration", "dealer_fees", "transport", "inspection", "other")
STATUSES = {"confirmed": "已确认", "assumed": "暂定假设", "unknown": "未知", "captured": "已存档",
            "blocked": "访问受阻", "unavailable": "未取得", "complete": "已完成所述范围",
            "partial": "部分覆盖", "not_searched": "尚未检索"}
KINDS = {"listing": "挂牌", "official": "官方资料", "guide": "指南", "dealer_quote": "经销商书面报价",
         "buyer_statement": "买方陈述"}


def _object(value, required, optional=(), *, field):
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{field}: expected an object with text keys")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f"{field}: missing keys {sorted(missing)}; unsupported keys {sorted(extra)}")


def _text(value, field, *, empty=False):
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError(f"{field}: expected {'possibly empty ' if empty else 'nonempty '}text")
    return value


def _list(value, field, *, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError(f"{field}: expected {'nonempty ' if nonempty else ''}list")
    return value


def _choice(value, choices, field):
    if not isinstance(value, str) or value not in choices:
        raise ValueError(f"{field}: expected one of {', '.join(sorted(choices))}")


def _date(value, field):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{field}: expected YYYY-MM-DD text")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field}: invalid date") from exc


def _amount(value, field):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{field}: expected nonnegative decimal or null")
    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", str(value)):
        raise ValueError(f"{field}: use a nonnegative decimal with at most two decimal places")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{field}: invalid amount") from exc
    if not result.is_finite() or result > 1000000000:
        raise ValueError(f"{field}: amount outside supported range")
    return result


def _index(records, field):
    result = {}
    for record in _list(records, field):
        if not isinstance(record, dict):
            raise ValueError(f"{field}: each record must be an object")
        ident = record.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", ident) or ident in result:
            raise ValueError(f"{field}: IDs must be unique letters, digits, underscores or hyphens")
        result[ident] = record
    return result


def _source_refs(values, sources, field, *, captured=False):
    for ident in _list(values, field):
        if not isinstance(ident, str) or ident not in sources:
            raise ValueError(f"{field}: unresolved source reference")
        if captured and sources[ident]["status"] != "captured":
            raise ValueError(f"{field}: supporting source must be captured")


def _validate(config, mode):
    required = ("document_type", "synthetic", "date", "language", "title", "decision_summary", "criteria",
                "sources", "coverage", "candidates", "sections")
    _object(config, required, ("costs", "written_quotes"), field="report")
    _choice(mode, ("demo", "live"), "mode")
    if config["document_type"] != "buyer_research" or config["synthetic"] is not (mode == "demo"):
        raise ValueError("document_type must be buyer_research; synthetic must match privacy mode")
    _choice(config["language"], ("cn",), "language")
    _text(config["title"], "title")
    _text(config["decision_summary"], "decision_summary")
    report_date = _date(config["date"], "date")
    if report_date > date.today():
        raise ValueError("date cannot be in the future")
    sources = _index(config["sources"], "sources")
    for ident, source in sources.items():
        field = f"source {ident}"
        _object(source, ("id", "title", "url", "observed_date", "status", "kind", "limitations"),
                ("artifact", "sha256"), field=field)
        for key in ("title", "url", "limitations"):
            _text(source[key], f"{field}.{key}", empty=key == "limitations")
        url = urlsplit(source["url"])
        if (url.scheme != "https" or not url.hostname or url.username or url.password
                or any(character.isspace() for character in source["url"])):
            raise ValueError(f"{field}: URL must be HTTPS without credentials or whitespace")
        _choice(source["status"], ("captured", "blocked", "unavailable"), field)
        _choice(source["kind"], KINDS, field)
        if _date(source["observed_date"], field) > report_date:
            raise ValueError(f"{field}: observed_date cannot be later than report date")
        if source["status"] != "captured":
            if not source["limitations"].strip():
                raise ValueError(f"{field}: uncaptured sources require limitations")
            if "artifact" in source or "sha256" in source:
                raise ValueError(f"{field}: uncaptured source cannot claim an evidence artifact")
        elif mode == "live":
            artifact = _text(source.get("artifact"), f"{field}.artifact")
            digest = source.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
                raise ValueError(f"{field}: SHA-256 is required")
            path = validate_data_path(artifact)
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest.lower():
                raise ValueError(f"{field}: artifact missing or SHA-256 mismatch")

    _list(config["criteria"], "criteria", nonempty=True)
    _index(config["criteria"], "criteria")
    for criterion in config["criteria"]:
        _object(criterion, ("id", "label", "value", "status", "source_ids", "notes"), field="criterion")
        _text(criterion["label"], "criterion.label")
        _text(criterion["notes"], "criterion.notes", empty=True)
        if criterion["value"] is not None:
            _text(criterion["value"], "criterion.value")
        _choice(criterion["status"], ("confirmed", "assumed", "unknown"), "criterion.status")
        if criterion["status"] != "unknown" and criterion["value"] is None:
            raise ValueError("criterion: confirmed/assumed values cannot be null")
        _source_refs(criterion["source_ids"], sources, "criterion.source_ids", captured=True)

    _list(config["coverage"], "coverage", nonempty=True)
    _index(config["coverage"], "coverage")
    for coverage in config["coverage"]:
        _object(coverage, ("id", "label", "status", "source_ids", "query", "limitations"), field="coverage")
        for key in ("label", "query", "limitations"):
            _text(coverage[key], f"coverage.{key}", empty=key == "limitations")
        _choice(coverage["status"], ("complete", "partial", "blocked", "not_searched"), "coverage.status")
        _source_refs(coverage["source_ids"], sources, "coverage.source_ids")
        if coverage["status"] in ("complete", "partial") and not any(
                sources[ident]["status"] == "captured" for ident in coverage["source_ids"]):
            raise ValueError("coverage: complete/partial coverage requires a captured source")
        if coverage["status"] != "complete" and not coverage["limitations"].strip():
            raise ValueError("coverage: incomplete coverage requires limitations")

    candidates = _index(config["candidates"], "candidates")
    for ident, candidate in candidates.items():
        _object(candidate, ("id", "vehicle", "configuration", "asking_price", "currency", "location", "source_id", "limitations"),
                ("vin", "stock"), field=f"candidate {ident}")
        for key in ("vehicle", "configuration", "location", "limitations"):
            _text(candidate[key], f"candidate.{key}", empty=key == "limitations")
        _amount(candidate["asking_price"], "candidate.asking_price")
        _choice(candidate["currency"], ("USD",), "candidate.currency")
        _source_refs([candidate["source_id"]], sources, "candidate.source_id", captured=True)
        if sources[candidate["source_id"]]["kind"] not in ("listing", "dealer_quote"):
            raise ValueError("candidate.source_id: expected captured listing or dealer_quote")
        if "vin" in candidate and (not isinstance(candidate["vin"], str)
                or not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", candidate["vin"].upper())):
            raise ValueError("candidate.vin: expected 17 VIN characters, excluding I/O/Q")
        if "stock" in candidate:
            _text(candidate["stock"], "candidate.stock")

    cost_candidates = set()
    for cost in _list(config.get("costs", []), "costs"):
        _object(cost, ("candidate_id", *COST_KEYS, "source_ids", "limitations"), field="cost")
        ident = cost["candidate_id"]
        if not isinstance(ident, str) or ident not in candidates or ident in cost_candidates:
            raise ValueError("cost: unresolved or duplicate candidate reference")
        cost_candidates.add(ident)
        for key in COST_KEYS:
            _amount(cost[key], f"cost.{key}")
        _source_refs(cost["source_ids"], sources, "cost.source_ids", captured=True)
        _text(cost["limitations"], "cost.limitations")

    _index(config.get("written_quotes", []), "written_quotes")
    for quote in config.get("written_quotes", []):
        _object(quote, ("id", "candidate_id", "otd", "currency", "source_id", "conditions"), field="quote")
        ident = quote["candidate_id"]
        if not isinstance(ident, str) or ident not in candidates:
            raise ValueError("quote: unresolved candidate reference")
        if _amount(quote["otd"], "quote.otd") in (None, Decimal(0)):
            raise ValueError("quote.otd must be positive")
        _choice(quote["currency"], ("USD",), "quote.currency")
        _source_refs([quote["source_id"]], sources, "quote.source_id", captured=True)
        if sources[quote["source_id"]]["kind"] != "dealer_quote":
            raise ValueError("quote requires a captured dealer_quote source")
        _text(quote["conditions"], "quote.conditions")

    sections = _index(config["sections"], "sections")
    topics = set()
    indexes = {"source": sources, "candidate": candidates, "section": sections}
    for section in sections.values():
        _object(section, ("id", "topic", "title", "blocks"), field="section")
        _choice(section["topic"], REQUIRED_TOPICS, "section.topic")
        topics.add(section["topic"])
        _text(section["title"], "section.title")
        for block in _list(section["blocks"], "section.blocks", nonempty=True):
            if not isinstance(block, dict):
                raise ValueError("block must be an object")
            kind = block.get("type")
            _choice(kind, ("paragraph", "bullets", "table"), "block.type")
            fields = {"paragraph": ("text",), "bullets": ("items",), "table": ("columns", "rows")}[kind]
            _object(block, ("type", *fields), ("refs",), field="block")
            if kind == "paragraph":
                _text(block["text"], "block.text")
            elif kind == "bullets":
                for item in _list(block["items"], "block.items", nonempty=True):
                    _text(item, "block.item")
            else:
                for column in _list(block["columns"], "block.columns", nonempty=True):
                    _text(column, "block.column")
                for row in _list(block["rows"], "block.rows", nonempty=True):
                    if not isinstance(row, list) or len(row) != len(block["columns"]):
                        raise ValueError("block table rows must match column count")
                    for cell in row:
                        if cell is not None and (isinstance(cell, bool) or not isinstance(cell, (str, int, float))
                                                 or isinstance(cell, float) and not math.isfinite(cell)):
                            raise ValueError("block table cells must be text, finite number or null")
            for reference in _list(block.get("refs", []), "block.refs"):
                if not isinstance(reference, str):
                    raise ValueError("block: invalid reference")
                kind, separator, ident = reference.partition(":")
                if not separator or kind not in indexes or ident not in indexes[kind]:
                    raise ValueError("block: unresolved reference")
                if (kind == "source" and sources[ident]["status"] != "captured"
                        and section["topic"] not in ("coverage", "sources", "next_actions")):
                    raise ValueError("block: uncaptured source may only document an evidence gap")
    if topics != set(REQUIRED_TOPICS):
        raise ValueError("sections must cover all research topics: " + ", ".join(sorted(set(REQUIRED_TOPICS) - topics)))


def group_candidates(candidates):
    """Group explicit VINs, preserving each offer; unbound IDs remain independent."""
    groups = {}
    for candidate in candidates:
        key = ("vin", candidate["vin"].upper()) if candidate.get("vin") else ("id", candidate["id"])
        groups.setdefault(key, []).append(candidate)
    return list(groups.values())


def _escape(value):
    return html.escape("未知" if value is None else str(value), quote=True)


def _money(value):
    amount = _amount(value, "amount")
    return "未知" if amount is None else f"USD {amount:,.2f}"


def _table(columns, rows):
    return ('<div class="table-wrap"><table><thead><tr>'
            + "".join(f"<th>{_escape(column)}</th>" for column in columns) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{_escape(cell)}</td>" for cell in row) + "</tr>" for row in rows)
            + "</tbody></table></div>")


def _refs(references):
    links = []
    labels = {"source": "来源", "candidate": "候选记录", "section": "章节"}
    for reference in references:
        kind, ident = reference.split(":", 1)
        links.append(f'<a href="#{kind}-{_escape(ident)}">{labels[kind]} [{_escape(ident)}]</a>')
    return '<p class="references">' + " · ".join(links) + "</p>" if links else ""


def _block(block):
    if block["type"] == "paragraph":
        content = "<p>" + _escape(block["text"]) + "</p>"
    elif block["type"] == "bullets":
        content = "<ul>" + "".join("<li>" + _escape(item) + "</li>" for item in block["items"]) + "</ul>"
    else:
        content = _table(block["columns"], block["rows"])
    return content + _refs(block.get("refs", []))


def _core_content(topic, config):
    if topic == "requirements":
        return _table(("需求", "取值", "确认状态", "备注 / 来源"),
                      [(row["label"], row["value"], STATUSES[row["status"]], row["notes"] + " " + ", ".join(row["source_ids"]))
                       for row in config["criteria"]])
    if topic == "coverage":
        return _table(("检索范围", "条件与范围", "状态", "限制 / 来源"),
                      [(row["label"], row["query"], STATUSES[row["status"]], row["limitations"] + " " + ", ".join(row["source_ids"]))
                       for row in config["coverage"]])
    if topic == "listings":
        groups = group_candidates(config["candidates"])
        if not groups:
            return '<p class="warning">尚无可列示的候选记录。请结合检索范围与限制阅读；此状态不证明市场上没有符合要求的车辆。</p>'
        parts = [f'<p class="scope">{len(config["candidates"])} 条观察记录；按明确 VIN 分组后为 {len(groups)} 个车辆组。无 VIN 记录未自动合并。</p>']
        sources = {source["id"]: source for source in config["sources"]}
        for index, group in enumerate(groups, 1):
            parts.append(f'<h3>车辆组 {index} · {_escape(group[0]["vehicle"])}</h3>')
            if len(group) > 1:
                parts.append('<p class="warning">同一 VIN 的不同记录：价格、配置或所在地不一致时，保留全部观察并等待核实。</p>')
            for candidate in group:
                source = sources[candidate["source_id"]]
                parts.append(f'<div class="candidate" id="candidate-{_escape(candidate["id"])}">')
                parts.append(_table(("观察记录", "挂牌价（非 OTD）", "地点 / 标识"), [[
                    candidate["id"], _money(candidate["asking_price"]),
                    candidate["location"] + " / VIN: " + candidate.get("vin", "未知") + " / Stock: " + candidate.get("stock", "未知")]]))
                parts.append(f'<p class="configuration">配置与价格口径：{_escape(candidate["vehicle"])}；{_escape(candidate["configuration"])}</p>')
                parts.append(f'<p class="details">观察日期：{_escape(source["observed_date"])}。限制：{_escape(candidate["limitations"])}</p>')
                parts.append(_refs(["source:" + candidate["source_id"]]) + "</div>")
        return "".join(parts)
    if topic == "costs":
        costs = {cost["candidate_id"]: cost for cost in config.get("costs", [])}
        rows = []
        details = []
        for candidate in config["candidates"]:
            cost = costs.get(candidate["id"], {})
            amounts = [candidate["asking_price"]] + [cost.get(key) for key in COST_KEYS]
            known = [_amount(value, "cost") for value in amounts if value is not None]
            subtotal = _money(sum(known)) if known else "未知"
            complete = all(value is not None for value in amounts)
            rows.append([candidate["id"], _money(candidate["asking_price"]),
                         *[_money(cost.get(key)) for key in COST_KEYS], subtotal,
                         "所列项目齐全，仍需核实口径" if complete else "完整交付成本未知"])
            if cost:
                details.append(f'<p class="details">{_escape(candidate["id"])} 成本情景：{_escape(cost["limitations"])}</p>'
                               + _refs(["source:" + ident for ident in cost["source_ids"]]))
        result = _table(("记录", "挂牌价（非 OTD）", "税", "产权 / 登记", "经销商费", "运输", "检查", "其他",
                         "已填项目情景小计", "完整性"), rows)
        result += '<p class="warning">成本情景并非书面报价。小计包含已填金额中的假设项，不能视为已确认费用。空缺均为未知；小计不是 OTD，也不证明完整交付成本。</p>' + "".join(details)
        quotes = config.get("written_quotes", [])
        result += f'<h3>{len(quotes)} 份书面 OTD 报价</h3>'
        if quotes:
            result += _table(("报价 / 候选", "书面 OTD", "条件", "来源"),
                             [(quote["id"] + " / " + quote["candidate_id"], _money(quote["otd"]), quote["conditions"], quote["source_id"])
                              for quote in quotes])
        else:
            result += "<p>尚无书面 OTD，不能据挂牌价确认最终成交或交付总额。</p>"
        return result
    if topic == "sources":
        parts = []
        for source in config["sources"]:
            parts.append(f'<article class="source" id="source-{_escape(source["id"])}"><h3>[{_escape(source["id"])}] {_escape(source["title"])}</h3>')
            parts.append(f'<p>{KINDS[source["kind"]]} · {STATUSES[source["status"]]} · 观察日期 {_escape(source["observed_date"])}</p>')
            parts.append(f'<p class="source-url"><a href="{_escape(source["url"])}" rel="noreferrer">{_escape(source["url"])}</a></p>')
            parts.append(f'<p>限制：{_escape(source["limitations"])}</p>')
            if source["status"] != "captured":
                parts.append('<p class="warning">未取得可核实内容；此项仅记录检索缺口。</p>')
            elif source.get("sha256"):
                parts.append(f'<p class="hash">私有存档 SHA-256：{_escape(source["sha256"].lower())}</p>')
            parts.append("</article>")
        return "".join(parts)
    return ""


def render_report(config, *, mode, config_path=None):
    """Validate and render structured research; live data must match a private file."""
    _choice(mode, ("demo", "live"), "mode")
    if mode == "demo":
        if config != demo_config():
            raise ValueError("demo mode accepts only generated synthetic fixtures; use private live DATA for custom inputs")
    else:
        if config_path is None:
            raise ValueError("live rendering requires a private config_path")
        path = validate_data_path(config_path)
        if load_config(path) != config:
            raise ValueError("live config must match the contents of its private config_path")
    _validate(config, mode)
    notice = "合成演示 · 内部买方研究" if mode == "demo" else "内部买方研究 · 非对外购车提案"
    style = (ROOT / "skills/orchestrator/assets/research_report.css").read_text(encoding="utf-8")
    # Only fixed renderer-owned prose enters CSS. User text is always escaped HTML.
    style += "\n@page { @bottom-left { content: " + json.dumps(notice, ensure_ascii=False) + "; } }"
    body = [f'<div class="document-mode">{notice}</div><header><p class="eyebrow">BUYER RESEARCH · 市场与购车决策</p>'
            f'<h1>{_escape(config["title"])}</h1><p>资料截点：{_escape(config["date"])}</p></header>',
            f'<aside class="summary"><h2>当前判断</h2><p>{_escape(config["decision_summary"])}</p></aside>',
            '<p class="scope">本报告面向买方内部研究。日期表示资料截点；已存档不代表仍然有效。挂牌价、成本情景与书面 OTD 分别列示。</p>']
    if mode == "demo":
        body.append('<p class="warning">本演示的全部身份、车型、金额、网址和观察均为虚构，不可作为真实购车证据。</p>')
    if any(row["status"] != "complete" for row in config["coverage"]):
        body.append('<p class="warning">研究状态：证据覆盖尚不完整。请结合检索范围和下一步阅读；生成报告不代表所有疑点已经关闭。</p>')
    body.append('<nav aria-label="章节目录"><ol>' + "".join(
        f'<li><a href="#section-{_escape(section["id"])}">{_escape(section["title"])}</a></li>' for section in config["sections"])
        + "</ol></nav>")
    core_rendered = set()
    for index, section in enumerate(config["sections"], 1):
        body.append(f'<section id="section-{_escape(section["id"])}" data-topic="{_escape(section["topic"])}">'
                    f'<h2><span class="section-number">{index:02d}</span> {_escape(section["title"])}</h2>')
        body.extend(_block(block) for block in section["blocks"])
        if section["topic"] not in core_rendered:
            body.append(_core_content(section["topic"], config))
            core_rendered.add(section["topic"])
        body.append("</section>")
    return ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'">'
            f'<title>{_escape(config["title"])}</title><style>{style}</style></head><body><main>'
            + "\n".join(body) + "</main></body></html>")


def _demo_output(path):
    result = Path(path).expanduser().resolve()
    if result == ROOT or ROOT in result.parents:
        raise ValueError("demo outputs must be outside the public tool repository")
    return result


def generate_report(config_path, output, *, mode, to_pdf=None, pdf_timeout=60):
    """Write validated HTML and optionally a verified PDF, returning their paths."""
    _choice(mode, ("demo", "live"), "mode")
    config_path = validate_data_path(config_path) if mode == "live" else Path(config_path).expanduser().resolve()
    config = load_config(config_path)
    rendered = render_report(config, mode=mode, config_path=config_path)
    output_path = validate_data_path(output, for_write=True) if mode == "live" else _demo_output(output)
    pdf_path = (validate_data_path(to_pdf, for_write=True) if mode == "live" else _demo_output(to_pdf)) if to_pdf else None
    protected = {config_path, Path(__file__).resolve(), ROOT / "skills/orchestrator/assets/research_report.css"}
    if isinstance(config, dict):
        protected.update(validate_data_path(source["artifact"]) for source in config["sources"]
                         if mode == "live" and source["status"] == "captured")
    if output_path in protected or pdf_path in protected or output_path == pdf_path:
        raise ValueError("config, evidence, HTML and PDF paths must be different")
    if output_path.suffix.lower() != ".html" or (pdf_path and pdf_path.suffix.lower() != ".pdf"):
        raise ValueError("output extensions must be .html and .pdf")
    if pdf_path and (isinstance(pdf_timeout, bool) or not 0 < pdf_timeout <= 300):
        raise ValueError("PDF timeout must be greater than zero and at most 300 seconds")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    if pdf_path:
        html_to_pdf(output_path, pdf_path, timeout=pdf_timeout)
    return {"html": output_path, "pdf": pdf_path}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mode", choices=("demo", "live"), required=True, help="Privacy mode; purpose is always internal buyer research")
    parser.add_argument("--config", required=True, help="Generated synthetic JSON/YAML or private DATA config")
    parser.add_argument("--output", required=True, help="HTML output, private DATA in live mode")
    parser.add_argument("--to-pdf", help="Optional PDF output, private DATA in live mode")
    parser.add_argument("--pdf-timeout", type=float, default=60)
    args = parser.parse_args(argv)
    try:
        outputs = generate_report(args.config, args.output, mode=args.mode, to_pdf=args.to_pdf, pdf_timeout=args.pdf_timeout)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(f"Buyer research HTML written ({args.mode}): {outputs['html']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
