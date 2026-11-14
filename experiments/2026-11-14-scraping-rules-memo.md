# Rules for scraping legal sources (memo)

**Date:** 2026-11-14
**Status:** _Draft, not yet reviewed by the owner._ Built with Claude Opus 5.5.
**Idea:** #6 "Data Scrapping Rules?" (Ideas Index). It unblocks #13, #23 and #31.

**Output:** [`docs/scraping-rules.md`](../docs/scraping-rules.md), a memo with a go/no-go verdict per source site and a checklist to run before any automated collection.

## Question / hypothesis

Under Indonesian law, and under each site's own rules, when may this lab collect regulations and court decisions automatically?

Hypothesis: copyright is not the problem, because regulations and decisions have no copyright. The real limits are the computer-access offences in the new KUHP, each site's terms and technical barriers, and personal data in court decisions.

## Method

1. Read the relevant provisions from Pasal.id:
   - UU 28/2014 Pasal 40–43
   - KUHP Pasal 332–335, including the UU 1/2026 rewrite of Pasal 332
   - UU ITE Pasal 32–34
   - UU PDP Pasal 2, 15, 16, 20
   - UU KIP Pasal 2 and 4
2. Fetched robots.txt for six sources and checked for bot challenges.
3. Read the Pasal.id terms and API pages.
4. Wrote a verdict per site and a checklist, then audited the lab's own UU ITE consolidation against the result.

## Sources used

- UU 28/2014: https://pasal.id/peraturan/uu/uu-no-28-tahun-2014
- UU 1/2023 (KUHP): https://pasal.id/peraturan/uu/uu-no-1-tahun-2023; UU 1/2026 Pasal VII angka 35: https://pasal.id/peraturan/uu/uu-no-1-tahun-2026
- UU 11/2008: https://pasal.id/peraturan/uu/uu-no-11-tahun-2008
- UU 27/2022: https://pasal.id/peraturan/uu/uu-no-27-tahun-2022
- UU 14/2008: https://pasal.id/peraturan/uu/uu-no-14-tahun-2008
- robots.txt: peraturan.go.id, jdihn.go.id, peraturan.bpk.go.id, putusan3.mahkamahagung.go.id, mkri.id, pasal.id (all fetched 2026-11-14)
- Pasal.id terms: https://pasal.id/ketentuan (effective 5 October 2026); API page: https://pasal.id/api

## Tools and models

Claude Code (desktop) with Claude Opus 5.5 and the Pasal.id MCP connector; `curl` for robots.txt and response headers; a web-page reader for the Pasal.id terms.

## Result

- **Hypothesis supported.** Copyright is not the limit for the law text itself (Pasal 42), but databases and data compilations are protected works (Pasal 40 ayat (1) huruf n and p).
  So a private site's structure and annotations are off-limits, while the text from official sources is free.
- **The access offence got wider.** UU 1/2026 rewrote KUHP Pasal 332 and removed "dengan sengaja". Access "tanpa hak atau melawan hukum" is enough on its face.
  Getting past a security measure (ayat (3)) is the heaviest form, and Pasal 333 covers government systems specifically.
- **Per-site verdicts:** go for peraturan.go.id, jdihn.go.id (except `/search-api/`) and MK decisions; by hand only for MA and BPK (bot challenges; MA also signals `ai-train=no`).
  For Pasal.id, read through MCP or the website only, because its terms ban automated bulk extraction without a licence.
- **Self-audit finding.** The UU ITE consolidation parsed Pasal.id's page data for three laws. The volume was small and the text is public domain, but the method sits close to Pasal.id's extraction ban.
  The memo recommends re-sourcing those files from the official PDFs.

## Known limitations and error notes

- Legal analysis by an AI model, not checked by the owner yet. What "tanpa hak" means for automated access to a public site is not settled law.
- The JDIHN terms page could not be loaded (TLS certificate error). No terms pages were found for peraturan.go.id, MA, MK or BPK.
- No implementing PP PDP was found in Pasal.id's corpus. That is not proof that none exists.
- KUHP and UU PDP text comes from Pasal.id. KUHP and UU PDP are marked verified there; UU 28/2014 and UU KIP are not.
- Foreign law (US scraping cases, the EU database right) is not covered.

## What the owner reviewed

_Pending._ Plan: read the whole memo, then decide:
- Do you agree with the per-site verdicts, especially Pasal.id?
- Should the UU ITE source files be re-sourced from the official PDFs?
- Should the lab ask Pasal.id for a licence, or stay within MCP limits?
