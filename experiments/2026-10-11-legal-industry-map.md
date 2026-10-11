# Legal Industry Map (pilot)

**Date:** 2026-10-11
**Status:** Pilot built. Waiting for owner review.
**Merged with:** "Legal Startup Reverse Engineer" idea. This dataset is the base for later deep dives on 2–3 companies.

**Interactive map:** https://claude.ai/artifact/9iALtpMBCiDZXF4x5zytDw (claude.ai artifact; will move to https://lab.statuta.id)

## Question / hypothesis

What does the legal-tech market look like in Indonesia compared with ASEAN and the global market?

Hypothesis: global investment goes to AI-native legal assistants, while Indonesian legal-tech money goes elsewhere (e-signature and services). If so, AI legal research for Indonesian law is an underfunded gap.

## Method

1. Fixed a schema and category list first (`data/schema.md`).
2. Picked a pilot sample of 27 companies: 11 Indonesia, 4 rest of ASEAN, 12 global.
3. Claude ran web searches for each company and filled one CSV row per company, with source URLs in every row.
   Valuation is filled only where a credible outlet reported it.
4. `scripts/build_map.py` turns the CSV into a filterable web page (`site/legal-industry-map.html`).

## Sources used

All public web sources. Each row in `data/legal_industry_map.csv` lists its own URLs. The main types are:
company press releases and websites; news (Bloomberg Law, DealStreetAsia, DailySocial, e27, TechNode Global, BetaKit, Legal Cheek);
directories and aggregators (Stanford CodeX TechIndex https://techindex.law.stanford.edu, CB Insights, Sacra, Dealroom, Preqin, Tracxn).

## Tools and models

- Claude Code (web), with web search, for collection and drafting.
- Python 3 (standard library only) for the build script.
- Plain HTML/JS for the page. No external libraries.

## Result

- 27 rows. 15 of 27 (56%) have no disclosed total funding, so the expectation that "valuation mostly won't exist" was right.
- Disclosed total funding in the sample: Indonesia about USD 115M, all of it in e-signature/digital identity (Privy, VIDA). ASEAN about USD 27M. Global about USD 3.9B.
- None of the 11 Indonesian rows in legal research or AI legal assistance has disclosed funding.
- The hypothesis is supported in this sample, but the sample is small and hand-picked. It is not a census:
  Tracxn counted 44 Indonesian legal-tech companies in July 2025.

## Known limitations and error notes

- Founded years for most global companies come from background knowledge. The row notes flag this.
- Several totals are lower bounds (VIDA, Lupl, Harvey). Notes mark them.
- Aggregator figures (CB Insights, Tracxn, Sacra) are secondary and sometimes conflict. Conflicts are recorded in `notes`.
- Stanford TechIndex, Tracxn and DailySocial pages could not be fetched directly from this environment. Their content was read through search-result summaries.
- Rows marked confidence = Low need checking before any public use.
- Selection bias: the sample favours well-known and well-covered companies.

## Conflict-of-interest disclosure

The author works at Hukumonline, which appears in this dataset together with its subsidiaries Justika and Easybiz.
Those rows use public sources only. No internal or non-public information was used.
Pasal.id is also a data source for this lab, and this is disclosed in its row.

## Evaluation plan (owner)

- Pick 6 random rows (about 20%) and check each field against its sources.
- Record errors per field (founded, category, funding, last round, valuation, status) in the table below.
- Rows with any error get fixed, and the error rate is reported in this log.

| Row id | Fields checked | Errors found | Fixed? |
|---|---|---|---|
| | | | |

## What the owner reviewed and approved

_Pending owner review._
