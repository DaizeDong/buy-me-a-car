"""Fictional purchase scenarios and routing queries built without runtime data."""
import json

ROUTES = [
    ('orchestrator', 'help me buy a car', 'Help me buy a used compact SUV, ZIP 10001, budget $30000 OTD, cash, within two months.'),
    ('dealer-reply-drafter', 'draft counter to dealer', 'Draft a counter to this dealer email using only my approved offer and documented competing quote.'),
    ('carfax-pdf-review', 'review this CARFAX', 'Review this CARFAX PDF for accident entries and gaps in service records.'),
    ('close-day-checklist', 'close day checklist', 'Give me the close day checklist before I sign the purchase contract.'),
    ('cpo-eligibility', 'CPO eligibility', 'Check factory CPO eligibility and current coverage for this used vehicle.'),
    ('dossier-builder', 'build dossier', 'Build a private decision dossier from my verified quotes and inspection evidence.'),
    ('ev-buyer-helper', 'EV purchase advice', 'Help me check current EV purchase incentives and whether I can charge at home.'),
    ('inbox-triage', 'triage dealer replies', 'Triage dealer replies, identify out-of-office messages, and record processed message IDs.'),
    ('insurance-shopper', 'shop car insurance', 'Shop car insurance and confirm the coverage binder required before collection.'),
    ('lease-vs-cash-analyzer', 'lease vs cash', 'Compare lease vs cash purchase using the quoted money factor and residual.'),
    ('otd-calculator', 'compute OTD', 'Compute OTD from a $30000 sale, explicit fees, and a confirmed registering state.'),
    ('payment-method-decider', 'choose payment method', 'Choose payment method: cashier check or credit card with a 3 percent surcharge.'),
    ('ppi-scheduler', 'book pre-purchase inspection', 'Plan how to book pre-purchase inspection with an independent mechanic.'),
    ('quote-evidence-collector', 'collect quote evidence', 'Collect quote evidence from these source links and retain dates and original artifacts.'),
    ('state-fee-lookup', 'state fee lookup', 'Look up the current state fee rules and tell me which fields still need official verification.'),
    ('trade-in-valuator', 'value my trade-in', 'Value my trade-in separately from its lien payoff and purchase tax treatment.'),
]


def _json(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def build():
    skills = {slug: {'name': slug, 'triggers': [trigger], 'readme_triggers': [trigger]}
              for slug, trigger, _ in ROUTES}
    cases = [{'id': f'R{i:02}', 'prompt': prompt, 'expected_skill': slug,
              'acceptable_skills': [slug], 'note': 'Synthetic task with one primary requested output.'}
             for i, (slug, _, prompt) in enumerate(ROUTES, 1)]
    for i, (slug, prompt, accepted) in enumerate([
        ('orchestrator', '帮我找车，预算三万美元落地价，邮编10001，先确认需求。', ['orchestrator']),
        ('dealer-reply-drafter', '给 dealer 起草回信，只使用我明确授权的报价，不透露最高预算。', ['dealer-reply-drafter']),
        ('dossier-builder', 'Crear un dossier con las ofertas verificadas y las fuentes.', ['dossier-builder']),
        ('state-fee-lookup', 'Before calculating a total, verify whether this state allows a trade-in tax credit.', ['state-fee-lookup', 'otd-calculator']),
    ], 17):
        cases.append({'id': f'R{i:02}', 'prompt': prompt, 'expected_skill': slug,
                      'acceptable_skills': accepted, 'note': 'Synthetic bilingual or narrowly ambiguous request.'})
    result = {
        'eval/fixtures/routing_prompts.json': _json({'_meta': {'synthetic': True, 'generated_by': 'tools/make_fixtures.py', 'skill_universe': list(skills)}, 'cases': cases}),
        'eval/golden/routing.json': _json({'_comment': 'Generated synthetic vocabulary for static routing checks, not measured host behavior.', 'skills': skills,
                                         'readme_trigger_table': [{'phrase': trigger, 'expected': slug} for slug, trigger, _ in ROUTES]}),
    }
    scenarios = [
        ('01_used_outback_ct_cash', 'Used SUV, cash, CT', 'Cash, used vehicle, no trade.', 'Verify the Connecticut tax and fee fields before computing. Request a written comparable quote and an independent inspection.'),
        ('02_new_rav4_hybrid_pa_financing', 'New hybrid, financing, PA', 'Loan preapproval supplied; new vehicle.', 'Separate price, financing and add-ons. Verify the effective APR, total loan cost and conditional rebates.'),
        ('03_used_crv_ca_trade', 'Used SUV with trade, CA', 'Trade valuation and payoff supplied separately.', 'Use the confirmed California tax treatment. Do not subtract the loan payoff from the trade tax basis.'),
        ('04_new_ioniq5_ev_tx_cash', 'New EV, cash, TX', 'Home charging has not been confirmed.', 'Check current incentives and charging access. Do not inherit historical federal credit assumptions.'),
        ('05_used_f150_il_finance_trade', 'Pickup with financed trade, IL', 'Trade has a lien; tow usage requires inspection.', 'Verify Illinois trade treatment on the purchase date, get lender payoff instructions, and inspect towing-related wear.'),
        ('06_lease_glc_ny', 'Lease, NY', '36 months; annual mileage and residual documented.', 'Use lease-specific tax and money-factor rules. Do not run a purchase tax formula on lease payments.'),
        ('07_private_party_civic_nj', 'Private seller, NJ', 'One seller; no dealer finance office.', 'Verify title, lien, tax basis and safe payment. Do not invent dealer doc fees or mass dealer outreach.'),
        ('08_cpo_grand_cherokee_stellantis_tx', 'Manufacturer-certified SUV, TX', 'Seller claims manufacturer certification.', 'Require the VIN-specific manufacturer certificate and current warranty terms. A dealer label alone is not proof.'),
    ]
    for slug, title, criteria, checks in scenarios:
        result[f'examples/{slug}.md'] = (
            f'# Synthetic scenario: {title}\n\n'
            'Generated by tools/make_fixtures.py. All people, counterparties, preferences and amounts below are fictional. '
            'This is an evaluation input and expected behavior, not an observed purchase outcome.\n\n'
            'Buyer: Alex Example, user1@example.com, (555) 867-5309. Seller: Acme Motors (or one fictional private seller). '
            'The example mailing ZIP is 10001; the registering state in the scenario must be confirmed separately.\n\n'
            f'Criteria: {criteria}\n\nExpected checks: {checks}\n\n'
            'Do not send any message during replay. Keep the private ceiling separate from the authorized outward offer. '
            'Capture actual output and tool receipts if this scenario is run; a written expectation is not a pass.\n'
        ).encode('utf-8')
    leaks = [
        ('D8_ct_tire_fee', 'state-fee mismatch', 'The supplied fictional comparison says lines labelled supplemental titling and tire fee do not apply to this transaction.',
         'Sales $28000; tax $1800; doc $500; title $100; registration $100; supplemental titling $10; tire fee $5; total $30515.',
         'Require current applicability evidence for both disputed lines and request a full revised quote. These fixture amounts are assumptions, not current state law.'),
        ('D9_rav4_adm', 'dealer markup', 'The supplied fictional MSRP is $30000; the seller adds a separate dealer adjustment.',
         'Sale at MSRP $30000; dealer adjustment $1500; quoted financing discussed separately.',
         'Identify the dealer adjustment as a discretionary markup and keep its removal separate from financing terms.'),
        ('D10_bait_switch', 'substitute vehicle', 'The original fictional VIN is unavailable; the substitute has different mileage and costs $2000 more.',
         'The original vehicle sold. Please consider the substitute at an additional $2000.',
         'Verify availability and the original sold status. Obtain a fresh quote and supported comparisons; do not infer fraud or fabricate a per-mile adjustment.'),
    ]
    for slug, title, assumption, body, expected in leaks:
        result[f'eval/fixtures/leak_quotes/{slug}.md'] = (
            f'# Synthetic fixture: {title}\n\nGenerated by tools/make_fixtures.py. No actual buyer or dealer interaction.\n\n'
            f'Assumption: {assumption}\n\nexpected_judge_flags: {expected}\n'
            'correct_skill_route: dealer-reply-drafter\n\n'
            f'From: Sam at Acme Motors <sales@example.com>\nSubject: Synthetic vehicle quote\n\n{body}\n'
        ).encode('utf-8')
    return result
