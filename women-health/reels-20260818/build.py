#!/usr/bin/env python3
"""Beat 1 reel, INK surface, with a logo outro.

GATED 2026-08-18. Two labels changed on the evidence check. "NORMAL" became
"NORMAL FERRITIN" because the argument holds for ferritin and NOT for
haemoglobin: Braat 2024, Lancet Haematol PMID 38432242, screened reference
populations properly across eight countries and the female haemoglobin limit
barely moved. Anchored to ferritin, Parker 2021 PMID 33179023 and Mei 2021
PMID 34329578 carry it. "whoever was tested" became "a group assumed healthy":
reference individuals are selected by exclusion criteria, not taken as found,
and the old wording was the line a lab-medicine colleague would attack.

Frames are drawn with PIL rather than rendered from a browser: a draw-on line is
a polyline truncated at frame n, so the whiteboard effect is exact and costs
about 30ms a frame instead of 2.7 seconds.

Surface roles come from surface.ink in tokens.json v3.0.0, not from inverting
the paper palette. Ink is a peer surface there, not a dark mode, so grape.800
is never used here: it dies on near-black. The curve takes surface.ink.accent
(grape.200) and the eyebrow takes grape.500.

The wordmark is rendered once from lockup-primary-delta-outlined.svg with the
delta polygon REMOVED, because the delta is animated here in PIL and the two
would otherwise fight over alignment.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H, FPS, DUR = 1080, 1920, 30, 34
N = FPS * DUR
OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)

# ---- surface.ink, read from tokens.json v3.0.0
FIELD      = (11, 11, 12)      # ink.max      #0B0B0C
FG         = (255, 255, 255)   # paper
FG_MUTED   = (228, 229, 231)   # ink.200
FG_SUBTLE  = (200, 202, 206)   # ink.300
RULE       = (42, 42, 45)      # ink.900
ACCENT     = (216, 207, 231)   # grape.200
EYEBROW    = (138, 111, 184)   # grape.500

F = os.path.expanduser("~/Library/Fonts")
def font(n, s): return ImageFont.truetype(os.path.join(F, n), s)
SERIF  = lambda s: font("DMSerifDisplay-Regular.ttf", s)
SANS   = lambda s: font("DMSans-Regular.ttf", s)
SANS_M = lambda s: font("DMSans-Medium.ttf", s)
SANS_B = lambda s: font("DMSans-Bold.ttf", s)

WORDMARK = Image.open(os.path.join(OUT, "wordmark.png")).convert("RGBA")

def smooth(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def seg(f, a, b):
    return smooth((f / FPS - a) / (b - a)) if b > a else 0.0
def mix(col, a):
    """fade toward the FIELD, not toward white. On ink that distinction is the
    difference between a fade and a glow."""
    return tuple(int(c * a + FIELD[i] * (1 - a)) for i, c in enumerate(col))

PX0, PX1, PY_BASE, PY_TOP = 110, W - 110, 1180, 720
xs = np.linspace(-3.4, 3.4, 400); ys = np.exp(-xs ** 2 / 2)
CURVE = [(PX0 + (PX1 - PX0) * (x + 3.4) / 6.8,
          PY_BASE - (PY_BASE - PY_TOP) * y) for x, y in zip(xs, ys)]
def x_at(z): return PX0 + (PX1 - PX0) * (z + 3.4) / 6.8
LO, HI = x_at(-1.96), x_at(1.96)

# ---- outro geometry, in lockup-SVG units, measured from the rendered bboxes
S = 1.56
DELTA_U = [(32, 38), (9, 80), (55, 80)]
WM_U    = (77.3, 36.3, 432.3, 59.0)     # x, y, w, h
CONTENT_W, CONTENT_H = (WM_U[0] + WM_U[2]) - 9, WM_U[3]
OX = (W - CONTENT_W * S) / 2
OY = 880
def ux(u): return OX + (u - 9) * S
def uy(v): return OY + (v - 36.3) * S

def partial(points, p):
    """the polyline truncated at fraction p of its total length: the draw-on"""
    if p <= 0: return []
    segs = [((points[i], points[i + 1]),
             ((points[i + 1][0] - points[i][0]) ** 2 +
              (points[i + 1][1] - points[i][1]) ** 2) ** 0.5)
            for i in range(len(points) - 1)]
    total = sum(s[1] for s in segs); want = total * min(p, 1.0)
    out, run = [points[0]], 0.0
    for (a, b), L in segs:
        if run + L <= want: out.append(b); run += L
        else:
            k = (want - run) / L if L else 0
            out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)); break
    return out

def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for w_ in text.split():
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def frame(f):
    img = Image.new("RGB", (W, H), FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - seg(f, 29.2, 30.0)          # everything before the outro clears

    if out > 0.01:
        a = seg(f, 0.2, 1.4) * (1 - seg(f, 8.4, 9.4)) * out
        if a > 0:
            d.text((W/2, 300), "“Your bloods came", font=SERIF(78), fill=mix(FG, a), anchor="ma")
            d.text((W/2, 396), "back normal.”",     font=SERIF(78), fill=mix(FG, a), anchor="ma")
        a = seg(f, 1.2, 2.2) * (1 - seg(f, 8.4, 9.2)) * out
        if a > 0:
            d.text((W/2, 520), "What that sentence actually means",
                   font=SANS(40), fill=mix(FG_SUBTLE, a), anchor="ma")

        a = seg(f, 3.0, 3.8) * out
        if a > 0:
            d.line([(PX0, PY_BASE), (PX0 + (PX1-PX0)*seg(f,3.0,3.8), PY_BASE)],
                   fill=mix(RULE, a), width=4)
        p = seg(f, 3.8, 8.2)
        if p > 0 and out > 0.01:
            k = max(2, int(len(CURVE) * p))
            d.line(CURVE[:k], fill=mix(ACCENT, out), width=7, joint="curve")

        band = seg(f, 9.4, 11.6)
        if band > 0:
            xl = LO + (x_at(0) - LO) * (1 - band); xr = HI - (HI - x_at(0)) * (1 - band)
            poly = [(x, y) for x, y in CURVE if xl <= x <= xr]
            if len(poly) > 2:
                d.polygon([(poly[0][0], PY_BASE)] + poly + [(poly[-1][0], PY_BASE)],
                          fill=ACCENT + (int(34 * out),))
        cut = seg(f, 9.0, 10.2)
        if cut > 0:
            for x in (LO, HI):
                d.line([(x, PY_BASE), (x, PY_BASE - (PY_BASE - 660) * cut)],
                       fill=mix(EYEBROW, out), width=5)
        a = seg(f, 11.4, 12.4) * out
        if a > 0:
            d.text((W/2, 320), "“NORMAL FERRITIN”", font=SANS_B(52), fill=mix(FG, a), anchor="ma")
            d.text((W/2, 396), "the middle 95% of a group assumed healthy",
                   font=SANS(34), fill=mix(FG_SUBTLE, a), anchor="ma")

        dfc = seg(f, 15.4, 18.0)
        if dfc > 0:
            xr = LO + (x_at(-0.35) - LO) * dfc
            poly = [(x, y) for x, y in CURVE if LO <= x <= xr]
            if len(poly) > 2:
                d.polygon([(poly[0][0], PY_BASE)] + poly + [(poly[-1][0], PY_BASE)],
                          fill=EYEBROW + (int(210 * out),))
        a = seg(f, 18.0, 19.0) * out
        if a > 0:
            d.text((PX0+30, 1245), "already iron deficient,", font=SANS_M(38), fill=mix(ACCENT, a))
            d.text((PX0+30, 1296), "and inside the range",    font=SANS_M(38), fill=mix(ACCENT, a))

        a = seg(f, 22.6, 23.8) * out
        if a > 0:
            d.line([(PX0, 1400), (PX0 + (PX1-PX0)*seg(f,22.4,23.4), 1400)], fill=mix(RULE, a), width=4)
            d.text((W/2, 1436), "Normal describes the population.",     font=SERIF(58), fill=mix(FG, a), anchor="ma")
            d.text((W/2, 1508), "It does not describe a healthy person.", font=SERIF(58), fill=mix(FG, a), anchor="ma")

        for a0, b0, txt in [(3.0, 9.0,  "A reference range is built by testing a population."),
                            (9.2, 15.2, "A line is drawn around the middle of them."),
                            (15.4, 22.4, "But a large share of the women tested were already deficient.")]:
            if a0 <= f/FPS < b0:
                al = min(smooth((f/FPS-a0)/0.5), smooth((b0-f/FPS)/0.5), 1.0) * out
                fnt = SANS_M(46); y = 1560
                for ln in wrap(d, txt, fnt, W-220):
                    d.text((W/2, y), ln, font=fnt, fill=mix(FG_MUTED, al), anchor="ma"); y += 62

    # ---------------------------------------------------------------- outro
    tri = [(ux(x), uy(y)) for x, y in DELTA_U]
    p = seg(f, 30.4, 31.6)
    if p > 0:
        path = partial(tri + [tri[0]], p)
        if len(path) > 1: d.line(path, fill=FG, width=6, joint="curve")
    fill = seg(f, 31.5, 32.1)
    if fill > 0:
        d.polygon(tri, fill=FG + (int(255 * fill),))
    wm = seg(f, 32.0, 32.9)
    if wm > 0:
        tw, th = int(WM_U[2]*S), int(WM_U[3]*S)
        strip = WORDMARK.resize((tw, th), Image.LANCZOS)
        k = max(1, int(tw * wm))
        img.paste(strip.crop((0, 0, k, th)), (int(ux(WM_U[0])), int(uy(WM_U[1]))), strip.crop((0, 0, k, th)))
    rl = seg(f, 32.9, 33.6)
    if rl > 0:
        y = uy(WM_U[1] + WM_U[3]) + 44
        half = (CONTENT_W * S / 2) * rl
        d.line([(W/2 - half, y), (W/2 + half, y)], fill=EYEBROW, width=3)
    return img

if __name__ == "__main__":
    for f in range(N):
        frame(f).save(os.path.join(FR, f"{f:05d}.png"))
        if f % 200 == 0: print(f"  {f}/{N}", flush=True)
    mp4 = os.path.join(OUT, "beat1-bloods-normal-ink.mp4")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),
                    "-i",os.path.join(FR,"%05d.png"),"-c:v","libx264","-pix_fmt","yuv420p",
                    "-crf","18","-movflags","+faststart",mp4], check=True)
    print("wrote", mp4)
