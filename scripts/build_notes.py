"""Build the Beyond Statutes notes: Markdown files that link to each other, like a small wiki.

How it works (plain language):
1. Read every .md file in content/beyond-statutes/. Each starts with a small header
   (between --- lines) giving its title, rank and tag, then the text.
2. In the text, [[Some title]] links to the note with that title. [[Some title|other words]]
   shows "other words" instead. A link to a title that doesn't exist stops the build,
   so broken links can't slip through.
3. For each note, work out which notes it links to and which notes link back to it ("backlinks").
4. Draw a map of all the notes and their links as an SVG picture (no JavaScript needed).
5. Write one page per note, an index page, and the chapter list for the home page.

Only a small part of Markdown is supported, on purpose: paragraphs, **bold**, *italic*
and [[links]]. That is all the notes use.
"""

import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "content" / "beyond-statutes"
NOTE_TEMPLATE = ROOT / "site" / "note.html"
URL_BASE = "/beyond-statutes/"

LINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def read_note(path):
    text = path.read_text(encoding="utf-8")
    _, header, body = text.split("---", 2)
    meta = dict(line.split(":", 1) for line in header.strip().splitlines())
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    return {"slug": path.stem, "title": meta["title"], "rank": int(meta["rank"]), "tag": meta["tag"], "body": body.strip()}


def read_notes():
    notes = sorted((read_note(p) for p in NOTES_DIR.glob("*.md")), key=lambda n: n["rank"])
    by_title = {n["title"].lower(): n for n in notes}
    for n in notes:
        n["links"] = []
        for title, _ in LINK.findall(n["body"]):
            target = by_title.get(title.strip().lower())
            if target is None:
                raise SystemExit(f'Broken link in {n["slug"]}.md: [[{title}]] matches no note title')
            if target not in n["links"]:
                n["links"].append(target)
    for n in notes:
        n["backlinks"] = [m for m in notes if n in m["links"]]
    return notes, by_title


def inline(text, by_title):
    """Turn one paragraph of Markdown into HTML."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    def link(m):
        target = by_title[m.group(1).strip().lower()]
        label = m.group(2) or m.group(1)
        return f'<a class="wikilink" href="{URL_BASE}{target["slug"]}/">{label}</a>'

    return LINK.sub(link, text)


def to_html(body, by_title):
    return "\n".join(f"<p>{inline(p.strip(), by_title)}</p>" for p in body.split("\n\n") if p.strip())


def plain(text):
    """The text with links reduced to their words, for short summaries."""
    return LINK.sub(lambda m: m.group(2) or m.group(1), text)


def graph_svg(notes, current=None, size=320):
    """A circle of numbered nodes with a line for every link. The current note is red."""
    c, r = size / 2, size / 2 - 34
    pos = {}
    for i, n in enumerate(notes):
        a = -math.pi / 2 + i * 2 * math.pi / len(notes)
        pos[n["slug"]] = (c + r * math.cos(a), c + r * math.sin(a))
    lines, nodes = [], []
    drawn = set()
    for n in notes:
        for m in n["links"]:
            pair = tuple(sorted((n["slug"], m["slug"])))
            if pair in drawn:
                continue
            drawn.add(pair)
            hot = current is not None and current["slug"] in pair
            (x1, y1), (x2, y2) = pos[pair[0]], pos[pair[1]]
            lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{"edge hot" if hot else "edge"}"/>')
    for n in notes:
        x, y = pos[n["slug"]]
        cls = "node current" if current is n else "node"
        nodes.append(
            f'<a href="{URL_BASE}{n["slug"]}/" class="{cls}"><title>{html.escape(n["title"])}</title>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17"/>'
            f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle">{n["rank"]}</text></a>'
        )
    return (f'<svg class="graph" viewBox="0 0 {size} {size}" role="img" aria-label="Map of how the notes link to each other">'
            + "".join(lines) + "".join(nodes) + "</svg>")


def link_list(notes):
    if not notes:
        return '<p class="muted">None yet.</p>'
    items = "".join(f'<li><a href="{URL_BASE}{n["slug"]}/">{n["rank"]}. {html.escape(n["title"])}</a></li>' for n in notes)
    return f'<ul class="refs">{items}</ul>'


def note_page(n, notes, by_title, template):
    main = f"""
<p class="crumb"><a href="/">statuta.id</a> / <a href="{URL_BASE}">beyond statutes</a></p>
<article>
  <span class="rank" aria-hidden="true">{n["rank"]}</span>
  <span class="ch">CH.{n["rank"]:02d} · {n["tag"]}</span>
  <h1>{html.escape(n["title"])}</h1>
  {to_html(n["body"], by_title)}
</article>
<div class="connections">
  <div><h2>Links to</h2>{link_list(n["links"])}</div>
  <div><h2>Linked from</h2>{link_list(n["backlinks"])}</div>
</div>
<figure>{graph_svg(notes, n)}<figcaption>How the notes connect. Red is this note.</figcaption></figure>
"""
    return template.replace("__TITLE__", html.escape(n["title"])).replace("__MAIN__", main)


def index_page(notes, template):
    items = "".join(
        f'<li><a href="{URL_BASE}{n["slug"]}/"><span class="ch">CH.{n["rank"]:02d} · {n["tag"]}</span>'
        f'<b>{html.escape(n["title"])}</b></a><span class="muted">{len(n["links"])} links out · {len(n["backlinks"])} links in</span></li>'
        for n in notes
    )
    main = f"""
<p class="crumb"><a href="/">statuta.id</a> / beyond statutes</p>
<h1>Beyond Statutes</h1>
<p class="muted">Notes from my journal, written as a small web of ideas. Each note links to the others it leans on.</p>
<figure>{graph_svg(notes, size=360)}<figcaption>Click a number to open that note.</figcaption></figure>
<ol class="index">{items}</ol>
"""
    return template.replace("__TITLE__", "Beyond Statutes").replace("__MAIN__", main)


def home_chapters(notes):
    """The chapter list shown on the home page: title, tag and the first paragraph."""
    out = []
    for n in notes:
        summary = html.escape(plain(n["body"].split("\n\n")[0]), quote=False)
        out.append(
            f'<li><span class="rank" aria-hidden="true">{n["rank"]}</span>\n'
            f'  <span class="ch">CH.{n["rank"]:02d} · {n["tag"]}</span>\n'
            f'  <h3><a href="{URL_BASE}{n["slug"]}/">{html.escape(n["title"])}</a></h3>\n'
            f'  <p>{summary}</p>\n</li>'
        )
    return '<ol class="chapters">\n' + "\n".join(out) + "\n</ol>"


def build(public_dir):
    """Write the note pages into public_dir and return the home-page chapter list."""
    notes, by_title = read_notes()
    template = NOTE_TEMPLATE.read_text(encoding="utf-8")
    out = public_dir / "beyond-statutes"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(index_page(notes, template), encoding="utf-8")
    for n in notes:
        (out / n["slug"]).mkdir(exist_ok=True)
        (out / n["slug"] / "index.html").write_text(note_page(n, notes, by_title, template), encoding="utf-8")
    links = sum(len(n["links"]) for n in notes)
    print(f"{len(notes)} notes, {links} links between them")
    return home_chapters(notes)


if __name__ == "__main__":
    # Self-check: links resolve, labels work, HTML is escaped, every note is reachable.
    notes, by_title = read_notes()
    assert inline("a [[Equivalent exchange.|value]] & b", by_title) == \
        'a <a class="wikilink" href="/beyond-statutes/equivalent-exchange/">value</a> &amp; b'
    assert plain("see [[Equivalent exchange.]]") == "see Equivalent exchange."
    assert all(n["backlinks"] for n in notes), "every note should be linked from at least one other"
    print("build_notes self-check passed:", len(notes), "notes")
