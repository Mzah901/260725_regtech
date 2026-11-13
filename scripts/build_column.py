"""Build the Column (statuta.id/column/): dated opinion posts, newest first, plus an RSS feed.

How it works (plain language):
1. Read every .md file in content/column/. Each starts with a header (between --- lines)
   giving its title, date (YYYY-MM-DD) and tag, then the text.
2. Sort the posts by date, newest first.
3. Write one page per post, a list page, and feed.xml. The feed is what lets feed readers,
   and later an email newsletter service, pick up new posts automatically.

Unlike Beyond Statutes (timeless notes, ordered by chapter), column posts are dated and react
to something happening. Posts stay in the language they were written in.
The text uses the same small Markdown as the Lab pages: paragraphs, "- " and "1. " lists,
**bold**, _italic_ and [links](url).
"""

import html
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

from build_lab import blocks

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "column"
TEMPLATE = ROOT / "site" / "note.html"
SITE = "https://statuta.id"
NOTICE = "Personal opinion. Not legal advice, and not the view of any employer."


def read_post(path):
    _, header, body = path.read_text(encoding="utf-8").split("---", 2)
    meta = {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in header.strip().splitlines())}
    datetime.strptime(meta["date"], "%Y-%m-%d")  # stops the build on a mistyped date
    return {"slug": path.stem, "title": meta["title"], "date": meta["date"], "tag": meta["tag"], "body": body.strip()}


def read_posts():
    return sorted((read_post(p) for p in POSTS_DIR.glob("*.md")), key=lambda p: p["date"], reverse=True)


def page(title, main):
    tab = "Column · statuta.id" if title == "Column" else f"{html.escape(title)} · Column"
    return (TEMPLATE.read_text(encoding="utf-8").replace("__TITLE__ · Beyond Statutes", tab)
            .replace("__TITLE__", html.escape(title)).replace("__MAIN__", main))


def post_page(p):
    return page(p["title"], f"""
<p class="crumb"><a href="/">statuta.id</a> / <a href="/column/">column</a></p>
<article class="exp" style="border-top:0;padding-top:0">
  <span class="ch">{p["date"]} · {html.escape(p["tag"])}</span>
  <h1>{html.escape(p["title"])}</h1>
  {blocks(p["body"].splitlines())}
</article>
<p class="muted">{NOTICE}</p>
<p class="muted"><a href="/column/">← All column posts</a> · <a href="/column/feed.xml">RSS</a></p>
""")


def index_page(posts):
    items = "".join(
        f'<li><a href="/column/{p["slug"]}/"><span class="ch">{p["date"]} · {html.escape(p["tag"])}</span>'
        f'<b>{html.escape(p["title"])}</b></a></li>' for p in posts)
    return page("Column", f"""
<p class="crumb"><a href="/">statuta.id</a> / column</p>
<h1>Column</h1>
<p class="muted">My opinions on law, policy and whatever else I can't stop thinking about. Dated, newest first, and written in whichever language came out. {NOTICE}</p>
<p class="muted"><a href="/column/feed.xml">Follow with RSS</a></p>
<ol class="index">{items}</ol>
""")


def feed_xml(posts):
    def item(p):
        when = format_datetime(datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc))
        url = f"{SITE}/column/{p['slug']}/"
        return (f"<item><title>{html.escape(p['title'])}</title><link>{url}</link><guid>{url}</guid>"
                f"<pubDate>{when}</pubDate><description>{html.escape(blocks(p['body'].splitlines()))}</description></item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f"<title>Column · statuta.id</title><link>{SITE}/column/</link><description>{NOTICE}</description>"
            + "".join(item(p) for p in posts) + "</channel></rss>\n")


def build(public_dir):
    posts = read_posts()
    out = public_dir / "column"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(index_page(posts), encoding="utf-8")
    (out / "feed.xml").write_text(feed_xml(posts), encoding="utf-8")
    for p in posts:
        (out / p["slug"]).mkdir(exist_ok=True)
        (out / p["slug"] / "index.html").write_text(post_page(p), encoding="utf-8")
    print(f"Column: {len(posts)} posts")


if __name__ == "__main__":
    # Self-check: posts sort newest first, the feed is valid XML with one item per post.
    import xml.etree.ElementTree as ET
    posts = read_posts()
    assert [p["date"] for p in posts] == sorted((p["date"] for p in posts), reverse=True)
    items = ET.fromstring(feed_xml(posts)).findall("./channel/item")
    assert len(items) == len(posts) and all(i.findtext("link").startswith(SITE) for i in items)
    print("build_column self-check passed:", len(posts), "posts")
