#!/usr/bin/env python3
"""IRON PANEL 02: serum iron. First appearance of THE FLEET.

THE ONE IDEA. Serum iron counts the seats that are taken, right now, and that is
all it counts. It moves with the last meal and across the day, so on its own it
settles nothing.

That last part is the reason this episode exists rather than being folded into
saturation. Auerbach, DeLoughery and Tirnauer, JAMA 2025;333(20):1813-1823, PMID
40159291, gives the diagnosis to ferritin and to transferrin saturation. Serum
iron is not the test, it is one of the two numbers saturation is built from.
Circadian movement in plasma iron: Cao et al, Biol Trace Elem Res 2012, PMID
22198869, and Casale et al, Age Ageing 1981, PMID 7246335. Both checked through
pubmed.py.

THE FLEET is defined in bio.py, not here. Episodes 02 to 05 draw the same eight
carriers with the same five taken seats, and light a different part each time.
If the layout or the loading is edited, it is edited there, once.

AU spelling throughout, Cory's call 19 Aug: all AUS spelling, everywhere.
No number, prevalence or threshold on screen.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 29

LOADED = [i for i, n in enumerate(bio.FILL) if n > 0]


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 24.0, 24.8)

    if out > 0.01:
        S.titlecard(d, f, "02", "Serum iron", "The iron in transit right now", out)

        focus = B.seg(f, 17.2, 18.2) * (1 - B.seg(f, 20.8, 21.6))
        bio.fleet(d,
                  draw_p=B.seg(f, 3.0, 7.0),
                  alpha=out,
                  seat_a=B.seg(f, 8.0, 9.6),
                  load_a=B.seg(f, 12.4, 15.0),
                  stagger=0.55,
                  only=LOADED, dim=focus)

        a = B.seg(f, 17.6, 18.6) * out
        if a > 0:
            d.text((S.W/2, 632), "SERUM IRON  =  THE SEATS THAT ARE TAKEN",
                   font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 21.6, 22.8) * out
        if a > 0:
            d.line([(110, 1200), (110 + (S.W-220)*B.seg(f, 21.4, 22.4), 1200)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1238), "A snapshot of the traffic.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1310), "Not a measure of the supply.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  7.8,  "Iron does not drift loose in blood. It travels bound to a carrier."),
            (8.0,  12.2, "Each carrier has two places an iron atom can sit."),
            (12.4, 17.0, "Serum iron counts the seats that are taken."),
            (17.2, 21.2, "It rises after a meal, and drifts across the day."),
        ], out)

    S.outro(img, d, f, 25.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep02-serum-iron-ink", frame, DUR)
