# GitHub as infrastructure for Indonesian law-making (research note)

**Date:** 2026-11-22
**Status:** _Draft, not yet reviewed by the owner._ Built with Claude Code.
**Experiment log:** [`experiments/2026-11-22-github-legal-production.md`](../experiments/2026-11-22-github-legal-production.md)
**Column version:** [`content/column/github-sebagai-ruang-legislasi.md`](../content/column/github-sebagai-ruang-legislasi.md)

> Independent personal research. Not affiliated with or endorsed by any employer.
> Experimental. Unverified unless marked as reviewed. Not legal advice, and not legal research to rely on.

## Question

Which of Indonesia's documented law-making problems could a Git/GitHub workflow actually solve, which can it only support, and which can it not touch? What do foreign examples teach about how it works in practice?

## Starting point: what a repository can and cannot do

A merged pull request has no legal force. A law is valid because the body authorised by the Constitution adopted it under the required procedure. For a UU, that means joint approval in the DPR plenary (Pasal 20 ayat (2) UUD 1945), then signature by the President.
So GitHub can only be **infrastructure**: the place where drafts live, changes are recorded, reviews happen and the published text is kept current. It cannot be the **source of validity**.

The same limit applies to the earlier TAP MPR idea. Since the constitutional amendments the MPR no longer issues rule-making (regeling) TAPs. Under the Penjelasan of Pasal 7 ayat (1) huruf b UU 12/2011, only the TAPs that TAP MPR I/MPR/2003 kept in force sit at that level of the hierarchy. TAP MPR I/2003 itself is a useful precedent for something else, though: it was a one-time "legacy refactor" that sorted every TAP from 1960–2002 into revoked, still in force, and spent.

## 1. The problems (latest data found)

| # | Problem | Evidence | Source quality |
|---|---|---|---|
| P1 | **Hyper-regulation (obesitas regulasi)** | PSHK's widely cited count is 42,996 regulations: 8,414 central, 14,453 ministerial, 4,164 from non-ministerial agencies, 15,965 regional. In October 2026 the Minister of Law said the ministry had cut 195 of its own regulations (Permenkum) to 34. | The PSHK count dates from around 2019–2020. **No newer PSHK count was found.** The 195→34 figure comes from press reports. |
| P2 | **Disharmony and overlap** | PSHK: about two-thirds of executive regulations come from ministries, and they overlap with each other. At the Forum Nasional Pembangunan Hukum (15 Oct 2026) the Minister named sectoral ego (ego sektoral) as the cause and set out two strategies, RIA and substantive harmonisation. | The PSHK finding is from 2019 (with Bappenas). The 2026 statement is from press reports. |
| P3 | **Opaque drafting** | PSHK monitoring for 2025: 87.5% of the Prolegnas Prioritas bills had no draft and no Naskah Akademik on the DPR website, and 71.4% had no session documents. Of the 9 bills passed, only 1 had both its draft and its Naskah Akademik online. In September 2026 the draft of the asset-forfeiture bill (RUU Perampasan Aset) was still unpublished while being "tidied up". | PSHK Catatan Akhir Tahun 2025 (read through press summaries; pshk.or.id could not be reached from the build environment). |
| P4 | **Planning that doesn't hold** | 9 of the 52 Prolegnas Prioritas 2025 bills were passed. The list grew from 41 to 52 during the year, and bills outside the list (BUMN, Minerba) were passed anyway. Achievement over 2020–2025 was about 8–22% of target. | PSHK 2025, Katadata/Databoks. |
| P5 | **Meaningful participation in form only** | Putusan MK 91/PUU-XVIII/2020 led to Pasal 96 UU 13/2022 on meaningful participation. A 2026 MK case (78/PUU-XXIV/2026) still uses both as its yardstick. The law does not clearly require drafts to be published. | The court decision and statute are primary sources. The interpretive point is secondary. |
| P6 | **Harmonisation bottleneck** | In 2025 the Ministry of Law received 11,392 harmonisation requests and completed 11,191. The e-Harmonisasi application launched in February 2025 and became the main channel under Permenkum 7/2026. The Riau regional office reports too few legislative drafters (perancang) for the volume of requests. | Ministry performance reports, via press. |
| P7 | **No official consolidated text** | Official portals publish the original texts. Consolidations (the law "as amended") are made privately or unofficially. Pasal.id labels its own as "Konsolidasi tidak resmi". This lab had to build one by hand for UU ITE. | Primary: the portals themselves, plus this lab's [UU ITE experiment](../experiments/2026-11-14-uu-ite-consolidation.md). |
| P9 | **The Naskah Akademik is a justification, not an analysis** | The owner's own study of 39 Naskah Akademik (2018–2022, from the DPR Expertise Body and BPHN): all used normative legal research, only 5% used RIA and 13% a cost-benefit analysis, 77% used qualitative analysis only, and **none** identified policy alternatives (not even "do nothing") or systematically mapped the affected groups. UU 13/2022 mentions RIA and ROCCIPI as options but doesn't require them. | Peer-reviewed: Al Faruq, Ruhpinesthi & Ismaya, *Jurnal Penelitian Hukum De Jure* 24(2), 2024, pp. 175–198. The data predates 2023, so it needs re-checking against newer Naskah Akademik. |
| P8 | **Weak regulatory-quality perception** | World Bank WGI Regulatory Quality for Indonesia: estimate 0.12 in 2024, down from 0.34 in 2023 (scale −2.5 to +2.5). | **Secondary aggregator.** The World Bank revised the whole series in December 2025, so check against govindicators.org before citing. |

## 2. Which problems Git can solve

Rating: **Solves** = Git provides the mechanism directly. **Supports** = Git helps, but the real fix is institutional. **Doesn't touch** = the cause is political.

| # | Problem | Rating | Git mechanism | Why it matters |
|---|---|---|---|---|
| P7 | No official consolidated text | **Solves** | Each amending law is one commit to the current text. `git log` gives the amendment history for each Pasal. A tagged release gives the text as of any date. | It's the core use in every foreign example (DC, Spain, Germany). Answers "which version applies today?", the [database problem](../content/beyond-statutes/law-is-a-database-problem.md). |
| P3 | Opaque drafting | **Solves (if mandated)** | A public repository from the first draft. Every version stays in history, with an author and a timestamp. | It turns "the draft is still being tidied up" into a visible commit history. The technology is trivial. The obstacle is political will. |
| P6 | Harmonisation bottleneck | **Supports** | Pull-request review; `CODEOWNERS` makes review by each affected ministry or committee mandatory; automated checks (CI) catch mechanical errors before a human looks. | It frees scarce drafters for substance. Routine checks (Lampiran II structure, broken references, hierarchy) run automatically. |
| P2 | Disharmony and overlap | **Supports** | One corpus in a single repository, searchable across sectors. CI can flag a new draft that touches the same subject or Pasal as an existing rule. | It makes overlap visible **before** enactment. It can't resolve ego sektoral, but it removes the excuse of "we didn't know". |
| P5 | Participation in form only | **Supports** | Issues as a public, numbered intake for input. Each issue is closed with a written reason or linked to the commit that took it on. | It maps onto the three rights in Putusan MK 91/PUU-XVIII/2020: to be heard (the issue is filed), to be considered (it's linked to a review), to be given an explanation (the closing comment). It also acts as a **live database**: the public sees the current text, not a stale PDF. |
| P1 | Hyper-regulation | **Supports (indirectly)** | A full inventory with status labels; "archiving" spent rules; a dashboard of rules with no recent activity. | Simplification starts with a count. TAP MPR I/2003 and the Permenkum 195→34 cut were done by hand. A repository makes that kind of stock-take continuous. |
| P9 | Naskah Akademik as justification | **Supports** | The Naskah Akademik lives in the same repository as the bill, so each Pasal can link to the analysis behind it. Policy alternatives become competing branches. A CI check flags a Naskah Akademik with no alternatives section or no affected-groups map. | It makes the gap the owner's study found visible on every bill. It can't make drafters do real research, but an empty section becomes a failed check in public. See [2b](#2b-the-owners-ria-article-what-git-adds). |
| P4 | Planning that doesn't hold | **Doesn't touch** | A Projects board could track the Prolegnas publicly. | Missing targets is a political choice. Visibility helps outside monitors (like PSHK) but doesn't change incentives. |
| P8 | Regulatory-quality perception | **Doesn't touch** (directly) | None. | It's an outcome indicator and would move only if P2, P3, P6 and P7 improve. |

### The owner's design point: fraction branches, merged by the legislation body

The owner's proposal is that each fraction (fraksi) submits its changes as its own branch and pull request, which the head of the legislation body (Baleg) merges. The current law supports the "maintainer" idea:

- Pasal 46 ayat (2) UU 12/2011: harmonisation of bills **from the DPR** is coordinated by the DPR body that handles legislation (Baleg).
- Pasal 47 ayat (3) UU 12/2011 as amended by UU 15/2019: harmonisation of bills **from the President** is coordinated by the minister or head of the agency responsible for law-making (pembentukan peraturan perundang-undangan). In practice today that is the Ministry of Law.

So a repository would have two maintainer roles, Baleg and the Ministry of Law, depending on where the bill comes from. Three design corrections:

1. **Merge ≠ enactment.** The `rancangan` (draft) branch can be merged by Baleg. The `main` branch, the law in force, should only move when the plenary approves and the text is promulgated, and a signed release tag should record that.
2. **A single merger is a single gatekeeper.** Branch protection should require approval from more than one fraction, or at least make every rejected pull request public with its reason. Otherwise the repository simply moves the backroom into a new room.
3. **The real negotiation (lobbying, the DIM list in the working committee, Panja) happens off the record.** A branch per fraction makes each fraction's position attributable. That is precisely why fractions may refuse to use it. The value is accountability, and that is also where the resistance will come from.

### 2b. The owner's RIA+ article: what Git adds

The owner's 2024 article ([De Jure 24(2)](https://doi.org/10.30641/dejure.2024.V24.175-198)) argues that the Naskah Akademik is treated as a formal requirement that justifies a bill already decided on, and proposes **RIA+**: Regulatory Impact Assessment with an extra first step, an inventory of affected communities. Its five recommendations map onto a repository like this:

| RIA+ recommendation (2024 article) | Git mechanism | What it changes |
|---|---|---|
| 1. Move RIA to the start of law-making, as the method for the whole Naskah Akademik, not one sub-chapter | The Naskah Akademik is the first commit of the repository, **before** any bill text. The bill branch can only open once the analysis is in. | Order becomes checkable: the history shows whether the analysis came before or after the text. |
| 2. Inventory of affected communities (directly affected, indirectly affected, unrelated, experts, practitioners) | A required `affected-groups` file, and an issue label for each of the five groups. Input from each group is counted per label. | "Who was consulted" stops being a sentence in Bab I and becomes a public count, which is also what Putusan MK 91/PUU-XVIII/2020 asks for. The article proposes keeping the map as a data bank for later Naskah Akademik; a repository is exactly that. |
| 3. Detailed instructions for the research behind the Naskah Akademik | A Naskah Akademik template in the repository, with required sections and a data folder for primary data. | Missing method or data shows up as an empty folder, not a vague paragraph. |
| 4. Restructure Bab II to hold policy alternatives (do nothing, better implementation, partial change, new norm) | One branch per alternative. The chosen branch is merged; the rejected ones stay in history with the reason. | The article found **no** Naskah Akademik that weighed alternatives. Branches make "we considered option B and rejected it because…" a visible record rather than a claim. |
| 5. Spell out the cost-benefit analysis | A structured CBA file (costs, benefits, who bears them) reviewed in the same pull request as the bill. | Reviewers can see the cost-benefit claim next to the Pasal it justifies. |

The same limit applies as for the rest of this note: Git makes a missing analysis visible but cannot force a good one. The article's own finding is that the law only *offers* RIA; a repository would only bite if the template and checks were made mandatory.

### 2c. Folder structure for one bill

One repository per bill (RUU). The six folders follow the life of a bill, from the first draft to the politics around it. The `main` branch only ever holds the promulgated law; everything below lives on the `rancangan` branch and the fraction branches until then.

```text
ruu-<short-name>/
├── README.md                         status, current stage, maintainers, key dates
├── 01-ruu/                           a. RUU drafts
│   ├── ruu.md                        the bill text: ONE file, versions live in Git history
│   ├── penjelasan.md
│   └── dim/                          Daftar Inventarisasi Masalah, one file per fraction
├── 02-naskah-akademik/               b. Naskah Akademik, as submitted by the initiator
│   ├── naskah-akademik.md
│   ├── affected-groups.md            RIA+ step 1: the five groups and who was reached
│   ├── alternatives/                 RIA+: do-nothing.md, implementation.md, partial-change.md, new-norm.md
│   ├── cost-benefit.md
│   └── data/                         primary data, survey results, FGD notes
├── 03-penyelarasan-pengharmonisasian/  c. review of the NA and harmonisation of the RUU
│   ├── penyelarasan-na/              findings + surat keterangan penyelarasan
│   └── pengharmonisasian-ruu/        meeting records, issues raised, how each was resolved
├── 04-partisipasi/                   d. documentation of meaningful participation
│   ├── inputs/                       every input, with a number (mirrors the Issues)
│   ├── hearings/                     RDPU, public consultations, regional visits
│   └── responses.md                  input → decision → reason
├── 05-proses/                        e. the legislation process
│   ├── timeline.md                   Prolegnas → drafting → deliberation → approval → promulgation
│   ├── risalah/                      session minutes, per stage
│   └── tingkat-i-ii/                 committee (tingkat I) and plenary (tingkat II) decisions, fraction views
└── 06-catatan-politik/               f. political setbacks
    └── log.md                        date · event · stage · actor · public source
```

What goes where, and why:

| Folder | What it records | Legal hook | Why it matters |
|---|---|---|---|
| **01-ruu** | The bill and the DIM. Each fraction edits on its own branch; the merge into `rancangan` is the agreed text. | Pasal 46 ayat (2) and Pasal 47 ayat (3) UU 12/2011 (the latter as amended by UU 15/2019): who coordinates harmonisation, i.e. the maintainer. | One file with history beats `RUU_final_v7_fix2.docx`. `git blame` shows who proposed each line. |
| **02-naskah-akademik** | The NA **as the initiator wrote it**, plus the RIA+ files from section 2b. | UU 13/2022 offers RIA and ROCCIPI as methods but doesn't require them. | The owner's study found no NA that weighed alternatives; here an empty `alternatives/` folder is visible to everyone. |
| **03-penyelarasan-pengharmonisasian** | Two different reviews: **penyelarasan** of the NA (its structure and content) and **pengharmonisasian** of the RUU. | Penyelarasan of a government NA: Pasal 9 Perpres 87/2014 (the Minister checks "sistematika dan materi muatan", in a meeting that includes stakeholders). The NA, the surat keterangan penyelarasan and the surat keterangan that harmonisation is complete are listed together as "dokumen kesiapan teknis", e.g. Pasal 23 ayat (2) and Pasal 25 ayat (4) Perpres 87/2014. Harmonisation of the RUU: Pasal 46–47 UU 12/2011. (Perpres 87/2014 was amended by Perpres 76/2021; only the original text was checked.) | Today these reviews are invisible. Here every finding is a numbered item with its outcome. |
| **04-partisipasi** | Every input, every hearing, and the answer given to each. | Pasal 96 UU 12/2011 as amended by UU 13/2022; Putusan MK 91/PUU-XVIII/2020 (right to be heard, considered, and given an explanation). | `responses.md` is the proof of the third right. Without it, participation is a photo of a meeting. |
| **05-proses** | Where the bill is, and the official record of each stage. | The stages of law-making in UU 12/2011: planning, drafting, deliberation, approval, promulgation. | Answers "what stage is this bill at?" without a press search. |
| **06-catatan-politik** | Delays, carry-overs between Prolegnas years, withdrawn positions, rejected pull requests, judicial review after enactment. | None: this is the political record, not a legal step. | Section 2 rates planning (P4) as something Git **doesn't touch**. Git can't fix the politics, but it can keep a dated, sourced record of it. |

Three design points:

1. **"Before" and "after" are tags, not folders.** Point b (NA before penyelarasan) and point c (NA after review) are the same file at two moments. Git keeps both: tag the commit as `na-diajukan` when submitted and `na-diselaraskan` when the surat keterangan is issued, and `git diff na-diajukan na-diselaraskan` shows exactly what the review changed. Folder 03 holds the *record* of the review (who asked for what, and why), not a second copy of the NA.
2. **Penyelarasan and pengharmonisasian are different steps.** In current law, penyelarasan applies to the **Naskah Akademik** and pengharmonisasian to the **RUU**. Folder 03 keeps them as two subfolders so the two don't get mixed up.
3. **The political log needs a source rule.** Every line in `06-catatan-politik/log.md` must link to a public source (minutes, an official statement, a news report). No anonymous claims. That keeps it a record, not an accusation, and keeps the repository defensible.

## 3. How other countries do it

| Example | Status | Mechanism | Lesson for Indonesia |
|---|---|---|---|
| **Washington DC** (DC Council, with Open Law Library) | **Official.** The GitHub copy is the authoritative digital code. | Enacted laws are codified as XML in `DCCouncil` repositories and published within about a week of enactment. In 2018 a citizen's pull request fixing a codification typo was merged. | The PR fixed **codification**, not substance. Substance still changes only through Council legislation. That is the right separation for Indonesia: Git for the text, the legislature for validity. |
| **EU** (LEOS / "EdiT", European Commission) | **Official**, used internally | Open-source drafting editor; texts in Akoma Ntoso XML; code hosted on the EU's **own** `code.europa.eu`, not github.com. | The sovereignty answer: governments use Git principles on infrastructure they control. Indonesia could do the same (self-hosted Git on national data centres). |
| **US House** (Comparative Print Suite) | **Official**, required by House Rule XXI clause 12 | Generates prints showing how a bill would change current law, and how two versions differ. | Diffs as a **procedural duty**, not a nicety. An Indonesian equivalent would be a mandatory comparison matrix attached to every bill. |
| **Spain** (`legalize-es`, 2026) | Civic, unofficial | Pulls the BOE's official consolidated-legislation API into Markdown; each reform is a commit. | It only worked because the state already publishes consolidated text through an open API. Indonesia doesn't yet (P7), so that's the first public good to ask for. |
| **Germany** (`bundestag/gesetze`) | Civic, unofficial; reported unmaintained | Federal laws converted to Markdown from the official XML. | Without an institutional owner, mirrors die. Ownership matters more than tooling. |
| **France** (La Fabrique de la Loi) | Academic or civic | Visualises amendments at every legislative stage; selected bills in Git (GitLab). | Legislative history becomes readable for non-lawyers. That is a participation tool in itself. |

## 4. Diagram (bagan)

```mermaid
flowchart TD
    subgraph PUBLIC["Public, open to anyone"]
        I["Issues: public input<br/>(numbered, logged)"]
        LIVE["Live database / API<br/>current consolidated text"]
    end

    subgraph DRAFT["Drafting, inside the repository"]
        NA["Naskah Akademik (RIA+)<br/>affected-groups map + alternatives<br/>first commit, before bill text"]
        B1["Branch: Fraksi A"]
        B2["Branch: Fraksi B"]
        B3["Branch: Kementerian X<br/>(government bill)"]
        PR["Pull request to the<br/>'rancangan' branch"]
        CI["Automated checks (CI)<br/>- Lampiran II structure<br/>- broken cross-references<br/>- hierarchy conflict<br/>- overlap with existing rules"]
        REV["Mandatory review (CODEOWNERS)<br/>Baleg (DPR bill, Pasal 46(2))<br/>Kemenkum (Presiden bill, Pasal 47(3), as amended 2019)<br/>+ affected ministries"]
        R["'rancangan' branch<br/>agreed draft"]
    end

    subgraph LEGAL["Legal act, outside GitHub"]
        P["Paripurna joint approval<br/>(Pasal 20(2) UUD 1945)<br/>+ President's signature<br/>+ Lembaran Negara"]
    end

    MAIN["'main' branch: law in force<br/>signed release tag, e.g. uu-2026-xx"]

    I -->|"heard"| PR
    NA --> B1
    NA --> B2
    NA --> B3
    B1 --> PR
    B2 --> PR
    B3 --> PR
    PR --> CI --> REV
    REV -->|"considered: merged or rejected,<br/>reason written publicly"| R
    REV -.->|"explained: issue closed<br/>with reason"| I
    R --> P
    P -->|"only after promulgation"| MAIN
    MAIN --> LIVE

    P3["P3 Opacity"] -.-> DRAFT
    P5["P5 Participation"] -.-> I
    P6["P6 Harmonisation bottleneck"] -.-> CI
    P2["P2 Disharmony"] -.-> CI
    P7["P7 No consolidation"] -.-> MAIN
    P9["P9 NA as justification"] -.-> NA
    P1["P1 Hyper-regulation"] -.-> LIVE
```

How to read it: solid arrows are the workflow. Dotted arrows show which documented problem each part addresses. The legal act (the box in the middle) deliberately stays outside the repository.

## 5. Critiques

1. **Data sovereignty.** github.com is a US platform owned by Microsoft. PP 71/2019 Pasal 20 ayat (2) requires public-scope electronic system operators to manage, process and store their systems and data **in Indonesia**. Ayat (3) allows storage abroad only where the storage technology isn't available domestically, and Git hosting clearly is. So an official Indonesian deployment would have to be **self-hosted Git** (e.g., Gitea/GitLab on national data centres), the EU model, not github.com. A public **mirror** on GitHub for reach is a separate, easier question.
2. **Authenticity.** The authoritative text today is the promulgated text in the Lembaran Negara and its certified copy (salinan). A repository becomes authoritative only if a legal instrument says so, as DC did. Releases would also need digital signatures from a certificate authority the state recognises. Even Pasal.id reports "signature integrity: unverified" for the texts it serves, which shows the gap.
3. **Git's model of change is not the law's.** Indonesian amending laws are written as *instructions* ("Ketentuan Pasal 27 diubah sehingga berbunyi…"), not as diffs. Someone has to translate each instruction into a commit, and errors can creep in. This lab hit exactly that in the UU ITE consolidation. The Cornell LII critique of "law in Git" makes the same point.
4. **Digital divide.** GitHub favours people who can already code. Issues must be fed by other channels (SIMAS PUU, public hearings, regional consultations) and summarised back, or "participation by pull request" becomes a new elite.
5. **Transparency theatre.** A public repository where real decisions happen off the record is worse than none, because it looks like accountability. The value depends on a rule that **only** text in the repository counts.
6. **Duplication with e-Harmonisasi.** The government already has a digital harmonisation channel (Permenkum 7/2026). The realistic path is to add version control, public diffs and an open API to what exists, not to build a rival system.

## Limitations of this note

- pshk.or.id and kompas.id could not be reached from the build environment. PSHK 2025 figures come from search-engine summaries of press coverage and must be checked against the PSHK PDF.
- The newest PSHK regulation count found dates from around 2019–2020.
- The WGI figures are from a secondary site.
- The owner's 2024 De Jure article is now included (P9 and section 2b). Its data covers Naskah Akademik from 2018–2022 and hasn't been updated for later ones.

## Sources

**01 Official (primary)**
- UU 12/2011 Pasal 46–47: https://pasal.id/peraturan/uu/uu-no-12-tahun-2011 (official: https://peraturan.bpk.go.id/Details/39188/uu-no-12-tahun-2011)
- UU 15/2019 Pasal I angka 6 (new wording of Pasal 47): https://peraturan.go.id/id/uu-no-15-tahun-2019
- Perpres 87/2014 Pasal 9, 23 and 25 (penyelarasan of the NA, technical readiness documents): https://peraturan.go.id/id/perpres-no-87-tahun-2014
- UU 13/2022 (Pasal 96, meaningful participation): https://peraturan.go.id/id/uu-no-13-tahun-2022
- PP 71/2019 Pasal 20–21: https://peraturan.go.id/id/pp-no-71-tahun-2019
- Permenkum 7/2026 (e-Harmonisasi): https://peraturan.go.id/files/permenkum-no-7-tahun-2026.pdf
- MK 78/PUU-XXIV/2026 summary: https://s.mkri.id/public/content/persidangan/sinopsis/ (ikhtisar 78/PUU-XXIV/2026)
- DPR Setjen presentation on SIMAS PUU: https://berkas.dpr.go.id/setjen/dokumen/-Regulasi-dan-Dokumen-Paparan-OPI-Partisipasi-Publik-Dalam-Legislasi-oleh-Hj.-Ledia-Hanifa-S.Si.-M.PSi.T-1622102422.pdf

**02 Research and civil society**
- PSHK, Catatan Akhir Tahun Kinerja Legislasi 2025: https://www.pshk.or.id/publikasi/catatan-akhir-tahun-pshk-tentang-kinerja-legislasi-tahun-2025-2/
- PSHK, Obesitas Regulasi: https://pshk.or.id/rr/obesitas-regulasi/
- Katadata/Databoks, DPR legislation achievement 2020–2025: https://databoks.katadata.co.id/pendidikan/statistik/69574030d84fd/selama-2020-2025-capaian-legislasi-dpr-ri-selalu-kurang-dari-25
- Kompas.id, DPR 2025 legislative performance: https://www.kompas.id/artikel/en-kinerja-legislasi-dpr-2025-ketika-prolegnas-dilupakan-dan-kehilangan-makna
- Kontan, unpublished RUU Perampasan Aset draft: https://insight.kontan.co.id/news/draf-ruu-perampasan-aset-masih-jadi-rahasia-berpotensi-melanggar-uu-132022-1
- Metro TV, the Minister's two regulatory strategies (Oct 2026): https://www.metrotvnews.com/read/KZmC4W95-menkum-beberkan-2-strategi-penataan-regulasi
- RCTI+/Okezone, 195 Permenkum cut to 34: https://www.rctiplus.com/news/detail/okezone/5494460/pangkas-195-permenkum-jadi-34--menkum--untuk-kepastian-hukum-dan-pelayanan-publik
- Metro TV, Ministry of Law performance (harmonisation figures): https://www.metrotvnews.com/read/KXyCQgJv-1-tahun-kinerja-moncer-kementerian-hukum-pilar-kuat-mendukung-visi-prabowo-gibran
- RRI, HARMONITAS Riau (drafter shortage): https://rri.co.id/pekanbaru/regional/2627877/harmonitas-siap-hadir-kemenkum-riau-satukan-proses-harmonisasi-ranperda
- World Bank WGI: https://www.worldbank.org/en/publication/worldwide-governance-indicators ; secondary: https://www.theglobaleconomy.com/Indonesia/wb_regulatory_quality/

- Al Faruq, M.H., Ruhpinesthi, G.E. & Ismaya, A.S. (2024), "Transplantasi Regulatory Impact Assessment+: Reposisi Naskah Akademik dalam Pembentukan Undang-Undang", *Jurnal Penelitian Hukum De Jure* 24(2): 175–198: https://doi.org/10.30641/dejure.2024.V24.175-198

**03 Foreign examples**
- DC Council GitHub: https://github.com/DCCouncil ; Ars Technica (2018, archived): https://webcf.waybackmachine.org/web/20211001074126/https://arstechnica.com/tech-policy/2018/11/how-i-changed-the-law-with-a-github-pull-request ; DCist: https://dcist.com/story/18/11/28/github-is-a-programming-website-so-what-is-d-c-s-legal-code-doing-on-there
- Open Law Library: https://github.com/openlawlibrary
- EU LEOS: https://interoperable-europe.ec.europa.eu/collection/justice-law-and-security/solution/leos-open-source-software-editing-legislation
- US House Comparative Print Suite: https://civictech.guide/projects/comparative-print-suite ; Clerk reports: https://cha.house.gov/
- legalize-es: https://www.xataka.com/aplicaciones/alguien-ha-cogido-12-000-leyes-espanolas-ha-pasado-a-codigo-fuente-autentica-joya-para-buscar-legislacion
- bundestag/gesetze: https://github.com/bundestag/gesetze
- Cornell LII critique (Tom Bruce): https://blog.law.cornell.edu/tbruce/page/2/
- Slaw, "GitHub: where law meets technology?": https://www.slaw.ca/2014/06/02/git-where-law-meets-technology/

Source regulation text is public domain under Pasal 42 UU 28/2014 (Hak Cipta).
