"""Generate fictional dossier inputs. No source observations are read here."""
import json


def demo_config(language="en"):
    """Return reproducible, explicitly fictional values for template exercises."""
    config = {
        "DOSSIER_MODE": "demo", "SYNTHETIC": True, "LANGUAGE": language,
        "BUYER_NAME": "Synthetic Buyer", "BUYER_EMAIL": "user1@example.com",
        "BUYER_PHONE": "(555) 867-5309", "BUYER_ADDRESS": "Synthetic City, NY 10001",
        "DATE": "2026-09-22", "DISTANCE": "Synthetic example: 5 miles",
        "CLOSE_TIMING": "Synthetic example: after an independent inspection",
        "PAYMENT_METHOD": "Synthetic example: cashier's check",
        "FINANCING_TERMS": "Synthetic example: no financing",
        "TRADE_IN_TERMS": "Synthetic example: no trade-in",
        "PLATE_PLAN": "Synthetic example: request new plates",
        "TITLE": "Synthetic 2024 AcmeCorp Example Crossover purchase proposal",
        "VEHICLE_DESCRIPTION": "Fictional 2024 AcmeCorp Example Crossover, 20,000 miles",
        "DEALER_NAME_ADDRESS": "Synthetic Dealer A, Example City",
        "YEAR": "2024", "MAKE_MODEL": "AcmeCorp / Example Crossover", "TRIM": "Example Plus",
        "MILES": "20,000", "DRIVETRAIN": "Synthetic AWD", "ENGINE": "Synthetic 2.0L engine",
        "TRANSMISSION": "Synthetic automatic", "COLOR": "Synthetic blue", "MSRP": "33,000.00",
        "ASK_OTD": "32,200.00", "TARGET_OTD": "30,000.00",
        "TERMS_SUMMARY": "Synthetic proposal only; no actual offer or available vehicle",
        "PROPOSED_SALES": "27,500.00", "TAX_BASE": "27,500.00", "TAX_RATE": "8",
        "TAX_AMOUNT": "2,200.00", "TAX_ADJUSTMENT": "0.00", "STATE": "NY",
        "REG_AMOUNT": "200.00", "TITLE_AMOUNT": "100.00", "DOC_AMOUNT": "0.00",
        "OTHER_FEES": "0.00", "TRADE_IN_CREDIT": "0.00", "REBATE_AMOUNT": "0.00",
        "EXEC_SUMMARY_PARAGRAPH_1": "This synthetic document demonstrates formatting and arithmetic. Every vehicle, quote, and market observation is fictional.",
        "EXEC_SUMMARY_PARAGRAPH_2": "No dealer has been contacted. These figures do not establish a market price, a tax rule, or a buyer commitment.",
        "SUPPORT_POINT_1": "Synthetic market data exercises the comparison table.",
        "SUPPORT_POINT_2": "Synthetic pricing assumptions illustrate an offer structure.",
        "SUPPORT_POINT_3": "Two fictional quotes are included for demonstration.",
        "SUPPORT_POINT_4": "Actual warranty and certification require vehicle-specific evidence.",
        "TRIM_ANALYSIS_PARA": "Synthetic equipment differences illustrate the template; they are not manufacturer specifications.",
        "BASIC_TERM": "Synthetic: 3 years / 36,000 miles", "BASIC_STATUS": "Synthetic: unverified",
        "PWRT_TERM": "Synthetic: 5 years / 60,000 miles", "PWRT_STATUS": "Synthetic: unverified",
        "CPO_TERM": "Synthetic certification program", "CPO_LIMIT": "Synthetic limits only",
        "CPO_STATUS": "Synthetic: not certified", "CPO_OR_WARRANTY_CONDITION": "Verify any actual warranty in writing before purchase.",
        "INTERNAL_ANCHOR_PARA": "Synthetic comparison only. No actual concurrent dealer inventory was used.",
        "CLOSING_PARAGRAPH": "This is a synthetic demonstration. Do not present it as a real buyer, dealer quote, or researched purchase proposal.",
    }
    for index, average in enumerate(("28,000.00", "29,000.00", "30,000.00"), 1):
        config.update({f"SOURCE_{index}": f"Synthetic source {index}", f"GEO_{index}": "Synthetic region",
                       f"AVG_{index}": average, f"RANGE_{index}": "Synthetic range: $27,000 to $31,000",
                       f"SAMPLE_{index}": "Synthetic sample: 10 listings"})
    for index, feature in enumerate(("Upholstery", "Audio", "Wheels"), 1):
        config.update({f"FEATURE_{index}": feature, f"LOWER_{index}": "Synthetic standard option",
                       f"HIGHER_{index}": "Synthetic upgraded option"})
    config["QUOTES"] = [
        {"id": f"demo-quote-{i}", "vehicle": f"Fictional 2024 AcmeCorp Example {i}",
         "vehicle_id": f"SYNTHETIC-STOCK-{i}", "registration_state": "NY",
         "conditions": "Synthetic cash purchase, no trade-in or conditional rebates",
         "expires_on": "2026-10-01",
         "dealer": f"Synthetic Dealer {i}", "otd": price, "mileage": "20,000 miles",
         "status": "synthetic", "source_id": f"demo-source-{i}"}
        for i, price in enumerate(("29,900.00", "30,100.00"), 1)
    ]
    config["EVIDENCE"] = [
        {"id": f"demo-source-{i}", "kind": "synthetic", "source": f"https://example.com/quote-{i}",
         "source_date": "2026-09-22", "supports": [f"quote:demo-quote-{i}"]}
        for i in (1, 2)
    ]
    if language == "cn":
        config.update(TITLE="合成示例：2024 AcmeCorp 购车提案", BUYER_NAME="虚构买家",
                      EXEC_SUMMARY_PARAGRAPH_1="本文仅用于演示版式和金额校验。车辆、经销商、报价及市场记录均为虚构。",
                      EXEC_SUMMARY_PARAGRAPH_2="没有联系任何经销商。这里的数字不能作为市场行情、税费规则或买家承诺。",
                      CLOSING_PARAGRAPH="本文件是合成演示，不能作为真实购车提案或真实报价使用。")
    elif language == "es":
        config.update(TITLE="Ejemplo sintético: propuesta de compra AcmeCorp 2024", BUYER_NAME="Comprador ficticio",
                      EXEC_SUMMARY_PARAGRAPH_1="Este documento demuestra el formato y la validación de importes. Todos los vehículos, concesionarios y precios son ficticios.",
                      EXEC_SUMMARY_PARAGRAPH_2="No se ha contactado con ningún concesionario. Estos importes no acreditan precios de mercado, normas fiscales ni compromisos del comprador.",
                      CLOSING_PARAGRAPH="Esta demostración sintética no debe presentarse como una propuesta de compra ni una cotización real.")
    return config


def build():
    """Produce JSON-compatible YAML using only the standard library."""
    outputs = {}
    for language, suffix in (("en", ""), ("cn", "_cn"), ("es", "_es")):
        text = "# Generated by tools/make_fixtures.py. Synthetic demonstration only.\n"
        for key, value in demo_config(language).items():
            text += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
        outputs[f"skills/orchestrator/assets/dossier_config_template{suffix}.yaml"] = text.encode("utf-8")
    return outputs
