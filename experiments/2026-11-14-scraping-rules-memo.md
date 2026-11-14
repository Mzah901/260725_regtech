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
   - UU PDP Pasal 4 and 25 (children's data)
   - PP 17/2025 on child protection by electronic system operators, read in full from the owner's copy (Salinan, LN 2025 No. 36)
   - PP 33/2026, the implementing regulation of UU PDP, read from the owner's copy (Salinan, LN 2026 No. 88), added after the owner pointed out it was missing
2. Fetched robots.txt for six sources and checked for bot challenges.
3. Read the Pasal.id terms and API pages.
4. Wrote a verdict per site and a checklist, then audited the lab's own UU ITE consolidation against the result.
5. Checked every quoted phrase from the Pasal.id terms and API pages against the raw page HTML, not a summary.
   All matched verbatim. One clause of UU 28/2014 (Pasal 40 ayat (1) huruf p) is OCR-garbled in Pasal.id, so it is paraphrased, not quoted.

## Sources used

- UU 28/2014: https://pasal.id/peraturan/uu/uu-no-28-tahun-2014
- UU 1/2023 (KUHP): https://pasal.id/peraturan/uu/uu-no-1-tahun-2023; UU 1/2026 Pasal VII angka 35: https://pasal.id/peraturan/uu/uu-no-1-tahun-2026
- UU 11/2008: https://pasal.id/peraturan/uu/uu-no-11-tahun-2008
- UU 27/2022: https://pasal.id/peraturan/uu/uu-no-27-tahun-2022
- UU 14/2008: https://pasal.id/peraturan/uu/uu-no-14-tahun-2008
- PP 17/2025: official Salinan PDF supplied by the owner; also at https://pasal.id/peraturan/pp/pp-no-17-tahun-2025
- PP 33/2026: official Salinan PDF supplied by the owner (not in Pasal.id's corpus as of 2026-11-14)
- robots.txt: peraturan.go.id, jdihn.go.id, peraturan.bpk.go.id, putusan3.mahkamahagung.go.id, mkri.id, pasal.id (all fetched 2026-11-14)
- Pasal.id terms: https://pasal.id/ketentuan (effective 5 October 2026); API page: https://pasal.id/api

## Tools and models

Claude Code (desktop) with Claude Opus 5.5 and the Pasal.id MCP connector; `curl` for robots.txt and response headers; a web-page reader for the Pasal.id terms.

## Result

- **Hypothesis supported.** Copyright is not the limit for the law text itself (Pasal 42), but databases and data compilations are protected works (Pasal 40 ayat (1) huruf n and p).
  So a private site's structure and annotations are off-limits, while the text from official sources is free.
- **The access offence is about what makes access "tanpa hak", not about intent.** UU 1/2026 rewrote KUHP Pasal 332 and removed the words "dengan sengaja".
  But KUHP Pasal 36 ayat (2) makes intent the default for every offence, so this is drafting clean-up, not a wider offence (an early draft of this memo got that wrong).
  Getting past a security measure (ayat (3)) is the heaviest form, and Pasal 333 covers government systems specifically.
- **Per-site verdicts:** go for peraturan.go.id, jdihn.go.id (except `/search-api/`) and MK decisions; by hand only for MA and BPK (bot challenges; MA also signals `ai-train=no`).
  For Pasal.id, read through MCP or the website only, because its terms ban automated bulk extraction without a licence.
- **Children.** Children's data is "spesifik" personal data that needs parental consent (UU PDP Pasal 4, 25), so the lab never collects data that identifies a child.
  PP 17/2025 governs services children use, not datasets about them. It probably does not cover statuta.id, which has no accounts, no personal data and no tracking.
  But its "design attractive to children" indicator (Pasal 4 ayat (2) huruf d) sits awkwardly with the site's game-like 3D home page, so the memo flags it. The same PP was added as a note on UU ITE Pasal 16A and 16B in the consolidation.
- **Self-audit finding.** The UU ITE consolidation parsed Pasal.id's page data for three laws. The volume was small and the text is public domain, but the method sits close to Pasal.id's extraction ban.
  The memo recommends re-sourcing those files from the official PDFs.
- **PP 33/2026 (added later).** The UU PDP implementing regulation, in force from 16 January 2027, says public-domain data still counts when combined to identify someone (Pasal 7 ayat (3)), and sets five conditions for the research exemption (Pasal 154).
  The memo now asks for a written balancing note before any dataset built from court decisions.

## Known limitations and error notes

- Legal analysis by an AI model, not checked by the owner yet. What "tanpa hak" means for automated access to a public site is not settled law.
- The JDIHN terms page could not be loaded (TLS certificate error). No terms pages were found for peraturan.go.id, MA, MK or BPK.
- **Missed source, now fixed.** The first version said no implementing PP PDP was found. That was wrong: PP 33/2026 exists but is not in Pasal.id's corpus, and the search relied on Pasal.id alone. The owner supplied it.
  PP 33/2026 takes effect on 16 January 2027 (Pasal 225). It confirms the memo's direction (no exemption for public data, a narrow household exemption) and adds one rule: a written balancing note before any dataset built from court decisions.
  It implements UU PDP only, so it adds nothing to the UU ITE consolidation. Lesson: for a recent regulation, check peraturan.go.id or JDIH too, not just one database.
- PP 33/2026 text was extracted from the scanned Salinan; only the provisions cited in the memo were read closely, not all 225 articles.
- KUHP and UU PDP text comes from Pasal.id. KUHP and UU PDP are marked verified there; UU 28/2014 and UU KIP are not.
- Foreign law (US scraping cases, the EU database right) is not covered.
- PP 17/2025 text was extracted from a scanned PDF and has OCR errors (for example, the enactment date reads "27 Maret 2021"; it is 2025).
  The Minister's decree on "likely to be used by children" indicators was not read.

## What the owner reviewed

_Pending._ Plan: read the whole memo, then decide:
- Do you agree with the per-site verdicts, especially Pasal.id?
- Should the UU ITE source files be re-sourced from the official PDFs?
- Should the lab ask Pasal.id for a licence, or stay within MCP limits?
