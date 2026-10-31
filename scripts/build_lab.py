"""Build the Lab page (statuta.id/lab/): every experiment log, plus the Python learning log.

How it works (plain language):
1. Read every .md file in experiments/. Each log has a # title, **Date:** and **Status:** lines,
   and ## sections. The page shows the question, the result, the known limits and whether
   I have reviewed it yet; the full log stays on GitHub.
2. Read content/learning/python.md: "- [x]" is a finished session, "- [ ]" is not done yet.
   Ticking a box there is all it takes to move the progress bar.
3. Put both into the same page template as the Beyond Statutes notes.

Only a small part of Markdown is supported: paragraphs, "- " and "1. " lists, **bold**,
`code` and [links](url). That is all the logs use in the sections shown.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = ROOT / "experiments"
LEARNING = ROOT / "content" / "learning" / "python.md"
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
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', text)
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


def learning_html():
    text = LEARNING.read_text(encoding="utf-8")
    _, header, body = text.split("---", 2)
    meta = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in header.strip().splitlines())}
    done = len(re.findall(r"^- \[x\]", body, re.M | re.I))
    total = len(re.findall(r"^- \[[ x]\]", body, re.M | re.I))
    out = [f'<h1 class="small">{html.escape(meta["title"])}</h1>',
           f'<p class="progress"><span style="width:{100 * done / total:.0f}%"></span></p>',
           f'<p class="ch">{done} / {total} sessions done</p>']
    if meta.get("repo"):
        out.append(f'<p class="muted">Code: <a href="{meta["repo"]}">{html.escape(meta["repo"])}</a></p>')
    for line in body.strip().splitlines():
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif m := re.match(r"- \[([ xX])\] (.+)", line):
            mark, cls = ("✓", "done") if m.group(1) != " " else ("·", "todo")
            out.append(f'<p class="session {cls}"><span aria-hidden="true">{mark}</span> {inline(m.group(2))}</p>')
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    return "\n".join(out), done, total


def build(public_dir):
    experiments = sorted((read_experiment(p) for p in EXPERIMENTS_DIR.glob("*.md")), key=lambda e: e["file"], reverse=True)
    learning, done, total = learning_html()
    main = f"""
<p class="crumb"><a href="/">statuta.id</a> / lab</p>
<h1>Lab</h1>
<p class="muted">What I tried, what came out, and what is still wrong with it. Every result is a draft until I have checked it by hand.</p>
<h2 id="experiments">Experiments</h2>
{"".join(experiment_html(e) for e in experiments)}
<section id="learning">
{learning}
</section>
"""
    page = TEMPLATE.read_text(encoding="utf-8").replace("__TITLE__ · Beyond Statutes", "Lab · Regulatory AI Labs")
    out = public_dir / "lab"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page.replace("__TITLE__", "Lab").replace("__MAIN__", main), encoding="utf-8")
    print(f"Lab: {len(experiments)} experiments, Python {done}/{total} sessions")


if __name__ == "__main__":
    # Self-check: lists, wrapped list lines, links and escaping come out right.
    got = blocks(["Intro & more.", "", "- one", "  still one", "- **two** see https://a.b/c", "", "1. first"])
    assert got == ('<p>Intro &amp; more.</p>\n<ul class="refs">\n<li>one still one</li>\n'
                   '<li><b>two</b> see <a href="https://a.b/c">https://a.b/c</a></li>\n</ul>\n'
                   '<ol class="refs">\n<li>first</li>\n</ol>'), got
    assert inline("_Pending._ snake_case") == "<i>Pending.</i> snake_case"
    assert inline("[x](https://e.com)") == '<a href="https://e.com">x</a>'
    e = read_experiment(EXPERIMENTS_DIR / "2026-10-11-legal-industry-map.md")
    assert list(e["sections"]) == ["Question", "Result", "Known limits", "Human review"], list(e["sections"])
    print("build_lab self-check passed")
