"""Build the Legal Industry Map web page from the CSV dataset.

How it works (plain language):
1. Read every row of data/legal_industry_map.csv.
2. Turn the number columns (funding, valuation) from text into numbers.
3. Put the rows into site/template.html, where the placeholder __DATA__ sits,
   and save the result as site/legal-industry-map.html.
4. Print a small summary so you can sanity-check the numbers.

Run it from the repo root:  python3 scripts/build_map.py
"""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "legal_industry_map.csv"
TEMPLATE_PATH = ROOT / "site" / "template.html"
OUTPUT_PATH = ROOT / "site" / "legal-industry-map.html"

# Columns that hold numbers (USD millions). An empty cell means "undisclosed".
NUMBER_COLUMNS = ["total_funding_usd_m", "last_round_usd_m", "valuation_usd_m"]


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
    data_json = json.dumps(rows, ensure_ascii=False)
    OUTPUT_PATH.write_text(template.replace("__DATA__", data_json), encoding="utf-8")
    print_summary(rows)
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
