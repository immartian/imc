"""Concept sketch: RE's layers on a Fibonacci spiral (not for the site yet)."""
import math, sys

SIZES = [1, 1, 2, 3, 5, 8, 13, 21, 34]
LAYERS = ["COSMOS", "MATTER", "CHEMISTRY", "LIFE", "NEURONS", "MIND", "CULTURE", "TECHNOLOGY", "SYNTHETIC"]
DIRS = ["right", "up", "left", "down"]           # each new square attaches on this side, turning counter-clockwise
INK, GREY = "#111", "#9a9a9a"

# lay the squares out in math coordinates (y up)
squares, x0, y0, x1, y1 = [], 0, 0, 1, 1
squares.append((0, 0, 1, "right"))              # the first square, oriented as if it had come in from the right
for k, s in enumerate(SIZES[1:], start=1):
    d = DIRS[k % 4]
    if d == "right": sq = (x1, y0, s)
    elif d == "up": sq = (x0, y1, s)
    elif d == "left": sq = (x0 - s, y0, s)
    else: sq = (x0, y0 - s, s)
    squares.append((*sq, d))
    x0, y0 = min(x0, sq[0]), min(y0, sq[1])
    x1, y1 = max(x1, sq[0] + s), max(y1, sq[1] + s)

W, M = 1100, 30
u = (W - 2 * M - 300) / (x1 - x0)              # leave room on the right for notes
H = int((y1 - y0) * u + 2 * M + 70)
X = lambda x: M + (x - x0) * u
Y = lambda y: M + (y1 - y) * u

def arc(x, y, s, d):
    """Quarter arc through the square, continuing the spiral (centre, start, end per side)."""
    if d == "right": c, a, b = (x, y + s), (x, y), (x + s, y + s)
    elif d == "up": c, a, b = (x, y), (x + s, y), (x, y + s)
    elif d == "left": c, a, b = (x + s, y), (x + s, y + s), (x, y)
    else: c, a, b = (x + s, y + s), (x, y + s), (x + s, y)
    r = s * u
    return f"M{X(a[0]):.1f} {Y(a[1]):.1f} A{r:.1f} {r:.1f} 0 0 0 {X(b[0]):.1f} {Y(b[1]):.1f}", a, b

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     '<defs><marker id="ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
     f'<path d="M0 1 L9 5 L0 9 z" fill="{INK}"/></marker></defs>']
path = ""
for i, (x, y, s, d) in enumerate(squares):
    o.append(f'<rect x="{X(x):.1f}" y="{Y(y + s):.1f}" width="{s*u:.1f}" height="{s*u:.1f}" fill="none" stroke="{GREY}" stroke-width="1"/>')
    seg, a, b = arc(x, y, s, d)
    path += (seg if not path else " " + seg.replace("M", "L", 1))
    cx, cy = X(x + s / 2), Y(y + s / 2)
    if s >= 5:
        fs = min(26, max(12, s * u / 7))
        o.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{fs:.0f}" font-weight="bold" letter-spacing="1.5" text-anchor="middle" fill="{INK}">{LAYERS[i]}</text>')
        o.append(f'<text x="{cx:.1f}" y="{cy + fs * 1.1:.1f}" font-size="{fs*0.75:.0f}" text-anchor="middle" fill="{GREY}">{s}</text>')
o.append(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#ar)"/>')
# callouts for the four small inner squares
small = [(i, sq) for i, sq in enumerate(squares) if sq[2] < 5]
for n, (i, (x, y, s, d)) in enumerate(small):
    cx, cy = X(x + s / 2), Y(y + s / 2)
    lx, ly = X(x1) + 40, M + 40 + n * 34
    o.append(f'<path d="M{cx:.1f} {cy:.1f} L{lx - 6:.1f} {ly - 5:.1f}" stroke="{GREY}" stroke-width="1"/>')
    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="{INK}"/>')
    o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="15" fill="{INK}"><tspan font-weight="bold" letter-spacing="1.2">{LAYERS[i]}</tspan>  {s}</text>')
# the seed and the notes
sx, sy = X(squares[0][0]), Y(squares[0][1])
o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5" fill="{INK}"/>')
nx = X(x1) + 40
notes = ["0, 1, 1, 2, 3, 5, 8, 13, 21, 34 …", "each layer = the two before it, kept", "",
         "34 / 21 = 1.619…", "ratios → φ = 1.6180…,", "always approaching, never arriving", "",
         "cut the newest square off a golden", "rectangle: what is left has the same", "shape, and always a remainder"]
for k, t in enumerate(notes):
    o.append(f'<text x="{nx:.1f}" y="{M + 210 + k * 22}" font-size="15" fill="{INK}" font-style="{"italic" if k > 2 else "normal"}">{t}</text>')
o.append("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
