"""Concept: the Fibonacci spiral as a label-free emblem of RE's law (numbers only, words in the caption)."""
import sys

SIZES = [1, 1, 2, 3, 5, 8, 13, 21, 34]
DIRS = ["right", "up", "left", "down"]
INK, GREY, FAINT = "#111", "#8a8a8a", "#d6d6d6"

squares, x0, y0, x1, y1 = [(0, 0, 1, "right")], 0, 0, 1, 1
for k, s in enumerate(SIZES[1:], start=1):
    d = DIRS[k % 4]
    sq = {"right": (x1, y0), "up": (x0, y1), "left": (x0 - s, y0), "down": (x0, y0 - s)}[d] + (s,)
    squares.append((*sq, d))
    x0, y0 = min(x0, sq[0]), min(y0, sq[1])
    x1, y1 = max(x1, sq[0] + s), max(y1, sq[1] + s)

W, M = 1000, 24
u = (W - 2 * M) / (x1 - x0)
H = round((y1 - y0) * u + 2 * M)
X = lambda x: M + (x - x0) * u
Y = lambda y: M + (y1 - y) * u

def arc(x, y, s, d):
    a, b = {"right": ((x, y), (x + s, y + s)), "up": ((x + s, y), (x, y + s)),
            "left": ((x + s, y + s), (x, y)), "down": ((x, y + s), (x + s, y))}[d]
    r = s * u
    return f"M{X(a[0]):.1f} {Y(a[1]):.1f} A{r:.1f} {r:.1f} 0 0 0 {X(b[0]):.1f} {Y(b[1]):.1f}"

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     '<defs><marker id="ar" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
     f'<path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>']
path = ""
for x, y, s, d in squares:
    o.append(f'<rect x="{X(x):.1f}" y="{Y(y + s):.1f}" width="{s*u:.1f}" height="{s*u:.1f}" fill="none" stroke="{FAINT}" stroke-width="1.5"/>')
    seg = arc(x, y, s, d)
    path += seg if not path else " " + seg.replace("M", "L", 1)
    if s >= 5:
        fs = min(72, s * u * 0.32)
        o.append(f'<text x="{X(x + s/2):.1f}" y="{Y(y + s/2) + fs*0.35:.1f}" font-size="{fs:.0f}" text-anchor="middle" fill="{GREY}">{s}</text>')
o.append(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" marker-end="url(#ar)"/>')
o.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="6" fill="{INK}"/>')
o.append("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
