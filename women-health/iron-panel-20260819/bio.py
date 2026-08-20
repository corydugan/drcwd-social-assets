#!/usr/bin/env python3
"""Brand-native biological primitives. The BioRender layer for this pipeline.

Every shape here is drawn in PIL from the ink palette, so a schematic in an
episode is made of the same lines and the same grape as the charts. A figure
pasted in from a general-purpose biology tool would carry its own palette, its
own stroke weight and its own idea of a cell, and would read as an import.

THE FLEET is the series' recurring picture and it runs across episodes 02 to 05.
It is one diagram, redrawn each time with a different part lit:

    02  serum iron    the seats that are TAKEN
    03  TSAT          taken as a share of all seats
    04  TIBC          ALL the seats, taken and empty
    05  transferrin   the CARRIERS themselves, and the liver that builds them

TWO seats per carrier is not decoration. Transferrin binds up to two atoms of
ferric iron per molecule, which is the definition Cory supplied, so the picture
counts the way the biochemistry counts.

FLEET and FILL are module-level on purpose. Four episodes drawing the same fleet
from four private copies of the layout is the same drift the reels' README warns
about, one folder further along.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "reels-20260818"))
import math                                        # noqa: E402
import build as B                                   # noqa: E402

TRUCK_W, TRUCK_H = 170, 86
ROW_Y = (700, 900)
COL_X = (110, 340, 570, 800)

# the eight carriers, four to a row
FLEET = [(x, y) for y in ROW_Y for x in COL_X]
# how many of the two seats are taken on each. Five of sixteen, which is the
# ratio episode 03 then reads as a saturation. Change it here or the two
# episodes stop agreeing.
FILL = [1, 0, 1, 0, 2, 0, 1, 0]


def road(d, y, p, alpha=1.0):
    if p <= 0 or alpha <= 0.01:
        return
    x0, x1 = COL_X[0] - 24, COL_X[-1] + TRUCK_W + 24
    d.line([(x0, y), (x0 + (x1 - x0) * min(p, 1.0), y)],
           fill=B.mix(B.RULE, alpha), width=4)


def carrier(d, x, y, filled=0, draw_p=1.0, alpha=1.0,
            seat_a=0.0, load_a=0.0, body_col=None, seat_col=None):
    """One transferrin. draw_p runs the body on, seat_a fades the empty seats
    in, load_a fills the taken ones."""
    if alpha <= 0.01:
        return
    body_col = body_col or B.FG_SUBTLE
    seat_col = seat_col or B.ACCENT
    w, h = TRUCK_W, TRUCK_H

    if draw_p > 0:
        pts = [(x, y + h), (x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        path = B.partial(pts, draw_p)
        if len(path) > 1:
            d.line(path, fill=B.mix(body_col, alpha), width=4)
    if draw_p > 0.92:
        # the cab, so it reads as something that travels rather than a box
        d.line([(x + w - 40, y), (x + w - 40, y + h)], fill=B.mix(body_col, alpha * 0.8), width=3)
        # wheels in RULE were invisible: RULE is ink.900 and sits a shade off the
        # field, so the carriers read as plain boxes. FG_SUBTLE carries them.
        for wx in (x + 40, x + w - 62):
            d.ellipse([wx - 12, y + h - 4, wx + 12, y + h + 20],
                      fill=B.mix(B.FG_SUBTLE, alpha * 0.75))

    cy = y + h // 2
    for i, sx in enumerate((x + 44, x + 96)):
        if seat_a > 0.01:
            d.ellipse([sx - 20, cy - 20, sx + 20, cy + 20],
                      outline=B.mix(body_col, alpha * seat_a), width=3)
        if i < filled and load_a > 0.01:
            r = 16
            d.ellipse([sx - r, cy - r, sx + r, cy + r],
                      fill=seat_col + (int(235 * alpha * load_a),))


def fleet(d, draw_p=1.0, alpha=1.0, seat_a=0.0, load_a=0.0, stagger=0.0,
          f=0, only=None, dim=1.0, seat_col=None):
    """The whole fleet. stagger delays each carrier a little so it builds.

    only: an iterable of indices held at full alpha. dim ramps the rest down,
    0 for no dimming and 1 for fully dimmed, so an episode can bring them back
    rather than end on a half-faded picture."""
    for i, (x, y) in enumerate(FLEET):
        p = draw_p
        if stagger > 0:
            p = max(0.0, min(1.0, (draw_p * len(FLEET) - i * stagger) / max(1e-6, 1.0)))
        a = alpha if (only is None or i in only) else alpha * (1 - 0.74 * dim)
        carrier(d, x, y, filled=FILL[i], draw_p=p, alpha=a,
                seat_a=seat_a, load_a=load_a, seat_col=seat_col)
    for y in ROW_Y:
        road(d, y + TRUCK_H + 21, draw_p, alpha)


def red_cell(d, cx, cy, r, alpha=1.0, pale=0.0, ring=None, draw_p=1.0, seed=0.5):
    """A red cell as the biconcave donut, drawn on an organic outline rather than
    a true circle. pale thins the fill, which is how a hypochromic cell is shown
    without reaching for a colour that is not in the palette."""
    if alpha <= 0.01 or draw_p <= 0:
        return
    ring = ring or B.ACCENT
    pts = blob_points(cx, cy, r, seed=seed, wobble=0.09)
    if draw_p > 0.96:
        d.polygon(pts, fill=ring + (int((225 - 150 * pale) * alpha),))
        ipts = blob_points(cx, cy, r * 0.44, seed=seed + 1.1, wobble=0.14)
        d.polygon(ipts, fill=B.FIELD)
    else:
        path = B.partial(pts, draw_p)
        if len(path) > 1:
            d.line(path, fill=B.mix(B.FG_SUBTLE, alpha), width=4)


def hungry_cell(d, cx, cy, r, alpha=1.0, antennae=0, ant_a=1.0):
    """A cell with receptor antennae on it. Episode 07, sTfR."""
    if alpha <= 0.01:
        return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=B.mix(B.FG_SUBTLE, alpha), width=4)
    import math
    for k in range(antennae):
        ang = -math.pi / 2 + (k - (antennae - 1) / 2) * 0.42
        x0, y0 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x1, y1 = cx + (r + 34 * ant_a) * math.cos(ang), cy + (r + 34 * ant_a) * math.sin(ang)
        d.line([(x0, y0), (x1, y1)], fill=B.mix(B.ACCENT, alpha * ant_a), width=4)
        d.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=B.mix(B.ACCENT, alpha * ant_a))


def tickbar(d, y, n, filled, p=1.0, alpha=1.0, x0=110, x1=970, h=54):
    """Every seat in the fleet, laid out in a line: taken ones solid, empty ones
    outlined. Episode 03 reads the share that is taken. Episode 04 grows n while
    filled stays put, which is what a rising binding capacity looks like."""
    if p <= 0 or alpha <= 0.01 or n < 1:
        return
    gap = 8
    wseg = ((x1 - x0) - gap * (n - 1)) / n
    shown = n * min(p, 1.0)
    for i in range(n):
        if i >= shown:
            break
        a = alpha * min(1.0, shown - i)
        sx = x0 + i * (wseg + gap)
        d.rectangle([sx, y, sx + wseg, y + h], outline=B.mix(B.FG_SUBTLE, a * 0.85), width=3)
        if i < filled:
            d.rectangle([sx + 4, y + 4, sx + wseg - 4, y + h - 4],
                        fill=B.ACCENT + (int(235 * a),))


# ---------------------------------------------------------------- organic bodies
#
# Cory's call, 19 Aug: organs looser and more organic than the carriers. The
# carriers are machinery and stay ruled; a liver drawn with the same straight
# edges reads as a filing cabinet.
#
# The wobble is DETERMINISTIC, three fixed harmonics keyed off a seed, never
# random. A random outline would redraw differently on every render, so a reshoot
# of one episode would no longer match the frame beside it in the next.

def blob_points(cx, cy, r, seed=0.0, wobble=0.16, squash=1.0, n=150, tilt=0.0):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        k = 1 + wobble * (0.55 * math.sin(3*t + seed)
                          + 0.30 * math.sin(5*t + 1.7*seed)
                          + 0.18 * math.sin(7*t + 2.9*seed))
        x, y = r * k * math.cos(t), r * k * squash * math.sin(t)
        if tilt:
            c, s = math.cos(tilt), math.sin(tilt)
            x, y = x*c - y*s, x*s + y*c
        pts.append((cx + x, cy + y))
    return pts


def blob(d, cx, cy, r, seed=0.0, alpha=1.0, draw_p=1.0, wobble=0.16, squash=1.0,
         tilt=0.0, fill=None, fill_a=1.0, line=None, width=4):
    """One organic closed body, drawn on as a truncated outline like everything
    else in this series."""
    if alpha <= 0.01 or draw_p <= 0:
        return
    pts = blob_points(cx, cy, r, seed, wobble, squash, tilt=tilt)
    if fill is not None and draw_p > 0.96:
        d.polygon(pts, fill=tuple(fill[:3]) + (int(alpha * fill_a * 235),))
    path = B.partial(pts, draw_p)
    if len(path) > 1:
        d.line(path, fill=B.mix(line or B.FG_SUBTLE, alpha), width=width)


def liver(d, cx, cy, r, alpha=1.0, draw_p=1.0, label=None, label_a=0.0):
    """The liver: a big right lobe and a smaller left one, wedge-shaped rather
    than round. Transferrin and hepcidin are both made here, so it appears twice
    in the series and has to be recognisable both times.

    The first cut ran at r=132 with the small lobe hung off the side, and read as
    a mouse. It is bigger now, the lobes overlap at the same height, and a soft
    grape wash gives it body so it is not a wire outline in a frame full of
    wire outlines."""
    blob(d, cx + r*0.10, cy, r, seed=0.8, alpha=alpha, draw_p=draw_p,
         wobble=0.19, squash=0.58, tilt=-0.07,
         fill=B.EYEBROW, fill_a=0.16, width=5)
    blob(d, cx - r*0.80, cy + r*0.09, r*0.50, seed=2.6, alpha=alpha*0.95,
         draw_p=draw_p, wobble=0.20, squash=0.66, tilt=0.10,
         fill=B.EYEBROW, fill_a=0.16, width=4)
    if label and label_a > 0.01:
        d.text((cx, cy - r*0.58 - 62), label, font=B.SANS_B(32),
               fill=B.mix(B.EYEBROW, label_a), anchor="ma")


def gut(d, x0, x1, y, amp=34, alpha=1.0, draw_p=1.0, thick=64):
    """A stretch of gut as two loose parallel walls. The door in episode 09 is
    cut into it rather than drawn as a rectangle."""
    if alpha <= 0.01 or draw_p <= 0:
        return
    for off, ph in ((-thick/2, 0.0), (thick/2, 0.35)):
        pts = [(x, y + off + amp * math.sin((x - x0) / 92.0 + ph))
               for x in range(int(x0), int(x1) + 1, 4)]
        path = B.partial(pts, draw_p)
        if len(path) > 1:
            d.line(path, fill=B.mix(B.FG_SUBTLE, alpha), width=4, joint="curve")


def ring_socket(d, cx, cy, r, alpha=1.0, draw_p=1.0, metal=None, metal_a=0.0):
    """The protoporphyrin ring with one socket at its centre. Episode 10 puts
    iron in it, then runs out and puts zinc in instead."""
    if alpha <= 0.01:
        return
    blob(d, cx, cy, r, seed=1.4, alpha=alpha, draw_p=draw_p, wobble=0.10, width=7)
    if draw_p > 0.9:
        for k in range(4):
            t = math.pi/4 + k * math.pi/2
            d.ellipse([cx + r*0.62*math.cos(t) - 15, cy + r*0.62*math.sin(t) - 15,
                       cx + r*0.62*math.cos(t) + 15, cy + r*0.62*math.sin(t) + 15],
                      outline=B.mix(B.FG_SUBTLE, alpha), width=4)
    if metal is not None and metal_a > 0.01:
        rr = r * 0.34
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=metal + (int(235*alpha*metal_a),))


def cell(d, cx, cy, r, alpha=1.0, draw_p=1.0, antennae=0, ant_a=1.0, seed=0.4):
    """A cell with receptor antennae. Organic membrane, ruled receptors: the
    receptor is the machinery, the cell is the body.

    The membrane carries the same soft grape wash the liver does. Drawn as a bare
    outline it read as unfinished next to the filled red cells in episode 06."""
    if alpha <= 0.01:
        return
    blob(d, cx, cy, r, seed=seed, alpha=alpha, draw_p=draw_p, wobble=0.13,
         fill=B.EYEBROW, fill_a=0.13, width=4)
    if draw_p < 0.9:
        return
    for k in range(antennae):
        ang = -math.pi/2 + (k - (antennae - 1) / 2) * 0.44
        x0, y0 = cx + r*math.cos(ang), cy + r*math.sin(ang)
        x1, y1 = cx + (r + 36*ant_a)*math.cos(ang), cy + (r + 36*ant_a)*math.sin(ang)
        d.line([(x0, y0), (x1, y1)], fill=B.mix(B.ACCENT, alpha*ant_a), width=4)
        d.ellipse([x1-7, y1-7, x1+7, y1+7], fill=B.mix(B.ACCENT, alpha*ant_a))
