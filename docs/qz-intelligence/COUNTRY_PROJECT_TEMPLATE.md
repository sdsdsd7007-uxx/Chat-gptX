# Country Intelligence Project Template
**Template ID:** QZ-COUNTRY-TEMPLATE-001  
**Status:** PROPOSED  
Use ISO 3166-1 alpha-3 country codes, with explicit handling for territories and disputed classifications.

## Naming convention
QZ-COUNTRY-{ISO3}-{DOMAIN}-{NNN}

Examples of proposed identifiers: QZ-COUNTRY-UGA-ECON-001, QZ-COUNTRY-UGA-TRADE-001 and QZ-COUNTRY-KEN-ECON-001. These are not deployed project records.

## Country module catalogue
| Module | Research scope | Preferred source classes |
|---|---|---|
| National profile | Geography, institutions and administrative divisions | Official government and statistics office |
| Economy | GDP, inflation, labor, rates, FX and fiscal position | Statistics office, central bank, finance ministry |
| Policy & budget | National plans, budgets and implementation | Official ministry, legislature, auditor |
| Trade & industry | Imports, exports, output and suppliers | Customs/trade authorities and industry statistics |
| Agriculture & food | Production, prices and food availability | Agriculture ministry and official statistics |
| Health | Outcomes, capacity and service delivery | Health ministry and official health statistics |
| Education & skills | Access, outcomes and workforce skills | Education ministry and statistics office |
| Energy & infrastructure | Electricity, fuel, transport and communications | Regulators, ministries and official operators |
| Technology & AI | Digital access, AI policy and cybersecurity | Digital ministry, regulators and standards bodies |
| Finance & investment | Credit, banking and investment conditions | Central bank, regulator and finance ministry |
| Climate & environment | Climate exposure, resources and environment | Official meteorological/environmental agencies |
| Risk & resilience | Continuity, disaster preparedness and cyber resilience | National risk agencies and official advisories |
| Law & regulation | Laws, obligations and effective dates | Official gazette, regulator and ministry |
| People & productivity | Employment, demographics and capability | Statistics office and labor ministry |
| Market & customers | Demand, service access and consumer context | Official surveys and transparent research |
| Regional relations | Agreements and cross-border dependencies | Foreign affairs/trade authorities and regional bodies |

## Minimum country metadata
Country key and jurisdiction caveats; project owner and independent reviewer; scope and data classification; source register with publisher, reference, publication date, observation period, retrieval time, revision and units; indicator dictionary; legal context; risk register; uncertainty and data gaps; recommendation log; model version and review schedule.

## Evidence and comparability rules
1. Prefer official national sources for country facts; use international sources for comparisons.
2. Separate publication date from the period measured.
3. Mark findings VERIFIED, REPORTED, ESTIMATED, STALE, UNKNOWN or NOT CONNECTED.
4. Preserve revisions and series breaks; do not splice incompatible definitions.
5. Harmonize units, currency basis, population denominator, fiscal year and methodology before comparisons.
6. Missing data is not zero; disclose coverage bias.
7. Local legal interpretation requires qualified review.
8. Do not infer individual traits from country averages.
9. Sensitive recommendations require independent review and human authorization.

## Country dashboard
Dated signals; structural context; sector/factor findings; cross-border dependencies; risks and scenario sensitivities; KPI status/baseline/target/trend/freshness; recommendations and owners; limitations and next validation.

## Uganda starter source map
Recheck for newer releases on every run. These are source entry points, not proof of live connectivity:
- UBOS: https://www.ubos.org/
- Bank of Uganda: https://www.bou.or.ug/
- MoFPED: https://www.finance.go.ug/
- MoFPED economy reports: https://mepd.finance.go.ug/

## Acceptance criteria
Required modules are covered or marked not applicable with rationale; source and indicator definitions are reviewed; at least one representative time series is checked for revision/freshness; uncertainty is documented; schema validation passes; independent reviewer signs the scoped acceptance record.
