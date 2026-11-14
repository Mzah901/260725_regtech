# Rules for collecting Indonesian legal sources automatically

**Memo for the lab, as of 14 November 2026.** Idea #6. Method and limits: `experiments/2026-11-14-scraping-rules-memo.md`.

Experimental. Unverified unless marked as reviewed. Not legal advice, and not legal research to rely on.

## Bottom line

| Source | Verdict | In one line |
|---|---|---|
| peraturan.go.id | **Go, politely** | robots.txt allows everything; no bot wall seen. |
| jdihn.go.id | **Go, except `/search-api/`** | robots.txt allows all bots, AI bots named, except the search API. Terms page not read. |
| mkri.id / s.mkri.id (MK decisions) | **Go, politely, one document at a time** | mkri.id has no robots.txt; s.mkri.id disallows only old sections (e.g. `/bak/`, `/pilkada2017/`). Decisions are public PDFs. Watch personal data. |
| putusan3.mahkamahagung.go.id (MA decisions) | **Limited: by hand only** | robots.txt says `search=yes, ai-train=no, use=reference`, and the site sits behind a bot challenge. Heavy personal data. |
| peraturan.bpk.go.id | **Limited: by hand only** | Parts of the site sit behind a bot challenge. Never automate past it. |
| pasal.id | **Limited: read through MCP or the website, no scraping** | Terms ban automated bulk extraction without a written licence and claim the structured data as Pasal.id's work. |

The rule underneath every verdict: **the law text is free, the access is not unlimited.** Regulations and court decisions have no copyright (UU 28/2014 Pasal 42). Whether you may collect them automatically depends on criminal access law, each site's terms, and personal-data law.

## 1. Copyright: the text is free, someone else's database is not

- **No copyright** in "peraturan perundang-undangan" and "putusan pengadilan atau penetapan hakim" (UU 28/2014 Pasal 42 huruf b and d).
  Ideas, methods, and data are not protected either (Pasal 41 huruf b).
- **But databases and data compilations are protected works:** "basis data" (Pasal 40 ayat (1) huruf n) and
  compilations of works or data, whether readable by a computer program or other media (huruf p; Pasal.id's text of this clause is garbled by OCR, so the wording is not quoted here).
  A site's own structure, summaries, tags, relationships and annotations can be protected even when the regulation inside is not.
- Government publications are generally free to reproduce unless declared protected (Pasal 43 huruf b).
- **Rule:** take regulation text from **official sources** (peraturan.go.id, JDIH, official PDFs). Do not republish a private site's structure, summaries or relationship data.

## 2. Access: the real risk

- **Illegal access, KUHP Pasal 332** (as rewritten by UU 1/2026 Pasal VII angka 35, in force since 2 January 2026):
  accessing a computer or electronic system "tanpa hak atau melawan hukum".
  The rewrite dropped the words "dengan sengaja", but intent is still required. Under KUHP Pasal 36 ayat (2), an offence is intentional unless a provision expressly covers negligence.
  So this is drafting clean-up, not a wider offence.
  Ayat (3) is the heaviest (up to 8 years): access "dengan melanggar, menerobos, melampaui, atau menjebol sistem pengamanan".
- **Government systems, KUHP Pasal 333:** huruf d covers using or accessing a government computer system "tanpa hak"; huruf g covers disrupting one (up to 7 years).
  Every official legal portal is a government system.
- **UU ITE Pasal 33** (still in force; Pasal 30 was revoked): acts that disrupt an electronic system. Pasal 34 ayat (2) exempts tools used for research or testing "secara sah".
- **What "tanpa hak" means for a public website is not settled.** Reading a public page as an ordinary visitor is plainly with right.
  The signals that move automated access toward "tanpa hak" are: ignoring robots.txt, breaking the site's terms, and especially **getting past a technical barrier** (a bot challenge, CAPTCHA, login, or rate limit).
- **Rules:**
  - Never solve, bypass, or spoof past a bot challenge, CAPTCHA, login, or rate limit. That is the "menjebol sistem pengamanan" zone.
  - Follow robots.txt for the user agent you actually are.
  - Be slow: at least 2 seconds between requests to one host, one request at a time, and cache everything so each page is fetched once.
  - Identify yourself honestly in the user agent; do not pose as a browser for bulk work.
  - Stop at the first 403 or 429 response and do it by hand instead.

## 3. Terms of use: a contract, even when the text is free

- **Pasal.id terms** (pasal.id/ketentuan, effective 5 October 2026):
  - Automated bulk extraction ("mengekstraksi konten secara otomatis dan massal") is banned without a written licence, through any channel, MCP included.
  - "Data terstruktur dan organisasi database merupakan hasil karya Pasal.id."
  - Using several accounts or tokens to get around limits is banned.
  - MCP full-text reads are capped at 300 per account per day. The API (`/api/v1`) gives metadata and links only, needs a free token, and is rate-limited.
  - Pasal.id itself confirms regulation text has no copyright (Pasal 42 huruf b).
- **Pasal.id robots.txt** separates bots: `ClaudeBot` (training) is blocked; `Claude-User` (fetches a person asks for) and `Claude-SearchBot` (crawl-delay 2) may read law pages.
  Search, correction, account and `/api/laws/` paths are off-limits for all of them; `/api/pdf/` is also off-limits for `Claude-SearchBot` (not for `Claude-User`).
  The memo quotes Pasal.id's terms verbatim; every quoted phrase was checked against the raw page on 2026-11-14.
- **MA Direktori Putusan robots.txt** sets content signals "as a condition of accessing this website": `search=yes, ai-train=no, use=reference`.
  So: no training models on MA decisions collected from that site.
- **Rule:** read the terms before any automated collection, and treat them as binding.

## 4. Personal data: court decisions are full of it

- UU PDP (UU 27/2022) has **no exemption for data that is already public.** Processing must follow its principles: limited and specific collection, a clear purpose, accuracy (Pasal 16 ayat (2)), and a lawful basis (Pasal 20).
- The research exemption is narrow. Pasal 15 ayat (1) huruf e lifts only certain data-subject rights for "statistik dan penelitian ilmiah", and only "dalam rangka pelaksanaan ketentuan Undang-Undang" (ayat (2)).
  The household exemption (Pasal 2 ayat (2)) does not cover a public research project.
- **Criminal records are "spesifik" personal data too** (UU PDP Pasal 4 ayat (2) huruf d). Every criminal court decision is one.
- **The implementing regulation, PP 33/2026** (Peraturan Pelaksanaan UU 27/2022), was promulgated on 16 July 2026 (LN 2026 No. 88) and takes effect 6 months later (Pasal 225), on **16 January 2027**.
  It is not in force yet, but it shows where the rules are going, and the lab should follow it now:
  - **Public data is still personal data.** Combining data to identify someone "termasuk penggunaan data yang tersedia pada domain publik" (Pasal 7 ayat (3)). Names in a published court decision are covered.
  - **The household exemption is narrow.** It covers only processing that is personal, not professional or commercial, and not meant for the public (Pasal 3 ayat (2)). A public research website is meant for the public, so it does not qualify.
  - **Legitimate interest needs paperwork.** Before relying on it, the controller must analyse purpose, need and the balance with the data subject's rights, and assess that the processing does not harm them (Pasal 53). Both must be documented (Pasal 54).
  - **The research exemption has five conditions** (Pasal 148 ayat (1) huruf e, Pasal 154): non-commercial; a lawful basis; a documented balancing test; results not used to judge or decide about the people in the data; and safeguards against misuse. It still lifts only certain rights, and only "dalam rangka pelaksanaan ketentuan Undang-Undang" (Pasal 148 ayat (2)).
  - **Children:** the controller must take steps to identify children, get parental or guardian consent, and verify that consent (Pasal 38 ayat (1), (2), (4)).
  - Retention policies must say how data used for statistics or research is de-identified (Pasal 75 ayat (2) huruf e).
- **Rules:**
  - Regulations: no personal-data issue.
  - Court decisions: do not build datasets indexed by person. Remove party and witness names unless the project needs them, and keep only the fields the question needs.
  - Before any dataset built from court decisions, write a short balancing note in the experiment log (purpose, why the data is needed, effect on the people named, safeguards), following PP 33/2026 Pasal 53, 54 and 154.
  - Never publish a list of named people with legal labels (the same reason idea #7 has a public alternative).
- **Children's data is "spesifik" personal data** (UU PDP Pasal 4 ayat (2) huruf e), and processing it needs parental or guardian consent (Pasal 25 ayat (2)).
  A research lab cannot get that consent. **Rule:** never collect, keep, or publish data that identifies a child, including from court decisions involving children.

## 5. Children: PP 17/2025 and the lab's own website

PP 17/2025 tentang Tata Kelola Penyelenggaraan Sistem Elektronik dalam Pelindungan Anak implements UU ITE Pasal 16A ayat (5) and Pasal 16B ayat (3).
It was promulgated on 27 March 2025 (LN 2025 No. 36), and operators must comply within 2 years of promulgation (Pasal 49), that is by 27 March 2027.

- **What it governs.** Electronic system operators whose products are designed for children, or are likely to be used by them (Pasal 3 ayat (3), Pasal 4 ayat (1)).
  It governs services children use, not datasets about children, so it does not change how the lab collects legal sources.
- **What it requires** of an operator in scope:
  - parental consent (Pasal 7 ayat (1) huruf a, Pasal 9);
  - a data protection impact assessment (Pasal 7 ayat (1) huruf b);
  - high-privacy settings by default (Pasal 10);
  - a self-assessed risk profile reported to the Minister (Pasal 5 ayat (6)–(7));
  - no profiling of children and no precise geolocation (Pasal 7 ayat (2), Pasal 18, Pasal 19).
  Breaches carry administrative sanctions, up to cutting off access (Pasal 38).
- **Does it cover statuta.id?** Probably not, but it is not a clean no.
  - The site is a legal-research portfolio. It is not designed for children, has no accounts, collects no personal data, and its visitor counter (GoatCounter) uses no cookies.
  - But one of the "likely to be used by children" indicators is design that is attractive to children (Pasal 4 ayat (2) huruf d).
    The home page is a game-like 3D room with anime-inspired art, posters and easter eggs. The Minister sets the assessment indicators by decree (Pasal 4 ayat (3)), and that decree was not read here.
  - **Rule:** keep the site free of accounts, tracking and personal data. Do not market it to children. Check the Minister's indicator decree before adding interactive features that collect anything.

## 6. Public information law points the same way, with limits

UU KIP (UU 14/2008) says public information is open and accessible to everyone (Pasal 2 ayat (1)), and everyone may see it and spread it "sesuai dengan peraturan perundang-undangan" (Pasal 4 ayat (2) huruf a and d).
That supports reading and sharing official legal texts. It is not a licence to overload a server or get around its protections.

## 7. Checklist before any automated collection

1. Is the content regulation text or a court decision (free) or someone's compilation (protected)? Take only the free part, from an official source if possible.
2. Read robots.txt for your real user agent. Disallowed means no.
3. Read the terms. A ban on automated or bulk access means no without a licence.
4. Is there a bot challenge, CAPTCHA, login or rate limit? If yes, **stop**; do it by hand.
5. Personal data involved? Minimise it, do not index by person, and write the balancing note (§4). Data that identifies a child: do not collect it at all.
6. Volume and speed: one request at a time, at least 2 seconds apart, cached, honest user agent, stop on 403 or 429.
7. Log it in the experiment: which site, how many requests, which user agent, and on what date.

## 8. Self-audit: the UU ITE consolidation (2026-11-14)

- **What was done:** besides the Pasal.id MCP reads, about 15 Pasal.id web pages were fetched with a generic browser user agent.
  The article text inside each page's data payload was parsed out and saved as `data/consolidation/uu-ite/sources/*.txt`, covering three laws.
  The MK decision pages were fetched the same way to read each ruling's AMAR section.
- **Assessment:** regulation text and court decisions have no copyright, and Pasal.id itself says so. The volume was small, three laws rather than "massal".
  No barrier was bypassed. The fetches were made on the owner's request, which matches what Pasal.id's robots.txt allows `Claude-User` to do.
  But the method, parsing Pasal.id's structured page data, sits close to the terms' ban on automated extraction. It also did not identify itself honestly as an agent.
- **Done (2026-11-14).** The three official PDFs were downloaded from peraturan.go.id, politely (one at a time, 3 seconds apart, honest user agent). Every source file was compared word by word with them.
  There were no wording differences for UU 11/2008 and UU 19/2016. For UU 1/2024 (a scanned PDF), 85 of 89 differences were OCR noise, and the other 4 were confirmed from the page images.
  The files now cite the official PDFs as their source; the text did not need to change.
  From now on, use Pasal.id through MCP (within the daily cap) or the website for reading only, and do not parse its page data.
  If a project needs more, ask for a licence (halo@pasal.id).

## Not covered

- Foreign comparisons (for example US cases on scraping public profiles, or the EU database right). They are not needed for a lab working on Indonesian sources.
- The JDIHN terms page (`/prasyarat`), which could not be loaded (TLS certificate error), and terms for peraturan.go.id, MA, MK and BPK, where no terms page was found.
- The Peraturan Lembaga that PP 33/2026 delegates to (for example on combining data, Pasal 7 ayat (4), and on legitimate interest, Pasal 57). None was read, and the PDP agency's rules may add detail.
- The Penjelasan of UU 1/2026 on why "dengan sengaja" was removed from KUHP Pasal 332 (not found on the page read). The conclusion above rests on KUHP Pasal 36 ayat (2).

Independent personal research. Not affiliated with or endorsed by any employer.
