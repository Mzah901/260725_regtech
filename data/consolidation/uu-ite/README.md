# UU ITE consolidation — files and columns

Unofficial consolidated text of UU 11/2008 tentang Informasi dan Transaksi Elektronik, as of 14 November 2026.
Rebuild with `python3 scripts/consolidate.py`. Method and limits: `experiments/2026-11-14-uu-ite-consolidation.md`.

| File | What it is |
|---|---|
| `sources/uu-11-2008.txt` | Base law, body only, with BAB headings |
| `sources/uu-19-2016.txt`, `sources/uu-1-2024.txt` | Pasal I (change points, labelled "Angka N") and Pasal II of each amending law |
| | All three source files are checked word by word against the official PDFs on peraturan.go.id (`scripts/compare_words.py`); each file's header gives the result |
| `changes.csv` | Ledger: one row per article touched by each change point |
| `status.csv` | Later events kept as notes: expiry, revocation, MK rulings, open questions |
| `uu-ite-konsolidasi.md` | Generated output. Do not edit by hand |
| `uu-ite-konsolidasi.pdf` | The same text as a PDF. Rebuild with `python3 scripts/build_pdf.py` (needs Microsoft Edge) after the Markdown changes |

`changes.csv`: `law` (amending law), `angka` (change point number in its Pasal I), `action` (`replace`, `insert`, or `penjelasan` = only the Penjelasan changed),
`target` (Pasal number), `anchor` (for `insert`: the Pasal it goes after), `note` (plain description).

`status.csv`: `pasal`, `ayat` (blank = the article as a whole), `kind` (`berakhir`, `dicabut`, `putusan MK`, `pertanyaan terbuka`), `source` (legal basis), `note`.

Regulation text is public domain under Pasal 42 UU 28/2014. This is research, not legal advice and not an official text.

Independent personal research. Not affiliated with or endorsed by any employer.
