# Regulatory AI Labs

AI applied to Indonesian regulatory compliance, using public sources only
(peraturan.go.id, JDIH portals, Pasal.id, official gazettes, published court decisions).

- `CLAUDE.md` — working rules and guardrails for AI-assisted development
- `docs/PROJECT_CONTEXT.md` — goals, conventions, decisions
- `experiments/` — one log file per experiment (`YYYY-MM-DD-short-name.md`)
- `data/` — datasets built from public sources, each with a data dictionary
- `scripts/` — small Python scripts (run from the repo root)
- `site/` — page templates (the map template and the lab home page)
- `.github/workflows/pages.yml` — will publish the website at https://lab.statuta.id (not switched on yet)

## Experiments

| Date | Experiment | View | Files |
|---|---|---|---|
| 2026-10-11 | [Legal Industry Map (pilot)](experiments/2026-10-11-legal-industry-map.md) | [Interactive map](https://claude.ai/artifact/9iALtpMBCiDZXF4x5zytDw) | `data/legal_industry_map.csv`, `site/legal-industry-map.html` |

The interactive views are hosted as claude.ai artifacts for now. They will move to https://lab.statuta.id later.

## Website (planned)

`python3 scripts/build_map.py` builds the site into `public/` (not committed).
GitHub Actions runs the same script on every push to check that the build works.
Publishing to GitHub Pages stays off until the repo variable `PAGES_ENABLED` is set to `true`
(Settings → Secrets and variables → Actions → Variables). After that, every merge into the
default branch goes live.

Outputs are research artifacts, not legal advice.

Source regulation text is public domain under Pasal 42 UU No. 28 Tahun 2014 tentang Hak Cipta.

*Independent personal research. Not affiliated with or endorsed by any employer.*
No any workplace materials are used in this repo, including documents, methodology, workflows, people, source, et cetera.
