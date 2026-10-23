#!/usr/bin/env python3
"""Build dist/index.html from source.html.

Only dist/ gets deployed, so the source and this script stay off the web.

The artifact runtime supplies a doctype and <head> at publish time; served
directly the raw file would land in quirks mode with no viewport tag."""
import re, sys, pathlib

SRC = sys.argv[1] if len(sys.argv) > 1 else "source.html"
DIST = pathlib.Path(__file__).parent / "dist"
DIST.mkdir(exist_ok=True)
OUT = DIST / "index.html"
DESC = ("A laser show that reads a whole track before it plays, so the lights "
        "anticipate the drops instead of chasing them. Drop in an audio file.")
FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'"
       "%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8E%9B%EF%B8%8F%3C/text%3E%3C/svg%3E")

src = pathlib.Path(SRC).read_text(encoding="utf-8")
m = re.search(r"<title>(.*?)</title>\s*", src, re.S)
title = m.group(1).strip() if m else "skanz.sounds"
body = (src[:m.start()] + src[m.end():]) if m else src

OUT.write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#06070C">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC}">
<link rel="icon" href="{FAV}">
<style>
  *,*::before,*::after{{box-sizing:border-box;}}
  html,body{{margin:0;padding:0;}}
</style>
</head>
<body>
{body.strip()}
</body>
</html>
""", encoding="utf-8")
print(f"built {OUT}  ({OUT.stat().st_size:,} bytes)  title = {title!r}")
