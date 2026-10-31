"""Build the Lab page (statuta.id/lab/) from the experiment logs, and the plain pages in content/pages/.

How it works (plain language):
1. Read every .md file in experiments/. Each log has a # title, **Date:** and **Status:** lines,
   and ## sections. The page shows the question, the result, the known limits and whether
   I have reviewed it yet; the full log stays on GitHub.
2. Each file in content/pages/ (about.md, lessons.md) becomes its own page: about.md → statuta.id/about/.
   "## Heading" starts a section; its id is the heading in lower case, so /about/#awards jumps there.
3. All of them use the same page template as the Beyond Statutes notes.

Only a small part of Markdown is supported: paragraphs, "- " and "1. " lists, **bold**,
`code`, _italic_ and [links](url), plus "## " headings in content/pages/.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = ROOT / "experiments"
PAGES_DIR = ROOT / "content" / "pages"
TEMPLATE = ROOT / "site" / "note.html"
LOG_URL = "https://github.com/Mzah901/260725_regtech/blob/claude/new-session-euryc2/experiments/"

# Which sections of a log appear on the page, and the heading they get there.
SHOWN = {"question": "Question", "result": "Result", "known limitations": "Known limits",
         "what the owner reviewed": "Human review"}


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<i>\1</i>", text)
    text = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\(((?:https?://|/)[^)\s]+)\)", r'<a href="\2">\1</a>', text)
    return re.sub(r"(?<![\"'>])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', text)


def blocks(lines):
    """Turn Markdown lines into HTML: lists for "- " or "1. " lines, paragraphs for the rest."""
    out, kind, item = [], None, []

    def flush():
        nonlocal kind, item
        if item:
            text = inline(" ".join(item))
            out.append(f"<li>{text}</li>" if kind else f"<p>{text}</p>")
        item = []

    for line in lines + [""]:
        bullet = re.match(r"\s*(-|\d+\.)\s+(.*)", line)
        if bullet:
            flush()
            tag = "ul" if bullet.group(1) == "-" else "ol"
            if kind != tag:
                if kind: out.append(f"</{kind}>")
                out.append(f'<{tag} class="refs">')
                kind = tag
            item = [bullet.group(2)]
        elif line.strip() and not line.startswith("|"):
            if kind and not line.startswith(" ") and not item:
                out.append(f"</{kind}>"); kind = None
            item.append(line.strip())
        else:
            flush()
            if kind and not line.strip():
                out.append(f"</{kind}>"); kind = None
    return "\n".join(out)


def read_experiment(path):
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    field = lambda name: (re.search(rf"^\*\*{name}:\*\* (.+)$", text, re.M) or [None, ""])[1]
    sections = {}
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        heading, _, body = part.partition("\n")
        for key, label in SHOWN.items():
            if heading.lower().startswith(key):
                sections[label] = blocks(body.strip().splitlines())
    return {"file": path.name, "title": title, "date": field("Date"), "status": field("Status"), "sections": sections}


def experiment_html(e):
    parts = "".join(f"<h2>{label}</h2>\n{body}\n" for label, body in e["sections"].items())
    return f"""<article class="exp">
  <span class="ch">{html.escape(e["date"])} · {inline(e["status"])}</span>
  <h1 class="small">{html.escape(e["title"])}</h1>
  {parts}<p class="muted"><a href="{LOG_URL}{e["file"]}">Full log: method, sources, tools →</a></p>
</article>"""


def plain_page(path):
    """A content/pages/ file: header with the title, then paragraphs, lists and ## sections."""
    _, header, body = path.read_text(encoding="utf-8").split("---", 2)
    title = header.split("title:", 1)[1].strip()
    out, chunk = [f'<p class="crumb"><a href="/">statuta.id</a> / {html.escape(title.lower())}</p>', f"<h1>{html.escape(title)}</h1>"], []
    for line in body.strip().splitlines() + ["## "]:
        if line.startswith("## "):
            out.append(blocks(chunk)); chunk = []
            if line[3:]:
                out.append(f'<h2 id="{line[3:].strip().lower().replace(" ", "-")}">{html.escape(line[3:].strip())}</h2>')
        else:
            chunk.append(line)
    return title, "\n".join(out)


# Star map on the home page: each concept hangs off its science, and each science links to the
# Beyond Statutes notes whose tag it feeds. The browser lays it out (see the sky script in site/home.html).
SCIENCE = {"Operations": "Computing", "Computing": "Computing", "Operating systems": "Computing",
           "Physics": "Physics", "Materials science": "Physics", "Chemistry": "Chemistry",
           "Probability": "Mathematics", "Statistics": "Mathematics", "Game theory": "Mathematics",
           "Economics": "Economics", "Finance": "Economics", "Behavioral finance": "Psychology",
           "Psychology": "Psychology", "Cognitive psychology": "Psychology", "Decision science": "Psychology",
           "Psychometrics": "Psychology", "Law": "Law", "Competition law": "Law", "Law and economics": "Law",
           "Law of evidence": "Law", "Legisprudence": "Law", "Negotiation": "Law"}
FEEDS = {"Law": ["LAW", "POLICY"], "Economics": ["FINANCE", "POLICY"], "Mathematics": ["FINANCE"],
         "Computing": ["TECH"], "Psychology": ["LIFE"], "Physics": ["LIFE"], "Chemistry": ["LIFE"]}


def sky_json(notes):
    """Nodes and links for the star map, as JSON for the home page."""
    nodes = [{"id": n["slug"], "label": n["title"].rstrip("."), "kind": "note", "href": f"/beyond-statutes/{n['slug']}/",
              "text": n["body"].split("\n\n")[0].replace("[[", "").replace("]]", "")} for n in notes]
    links = [[n["slug"], m["slug"]] for n in notes for m in n["links"]]
    for line in (PAGES_DIR / "lessons.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"- \*\*(.+?)\*\* · ([^.]+)\. (.+)", line)
        if not m:
            continue
        name, field, text = m.groups()
        sci = SCIENCE[field]   # a new field in lessons.md needs a line in SCIENCE above
        if not any(x["id"] == sci for x in nodes):
            nodes.append({"id": sci, "label": sci, "kind": "science", "href": "/lessons/"})
            links += [[sci, n["slug"]] for n in notes if n["tag"] in FEEDS[sci]]
        nodes.append({"id": name, "label": name, "kind": "concept", "text": f"{field}. {text}"})
        links.append([sci, name])
    return json.dumps({"nodes": nodes, "links": links}, ensure_ascii=False).replace("</", "<\\/")


def books_json(notes, by_title):
    """The flipbooks the home page opens: Beyond Statutes, the awards (trophies) and the papers (journal stack)."""
    import build_notes
    def items(section):
        body = (PAGES_DIR / "about.md").read_text(encoding="utf-8").split(f"## {section}\n", 1)[1].split("\n## ", 1)[0]
        for line in body.splitlines():
            if m := re.match(r"- \*\*(.+?)\*\*[,.]?\s*(.*)", line):
                yield m.group(1).rstrip("."), m.group(2)
    papers = [{"k": f"Paper {i} of 5", "t": t, "h": f"<p>{inline(rest)}</p>", "w": re.findall(r"20\d\d", rest)[0]}
              for i, (t, rest) in enumerate(items("Publications"), 1)]
    awards = [{"k": "Honours", "t": t, "h": f"<p>{inline(rest[0].upper() + rest[1:])}</p>", "w": re.match(r"\d\w\w|", t).group() or "★"}
              for t, rest in items("Awards")]
    statutes = [{"k": f"CH.{n['rank']:02d} · {n['tag']}", "t": n["title"], "h": build_notes.to_html(n["body"], by_title),
                 "a": f"/beyond-statutes/{n['slug']}/", "id": n["slug"], "w": n["rank"]} for n in notes]
    books = {
        "statutes": [{"cover": True, "t": "Beyond Statutes", "sub": "Mzah in journey"}] + statutes,
        "papers": [{"cover": True, "t": "Published papers", "sub": "Constitutional law and lawmaking, 2023–2024"}] + papers,
        "awards": [{"cover": True, "t": "Honours", "sub": "Writing and drafting competitions"}] + awards,
    }
    for book in books.values():
        for p in book:
            p["t"] = html.escape(p["t"])
    return json.dumps(books, ensure_ascii=False).replace("</", "<\\/")


def build(public_dir):
    experiments = sorted((read_experiment(p) for p in EXPERIMENTS_DIR.glob("*.md")), key=lambda e: e["file"], reverse=True)
    main = f"""
<p class="crumb"><a href="/">statuta.id</a> / lab</p>
<h1>Lab</h1>
<p class="muted">What I tried, what came out, and what is still wrong with it. Every result is a draft until I have checked it by hand.</p>
<h2 id="experiments">Experiments</h2>
{"".join(experiment_html(e) for e in experiments)}
"""
    page = TEMPLATE.read_text(encoding="utf-8").replace("__TITLE__ · Beyond Statutes", "Lab · Regulatory AI Labs")
    out = public_dir / "lab"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page.replace("__TITLE__", "Lab").replace("__MAIN__", main), encoding="utf-8")
    for path in sorted(PAGES_DIR.glob("*.md")):
        title, body = plain_page(path)
        (public_dir / path.stem).mkdir(exist_ok=True)
        (public_dir / path.stem / "index.html").write_text(
            TEMPLATE.read_text(encoding="utf-8").replace("__TITLE__ · Beyond Statutes", f"{title} · Regulatory AI Labs")
            .replace("__TITLE__", html.escape(title)).replace("__MAIN__", f'<div class="page">{body}</div>'), encoding="utf-8")
    print(f"Lab: {len(experiments)} experiments; pages: {', '.join(p.stem for p in PAGES_DIR.glob('*.md'))}")


if __name__ == "__main__":
    # Self-check: lists, wrapped list lines, links and escaping come out right.
    got = blocks(["Intro & more.", "", "- one", "  still one", "- **two** see https://a.b/c", "", "1. first"])
    assert got == ('<p>Intro &amp; more.</p>\n<ul class="refs">\n<li>one still one</li>\n'
                   '<li><b>two</b> see <a href="https://a.b/c">https://a.b/c</a></li>\n</ul>\n'
                   '<ol class="refs">\n<li>first</li>\n</ol>'), got
    assert inline("_Pending._ snake_case") == "<i>Pending.</i> snake_case"
    assert inline("[x](https://e.com)") == '<a href="https://e.com">x</a>'
    assert inline("[Lab](/lab/)") == '<a href="/lab/">Lab</a>'
    e = read_experiment(EXPERIMENTS_DIR / "2026-10-11-legal-industry-map.md")
    assert list(e["sections"]) == ["Question", "Result", "Known limits", "Human review"], list(e["sections"])
    title, body = plain_page(PAGES_DIR / "about.md")
    assert '<h2 id="awards">Awards</h2>' in body and "<i>Jurnal Konstitusi</i>" in body, body[:400]
    import build_notes
    sky = json.loads(sky_json(build_notes.read_notes()[0]))
    ids = {x["id"] for x in sky["nodes"]}
    assert all(a in ids and b in ids for a, b in sky["links"]), "every link joins two stars"
    assert sum(x["kind"] == "concept" for x in sky["nodes"]) == 36, "every lesson became a star"
    books = json.loads(books_json(*build_notes.read_notes()))
    assert [len(books[b]) for b in ("statutes", "papers", "awards")] == [8, 6, 8], [len(b) for b in books.values()]
    assert books["awards"][1]["t"] == "1st place" and "Universitas Indonesia" in books["awards"][1]["h"]
    print("build_lab self-check passed")
