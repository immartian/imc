"""Usage: python3 tools/make_continuum.py static/images/re-continuum.svg

Generate the Recursive Emergence continuum diagram (rings, gaps, thread)."""
import math, random, sys

C = 450                      # centre
RINGS = [                    # inner -> outer: (layer, thinkers)
    ("COSMOS", "Penrose · Smolin · Gödel"),
    ("MATTER", "Einstein · Rovelli"),
    ("CHEMISTRY", "Empedocles · Prigogine"),
    ("LIFE", "Darwin · Schrödinger · von Neumann"),
    ("NEURONS", "Ramón y Cajal · Hebb"),
    ("MIND", "Descartes · James · Zhuangzi · Dennett"),
    ("CULTURE", "Teilhard · Vygotsky · Dewey · Sharism"),
    ("TECHNOLOGY", "Turing · von Neumann · Bush · Engelbart"),
    ("SYNTHETIC", "Gödel · Turing · Feferman · Nāgārjuna · Rovelli"),
]
R0, STEP = 80, 36
EDGE = R0 + STEP * len(RINGS) + 4          # dashed edge: the residue
INK = "#222"
FONT = "Georgia, 'Times New Roman', serif"

def pt(r, deg):
    a = math.radians(deg)
    return C + r * math.cos(a), C + r * math.sin(a)

out = []
w = out.append
w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 900" width="900" height="900" '
  f'font-family="{FONT}" role="img" aria-labelledby="t d">')
w('<title id="t">A continuum of Recursive Emergence</title>')
w('<desc id="d">Nine concentric rings, one per layer from cosmos to the synthetic layer, each labelled with '
  'thinkers. Every ring has a gap, the residue it cannot close from inside; a thread of recursion starts at a '
  'central dot and passes out through each gap, past a dashed edge into an open haze marked: whatever comes next.</desc>')
w('<rect width="900" height="900" fill="#fff"/>')
w('<defs><marker id="arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" '
  f'orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="{INK}"/></marker></defs>')

# haze beyond the edge: the unknown
random.seed(7)
for _ in range(520):
    r = EDGE + 8 + random.random() ** 1.6 * 44
    x, y = pt(r, random.uniform(0, 360))
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(0.6, 1.5):.2f}" fill="{INK}" '
      f'opacity="{random.uniform(0.12, 0.45):.2f}"/>')

# door (gap) angles: sweep across the bottom, left to right, as the thread climbs outward
n = len(RINGS)
door = [140 - i * (100 / (n - 1)) for i in range(n)]   # 140deg ... 40deg
edge_door = 30

# rings with a gap, and their labels on the upper half
for i, (name, who) in enumerate(RINGS):
    r = R0 + STEP * i
    half = math.degrees(17 / r)                          # ~34px door
    a0, a1 = door[i] + half, door[i] - half + 360       # draw the long way round
    x0, y0 = pt(r, a0); x1, y1 = pt(r, a1)
    w(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{INK}" '
      f'stroke-width="{1.6 if i % 2 == 0 else 1.1}" stroke-linecap="round"/>')
    # label path: upper half, left to right, slightly inside the ring
    lr = r - 13
    lx0, ly0 = pt(lr, 180); lx1, ly1 = pt(lr, 360)
    w(f'<path id="l{i}" d="M{lx0:.1f} {ly0:.1f} A{lr} {lr} 0 0 1 {lx1:.1f} {ly1:.1f}" fill="none"/>')
    w(f'<text font-size="12.5" fill="{INK}"><textPath href="#l{i}" startOffset="50%" text-anchor="middle">'
      f'<tspan font-weight="bold" letter-spacing="1.2" font-size="11">{name}</tspan>'
      f'<tspan font-style="italic">  {who}</tspan></textPath></text>')

# the dashed edge: the residue no layer can settle from inside
hx = math.degrees(17 / EDGE)
ex0, ey0 = pt(EDGE, edge_door + hx); ex1, ey1 = pt(EDGE, edge_door - hx + 360)
w(f'<path d="M{ex0:.1f} {ey0:.1f} A{EDGE} {EDGE} 0 1 1 {ex1:.1f} {ey1:.1f}" fill="none" stroke="{INK}" '
  f'stroke-width="1.2" stroke-dasharray="3 6" stroke-linecap="round"/>')
lr = EDGE + 14
lx0, ly0 = pt(lr, 180); lx1, ly1 = pt(lr, 360)
w(f'<path id="le" d="M{lx0:.1f} {ly0:.1f} A{lr} {lr} 0 0 1 {lx1:.1f} {ly1:.1f}" fill="none"/>')
w(f'<text font-size="13" fill="{INK}"><textPath href="#le" startOffset="50%" text-anchor="middle">'
  '<tspan font-weight="bold" letter-spacing="1.5" font-size="11.5">THE RESIDUE</tspan>'
  '<tspan font-style="italic">  what no layer can settle from inside</tspan></textPath></text>')

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
w(f'<path d="{catmull(pts)}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" '
  'marker-end="url(#arrow)"/>')
for (x, y) in pts[1:-1]:
    w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')

# the origin: a zero waiting to be a one
w(f'<circle cx="{C}" cy="{C}" r="6" fill="{INK}"/>')
w(f'<text x="{C}" y="{C - 18}" font-size="15" text-anchor="middle" fill="{INK}" font-style="italic">0 → 1</text>')

# the open future
w(f'<text font-size="14" fill="{INK}" font-style="italic" text-anchor="end">'
  '<tspan x="884" y="688">? whatever</tspan><tspan x="884" y="706">comes next</tspan></text>')

# legend
w(f'<g font-size="12.5" fill="{INK}">'
  f'<line x1="22" y1="30" x2="50" y2="30" stroke="{INK}" stroke-width="1.6"/><text x="58" y="34">ring: a layer</text>'
  f'<circle cx="36" cy="54" r="3.2" fill="#fff" stroke="{INK}" stroke-width="1.6"/><text x="58" y="58">gap: its residue, a door</text>'
  f'<line x1="22" y1="78" x2="50" y2="78" stroke="{INK}" stroke-width="2.6"/><text x="58" y="82">thread: recursion</text>'
  '</g>')
w('</svg>')
open(sys.argv[1], "w").write("\n".join(out))
