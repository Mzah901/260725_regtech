# GitHub as infrastructure for law-making (research note + column)

**Date:** 2026-11-22
**Status:** _Draft, not yet reviewed by the owner._ Built with Claude Code.

**Output:**
- [`docs/github-legislation.md`](../docs/github-legislation.md): research note with a problem table, a solvability rating, foreign examples, a Mermaid diagram (bagan) and critiques
- [`content/column/github-sebagai-ruang-legislasi.md`](../content/column/github-sebagai-ruang-legislasi.md): the same argument as a short column post

## Question / hypothesis

Could a TAP MPR, or law-making in general, be produced and harmonised on GitHub? Which documented problems in Indonesian law-making would a Git workflow actually solve?

Hypothesis: Git can't confer legal validity, but it can solve the *text* problems (versioning, consolidation, transparency of drafts) and support harmonisation and participation. It can't solve the *political* ones (planning, off-the-record bargaining).

## Method

1. Checked the legal frame in Pasal.id: UU 12/2011 Pasal 46–47 (who coordinates harmonisation) and PP 71/2019 Pasal 20–21 (where public systems must store data).
2. Searched the web for the latest data on regulatory quality: PSHK 2025, Ministry of Law harmonisation figures, World Bank WGI.
3. Searched for foreign examples of Git and legislation (DC, EU LEOS, US House, Spain, Germany, France) and recorded for each one whether it is official or civic.
4. Rated each problem as Solves, Supports or Doesn't touch, and drew the workflow as a Mermaid diagram.

## Sources used

Listed in full at the end of [`docs/github-legislation.md`](../docs/github-legislation.md#sources), grouped as 01 Official / 02 Research and civil society / 03 Foreign examples.
No employer material was used. The owner's local folder "02 Konsolidasi dan Hukumonline" was not used and should stay out of this repo (guardrails 1–2).

## Tools and models

Claude Code (cloud session) with Claude Opus 5.5, the Pasal.id MCP connector and web search. Page fetches to pshk.or.id and kompas.id failed (host not reachable from the session), so those figures come from search-result summaries.

## Result

- **Hypothesis supported.** Two problems are solvable through Git: no official consolidated text (P7), and opaque drafting (P3, but only if publication is mandated). Four it can only support: harmonisation bottleneck, disharmony, participation, hyper-regulation. Two it doesn't touch: Prolegnas planning, and regulatory-quality perception.
- The owner's "branch per fraksi, merged by Baleg" idea fits UU 12/2011 Pasal 46 ayat (2) and 47 ayat (3). It needs a split between a `rancangan` branch (merged by Baleg) and `main` (moved only after plenary approval and promulgation).
- Every *official* foreign example keeps validity with the legislature and uses Git for text. The EU self-hosts, which answers the sovereignty problem raised by PP 71/2019 Pasal 20 ayat (2).

## Known limitations and error notes

- PSHK 2025 numbers (87.5%, 71.4%, 9 of 52) come from press summaries, not the PSHK PDF. They need checking.
- The newest PSHK regulation count found (42,996) dates from around 2019–2020.
- WGI figures are from a secondary aggregator, and the World Bank revised the series in December 2025.
- The owner's own journal (local "Regulatory Making" folder) was not read. Its findings and writing style still need to be merged into the column.

## What the owner reviewed and approved

Nothing yet.
