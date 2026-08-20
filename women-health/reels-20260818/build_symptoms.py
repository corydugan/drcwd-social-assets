#!/usr/bin/env python3
"""Reel 2: iron and the symptoms. Ink surface, same outro.

Palette, fonts, easing, the draw-on helper and the logo outro are IMPORTED from
build.py rather than copied. Two files drawing the same brand from two copies of
the same constants is how the look drifts.

A list of symptoms teaches nothing. This draws the spine first, so every symptom
that branches off it is visibly downstream of the same cause.

DIFFERENTIAL BEAT, added 2026-08-19, and it is the reason this reel was held.
Six symptoms with no differential is a self-diagnosis engine: all six also fit
hypothyroidism, depression, sleep apnoea and coeliac disease. The beat dims every
row, names those four, then brings back the three rows that are, on their own, a
recognised indication to test.

Those three are not a judgement call. Auerbach, DeLoughery and Tirnauer, JAMA
2025;333(20):1813-1823, PMID 40159291, states that testing for iron deficiency is
indicated for patients with anaemia and/or symptoms of iron deficiency, naming
fatigue, pica and restless legs syndrome. On this reel those are rows 0, 5 and 4:
Exhausted, Craving ice, Restless legs. TRIGGERS below is that sentence and
nothing else, so if the source changes, that set changes with it.

Coeliac disease is deliberately in the differential list even though the same
review names it as a CAUSE of iron deficiency through impaired absorption. It
belongs in both places, and putting it here is the more conservative reading.

NOTE ON CLAIMS: every symptom here is a recognised feature of iron deficiency,
but nothing on screen carries a number, a prevalence or a threshold. The JAMA
review gives prevalences for pica and restless legs. They stay out of the frame
on purpose. Gate it before it goes public.
"""
import os, subprocess
from PIL import Image, ImageDraw
import build as B

W, H, FPS, DUR = 1080, 1920, 30, 38
N = FPS * DUR
OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames2"); os.makedirs(FR, exist_ok=True)

SPINE_X, SPINE_TOP, SPINE_BOT = 250, 700, 1330
ROWS = [
    (740,  "Exhausted",     "and sleep does not fix it"),
    (838,  "Breathless",    "on stairs, hills, a brisk walk"),
    (936,  "Foggy",         "concentration and memory"),
    (1034, "Cold",          "hands and feet"),
    (1132, "Restless legs", "worse at night"),
    (1230, "Craving ice",   "chewing it, constantly"),
]
T0, STEP = 7.4, 2.2          # first branch, then one every 2.2s

# rows 0, 4, 5: fatigue, restless legs, pica. JAMA 2025 PMID 40159291 names
# these three as symptoms for which testing is indicated on their own.
TRIGGERS = {0, 4, 5}
FADE = 0.78                  # how far a non-trigger row drops in the differential

ALSO = ["Thyroid  ·  Depression", "Sleep apnoea  ·  Coeliac disease"]


def frame(f):
    img = Image.new("RGB", (W, H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 33.2, 34.0)

    # the differential: everything dims, then the three testing triggers return
    dim  = B.seg(f, 20.2, 21.2)
    pick = B.seg(f, 24.8, 25.8)
    rest = B.seg(f, 27.6, 28.6)   # the four come back, so the payoff plays over
                                  # the whole list rather than a half-faded one

    if out > 0.01:
        a = B.seg(f, 0.2, 1.4) * out
        if a > 0:
            d.text((W/2, 300), "Iron does not just",  font=B.SERIF(74), fill=B.mix(B.FG, a), anchor="ma")
            d.text((W/2, 392), "make blood.",         font=B.SERIF(74), fill=B.mix(B.FG, a), anchor="ma")
        a = B.seg(f, 1.4, 2.4) * out
        if a > 0:
            d.text((W/2, 512), "Every cell needs it to turn oxygen into energy",
                   font=B.SANS(36), fill=B.mix(B.FG_SUBTLE, a), anchor="ma")

        # the spine: drawn ONCE, before any symptom, so the symptoms read as
        # branches of one cause rather than as a list
        sp = B.seg(f, 4.0, 6.8)
        if sp > 0:
            d.line([(SPINE_X, SPINE_TOP), (SPINE_X, SPINE_TOP + (SPINE_BOT-SPINE_TOP)*sp)],
                   fill=B.mix(B.ACCENT, out * (1 - 0.5*dim + 0.5*max(pick, rest))), width=6)
        a = B.seg(f, 4.2, 5.2) * out
        if a > 0:
            d.text((SPINE_X, SPINE_TOP - 66), "LOW IRON", font=B.SANS_B(42),
                   fill=B.mix(B.EYEBROW, a), anchor="la")

        for i, (y, big, sub) in enumerate(ROWS):
            t = T0 + i * STEP
            keep = 1 - FADE*dim + FADE*(pick if i in TRIGGERS else rest)
            arm = B.seg(f, t, t + 0.55)
            if arm > 0:
                d.line([(SPINE_X, y), (SPINE_X + 78*arm, y)],
                       fill=B.mix(B.ACCENT, out*keep), width=5)
            a = B.seg(f, t + 0.35, t + 1.1) * out * keep
            if a > 0:
                d.ellipse([SPINE_X-9, y-9, SPINE_X+9, y+9], fill=B.mix(B.ACCENT, a))
                d.text((SPINE_X + 104, y - 34), big, font=B.SANS_B(46), fill=B.mix(B.FG, a))
                d.text((SPINE_X + 104, y + 16), sub, font=B.SANS(32), fill=B.mix(B.FG_SUBTLE, a))
            # a ring on the three that are enough on their own
            ring = pick * (1 - rest)
            if i in TRIGGERS and ring > 0.01 and out > 0.01:
                r = 9 + 13 * ring
                d.ellipse([SPINE_X-r, y-r, SPINE_X+r, y+r],
                          outline=B.mix(B.ACCENT, out*ring), width=3)

        # the four conditions the same six symptoms also fit
        blk = B.seg(f, 20.6, 21.8) * (1 - B.seg(f, 24.6, 25.6)) * out
        if blk > 0:
            d.text((W/2, 1364), "THESE ALSO FIT", font=B.SANS_B(34),
                   fill=B.mix(B.EYEBROW, blk), anchor="ma")
            for j, ln in enumerate(ALSO):
                d.text((W/2, 1428 + j*62), ln, font=B.SANS_M(42),
                       fill=B.mix(B.FG_MUTED, blk), anchor="ma")

        a = B.seg(f, 28.2, 29.4) * out
        if a > 0:
            d.line([(110, 1440), (110 + (W-220)*B.seg(f, 28.0, 29.0), 1440)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((W/2, 1478), "All of this can start before", font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")
            d.text((W/2, 1548), "your haemoglobin drops.",      font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")
        a = B.seg(f, 30.4, 31.4) * out
        if a > 0:
            d.text((W/2, 1650), "Which is why the blood test can look fine.",
                   font=B.SANS_M(38), fill=B.mix(B.EYEBROW, a), anchor="ma")

        for a0, b0, txt in [(4.0, 7.2,   "Iron's job: carry oxygen, make energy."),
                            (7.4, 19.9,  "So a shortage shows up wherever energy is spent."),
                            (20.6, 24.6, "Symptoms narrow it down. They do not name it."),
                            (25.0, 28.0, "Three of these are enough on their own to test.")]:
            if a0 <= f/FPS < b0:
                al = min(B.smooth((f/FPS-a0)/0.5), B.smooth((b0-f/FPS)/0.5), 1.0) * out
                d.text((W/2, 1760), txt, font=B.SANS_M(40), fill=B.mix(B.FG_MUTED, al), anchor="ma")

    # ---- outro, identical to reel 1, shifted +4.0s by the differential beat
    tri = [(B.ux(x), B.uy(y)) for x, y in B.DELTA_U]
    p = B.seg(f, 34.4, 35.6)
    if p > 0:
        path = B.partial(tri + [tri[0]], p)
        if len(path) > 1: d.line(path, fill=B.FG, width=6, joint="curve")
    fl = B.seg(f, 35.5, 36.1)
    if fl > 0: d.polygon(tri, fill=B.FG + (int(255*fl),))
    wm = B.seg(f, 36.0, 36.9)
    if wm > 0:
        tw, th = int(B.WM_U[2]*B.S), int(B.WM_U[3]*B.S)
        strip = B.WORDMARK.resize((tw, th), Image.LANCZOS)
        k = max(1, int(tw*wm)); c = strip.crop((0, 0, k, th))
        img.paste(c, (int(B.ux(B.WM_U[0])), int(B.uy(B.WM_U[1]))), c)
    rl = B.seg(f, 36.9, 37.6)
    if rl > 0:
        y = B.uy(B.WM_U[1] + B.WM_U[3]) + 44
        half = (B.CONTENT_W * B.S / 2) * rl
        d.line([(W/2 - half, y), (W/2 + half, y)], fill=B.EYEBROW, width=3)
    return img

if __name__ == "__main__":
    # clear the directory first: a shorter previous render leaves frames behind
    # that ffmpeg would happily read off the end of this one
    for old in os.listdir(FR):
        os.remove(os.path.join(FR, old))
    for f in range(N):
        frame(f).save(os.path.join(FR, f"{f:05d}.png"))
        if f % 250 == 0: print(f"  {f}/{N}", flush=True)
    mp4 = os.path.join(OUT, "beat-iron-symptoms-ink.mp4")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),
                    "-i",os.path.join(FR,"%05d.png"),"-c:v","libx264","-pix_fmt","yuv420p",
                    "-crf","18","-movflags","+faststart",mp4], check=True)
    print("wrote", mp4)
