# Regulatory AI Labs — Claude Code Instructions

## What this repo is
Personal research sandbox: AI applied to Indonesian regulation, using public sources only.
Independent work, not affiliated with any employer.

Full project context (goals, conventions, decisions): @docs/PROJECT_CONTEXT.md

## Owner profile
- Legal background (UGM law), no formal tech background, learning to code.
- When you write or change code: explain each change in one or two plain sentences,
  and flag concepts worth learning. Never make large unexplained changes.

## Hard guardrails (stop and ask if any request would break these)
1. **Public sources only**: peraturan.go.id, JDIH portals, Pasal.id, official gazettes,
   published court decisions. No internal company data, client names, internal
   annotations, or anything that could only be seen through employment.
   If a source's origin is unclear, treat it as confidential and ask.
2. **No employer-specific artifacts**: methodology is the owner's, but no internal
   channel IDs, sheet names, column schemas, internal templates, sector assignments,
   or internal database formats may appear in this repo.
3. **No work systems**: never use or reference work Slack, work accounts, or files
   shared from work. Only this repo and public web sources.
4. **Commercial use**: do not build anything packaged for sale to compliance clients
   without the owner confirming management disclosure first.
5. **Human review**: every output is reviewed by the owner before it is treated as final.
6. **Collaborators**: anyone contributing works with public data only, under written
   IP-assignment and confidentiality terms.

If a request crosses guardrails 1–4: stop, name the guardrail at risk, and ask.

## Experiment log (required)
Every experiment gets a file in `/experiments/` named `YYYY-MM-DD-short-name.md` with:
- Date
- Question / hypothesis
- Sources used (with URLs)
- Tools and models used
- Result
- What the owner reviewed and approved

## Publishing
Any README, dataset card, or published output must include:
"Independent personal research. Not affiliated with or endorsed by any employer."
Source regulation text is public domain under Pasal 42 UU 28/2014 (Hak Cipta).
