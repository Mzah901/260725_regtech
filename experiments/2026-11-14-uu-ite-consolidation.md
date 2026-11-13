# Consolidated UU ITE (pilot)

**Date:** 2026-11-14
**Status:** _Draft, not yet reviewed by the owner._ Built with Claude Opus 5.5; a Claude Fable 5.2 re-run is planned as a comparison.
**Idea:** #8 "Pembuatan Peraturan Konsolidasi" (Ideas Index).

**Output:** `data/consolidation/uu-ite/uu-ite-konsolidasi.md`, built by `scripts/consolidate.py` from the files in `data/consolidation/uu-ite/`.

## Question / hypothesis

Can AI, working only from public sources, produce a correct consolidated text of an Indonesian law that has been amended more than once, and say clearly which parts are still in force today?

UU 11/2008 (UU ITE) is a hard test case. It was amended twice (UU 19/2016, UU 1/2024). Then, on 2 January 2026, the new KUHP (UU 1/2023) and UU 1/2026 on Penyesuaian Pidana revoked or adjusted parts of it, and the Constitutional Court (MK) attached conditional meanings to several articles.

## Method

1. Read the base law and both amending laws in full from Pasal.id. Saved the body text (no Penjelasan) to `sources/`.
2. Every change point (angka) in the amending laws that touches the body restates the whole new article.
   So the consolidation only ever replaces a whole Pasal or inserts a new one; nothing is edited inside a sentence.
3. Wrote a ledger by hand (`changes.csv`): one row per article touched by each angka (replace, insert, or penjelasan-only).
   The script refuses to run if the ledger and the source text disagree. Every angka must be covered exactly once,
   a replaced Pasal must already exist, and an inserted Pasal must not exist yet.
4. Kept later events as notes, not text edits (`status.csv`): provisions that expired under UU 1/2024 Pasal II,
   provisions revoked by KUHP Pasal 622 (as amended by UU 1/2026), MK conditional rulings, and open questions.
5. Checked every MK ruling against the Court's own AMAR PUTUSAN section, not the database summary.

## Sources used

- UU 11/2008: https://peraturan.go.id/files/UU+11+Tahun+2008.pdf, via https://pasal.id/peraturan/uu/uu-no-11-tahun-2008 (Pasal.id: verified)
- UU 19/2016: https://peraturan.go.id/files/UU+19+Tahun+2016.pdf, via https://pasal.id/peraturan/uu/uu-no-19-tahun-2016 (Pasal.id: _not_ verified)
- UU 1/2024: https://peraturan.go.id/files/uu-no-1-tahun-2024.pdf, via https://pasal.id/peraturan/uu/uu-no-1-tahun-2024 (Pasal.id: _not_ verified)
- UU 1/2023 (KUHP) Pasal 441, 622: https://pasal.id/peraturan/uu/uu-no-1-tahun-2023
- UU 1/2026 (Penyesuaian Pidana) Pasal I–III and Pasal VII angka 55: https://pasal.id/peraturan/uu/uu-no-1-tahun-2026
- MK rulings 105/PUU-XXII/2024, 115/PUU-XXII/2024, 311/PUU-XXIV/2026, 50/PUU-XXIV/2026, 78/PUU-XXI/2023: https://pasal.id/peraturan/putusan-mk/ (PDFs at s.mkri.id)

## Tools and models

- Claude Code (desktop) with Claude Opus 5.5 and the Pasal.id MCP connector (search, read, relationships, MK decisions).
- Python 3, standard library only (`scripts/consolidate.py`).

## Result

- 63 articles in the consolidated text: 54 original, plus 45A and 45B (UU 19/2016), plus 13A, 16A, 16B, 18A, 27A, 27B and 40A (UU 1/2024).
  22 articles were changed or inserted. Pasal 5, 15 and 27 also had Penjelasan-only changes, which are recorded but not consolidated.
- The ledger matched the sources on the first full run: 8 angka in UU 19/2016 and 18 in UU 1/2024, all covered once.
- **Status today is not the same as the amended text.** UU 1/2024 Pasal II(1) said 13 of its new criminal provisions apply only until the KUHP takes effect,
  and the KUHP took effect on 2 January 2026. KUHP Pasal 622 separately revokes Pasal 27(1), 28(2), 30, 31(1)–(2), 36, 45(1), 45A(2), 46, 47 and 51(2).
- **Open legal question found.** UU 1/2026 rewrote KUHP Pasal 622 so that it revokes "Pasal 27 ayat (3)" and "Pasal 45 ayat (3)" of UU ITE
  _as last amended by UU 1/2024_. After UU 1/2024, Pasal 27 has no ayat (3), and Pasal 45 ayat (3) is the **gambling** penalty.
  Pasal 622(10)(b) maps both to KUHP Pasal 441 (insult via IT), which suggests the drafters meant the old 2016 defamation provisions.
  Read literally, the gambling penalty would be revoked; read by intent, it stays. The text marks this as open and does not treat Pasal 45(3) as revoked.
- **Database error found.** Pasal.id lists MK 50/PUU-XXIV/2026 as "inkonstitusional bersyarat" and quotes a long list of conditional meanings for UU ITE Pasal 27A, 28(2), 32(1) and 35.
  That text is the applicants' petitum. The Court's real ruling is "Menyatakan permohonan para Pemohon tidak dapat diterima" (the petition was unclear).
  Relying on the summary would have added four false annotations. 78/PUU-XXI/2023 was granted only on UU 1/1946 and KUHP Pasal 310, not on UU ITE.
- Only one conditional MK ruling still bites on text that is in force: 311/PUU-XXIV/2026 on Pasal 40(2b), which requires notice before access is cut.
  The rulings on 27A, 28(2)–(3), 45(4) and 45A(2)–(3) concern provisions that expired on 2 January 2026. They are kept as history.

## Known limitations and error notes

- The text of UU 19/2016 and UU 1/2024 comes from Pasal.id copies that Pasal.id itself marks as unverified. It has not yet been checked against the PDFs.
- Penjelasan is not consolidated.
- UU 1/2026 converts the fines in Bab XI into fine categories (Lampiran I). The text shows the original rupiah amounts with one general note.
  The category for each article has not been checked against Lampiran I.
- MK rulings come from Pasal.id's records, which are incomplete before 2017. Rulings before UU 19/2016 are not annotated.
- Pasal 52(1) still refers to Pasal 27(1), which has since expired and been revoked. Cross-references like this are not checked here (a job for a teknik-pengacuan check).
- Pasal.id lists UU 19/2016 as enacted on 25 December 2016, one month _after_ its promulgation on 25 November 2016. This is probably a database error; it is not yet checked against the PDF.
- Three base-law articles (Pasal 1, 12, 43) came back truncated from the website. They were filled from the Pasal.id connector text, and the ayat (5) list of Pasal 43 in UU 19/2016 was filled the same way.

## What the owner reviewed

_Pending._ Plan:
- Check this random sample (seed 20261114, 5 of the 22 changed articles, about 23%) against the official PDFs: **Pasal 13, 18A, 36, 40A, 43**.
  Count word-level errors per article and record them here.
- Decide the open question on Pasal 45 ayat (3) (and the ghost "Pasal 27 ayat (3)"), or keep it open.
- Confirm the expiry and revocation lists against UU 1/2024 Pasal II and KUHP Pasal 622.
