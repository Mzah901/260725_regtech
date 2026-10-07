# Project Context — Regulatory AI Labs

## Why this lab exists
Primary goal: build a public portfolio that supports an application to NTU Singapore's
Master of Computing in Applied AI (MCAAI).

MCAAI targets professionals from non-computing disciplines who apply AI responsibly in
their own domain. This lab is the proof: a legal professional applying AI to Indonesian
regulatory compliance, with responsible-AI practice built in from day one.

Secondary goals: learn programming fundamentals properly, and produce reusable public
datasets/tools for Indonesian legal-tech.

## What every piece of work should demonstrate
1. **Domain depth** — real Indonesian regulatory problems (obligation extraction,
   amendment tracking, cross-reference mapping, regulation hierarchy).
2. **Applied AI skill** — working code, evaluated results, honest failure analysis.
3. **Responsible AI** — documented sources, human review, limitations, bias/error notes,
   and the guardrails in CLAUDE.md as an explicit governance design.

If an experiment doesn't advance at least one of these, question whether to run it.

## Portfolio artifacts (target)
- This GitHub repo: clean README, documented experiments in `/experiments/`.
- At least one public dataset on Hugging Face built from public regulations,
  with a dataset card covering sources, method, limitations, and license basis.
- One or two write-ups explaining method and results in plain language
  (reusable for the application essay).

## Working conventions
- Owner is learning to code: explain every change in plain language, prefer simple
  readable code over clever code, and point out concepts worth studying.
- Every experiment has a log entry (format in CLAUDE.md).
- Evaluate results: report accuracy/error counts against a manually checked sample,
  never only "it looks right".
- Python is the default language unless there's a clear reason otherwise.

## Non-goals
- Not a commercial product.
- Not a replacement for legal advice; outputs are research artifacts.

## Decisions log
- Public sources only; employer-independent (see CLAUDE.md guardrails).
- GitHub is home base; Hugging Face for publishing datasets.
- Claude Code (web) for building; planning happens in a separate claude.ai Project.
