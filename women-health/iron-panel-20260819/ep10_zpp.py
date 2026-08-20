#!/usr/bin/env python3
"""IRON PANEL 10: zinc protoporphyrin.

THE ONE IDEA. The last step of building haem drops a metal into a ring. When
iron is not there, zinc goes in instead, and the wrong molecule accumulates. The
body does not stop the line, it substitutes, and the count of the substitutions
is the measurement.

Zinc being inserted into protoporphyrin IX in place of iron when iron supply
falls short at the final step of haem synthesis is the definition Cory supplied.

Iron is drawn in grape and zinc in white. Two greys would have been true to the
palette and useless on screen, and the whole beat is that the viewer sees the
swap happen.

AU spelling throughout. No number on screen.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 31
CX, CY, R = 540, 806, 206


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 25.6, 26.4)

    if out > 0.01:
        S.titlecard(d, f, "10", "Zinc protoporphyrin", "The wrong metal in the seat", out)

        iron_in = B.seg(f, 7.2, 9.4) * (1 - B.seg(f, 13.0, 14.4))
        zinc_in = B.seg(f, 15.2, 17.4)
        metal = B.ACCENT if zinc_in < 0.02 else B.FG
        bio.ring_socket(d, CX, CY, R, alpha=out, draw_p=B.seg(f, 3.0, 6.4),
                        metal=metal, metal_a=max(iron_in, zinc_in))

        a = B.seg(f, 6.0, 7.0) * out
        if a > 0:
            d.text((CX, CY - R - 74), "THE RING THAT BECOMES HAEM", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 9.4, 10.4) * (1 - B.seg(f, 13.0, 13.8)) * out
        if a > 0:
            d.text((CX, CY + R + 46), "IRON", font=B.SANS_B(34),
                   fill=B.mix(B.ACCENT, a), anchor="ma")
        a = B.seg(f, 17.4, 18.4) * out
        if a > 0:
            d.text((CX, CY + R + 46), "ZINC", font=B.SANS_B(34),
                   fill=B.mix(B.FG, a), anchor="ma")

        a = B.seg(f, 23.0, 24.2) * out
        if a > 0:
            d.line([(110, 1240), (110 + (S.W-220)*B.seg(f, 22.8, 23.8), 1240)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1278), "The body does not stop.", font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1350), "It substitutes.",          font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.4,  "The last step of building haem drops one metal into a ring."),
            (8.6,  13.0, "When iron is there to be had, that metal is iron."),
            (13.2, 18.6, "When it is not, zinc goes in instead."),
            (18.8, 22.4, "The wrong molecule builds up, and counting it is the test."),
        ], out)

    S.outro(img, d, f, 26.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep10-zpp-ink", frame, DUR)
