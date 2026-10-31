"""Build the Legal Industry Map web page from the CSV dataset.

How it works (plain language):
1. Read every row of data/legal_industry_map.csv.
2. Turn the number columns (funding, valuation) from text into numbers.
3. Put the rows into site/template.html, where the placeholder __DATA__ sits.
4. Save two versions of the page:
   - site/legal-industry-map.html: page content only, for the claude.ai artifact
     (the artifact service adds the <html>/<head> wrapper itself).
   - public/legal-industry-map/index.html: a complete web page for the public
     website (statuta.id), plus public/index.html (the lab home page),
     public/404.html (the "page not found" page) and public/CNAME (tells GitHub Pages which domain to use).
   - public/beyond-statutes/: one page per note, built by build_notes.py. The home page's
     chapter list is filled in from the same notes, where site/home.html says <!--CHAPTERS-->.
   - public/lab/: experiment logs and the Python learning log, built by build_lab.py.
   - public/og.png: the picture WhatsApp, LinkedIn etc. show when someone shares a link.
5. Print a small summary so you can sanity-check the numbers.

Run it from the repo root:  python3 scripts/build_map.py
"""

import csv
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import build_lab
import build_notes

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "legal_industry_map.csv"
TEMPLATE_PATH = ROOT / "site" / "template.html"
HOME_PATH = ROOT / "site" / "home.html"
NOT_FOUND_PATH = ROOT / "site" / "404.html"
OG_IMAGE = ROOT / "site" / "og.png"  # link-preview picture, drawn from site/og-card.html
ARTIFACT_OUTPUT = ROOT / "site" / "legal-industry-map.html"
PUBLIC_DIR = ROOT / "public"
CUSTOM_DOMAIN = "statuta.id"

# Columns that hold numbers (USD millions). An empty cell means "undisclosed".
NUMBER_COLUMNS = ["total_funding_usd_m", "last_round_usd_m", "valuation_usd_m"]

# The template is split here: everything before goes in <head>, the rest in <body>.
BODY_MARKER = '<div class="wrap">'


def read_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for col in NUMBER_COLUMNS:
            text = row[col].strip()
            row[col] = float(text) if text else None
        row["id"] = int(row["id"])
        row["source_urls"] = row["source_urls"].split()
    return rows


def full_document(fragment):
    """Wrap page content in a complete HTML document for normal web hosting."""
    head, body = fragment.split(BODY_MARKER, 1)
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"{head}</head>\n<body>\n{BODY_MARKER}{body}</body>\n</html>\n"
    )


def print_summary(rows):
    print(f"{len(rows)} companies")
    print("By region:", dict(Counter(r["region"] for r in rows)))
    print("AI-native:", dict(Counter(r["ai_native"] for r in rows)))

    funding_by_region = defaultdict(float)
    for r in rows:
        if r["total_funding_usd_m"]:
            funding_by_region[r["region"]] += r["total_funding_usd_m"]
    print("Disclosed total funding (USD M) by region:", dict(funding_by_region))

    missing = sum(1 for r in rows if r["total_funding_usd_m"] is None)
    print(f"Rows with no disclosed total funding: {missing}/{len(rows)}")


def main():
    rows = read_rows()
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    fragment = template.replace("__DATA__", json.dumps(rows, ensure_ascii=False))

    # 1. Artifact version (content only).
    ARTIFACT_OUTPUT.write_text(fragment, encoding="utf-8")

    # 2. Public website version. Start from an empty folder each time.
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    (PUBLIC_DIR / "legal-industry-map").mkdir(parents=True)
    (PUBLIC_DIR / "legal-industry-map" / "index.html").write_text(full_document(fragment), encoding="utf-8")
    chapters = build_notes.build(PUBLIC_DIR)
    build_lab.build(PUBLIC_DIR)
    shutil.copy(OG_IMAGE, PUBLIC_DIR / "og.png")
    shutil.copy(ROOT / "site" / "logo.svg", PUBLIC_DIR / "logo.svg")
    home = HOME_PATH.read_text(encoding="utf-8").replace("<!--CHAPTERS-->", chapters)
    notes, by_title = build_notes.read_notes()
    home = home.replace("<!--SKY-->", build_lab.sky_json(notes)).replace("<!--BOOKS-->", build_lab.books_json(notes, by_title))
    (PUBLIC_DIR / "index.html").write_text(home, encoding="utf-8")
    shutil.copy(NOT_FOUND_PATH, PUBLIC_DIR / "404.html")
    (PUBLIC_DIR / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")

    print_summary(rows)
    print(f"Wrote {ARTIFACT_OUTPUT.relative_to(ROOT)} and {PUBLIC_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
