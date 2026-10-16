"""Usage: python3 tools/make_continuum.py static/images/re-continuum.svg

Generate the Recursive Emergence continuum diagram (rings, gaps, thread)."""
import math, random, sys

SIZE, C = 1000, 500          # viewBox and centre
RINGS = [                    # inner -> outer: (layer, a few thinkers; the full lineage is in the page text)
    ("COSMOS", "Smolin · Gödel"),
    ("MATTER", "Einstein · Rovelli"),
    ("CHEMISTRY", "Empedocles · Prigogine"),
    ("LIFE", "Darwin · Schrödinger"),
    ("NEURONS", "Cajal · Hebb"),
    ("MIND", "Descartes · Zhuangzi · Dennett"),
    ("CULTURE", "Teilhard · Dewey · Sharism"),
    ("TECHNOLOGY", "Turing · von Neumann · Engelbart"),
    ("SYNTHETIC", "Gödel · Feferman · Nāgārjuna"),
]
R0, STEP = 100, 38
EDGE = R0 + STEP * (len(RINGS) - 1) + 30     # dashed edge: the residue
INK = "#111"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
NAME_PX, LAYER_PX = 18, 15

def pt(r, deg):
    a = math.radians(deg)
    return C + r * math.cos(a), C + r * math.sin(a)

out = []
w = out.append
w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}" '
  f'font-family="{SANS}" role="img" aria-labelledby="t d">')
w('<title id="t">A continuum of Recursive Emergence</title>')
w('<desc id="d">Nine concentric rings, one per layer from cosmos to the synthetic layer, each labelled with '
  'thinkers. Every ring has a gap, the residue it cannot close from inside; a thread of recursion starts at a '
  'central dot and passes out through each gap, past a dashed edge into an open haze marked: whatever comes next.</desc>')
w(f'<rect width="{SIZE}" height="{SIZE}" fill="#fff"/>')
w('<defs><marker id="arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" '
  f'orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="{INK}"/></marker></defs>')

# haze beyond the edge: the unknown
random.seed(7)
for _ in range(600):
    r = EDGE + 24 + random.random() ** 1.6 * 36
    x, y = pt(r, random.uniform(0, 360))
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(0.7, 1.6):.2f}" fill="{INK}" '
      f'opacity="{random.uniform(0.10, 0.40):.2f}"/>')

# door (gap) angles: sweep across the bottom, left to right, as the thread climbs outward
n = len(RINGS)
door = [140 - i * (100 / (n - 1)) for i in range(n)]   # 140deg ... 40deg
edge_door = 30

def label_path(pid, r):
    """Upper half-circle, left to right, so text along it reads upright."""
    x0, y0 = pt(r, 180); x1, y1 = pt(r, 360)
    w(f'<path id="{pid}" d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" fill="none"/>')

for i, (name, who) in enumerate(RINGS):
    r = R0 + STEP * i
    half = math.degrees(20 / r)                          # ~40px door
    a0, a1 = door[i] + half, door[i] - half + 360
    x0, y0 = pt(r, a0); x1, y1 = pt(r, a1)
    w(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{INK}" '
      f'stroke-width="{2 if i % 2 == 0 else 1.4}" stroke-linecap="round"/>')
    label_path(f"l{i}", r - 24)                          # baseline mid-band, glyphs clear of the ring
    w(f'<text fill="{INK}"><textPath href="#l{i}" startOffset="50%" text-anchor="middle">'
      f'<tspan font-weight="bold" letter-spacing="1.5" font-size="{LAYER_PX}">{name}</tspan>'
      f'<tspan font-size="{NAME_PX}">  {who}</tspan></textPath></text>')

# the dashed edge: the residue no layer can settle from inside
hx = math.degrees(20 / EDGE)
ex0, ey0 = pt(EDGE, edge_door + hx); ex1, ey1 = pt(EDGE, edge_door - hx + 360)
w(f'<path d="M{ex0:.1f} {ey0:.1f} A{EDGE} {EDGE} 0 1 1 {ex1:.1f} {ey1:.1f}" fill="none" stroke="{INK}" '
  f'stroke-width="1.6" stroke-dasharray="4 7" stroke-linecap="round"/>')
label_path("le", EDGE + 10)
w(f'<text fill="{INK}"><textPath href="#le" startOffset="50%" text-anchor="middle">'
  f'<tspan font-weight="bold" letter-spacing="1.5" font-size="{LAYER_PX}">THE RESIDUE</tspan>'
  f'<tspan font-size="{NAME_PX}" font-style="italic">  what no layer can settle from inside</tspan></textPath></text>')

# the thread of recursion: centre -> each door -> through the edge -> into the unknown
pts = [(C, C)] + [pt(R0 + STEP * i, door[i]) for i in range(n)] + [pt(EDGE, edge_door), pt(EDGE + 46, edge_door - 6)]
def catmull(p):
    d = f'M{p[0][0]:.1f} {p[0][1]:.1f}'
    for k in range(len(p) - 1):
        p0 = p[k - 1] if k else p[k]; p1 = p[k]; p2 = p[k + 1]; p3 = p[k + 2] if k + 2 < len(p) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d
w(f'<path d="{catmull(pts)}" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" '
  'marker-end="url(#arrow)"/>')
for (x, y) in pts[1:-1]:
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff" stroke="{INK}" stroke-width="2"/>')

# the origin: a zero waiting to be a one
w(f'<circle cx="{C}" cy="{C}" r="7" fill="{INK}"/>')
w(f'<text x="{C}" y="{C - 22}" font-size="22" text-anchor="middle" fill="{INK}">0 → 1</text>')

# the open future
w(f'<text font-size="{NAME_PX}" fill="{INK}" font-style="italic" text-anchor="end">'
  f'<tspan x="{SIZE - 14}" y="736">? whatever</tspan><tspan x="{SIZE - 14}" y="758">comes next</tspan></text>')

# legend
w(f'<g font-size="{NAME_PX - 1}" fill="{INK}">'
  f'<line x1="18" y1="30" x2="48" y2="30" stroke="{INK}" stroke-width="2"/><text x="58" y="36">ring = layer</text>'
  f'<circle cx="33" cy="60" r="4" fill="#fff" stroke="{INK}" stroke-width="2"/><text x="58" y="66">gap = residue, a door</text>'
  f'<line x1="18" y1="90" x2="48" y2="90" stroke="{INK}" stroke-width="3.2"/><text x="58" y="96">thread = recursion</text>'
  '</g>')
w('</svg>')
open(sys.argv[1], "w").write("\n".join(out))
