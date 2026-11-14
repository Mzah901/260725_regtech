"""Make the PDF of the consolidated UU ITE (data/consolidation/uu-ite/uu-ite-konsolidasi.pdf).

How it works (plain language):
1. Read uu-ite-konsolidasi.md (made by scripts/consolidate.py). Every line of it becomes one line
   of HTML: "## " is a BAB heading, "### " a Pasal heading, "> " a status note in a grey box.
2. Wrap that in a print stylesheet (A4, page numbers, the disclaimer at the top).
3. Ask Microsoft Edge, running without a window ("headless"), to print the page to PDF.

Run it again whenever consolidate.py changes the text, and commit the new PDF.
shortcut: needs Edge on this Mac, so the website build only copies the committed PDF; move to CI if it goes stale often.
"""
import html
import subprocess
import tempfile
from pathlib import Path

from build_lab import inline

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "consolidation" / "uu-ite" / "uu-ite-konsolidasi.md"
OUT = SRC.with_suffix(".pdf")
EDGE = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
DISCLAIMER = ("Experimental. Unverified unless marked as reviewed. Not legal advice, and not legal research to rely on. "
              "Independent personal research. Not affiliated with or endorsed by any employer.")

CSS = """
@page { size: A4; margin: 18mm 18mm 20mm;
  @bottom-center { content: "UU ITE konsolidasi tidak resmi · statuta.id · " counter(page) " / " counter(pages);
                   font: 8pt Georgia, serif; color: #666; } }
body { font: 10.5pt/1.45 Georgia, "Times New Roman", serif; color: #111; }
h1 { font-size: 16pt; margin: 0 0 6pt; }
h2 { font-size: 12pt; margin: 18pt 0 4pt; text-align: center; break-after: avoid; }
h3 { font-size: 11pt; margin: 12pt 0 3pt; text-align: center; break-after: avoid; }
p { margin: 0 0 3pt; text-align: justify; }
.note { background: #f2f2f2; border-left: 3px solid #999; padding: 4pt 8pt; margin: 4pt 0 6pt; font-size: 9pt; break-inside: avoid; }
.note p { margin: 0 0 2pt; text-align: left; }
.disclaimer { border: 1px solid #b00; color: #800; padding: 5pt 8pt; font-size: 9pt; margin: 0 0 8pt; }
"""


def to_html(md):
    out, note, joined = [], [], False
    def flush():
        if note:
            out.append('<div class="note">' + "".join(f"<p>{inline(n)}</p>" for n in note) + "</div>")
            note.clear()
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith(">"):
            text = line[1:].strip()
            if text and joined and note: note[-1] += " " + text   # a wrapped line continues the note above
            elif text: note.append(text)
            joined = not raw.endswith("  ")   # Markdown: two trailing spaces = a real line break
            continue
        flush()
        if line.startswith("### "):  out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "): out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):  out.append(f"<h1>{html.escape(line[2:])}</h1><div class=\"disclaimer\">{DISCLAIMER}</div>")
        elif line:                   out.append(f"<p>{inline(line)}</p>")
    flush()
    return f'<!doctype html><html lang="id"><meta charset="utf-8"><title>UU ITE konsolidasi</title><style>{CSS}</style>{"".join(out)}</html>'


if __name__ == "__main__":
    # Self-check: headings, notes and the disclaimer come out right before printing anything.
    t = to_html("# T\n\n## BAB I\n### Pasal 1\n(1) a & b.  \n\n> **Berakhir**: x.  \n> y\n> z\n")
    assert "<h2>BAB I</h2><h3>Pasal 1</h3><p>(1) a &amp; b.</p>" in t, t
    assert '<div class="note"><p><b>Berakhir</b>: x.</p><p>y z</p></div>' in t and DISCLAIMER in t, t
    page = to_html(SRC.read_text(encoding="utf-8"))
    assert page.count("<h3>Pasal") == 63, "all 63 Pasal are in the PDF"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT}", Path(f.name).as_uri()], check=True, capture_output=True)
    Path(f.name).unlink()
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
