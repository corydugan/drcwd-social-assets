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
DUR = 31

TRUE = (250, 640, 470, 1160)
READ = (610, 640, 830, 1160)


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 25.6, 26.4)

    if out > 0.01:
        S.titlecard(d, f, "11", "C-reactive protein",
                    "Why a normal ferritin can still be low", out)

        S.column(d, TRUE, B.seg(f, 3.0, 5.2), 0.17 * B.seg(f, 5.4, 7.6), out)
        S.caplabel(d, TRUE, "THE STORE", "what is actually there", B.seg(f, 6.4, 7.4) * out)

        # the reading agrees, until inflammation lifts it
        lift = B.seg(f, 14.0, 17.6)
        S.column(d, READ, B.seg(f, 9.0, 10.6),
                 0.17 * B.seg(f, 10.6, 12.4) + 0.52 * lift, out)
        S.caplabel(d, READ, "THE READING", "what the test returns", B.seg(f, 11.8, 12.8) * out)

        a = B.seg(f, 15.0, 16.0) * out
        if a > 0:
            d.text((720, 596), "INFLAMMATION", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 18.4, 19.4) * out
        if a > 0:
            d.text((360, 596), "UNCHANGED", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 23.0, 24.2) * out
        if a > 0:
            d.line([(110, 1300), (110 + (S.W-220)*B.seg(f, 22.8, 23.8), 1300)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1338), "A normal ferritin",    font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1410), "is not always a full one.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.6,  "Ferritin is a store protein. It is also an inflammation protein."),
            (8.8,  13.6, "With nothing inflamed, the store and the reading agree."),
            (13.8, 18.6, "Add inflammation and the reading climbs while the store does not."),
            (18.8, 22.4, "CRP is what tells you which of the two you are looking at."),
        ], out)

    S.outro(img, d, f, 26.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep11-crp-ink", frame, DUR)
