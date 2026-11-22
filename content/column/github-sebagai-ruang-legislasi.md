---
title: What if our laws lived on GitHub?
date: 2026-11-22
tag: POLICY
---
_Draft. Not yet reviewed by the author; figures still to be checked against the original sources._

It started with a silly question: could we make a Ketetapan MPR on GitHub? The honest answer is no, and for two reasons. A merged pull request has no legal force. Validity comes from who adopts the text and how, not from where it was drafted. And since the constitutional amendments the MPR no longer makes rule-making TAPs at all. TAP MPR I/MPR/2003 closed that book.

But the question behind it is better than the question itself. Our problem was never a shortage of rules. It's that nobody can see how they're made, who changed what, and which version applies today.

Look at the data. PSHK found that in 2025, 87.5% of the Prolegnas Prioritas bills had no draft or Naskah Akademik on the DPR website. Of the 9 bills passed that year (out of a target of 52), only one had both online. Meanwhile the Ministry of Law handled 11,392 harmonisation requests in one year with too few legislative drafters. And there is still no official consolidated text. If you want to know what UU ITE says today, you have to stitch the amendments together yourself. I did exactly that in this lab.

That is where GitHub, or more precisely Git, becomes relevant. Not as a place where laws are "made", but as infrastructure:

- **Commit = one change, with a name and a reason.** No more "RUU_final_v7_REVISI_fix2.docx".
- **Branch per fraction (fraksi).** Each fraction proposes its own version, so its position can be traced.
- **Pull request + mandatory review.** Baleg acts as maintainer for DPR bills (Pasal 46 ayat (2) UU 12/2011) and the Ministry of Law for government bills (Pasal 47 ayat (3)).
- **Automated checks.** Lampiran II structure, broken cross-references and overlap with existing rules get checked by machine, so drafters can focus on substance.
- **Issues as participation.** Every input gets a number, is linked to the decision on it, and is closed with a reason. That is the right to be heard, to be considered and to be given an explanation from Putusan MK 91/PUU-XVIII/2020, made concrete.
- **A live database.** The `main` branch is the law in force, updated every time a law is promulgated. Not a stale PDF.

There is precedent abroad. Washington DC has made its GitHub copy the authoritative digital version of its code. In 2018 a citizen fixed a typo through a pull request and it was merged. The EU built its own open-source drafting editor, LEOS, on its own servers. The US House requires a comparison print showing how a bill would change existing law. Spain got a civic Git repository in 2026, built from the BOE's consolidated-text API.

The lesson I take from all of them: Git solves the text problem (versions, consolidation, transparency). It can't solve the political problem. Prolegnas targets that are never met, and lobbying that happens outside the room, won't disappear because of a repository. A branch per fraction makes positions accountable, and that is exactly why some people will refuse to use it. If the real decisions still happen off the record, a public repository is just transparency theatre.

Two critiques I take seriously:

1. **Data sovereignty.** PP 71/2019 Pasal 20 requires public-scope systems to store their data in Indonesia. So if this is ever official, it has to be self-hosted Git on national infrastructure, like the EU's own code.europa.eu, not github.com.
2. **Authenticity.** The authoritative text today is what's in the Lembaran Negara. A repository becomes authoritative only if a legal instrument says so and every release is signed with a certificate the state recognises.

So my answer to the opening question: not GitHub as the lawmaker, but Git as the public notebook of the lawmakers. The full analysis, including a diagram of how it would work and which problems it can and can't solve, is in the [lab research note](https://github.com/Mzah901/260725_regtech/blob/HEAD/docs/github-legislation.md).
