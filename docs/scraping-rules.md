# Rules for collecting Indonesian legal sources automatically

**Memo for the lab, as of 14 November 2026.** Idea #6. Method and limits: `experiments/2026-11-14-scraping-rules-memo.md`.

Experimental. Unverified unless marked as reviewed. Not legal advice, and not legal research to rely on.

## Bottom line

| Source | Verdict | In one line |
|---|---|---|
| peraturan.go.id | **Go, politely** | robots.txt allows everything; no bot wall seen. |
| jdihn.go.id | **Go, except `/search-api/`** | robots.txt allows all bots, AI bots named, except the search API. Terms page not read. |
| mkri.id / s.mkri.id (MK decisions) | **Go, politely, one document at a time** | No robots.txt; decisions are public PDFs. Watch personal data. |
| putusan3.mahkamahagung.go.id (MA decisions) | **Limited: by hand only** | robots.txt says `search=yes, ai-train=no, use=reference`, and the site sits behind a bot challenge. Heavy personal data. |
| peraturan.bpk.go.id | **Limited: by hand only** | Parts of the site sit behind a bot challenge. Never automate past it. |
| pasal.id | **Limited: read through MCP or the website, no scraping** | Terms ban automated bulk extraction without a written licence and claim the structured data as Pasal.id's work. |

The rule underneath every verdict: **the law text is free, the access is not unlimited.** Regulations and court decisions have no copyright (UU 28/2014 Pasal 42). Whether you may collect them automatically depends on criminal access law, each site's terms, and personal-data law.

## 1. Copyright: the text is free, someone else's database is not

- **No copyright** in "peraturan perundang-undangan" and "putusan pengadilan atau penetapan hakim" (UU 28/2014 Pasal 42 huruf b and d).
  Ideas, methods, and data are not protected either (Pasal 41 huruf b).
- **But databases and data compilations are protected works:** "basis data" (Pasal 40 ayat (1) huruf n) and
  "kompilasi Ciptaan atau data … yang dapat dibaca dengan Program Komputer" (huruf p).
  A site's own structure, summaries, tags, relationships and annotations can be protected even when the regulation inside is not.
- Government publications are generally free to reproduce unless declared protected (Pasal 43 huruf b).
- **Rule:** take regulation text from **official sources** (peraturan.go.id, JDIH, official PDFs). Do not republish a private site's structure, summaries or relationship data.

## 2. Access: the real risk

- **Illegal access, KUHP Pasal 332** (as rewritten by UU 1/2026 Pasal VII angka 35, in force since 2 January 2026):
  accessing a computer or electronic system "tanpa hak atau melawan hukum". The rewrite **dropped "dengan sengaja"**, so no intent element is written in.
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
  `/api/laws/`, `/api/pdf/`, search, and correction pages are off-limits for these bots.
- **MA Direktori Putusan robots.txt** sets content signals "as a condition of accessing this website": `search=yes, ai-train=no, use=reference`.
  So: no training models on MA decisions collected from that site.
- **Rule:** read the terms before any automated collection, and treat them as binding.

## 4. Personal data: court decisions are full of it

- UU PDP (UU 27/2022) has **no exemption for data that is already public.** Processing must follow its principles: limited and specific collection, a clear purpose, accuracy (Pasal 16 ayat (2)), and a lawful basis (Pasal 20).
- The research exemption is narrow. Pasal 15 ayat (1) huruf e lifts only certain data-subject rights for "statistik dan penelitian ilmiah", and only "dalam rangka pelaksanaan ketentuan Undang-Undang" (ayat (2)).
  The household exemption (Pasal 2 ayat (2)) does not cover a public research project.
- No implementing PP PDP was found in Pasal.id's corpus. Its status is not confirmed here.
- **Rules:**
  - Regulations: no personal-data issue.
  - Court decisions: do not build datasets indexed by person. Remove party and witness names unless the project needs them, and keep only the fields the question needs.
  - Never publish a list of named people with legal labels (the same reason idea #7 has a public alternative).

## 5. Public information law points the same way, with limits

UU KIP (UU 14/2008) says public information is open and accessible to everyone (Pasal 2 ayat (1)), and everyone may see it and spread it "sesuai dengan peraturan perundang-undangan" (Pasal 4 ayat (2) huruf a and d).
That supports reading and sharing official legal texts. It is not a licence to overload a server or get around its protections.

## 6. Checklist before any automated collection

1. Is the content regulation text or a court decision (free) or someone's compilation (protected)? Take only the free part, from an official source if possible.
2. Read robots.txt for your real user agent. Disallowed means no.
3. Read the terms. A ban on automated or bulk access means no without a licence.
4. Is there a bot challenge, CAPTCHA, login or rate limit? If yes, **stop**; do it by hand.
5. Personal data involved? Minimise it, and do not index by person.
6. Volume and speed: one request at a time, at least 2 seconds apart, cached, honest user agent, stop on 403 or 429.
7. Log it in the experiment: which site, how many requests, which user agent, and on what date.

## 7. Self-audit: the UU ITE consolidation (2026-11-14)

- **What was done:** besides the Pasal.id MCP reads, about 15 Pasal.id web pages were fetched with a generic browser user agent.
  The article text inside each page's data payload was parsed out and saved as `data/consolidation/uu-ite/sources/*.txt`, covering three laws.
  The MK decision pages were fetched the same way to read each ruling's AMAR section.
- **Assessment:** regulation text and court decisions have no copyright, and Pasal.id itself says so. The volume was small, three laws rather than "massal".
  No barrier was bypassed. The fetches were made on the owner's request, which matches what Pasal.id's robots.txt allows `Claude-User` to do.
  But the method, parsing Pasal.id's structured page data, sits close to the terms' ban on automated extraction. It also did not identify itself honestly as an agent.
- **Recommendation:** re-source the three text files from the official PDFs on peraturan.go.id, so the repo no longer depends on Pasal.id's structured data.
  From now on, use Pasal.id through MCP (within the daily cap) or the website for reading only, and do not parse its page data.
  If a project needs more, ask for a licence (halo@pasal.id).

## Not covered

- Foreign comparisons (for example US cases on scraping public profiles, or the EU database right). They are not needed for a lab working on Indonesian sources.
- The JDIHN terms page (`/prasyarat`), which could not be loaded (TLS certificate error), and terms for peraturan.go.id, MA, MK and BPK, where no terms page was found.
- Whether the UU 1/2026 rewrite of KUHP Pasal 332 changes how intent is proven in practice.

Independent personal research. Not affiliated with or endorsed by any employer.
