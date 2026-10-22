"""Wrap index.html (written as an Artifact page, without <html>/<head>/<body>)
into a standalone document for GitHub Pages and Vercel, plus a web app
manifest and icons so "Add to Home screen" opens the app full screen.

Usage: python3 build.py index.html _site/index.html
"""
import json
import math
import pathlib
import struct
import sys
import zlib

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
site = out.parent
page = src.read_text(encoding="utf-8")

# everything before the app markup is head material (title, metas, fonts, styles)
marker = '<div class="app"'
split = page.index(marker)
head, body = page[:split], page[split:]

# the same base the Artifact viewer adds around the page, plus the manifest and icons
base = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-512.png">
<style>
:root { box-sizing: border-box; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; font: 14px/1.4 system-ui, -apple-system, sans-serif; }
img { max-width: 100%; }
[hidden] { display: none !important; }
</style>
"""

NIGHT = "#0d1b2e"
manifest = {
    "name": "Song Match Prop",
    "short_name": "Song Match",
    "start_url": ".",
    "scope": ".",
    "display": "fullscreen",
    "orientation": "any",
    "background_color": NIGHT,
    "theme_color": NIGHT,
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


# the orb's music note, in the 24-unit box the app's SVG uses: stem, flag (a flattened curve) and head
FLAG = [(12 + 6 * t * t, 4 + 4 * t * t - 2.5 * t * (1 - t) * 0.8) for t in [i / 12 for i in range(13)]]
NOTE_SEGS = [((12, 17), (12, 4))] + list(zip(FLAG, FLAG[1:]))


def icon_png(size):
    night, peach_hi, peach, ember = hex_rgb(NIGHT), hex_rgb("#ffd2ad"), hex_rgb("#ffb27a"), hex_rgb("#ef6f6c")
    c, r = size / 2, size * 0.36                 # orb inside the maskable safe zone
    note_scale = (r * 2 * 0.46) / 24             # note fills 46% of the orb, as in the app
    nx, ny = c - 12 * note_scale, c - 12 * note_scale
    half_w = 1.1 * note_scale                    # stroke width 2.2
    sub = [(i + 0.5) / 3 for i in range(3)]
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            acc = [0.0, 0.0, 0.0]
            for sy in sub:
                for sx in sub:
                    px, py = x + sx, y + sy
                    d = math.hypot(px - c, py - c)
                    col = night
                    if d <= r:
                        # radial light from the upper left, like the app's orb
                        t = min(1.0, math.hypot(px - (c - r * 0.3), py - (c - r * 0.4)) / (r * 1.45))
                        col = mix(peach_hi, peach, t / 0.38) if t < 0.38 else mix(peach, ember, (t - 0.38) / 0.62)
                        ux, uy = (px - nx) / note_scale, (py - ny) / note_scale
                        on_note = abs(math.hypot(ux - 8.5, uy - 17) - 3.5) <= 1.1 or any(
                            seg_dist(ux, uy, *a, *b) <= 1.1 for a, b in NOTE_SEGS)
                        if on_note:
                            col = night
                    acc = [acc[i] + col[i] for i in range(3)]
            row += bytes(int(v / 9 + 0.5) for v in acc)
        rows.append(bytes(row))
    raw = zlib.compress(b"".join(rows), 9)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) + chunk(b"IDAT", raw) + chunk(b"IEND", b"")


site.mkdir(parents=True, exist_ok=True)
out.write_text(base + head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n", encoding="utf-8")
(site / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
for size in (192, 512):
    (site / f"icon-{size}.png").write_bytes(icon_png(size))
print(f"wrote {out}, manifest and icons")
