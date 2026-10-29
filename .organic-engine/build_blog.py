#!/usr/bin/env python3
"""Rebuild /blog/index.html, /feed.xml and the sitemap from the pages in /guides/.

Each guide supplies its own <title>, meta description, canonical URL and
JSON-LD datePublished/dateModified. Run from the repo root after adding or
editing a guide:  python3 .organic-engine/build_blog.py
"""
import glob, html, json, os, re
from datetime import datetime, timezone
from email.utils import format_datetime

BASE = "https://somersetnomad.github.io/FIELD-TOPOLOGY-ASTROMETRY/"
SITE_TITLE = "Field-Topology Astrometry"
FEED_TITLE = "Field-Topology Astrometry: Blog"
FEED_DESC = ("Plain guides to the real astronomy of a birth moment, and how Bala Danmeri's "
             "Field-Topology Astrometry framework reads it.")
AUTHOR = "Bala Danmeri"
EMAIL = "info@baladanmeri.com"
FORM = "https://tally.so/r/ArrMak"

def meta(page):
    s = open(page, encoding="utf-8").read()
    title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip())
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)"', s).group(1))
    url = re.search(r'<link rel="canonical" href="(.*?)"', s).group(1)
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    nodes = ld.get("@graph", [ld])
    art = next(n for n in nodes if n.get("@type") in ("Article", "BlogPosting"))
    pub = art["datePublished"]
    mod = art.get("dateModified", pub)
    return {"title": title, "desc": desc, "url": url, "published": pub, "modified": mod}

def rfc822(d):
    return format_datetime(datetime.fromisoformat(d).replace(hour=9, tzinfo=timezone.utc))

def nice(d):
    return datetime.fromisoformat(d).strftime("%-d %B %Y")

posts = sorted((meta(p) for p in glob.glob("guides/*.html") if not p.endswith("index.html")),
               key=lambda p: (p["published"], p["title"]), reverse=True)

# ---------- RSS 2.0 ----------
items = "\n".join(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{p['url']}</link>
      <guid isPermaLink="true">{p['url']}</guid>
      <pubDate>{rfc822(p['published'])}</pubDate>
      <dc:creator>{AUTHOR}</dc:creator>
      <description>{html.escape(p['desc'])}</description>
    </item>""" for p in posts)
last = rfc822(max((p["modified"] for p in posts), default="2026-10-29"))
open("feed.xml", "w", encoding="utf-8").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>{html.escape(FEED_TITLE)}</title>
    <link>{BASE}blog/</link>
    <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
    <description>{html.escape(FEED_DESC)}</description>
    <language>en-gb</language>
    <managingEditor>{EMAIL} ({AUTHOR})</managingEditor>
    <lastBuildDate>{last}</lastBuildDate>
{items}
  </channel>
</rss>
""")

# ---------- Blog listing ----------
cards = "\n".join(f"""      <article class="post">
        <time datetime="{p['published']}">{nice(p['published'])}</time>
        <h2><a href="{p['url'].replace(BASE, '../')}">{html.escape(p['title'])}</a></h2>
        <p>{html.escape(p['desc'])}</p>
      </article>""" for p in posts) or "      <p>The first post is on its way.</p>"
ld = {"@context": "https://schema.org", "@type": "Blog", "name": FEED_TITLE, "url": BASE + "blog/",
      "description": FEED_DESC, "inLanguage": "en-GB",
      "author": {"@type": "Person", "name": AUTHOR, "url": "https://baladanmeri.com/"},
      "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": p["url"],
                    "datePublished": p["published"], "dateModified": p["modified"]} for p in posts]}
open("blog/index.html", "w", encoding="utf-8").write(f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog: Field-Topology Astrometry</title>
  <meta name="description" content="{html.escape(FEED_DESC)}">
  <link rel="canonical" href="{BASE}blog/">
  <link rel="alternate" type="application/rss+xml" title="{html.escape(FEED_TITLE)}" href="{BASE}feed.xml">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Blog: Field-Topology Astrometry">
  <meta property="og:description" content="{html.escape(FEED_DESC)}">
  <meta property="og:url" content="{BASE}blog/">
  <meta property="og:site_name" content="{SITE_TITLE}">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23070a0f'/%3E%3Cpath d='M16 4C16 4 24 12 24 19C24 23.4 20.4 27 16 27C11.6 27 8 23.4 8 19C8 12 16 4 16 4Z' fill='%23ff5414'/%3E%3Cpath d='M16 9C16 9 21 14.5 21 19C21 21.8 18.8 24 16 24C13.2 24 11 21.8 11 19C11 14.5 16 9 16 9Z' fill='%23fbb034'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
  <style>
    :root {{ --void:#05070a; --abyss:#090d14; --border:#1e293b; --muted:#94a3b8; --text:#e2e8f0; --ember:#ff5414; --gold:#fbb034; --frost:#7dd3fc; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--void); color:var(--text); font:17px/1.7 Inter, system-ui, sans-serif; }}
    a {{ color:var(--frost); }}
    header.site {{ border-bottom:1px solid var(--border); padding:14px 16px; display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; max-width:760px; margin:0 auto; }}
    header.site a.brand {{ font-family:Cinzel, serif; color:#fff; text-decoration:none; letter-spacing:.06em; font-size:15px; }}
    header.site a.cta {{ background:var(--ember); color:#fff; text-decoration:none; padding:6px 12px; border-radius:8px; font-size:14px; font-weight:600; }}
    main {{ max-width:760px; margin:0 auto; padding:24px 16px 64px; }}
    h1 {{ font-family:Cinzel, serif; font-size:clamp(28px, 6vw, 40px); color:#fff; margin:.2em 0 .2em; }}
    .intro {{ color:var(--muted); margin:0 0 1.5em; }}
    .rss {{ display:inline-flex; align-items:center; gap:6px; font:500 13px "JetBrains Mono", monospace; color:var(--gold); text-decoration:none; border:1px solid var(--border); padding:5px 10px; border-radius:8px; }}
    .post {{ border-top:1px solid var(--border); padding:20px 0; }}
    .post time {{ font:500 12px "JetBrains Mono", monospace; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
    .post h2 {{ font-size:22px; line-height:1.3; margin:.25em 0 .3em; }}
    .post h2 a {{ color:#fff; text-decoration:none; }}
    .post h2 a:hover {{ color:var(--gold); }}
    .post p {{ margin:0; color:var(--text); }}
    footer {{ color:var(--muted); font-size:14px; border-top:1px solid var(--border); padding-top:16px; margin-top:24px; }}
  </style>
</head>
<body>
  <header class="site">
    <a class="brand" href="../">{SITE_TITLE}</a>
    <a class="cta" href="{FORM}" target="_blank" rel="noopener">Commission a monograph</a>
  </header>
  <main>
    <h1>Blog</h1>
    <p class="intro">{html.escape(FEED_DESC)}</p>
    <p><a class="rss" href="../feed.xml">RSS feed</a></p>
{cards}
    <footer>
      <p>Written by Bala Danmeri, Wincanton, Somerset. <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><a href="../">&larr; Back to the FTA calculator</a></p>
    </footer>
  </main>
</body>
</html>
""")

# ---------- Sitemap ----------
urls = [(BASE, "2026-10-29"), (BASE + "blog/", max((p["modified"] for p in posts), default="2026-10-29"))]
urls += [(p["url"], p["modified"]) for p in posts]
sm = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>" for u, d in urls)
open("sitemap.xml", "w", encoding="utf-8").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
print(f"built blog/index.html, feed.xml, sitemap.xml with {len(posts)} post(s)")
