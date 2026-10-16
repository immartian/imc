#!/usr/bin/env python3
"""Generate the Recursive Emergence continuum diagrams for isaacmao.com.

Usage: python3 tools/make_continuum.py

Reads data/continuum.yaml and writes, relative to the site root:
  static/images/re-continuum.svg          the map on the home page
  static/images/continuum/map.svg         the same map with every ring linked to its
                                          layer card (inlined on /continuum/)
  static/images/continuum/mini-<id>.svg   one small diagram per layer
  static/images/continuum/ladder.svg      one step of reflect / residue / extend

Label widths are measured with Liberation Sans, which shares Arial's metrics, so a
label that would overflow its ring stops the script instead of shipping.
"""
import math
import random
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LAYERS = yaml.safe_load((ROOT / "data" / "continuum.yaml").read_text())["layers"]
INDEX = {layer["id"]: i for i, layer in enumerate(LAYERS)}
N = len(LAYERS)

INK, GREY, PAPER = "#111", "#999", "#fff"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
NAME_PX, LAYER_PX, LAYER_LS = 18, 15, 1.5

# ---- geometry of the map (viewBox units, y pointing down) ----
SIZE, C = 1000, 500
R0, STEP, LABEL_OFF = 108, 37, 22              # first ring, ring spacing, label baseline inside its ring
RADII = [R0 + STEP * i for i in range(N)]
EDGE = RADII[-1] + 30                          # dashed edge: the residue of the whole map
DOOR = [140 - i * (100 / (N - 1)) for i in range(N)]   # each ring's gap, 140deg .. 40deg
EDGE_DOOR = 30
REFLECT = [(RADII[INDEX["culture"]], 168), (30, 176)]   # Gödel's mathematics back toward the start, stopping short
# Below life, RE says layers find their doors by search; residues begin with the first
# carrier that can describe itself, the gene (appendix M, "below self-representing depth").
FIRST_RESIDUE = INDEX["life"]
KEEP_CLEAR = [(0, 0, 262, 110), (700, 0, 1000, 80), (878, 712, 1000, 768)]   # no haze under text

# ---- text metrics ----
try:
    from PIL import ImageFont
    _FONTS = {bold: ImageFont.truetype(
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{'Bold' if bold else 'Regular'}.ttf", 100)
        for bold in (False, True)}
except (ImportError, OSError):
    _FONTS = None
    print("warning: Liberation Sans not found; label widths are not checked", file=sys.stderr)


def text_w(s, px, bold=False, ls=0.0):
    return _FONTS[bold].getlength(s) * px / 100 + ls * len(s) if _FONTS else 0.0


def check_labels():
    """Each ring label must sit well inside its upper half, clear of the threads near 180 and 360 deg."""
    bad = []
    for i, layer in enumerate(LAYERS):
        width = text_w(layer["ring"], LAYER_PX, True, LAYER_LS) + 8 + text_w(layer["who"], NAME_PX)
        if layer.get("note"):
            width += 8 + text_w(layer["note"], NAME_PX - 2)
        limit = 0.85 * math.pi * (RADII[i] - LABEL_OFF)
        if width > limit:
            bad.append(f"{layer['ring']}: label {width:.0f} > {limit:.0f}")
    if bad:
        sys.exit("labels do not fit:\n  " + "\n  ".join(bad))


# ---- geometry helpers ----
def pt(r, deg, cx=C, cy=None):
    a = math.radians(deg)
    return cx + r * math.cos(a), (cx if cy is None else cy) + r * math.sin(a)


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def arc_with_gap(r, door_deg, gap, cx=C, cy=None):
    """A ring drawn the long way round, leaving a gap `gap` units wide centred on door_deg."""
    half = math.degrees(gap / 2 / r)
    x0, y0 = pt(r, door_deg + half, cx, cy)
    x1, y1 = pt(r, door_deg - half + 360, cx, cy)
    return f"M{f(x0)} {f(y0)} A{f(r)} {f(r)} 0 1 1 {f(x1)} {f(y1)}"


def upper_half(r):
    """Upper half-circle, left to right, so text along it reads upright."""
    (x0, y0), (x1, y1) = pt(r, 180), pt(r, 360)
    return f"M{f(x0)} {f(y0)} A{f(r)} {f(r)} 0 0 1 {f(x1)} {f(y1)}"


def full_circle(r):
    (x0, y0), (x1, y1) = pt(r, 0), pt(r, 180)
    return f"M{f(x0)} {f(y0)} A{f(r)} {f(r)} 0 1 1 {f(x1)} {f(y1)} A{f(r)} {f(r)} 0 1 1 {f(x0)} {f(y0)}"


def smooth(points):
    """Catmull-Rom spline through the points, as cubic Beziers."""
    d = f"M{f(points[0][0])} {f(points[0][1])}"
    for k in range(len(points) - 1):
        p0 = points[k - 1] if k else points[k]
        p1, p2 = points[k], points[k + 1]
        p3 = points[k + 2] if k + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def thread_points():
    pts = [(C, C)] + [pt(RADII[i], DOOR[i]) for i in range(N)]
    return pts + [pt(EDGE, EDGE_DOOR), pt(EDGE + 46, EDGE_DOOR - 6)]


def reflection_points(shift_y=0.0, steps=8):
    (r0, a0), (r1, a1) = REFLECT
    pts = []
    for s in range(steps + 1):
        t = s / steps
        x, y = pt(r0 + (r1 - r0) * t ** 0.9, a0 + (a1 - a0) * t)
        pts.append((x, y + shift_y))
    return pts


def markers(p, small=False):
    size = 5 if small else 6
    return ('<defs>'
            f'<marker id="{p}arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto">'
            f'<path d="M0 1 L9 5 L0 9 z" fill="{INK}"/></marker>'
            f'<marker id="{p}chevron" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{size + 1}" markerHeight="{size + 1}" orient="auto">'
            f'<path d="M1 1 L8 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/></marker>'
            '</defs>')


# ---- the map ----
def map_svg(linked):
    """The continuum map. linked=True wraps rings, edge and threads in links to the explainer's sections."""
    p = "cm-" if linked else ""
    o = []
    w = o.append

    def link(href, label):
        if linked:
            w(f'<a href="{href}" class="cm-link" aria-label="{label}"><title>{label}</title>')

    def unlink():
        if linked:
            w("</a>")

    root = 'class="continuum-map-svg"' if linked else 'role="img"'
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" font-family="{SANS}" {root} '
      f'aria-labelledby="{p}t {p}d">')
    w(f'<title id="{p}t">A continuum of Recursive Emergence</title>')
    w(f'<desc id="{p}d">Nine concentric rings, one per layer from cosmos to the synthetic layer, each labelled '
      'with thinkers; the synthetic ring is marked not yet. Every ring has a gap, a door to the next. The doors of '
      'the cosmos, matter and chemistry rings are found by search; from life outward each door is a residue, '
      'something the layer can state about itself but not settle from inside. A solid thread of recursion starts '
      'at a central dot and extends outward through every door, past a dashed edge into an open haze: whatever '
      'comes next. A dashed thread of reflection runs back inward from the cultural layer, labelled Gödel to '
      'Einstein, 1949, and stops just short of the centre.</desc>')
    w(f'<rect width="{SIZE}" height="{SIZE}" fill="{PAPER}"/>')
    w(markers(p))

    # haze beyond the edge: the unknown
    rnd = random.Random(7)
    dots = []
    for _ in range(640):
        r = EDGE + 24 + rnd.random() ** 1.6 * 36
        x, y = pt(r, rnd.uniform(0, 360))
        size, op = rnd.uniform(0.7, 1.6), rnd.uniform(0.10, 0.40)
        if not any(b[0] <= x <= b[2] and b[1] <= y <= b[3] for b in KEEP_CLEAR):
            dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{size:.2f}" fill="{INK}" opacity="{op:.2f}"/>')
    w('<g aria-hidden="true">' + "".join(dots) + "</g>")

    # rings: each with its gap and its label along the upper half
    for i, layer in enumerate(LAYERS):
        r = RADII[i]
        link(f"#layer-{layer['id']}", f"{layer['ring'].title()}: read about this layer")
        if linked:
            w(f'<path class="cm-hit" d="{full_circle(r)}" fill="none" stroke="transparent" stroke-width="34" pointer-events="stroke"/>')
        w(f'<path class="cm-ring" d="{arc_with_gap(r, DOOR[i], 40)}" fill="none" stroke="{INK}" '
          f'stroke-width="{2 if i % 2 == 0 else 1.4}" stroke-linecap="round"/>')
        w(f'<path id="{p}l{i}" d="{upper_half(r - LABEL_OFF)}" fill="none"/>')
        w(f'<text class="cm-label" fill="{INK}"><textPath href="#{p}l{i}" startOffset="50%" text-anchor="middle">'
          f'<tspan font-weight="bold" letter-spacing="{LAYER_LS}" font-size="{LAYER_PX}">{layer["ring"]}</tspan>'
          f'<tspan dx="8" font-size="{NAME_PX}">{layer["who"]}</tspan>'
          + (f'<tspan dx="8" font-size="{NAME_PX - 2}" font-style="italic">{layer["note"]}</tspan>' if layer.get("note") else "")
          + '</textPath></text>')
        unlink()

    # the dashed edge: the residue of the whole map, and the open future beyond it
    link("#the-edge", "The edge: the residue, and whatever comes next")
    w(f'<path class="cm-edge" d="{arc_with_gap(EDGE, EDGE_DOOR, 40)}" fill="none" stroke="{INK}" '
      'stroke-width="1.6" stroke-dasharray="4 7" stroke-linecap="round"/>')
    w(f'<path id="{p}le" d="{upper_half(EDGE + 10)}" fill="none"/>')
    w(f'<text fill="{INK}"><textPath href="#{p}le" startOffset="50%" text-anchor="middle">'
      f'<tspan font-weight="bold" letter-spacing="{LAYER_LS}" font-size="{LAYER_PX}">THE RESIDUE</tspan>'
      f'<tspan dx="8" font-size="{NAME_PX}" font-style="italic">what no layer can settle from inside</tspan></textPath></text>')
    w(f'<text font-size="{NAME_PX}" fill="{INK}" font-style="italic" text-anchor="end">'
      f'<tspan x="{SIZE - 14}" y="736">? whatever</tspan><tspan x="{SIZE - 14}" y="758">comes next</tspan></text>')
    unlink()

    # the two motions: extension outward through the gaps, reflection back inward
    link("#two-motions", "Two motions: extension outward, reflection inward")
    pts = thread_points()
    w(f'<path class="cm-thread" d="{smooth(pts)}" fill="none" stroke="{INK}" stroke-width="3.2" '
      f'stroke-linecap="round" marker-end="url(#{p}arrow)"/>')
    for k, (x, y) in enumerate(pts[1:-1]):   # the ring doors, then the edge's own
        searched = k < FIRST_RESIDUE
        w(f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="{INK if searched else PAPER}" stroke="{INK}" stroke-width="2"/>')
    refl = reflection_points()
    w(f'<path class="cm-reflection" d="{smooth(refl)}" fill="none" stroke="{INK}" stroke-width="2.2" '
      f'stroke-dasharray="7 6" stroke-linecap="round" marker-end="url(#{p}chevron)"/>')
    w(f'<circle cx="{f(refl[0][0])}" cy="{f(refl[0][1])}" r="4.5" fill="{INK}"/>')
    w(f'<path id="{p}lr" d="{smooth(reflection_points(-11))}" fill="none"/>')
    # drawn twice, a paper-coloured halo under the ink, so ring lines break around the words
    # (paint-order on textPath is not honoured everywhere)
    for paint in (f'fill="{PAPER}" stroke="{PAPER}" stroke-width="9" stroke-linejoin="round" aria-hidden="true"',
                  f'fill="{INK}"'):
        w(f'<text {paint} font-size="17"><textPath href="#{p}lr" startOffset="5%">'
          'Gödel → Einstein, 1949</textPath></text>')
    unlink()

    # the origin: a zero waiting to be a one
    w(f'<circle cx="{C}" cy="{C}" r="7" fill="{INK}"/>')
    w(f'<text x="{C}" y="{C - 22}" font-size="22" text-anchor="middle" fill="{INK}">0 → 1</text>')

    # legend: rings and doors top left, the two motions top right
    w(f'<g font-size="{NAME_PX - 1}" fill="{INK}">'
      f'<line x1="18" y1="30" x2="48" y2="30" stroke="{INK}" stroke-width="2"/><text x="58" y="36">ring: a layer</text>'
      f'<circle cx="33" cy="60" r="4" fill="{INK}" stroke="{INK}" stroke-width="2"/><text x="58" y="66">door found by search</text>'
      f'<circle cx="33" cy="90" r="4" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><text x="58" y="96">door that is a residue</text>'
      '</g>')
    w(f'<g font-size="{NAME_PX - 1}" fill="{INK}" text-anchor="end">'
      f'<text x="{SIZE - 58}" y="36">thread: extends outward</text>'
      f'<line x1="{SIZE - 48}" y1="30" x2="{SIZE - 18}" y2="30" stroke="{INK}" stroke-width="3.2"/>'
      f'<text x="{SIZE - 58}" y="66">dashed: reflects inward</text>'
      f'<line x1="{SIZE - 48}" y1="60" x2="{SIZE - 18}" y2="60" stroke="{INK}" stroke-width="2.2" stroke-dasharray="7 6"/>'
      '</g>')
    w("</svg>")
    return "\n".join(o)


# ---- one small map per layer ----
def mini_svg(i):
    """One layer highlighted, the thread leaving through its gap, and the reflection that reaches it."""
    S, c, k = 240, 120, 0.235
    radii = [r * k for r in RADII]
    layer = LAYERS[i]
    reader = INDEX[layer["read_by"]]
    o = []
    w = o.append
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" role="img" '
      f'aria-label="The {layer["ring"].lower()} ring highlighted on the continuum">')
    w(markers("", small=True))
    for j, r in enumerate(radii):
        if j != i:
            stroke, width = ("#444", 2.4) if j == reader else (GREY, 1.3)
            w(f'<path d="{arc_with_gap(r, DOOR[j], 7, c)}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"/>')
    r = radii[i]
    w(f'<path d="{arc_with_gap(r, DOOR[i], 9, c)}" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
    (x0, y0), (x1, y1) = pt(r - 8, DOOR[i], c), pt(r + 11, DOOR[i], c)
    w(f'<path d="M{f(x0)} {f(y0)} L{f(x1)} {f(y1)}" stroke="{INK}" stroke-width="2.4" marker-end="url(#arrow)"/>')
    if reader == i:                       # a layer reading itself: a loop that leaves and returns
        a, m, b = pt(r, 206, c), pt(r + 34, 180, c), pt(r + 1, 154, c)
        w(f'<circle cx="{f(a[0])}" cy="{f(a[1])}" r="3" fill="{INK}"/>')
        w(f'<path d="M{f(a[0])} {f(a[1])} Q{f(m[0])} {f(m[1])} {f(b[0])} {f(b[1])}" fill="none" stroke="{INK}" '
          'stroke-width="2.2" stroke-dasharray="4 3" marker-end="url(#chevron)"/>')
    else:                                 # an outer layer spiralling back in to this one, on the left
        r_from, r_to = radii[reader], r + 2
        spiral = [pt(r_from + (r_to - r_from) * s / 10, 204 - 44 * s / 10, c) for s in range(11)]
        w(f'<circle cx="{f(spiral[0][0])}" cy="{f(spiral[0][1])}" r="3" fill="{INK}"/>')
        w(f'<path d="{smooth(spiral)}" fill="none" stroke="{INK}" stroke-width="2.2" '
          'stroke-dasharray="4 3" marker-end="url(#chevron)"/>')
    w(f'<circle cx="{c}" cy="{c}" r="3" fill="{INK}"/>')
    w("</svg>")
    return "\n".join(o)


# ---- one step of the ladder ----
def sub(base, idx, size, after=None):
    """base with a subscript; `after` continues on the normal baseline."""
    s = f'{base}<tspan dy="6" font-size="{size * 0.68:.0f}">{idx}</tspan>'
    return s + (f'<tspan dy="-6">{after}</tspan>' if after is not None else "")


def ladder_svg():
    """A system reflects on itself, meets a sentence it cannot settle, and extends by adding it."""
    W_, H_, cy = 1000, 370, 165
    systems = [(150, 64, "0"), (450, 84, "1"), (790, 104, "2")]
    o = []
    w = o.append
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}" font-family="{SANS}" role="img" '
      'aria-labelledby="lt ld">')
    w('<title id="lt">One step of the ladder</title>')
    w('<desc id="ld">Three circles of growing size, T0, T1 and T2. Inside each, a dashed loop: the system '
      'describes itself. In each circle\'s edge, a gap marked G: a true sentence it can state but cannot prove. '
      'A solid arrow leaves through the gap to the next, larger circle: T1 is T0 plus G0, T2 is T1 plus G1, '
      'and the ladder continues.</desc>')
    w(f'<rect width="{W_}" height="{H_}" fill="{PAPER}"/>')
    w(markers("l"))
    for n, (cx, r, idx) in enumerate(systems):
        w(f'<path d="{arc_with_gap(r, 0, 26, cx, cy)}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
        lr = r * 0.52                     # reflection: a dashed loop round the system's own name
        (x0, y0), (x1, y1) = pt(lr, -40, cx, cy), pt(lr, 230, cx, cy)
        w(f'<path d="M{f(x0)} {f(y0)} A{f(lr)} {f(lr)} 0 1 1 {f(x1)} {f(y1)}" fill="none" stroke="{INK}" '
          'stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#lchevron)"/>')
        w(f'<text x="{cx}" y="{cy + 11}" font-size="32" text-anchor="middle" fill="{INK}">{sub("T", idx, 32)}</text>')
        gx = cx + r                       # the residue sits in the gap
        w(f'<circle cx="{f(gx)}" cy="{cy}" r="5" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
        w(f'<text x="{f(gx + 6)}" y="{cy - 14}" font-size="25" fill="{INK}">{sub("G", idx, 25)}</text>')
        if n + 1 < len(systems):          # extension: out through the gap to the next system
            nx, nr = systems[n + 1][0], systems[n + 1][1]
            w(f'<path d="M{f(gx + 8)} {cy} L{f(nx - nr - 10)} {cy}" stroke="{INK}" stroke-width="3" marker-end="url(#larrow)"/>')
    last_cx, last_r = systems[-1][0], systems[-1][1]
    w(f'<path d="M{last_cx + last_r + 10} {cy} L{W_ - 16} {cy}" stroke="{INK}" stroke-width="3" '
      'stroke-dasharray="1 8" stroke-linecap="round"/>')
    captions = [
        (150, ["reflect: the system", "describes itself"]),
        (450, [sub("T", "1", 23, " = ") + sub("T", "0", 23, " + ") + sub("G", "0", 23), "extend: a larger system"]),
        (790, [sub("T", "2", 23, " = ") + sub("T", "1", 23, " + ") + sub("G", "1", 23), "with a residue of its own"]),
    ]
    for cx, lines in captions:
        for k, line in enumerate(lines):
            w(f'<text x="{cx}" y="{300 + k * 29}" font-size="23" text-anchor="middle" fill="{INK}">{line}</text>')
    w(f'<text x="330" y="40" font-size="22" font-style="italic" text-anchor="middle" fill="{INK}">'
      f'{sub("G", "0", 22, ": true, and statable in ")}{sub("T", "0", 22, ", but not provable there")}</text>')
    w(f'<path d="M250 52 Q226 76 {150 + 64 + 6} {cy - 16}" fill="none" stroke="{INK}" stroke-width="1.4" '
      'marker-end="url(#larrow)"/>')
    w("</svg>")
    return "\n".join(o)


def main():
    check_labels()
    out = ROOT / "static" / "images"
    (out / "continuum").mkdir(parents=True, exist_ok=True)
    (out / "re-continuum.svg").write_text(map_svg(linked=False) + "\n")
    (out / "continuum" / "map.svg").write_text(map_svg(linked=True) + "\n")
    for i, layer in enumerate(LAYERS):
        (out / "continuum" / f"mini-{layer['id']}.svg").write_text(mini_svg(i) + "\n")
    (out / "continuum" / "ladder.svg").write_text(ladder_svg() + "\n")
    print(f"wrote the map, the linked map, {N} mini maps and the ladder into {out.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
