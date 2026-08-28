#!/usr/bin/env python3
"""IRON PANEL 06: haemoglobin.

THE ONE IDEA. Haemoglobin is the iron already at work, and it is the LAST thing
in the sequence to move. Which means a normal result rules out very little.

Auerbach, DeLoughery and Tirnauer, JAMA 2025;333(20):1813-1823, PMID 40159291,
describes iron deficiency running from low stores through to iron deficiency
anaemia, and reports that in high-income countries a far larger share of
non-pregnant women of reproductive age have iron deficiency WITHOUT anaemia than
with it. That is the whole episode. The share itself stays off screen.

Cells are drawn with bio.red_cell, which sits on an organic outline rather than
a circle. Cory's call: organs and cells loose, machinery ruled.

AU spelling throughout.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 38
CELLS = [(cx, cy) for cy in (720, 884) for cx in (250, 443, 636, 829)]
STAGE = [(250, "STORES GO"), (540, "SUPPLY TIGHTENS"), (830, "HAEMOGLOBIN FALLS")]


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 32.6, 33.4)

    if out > 0.01:
        S.titlecard(d, f, "06", "Haemoglobin", "The iron already at work", out)

        pale = 0.62 * B.seg(f, 26, 28.6)
        for i, (cx, cy) in enumerate(CELLS):
            p = max(0.0, min(1.0, (B.seg(f, 10, 13.6) * len(CELLS) - i * 0.45)))
            bio.red_cell(d, cx, cy, 72, alpha=out, pale=pale, draw_p=p, seed=0.4 + i)

        # the sequence, so "last" is a position and not an assertion
        ln = B.seg(f, 19.8, 21)
        if ln > 0:
            d.line([(190, 1088), (190 + 700*ln, 1088)], fill=B.mix(B.RULE, out), width=4)
        for i, (x, lab) in enumerate(STAGE):
            a = B.seg(f, 14.2 + i*1.8, 15.2 + i*1.8) * out
            if a > 0:
                d.ellipse([x-13, 1075, x+13, 1101], fill=B.mix(B.ACCENT, a))
                d.text((x, 1122), lab, font=B.SANS_B(26), fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 30, 31.2) * out
        if a > 0:
            d.line([(110, 1250), (110 + (S.W-220)*B.seg(f, 29.8, 30.8), 1250)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1288), "A normal haemoglobin", font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1360), "rules out very little.",  font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (2.6, 6.3, "Haemoglobin is the iron-carrying protein inside your red blood cells."),
            (6.5, 10.5, "This test measures how much of it is in your blood."),
            (10.7, 14.8, "It is what carries oxygen from your lungs to everything else."),
            (15.0, 19.4, "In the order things go wrong, it is the last to move."),
            (19.6, 23.3, "Anaemia is where the shortage ends, not where it starts."),
        ], out)

    S.outro(img, d, f, 33.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep06-haemoglobin-ink", frame, DUR)
