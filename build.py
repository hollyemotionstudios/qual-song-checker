"""Wrap index.html (written as an Artifact page, without <html>/<head>/<body>)
into a standalone document for GitHub Pages.

Usage: python3 build.py index.html _site/index.html
"""
import pathlib
import sys

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
page = src.read_text(encoding="utf-8")

# everything before the app markup is head material (title, metas, fonts, styles)
marker = '<div class="app"'
split = page.index(marker)
head, body = page[:split], page[split:]

# the same base the Artifact viewer adds around the page
base = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
:root { box-sizing: border-box; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; font: 14px/1.4 system-ui, -apple-system, sans-serif; }
img { max-width: 100%; }
[hidden] { display: none !important; }
</style>
"""

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(base + head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n", encoding="utf-8")
print(f"wrote {out}")
