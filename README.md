# Regulatory AI Labs

AI applied to Indonesian regulatory compliance, using public sources only
(peraturan.go.id, JDIH portals, Pasal.id, official gazettes, published court decisions).

- `CLAUDE.md` — working rules and guardrails for AI-assisted development
- `docs/PROJECT_CONTEXT.md` — goals, conventions, decisions
- `experiments/` — one log file per experiment (`YYYY-MM-DD-short-name.md`)
- `data/` — datasets built from public sources, each with a data dictionary
- `scripts/` — small Python scripts (run from the repo root)
- `site/` — generated web pages

## Experiments

| Date | Experiment | Output |
|---|---|---|
| 2026-10-11 | [Legal Industry Map (pilot)](experiments/2026-10-11-legal-industry-map.md) | `data/legal_industry_map.csv`, `site/legal-industry-map.html` (rebuild with `python3 scripts/build_map.py`) |

Outputs are research artifacts, not legal advice.

Source regulation text is public domain under Pasal 42 UU No. 28 Tahun 2014 tentang Hak Cipta.

*Independent personal research. Not affiliated with or endorsed by any employer.*
No any workplace materials are used in this repo, including documents, methodology, workflows, people, source, et cetera.
