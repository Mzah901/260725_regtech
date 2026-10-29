# Regulatory AI Labs

AI applied to Indonesian regulatory compliance, using public sources only
(peraturan.go.id, JDIH portals, Pasal.id, official gazettes, published court decisions).

- `CLAUDE.md` — working rules and guardrails for AI-assisted development
- `docs/PROJECT_CONTEXT.md` — goals, conventions, decisions
- `experiments/` — one log file per experiment (`YYYY-MM-DD-short-name.md`)
- `data/` — datasets built from public sources, each with a data dictionary
- `scripts/` — small Python scripts (run from the repo root)
- `site/` — page templates (the map template, the lab home page and the 404 page)
- `content/beyond-statutes/` — the Beyond Statutes notes, one Markdown file each. Start a file with a
  `---` header (`title`, `rank`, `tag`), write paragraphs, and link to another note with `[[Its title]]`.
  The build makes a page per note with its links and backlinks, and fills the home page's chapter list.
- `.github/workflows/pages.yml` — publishes the website at https://statuta.id

## Experiments

| Date | Experiment | View | Files |
|---|---|---|---|
| 2026-10-11 | [Legal Industry Map (pilot)](experiments/2026-10-11-legal-industry-map.md) | [Interactive map](https://claude.ai/artifact/9iALtpMBCiDZXF4x5zytDw) | `data/legal_industry_map.csv`, `site/legal-industry-map.html` |

The interactive views are also live at https://statuta.id.

## Website: https://statuta.id

`python3 scripts/build_map.py` builds the site into `public/` (not committed).
GitHub Actions runs the same script on every push to check that the build works.
Publishing to GitHub Pages stays off until the repo variable `PAGES_ENABLED` is set to `true`.
After that, every merge into the default branch goes live.

The domain is registered at Hostinger; Hostinger only handles DNS, GitHub Pages hosts the site.
Setup checklist:

1. Hostinger hPanel → Domains → statuta.id → DNS: remove the default parking `A` record for `@`
   and any `www` record, then add four `A` records for `@`:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`,
   and one `CNAME` record: `www` → `mzah901.github.io`.
2. Repo Settings → Pages → Source: **GitHub Actions**.
3. Repo Settings → Secrets and variables → Actions → Variables: `PAGES_ENABLED` = `true`.
4. After DNS has updated (up to 24 hours): Settings → Pages → tick **Enforce HTTPS**.
5. GitHub account Settings → Pages → **Verify** statuta.id, so no one else can claim the domain on GitHub.

Outputs are research artifacts, not legal advice.

Source regulation text is public domain under Pasal 42 UU No. 28 Tahun 2014 tentang Hak Cipta.

*Independent personal research. Not affiliated with or endorsed by any employer.*
No workplace materials are used in this repo: no documents, methodology, workflows, people, sources or other internal information.
