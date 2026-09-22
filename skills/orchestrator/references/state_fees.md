# US vehicle tax and fee reference

The dataset in `data/state_fees.json` contains 51 jurisdiction records. Its field evidence is the authority for this tool; an inherited boolean or timestamp is not proof. Legacy values without field-level official evidence remain unverified, are hidden in the generated table and cannot authorize a calculation.

The old prose tables contained contradictory taxes, title amounts, fee caps and trade rules. This reference now displays only reviewed fields and links to their evidence. It does not claim a complete 51-state legal or DMV-fee audit.

## Calculation scope

The currently enabled profiles handle ordinary in-state resident dealer purchases of passenger ICE vehicles with no rebate, exemption or unusual valuation. The calculator requires explicit title and registration costs. It separates taxable additions, independently verified nontaxable additions, gross trade allowance and payoff. The output is always an estimate; verified tax rules do not establish a confirmed dealer offer or complete fee schedule.

Enabled jurisdictions are CT, MD, MI, NC, NJ, NY, TX and VA. NJ requires explicit used condition; new vehicles are refused because the separate luxury/fuel-inefficient surcharge is not encoded. NY requires the purchaser-residence local rate and a qualifying separately stated doc service of at most $175. CT classifies the vehicle before trade at the $50,000 threshold and taxes separately entered warranties at 6.35%. MI temporary-registration and electronic-filing charges are taxable additions, not nontaxable registration inputs.

CT transactions where the warranty alone could cross $50,000 require a separate itemized tax review; the reviewed sources establish the warranty rate but do not explicitly settle that threshold classification. A reverse estimate searches the supported intervals and warns if a higher price was excluded for this reason.

Unsupported TAVT, weight/value-based excise, privilege taxes, local rules, leases, private-party sales, EVs, commercial vehicles and new-resident transfers require a transaction-specific official or dealer calculation. A headline percentage must never be used as a substitute.

## Reviewed field summary

The table is generated, including explicit unknowns. Use `render_state_data.py --check` to check the three reference surfaces against the JSON. “Supported” describes an implemented profile, subject to its runtime field-evidence gate; it is not a whole-state verification claim.

<!-- state-data:start -->
| State | Reviewed tax rate | Doc cap | Title | Registration | Trade credit | Calculator profile |
|---|---|---|---|---|---|---|
| AK | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| AL | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| AR | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| AZ | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| CA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| CO | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| CT | 6.35%; 7.75% over $50,000 | Unverified | Unverified | Unverified | Full eligible allowance | supported |
| DC | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| DE | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| FL | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| GA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| HI | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| IA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| ID | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| IL | Unverified | Unverified | Unverified | Unverified | Full eligible allowance | unsupported |
| IN | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| KS | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| KY | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| LA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MD | 6.5% | $800 | $200 | Unverified | Full eligible allowance | supported |
| ME | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MI | 6% | Unverified | Unverified | Unverified | Up to $12,000 (2026); annual schedule | supported |
| MN | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MO | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MS | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MT | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NC | 3% | Unverified | Unverified | Unverified | Full eligible allowance | supported |
| ND | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NE | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NH | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NJ | 6.625% | Unverified | Unverified | Unverified | Full eligible allowance | supported (used only) |
| NM | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NV | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NY | 4% + supplied local rate | $175 | Unverified | Unverified | Full eligible allowance | supported |
| OH | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| OK | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| OR | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| PA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| RI | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| SC | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| SD | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| TN | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| TX | 6.25% | Unverified | Unverified | Unverified | Full eligible allowance | supported |
| UT | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| VA | 4.15% | Unverified | Unverified | Unverified | No tax credit | supported |
| VT | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WI | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WV | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WY | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
<!-- state-data:end -->

## Official evidence reviewed on September 22, 2026

| Field or rule | Verified result and scope | Official source |
|---|---|---|
| MD tax and title change | Non-rental excise 6.5%; standard title $200; effective July 1, 2025 | [MVA implementation notice](https://mva.maryland.gov/your-mva-guide/businesses/bulletins-businesses/new-vehicle-registration-fees-and-term) |
| MD dealer tax base | Certified dealer price including processing charge, less eligible trade; local certificate-of-title tax prohibited | [Transportation 13-809](https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gtr&section=13-809) |
| MD doc cap | $800 from July 1, 2024 | [Transportation 15-311.1](https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gtr&section=15-311.1) |
| MD registration | Varies by class, weight, term and surcharge; no universal $135 default retained for calculation | [MVA fees](https://mva.maryland.gov/title-registration/fees-payment-options) |
| TX motor vehicle tax | 6.25%, eligible same-transaction trade deducted | [Comptroller sales and use tax](https://comptroller.texas.gov/taxes/motor-vehicle/sales-use.php) |
| TX doc taxability | Separately stated documentary charge is not motor-vehicle-tax consideration | [Total Consideration, March 2026 guide](https://comptroller.texas.gov/taxes/publications/96-254/total-consideration.php) |
| TX trade value | Gross vehicle allowance, not equity; direct transfer to the seller in the same transaction; no tax on a trade-down | [Comptroller trade-ins](https://comptroller.texas.gov/taxes/publications/96-254/trade-ins.php) |
| VA tax and trade | 4.15%, minimum $75; doc taxable, no trade reduction | [Virginia DMV](https://www.dmv.virginia.gov/vehicles/taxes-fees/sut) |
| VA processing charge | Disclosure provision contains no $599 cap; other applicable limits not comprehensively verified | [Code 46.2-1530](https://law.lis.virginia.gov/vacode/title46.2/chapter15/section46.2-1530/) |
| NC HUT | 3% includes admin fee; eligible trade credit; $2,000 maximum only for specified commercial/RV categories | [G.S. 105-187.3](https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/BySection/Chapter_105/GS_105-187.3.html) |
| NC admin fee | Disclosure rule does not establish the old $129 cap | [G.S. 20-101.1](https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/BySection/Chapter_20/GS_20-101.1.html) |
| NJ documentary fee | Itemize actual services and prices; old $799 maximum unsupported | [N.J.A.C. 13:45A-26B.3](https://www.njconsumeraffairs.gov/regulations/Chapter-45A-Administrative-Rules-of-the-Division-of-Consumer-Affairs.pdf) |
| NJ used purchase | 6.625%; doc taxable, eligible trade credit; actual MVC title/registration excluded | [Consumer Automotive Tax Guide](https://www.nj.gov/treasury/taxation/documents/pdf/guides/New-Jersey-Consumer-Automotive-Tax-Guide.pdf), [rate guide](https://www.nj.gov/treasury/taxation/pdf/pubs/sales/su4.pdf) |
| NJ new-vehicle exclusion | Separate 0.4% surcharge on new passenger automobiles priced at least $45,000 or rated below 19 mpg; not encoded | [Luxury and Fuel-Inefficient Vehicle Surcharge](https://www.nj.gov/treasury/taxation/luxury.shtml) |
| NY tax and doc | 4% plus residence-local rate; eligible trade deductible; separately stated reasonable title/registration service exempt, current DMV service fee $175 | [Publication 838](https://www.tax.ny.gov/pdf/publications/sales/pub838.pdf), [current DMV page](https://dmv.ny.gov/titles/buy-sell-or-transfer-vehicle-ownership), [rate page](https://www.tax.ny.gov/pubs_and_bulls/tg_bulletins/st/sales_tax_rates_additional_sales_taxes_and_fees.htm) |
| CT purchase and warranty | 6.35%; 7.75% over $50,000 before trade; doc taxable; separately stated service/extended warranties remain at 6.35% | [DMV tax calculator categories](https://portal.ct.gov/dmv/vehicle-services/sales-tax-registrations/sales-tax-calculator), [dealer purchase rules](https://portal.ct.gov/dmv/vehicle-services/sales-tax-registrations), [valuation notice with rate correction](https://portal.ct.gov/drs/publications/special-notices/2011/sn-2011-10?archived=true) |
| IL trade credit | Full eligible like-kind credit resumed January 1, 2022; $10,000 cap was limited to 2020-2021 | [35 ILCS 120/1](https://www.ilga.gov/legislation/ilcs/documents/003501200K1.htm) |
| MI trade credit | $5,000 in 2019, +$1,000/year; $12,000 in 2026; unlimited from 2029 | [MCL 205.51](https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-205-51) |
| MI tax and doc | 6%; doc and specified temporary-registration/electronic-filing charges taxable; tax rounded to cents | [Dealer Manual Chapter 7](https://www.michigan.gov/-/media/Project/Websites/sos/01preston/Dealer_Manual_Chapter_7.pdf?rev=ee8349e8aa5f426fb637967e6b1fcaf3), [Chapter 8, April 2026](https://www.michigan.gov/sos/-/media/Project/Websites/sos/01preston/Dealer_Manual_Chapter_8.pdf?rev=c533c705a9594ca780efff27a0f7cfcd&hash=EA004E836D8A681CE7FC16D26E045320) |

The IL and MI statutes and the NJ administrative-rule PDF were read through Jina Reader's rendering of the official URL after direct access failed. The NJ PDF identifies a June 20, 2022 revision, so it does not by itself prove a current statewide absence of fee limits. JSON records that distinction.

NY Publication 838 is dated December 2012 and was downloaded and re-read alongside the current DMV fee and tax-rate pages. CT's valuation notice is archived from 2011; its header states the 2015 increase to 7.75%, and the current DMV page confirms that rate. Review on September 22, 2026 does not turn either source into a 2026 publication. The JSON retains these source-age limits and the supporting citations.

IL's full eligible trade-credit rule is encoded, but its complete OTD profile remains unavailable. ST-556 instructs rounding return lines to whole dollars, and the applicable local rate needs transaction-specific sourcing; the ordinary cents-based engine is not presented as an Illinois tax-return implementation.

For the MD dealer profile, residual taxable bases below $640 require separate valuation/minimum review. The statutory $640 floor concerns specified private-sale valuation branches; the general fee page's minimum summary is not treated as a universal dealer formula.

## Review rules

A verified field must store its exact value, official source URL, supporting excerpt, real review date and applicability. Record an effective date only when the source supports it. If original commencement is unknown, leave it null and limit use to the review date forward. Annual fee/cap schedules need a year or explicit statutory schedule.

The default three-month freshness gate catches expired review windows; it cannot discover a new law by itself. Recheck transaction-specific changes before relying on a quote. Full-dataset strict freshness is expected to fail while any reference fields remain unverified. `--calculator --strict` checks only the required tax-rule fields for enabled profiles.

The deterministic [OTD cases](../../../eval/golden/otd_cases.json) are synthetic, generated by `tools/make_fixtures.py`, and use independently specified expected amounts. They do not prove real dealer performance.
