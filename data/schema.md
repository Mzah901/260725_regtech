# Legal Industry Map — data dictionary

File: `legal_industry_map.csv` (one row per company or product line, UTF-8, comma-separated).
Multi-value cells use ` | ` as the separator. `source_urls` holds space-separated URLs.

| Column | Meaning | Allowed values / format |
|---|---|---|
| id | Row number | integer |
| name | Company or product name | text |
| hq_country | Country of headquarters | text |
| region | Grouping used for filters | Indonesia · ASEAN · Global |
| founded | Year founded or launched | YYYY, blank if unknown |
| category | Main business category | see list below |
| secondary_category | Optional second category | same list, or blank |
| products | Main products, in plain words | text |
| target_customer | Who buys it | `|`-separated list |
| ai_native | Is the product built on AI? | Yes · Partial (AI added to an older product) · No |
| indonesian_law_coverage | Does it cover Indonesian law? | Core · Partial · None |
| business_model | How it earns money | text |
| total_funding_usd_m | Total disclosed equity funding, USD millions | number, blank = undisclosed |
| last_round | Stage of latest known round | text |
| last_round_date | Date of latest round | YYYY-MM or YYYY |
| last_round_usd_m | Size of latest round, USD millions | number or blank |
| valuation_usd_m | Latest reported valuation (or acquisition price), USD millions | number or blank |
| key_investors | Main investors named in sources | `|`-separated list |
| status | Operating status | Active · Acquired · Distressed · Unknown |
| parent_or_acquirer | Parent group or buyer | text or blank |
| source_urls | Public sources for this row | URLs |
| confidence | Overall trust in the row | High (primary or major press) · Medium (mixed) · Low (directories/aggregators only) |
| notes | Conflicts between sources, lower bounds, disclosures | text |

## Categories

Loosely based on the public Stanford CodeX TechIndex taxonomy, simplified:

- Legal research & information
- AI legal assistant
- Legal services marketplace
- Company formation & licensing
- Contract drafting & review
- Contract lifecycle management
- E-signature & digital identity
- Practice management
- Knowledge management
- Litigation & claims AI
- RegTech / compliance

## Rules

1. Public sources only. Every number needs a source URL in the same row.
2. Blank means "not disclosed", never zero.
3. Where sources conflict, use the most primary one and record the conflict in `notes`.
4. Funding raised by a parent company is not copied onto a product line's row.
