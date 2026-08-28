#!/usr/bin/env python3
"""IRON PANEL 11: C-reactive protein. Cory's addition, 19 Aug.

THE ONE IDEA, and it is the debt episode 01 left open. Ferritin is a store
protein AND an inflammation protein. Inflammation lifts the reading while the
store underneath does not move, so a normal ferritin in an inflamed patient
settles nothing. CRP is what tells you which of the two you are looking at.

Auerbach, DeLoughery and Tirnauer, JAMA 2025;333(20):1813-1823, PMID 40159291,
gives the low-ferritin diagnosis specifically for individuals WITHOUT
inflammatory conditions, and offers transferrin saturation as the route when
inflammation is present. That caveat is this episode. Checked through pubmed.py.

This is why the brief's line about ferritin showing "exactly" how much iron is
stored was dropped from episode 01 rather than softened. The word had to go, and
the caveat had to get its own episode instead of a rushed half sentence.

AU spelling throughout. No number, and no threshold: the columns show a
direction, not a cut-off.
"""
import os
from PIL import Image, ImageDraw
import series as S
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 38

TRUE = (250, 640, 470, 1160)
READ = (610, 640, 830, 1160)


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 32.6, 33.4)

    if out > 0.01:
        S.titlecard(d, f, "11", "C-reactive protein",
                    "Why a normal ferritin can still be low", out)

        S.column(d, TRUE, B.seg(f, 10, 12.2), 0.17 * B.seg(f, 12.4, 14.6), out)
        S.caplabel(d, TRUE, "THE STORE", "what is actually there", B.seg(f, 13.4, 14.4) * out)

        # the reading agrees, until inflammation lifts it
        lift = B.seg(f, 21, 24.6)
        S.column(d, READ, B.seg(f, 16, 17.6),
                 0.17 * B.seg(f, 17.6, 19.4) + 0.52 * lift, out)
        S.caplabel(d, READ, "THE READING", "what the test returns", B.seg(f, 18.8, 19.8) * out)

        a = B.seg(f, 22, 23) * out
        if a > 0:
            d.text((720, 596), "INFLAMMATION", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 25.4, 26.4) * out
        if a > 0:
            d.text((360, 596), "UNCHANGED", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 30, 31.2) * out
        if a > 0:
            d.line([(110, 1300), (110 + (S.W-220)*B.seg(f, 29.8, 30.8), 1300)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1338), "A normal ferritin",    font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1410), "is not always a full one.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (2.6, 8.4, "C-reactive protein is made by your liver and rises when something in the body is inflamed."),
            (8.6, 15.8, "It sits on the iron panel for one reason: ferritin is a store protein and an inflammation protein at once."),
            (16.0, 19.2, "With nothing inflamed, the store and the reading agree."),
            (19.4, 23.4, "Add inflammation and the reading climbs while the store does not."),
            (23.6, 28.3, "CRP is what tells you which of the two you are looking at."),
        ], out)

    S.outro(img, d, f, 33.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep11-crp-ink", frame, DUR)
