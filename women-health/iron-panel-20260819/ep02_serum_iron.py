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
DUR = 36

LOADED = [i for i, n in enumerate(bio.FILL) if n > 0]


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 31, 31.8)

    if out > 0.01:
        S.titlecard(d, f, "02", "Serum iron", "The iron in transit right now", out)

        focus = B.seg(f, 24.2, 25.2) * (1 - B.seg(f, 27.8, 28.6))
        bio.fleet(d,
                  draw_p=B.seg(f, 10, 14),
                  alpha=out,
                  seat_a=B.seg(f, 15, 16.6),
                  load_a=B.seg(f, 19.4, 22),
                  stagger=0.55,
                  only=LOADED, dim=focus)

        a = B.seg(f, 24.6, 25.6) * out
        if a > 0:
            d.text((S.W/2, 632), "SERUM IRON  =  THE SEATS THAT ARE TAKEN",
                   font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 28.6, 29.8) * out
        if a > 0:
            d.line([(110, 1200), (110 + (S.W-220)*B.seg(f, 28.4, 29.4), 1200)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1238), "A snapshot of the traffic.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1310), "Not a measure of the supply.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (2.6, 6.9, "Serum iron measures the iron travelling in your blood right now."),
            (7.1, 12.7, "It does not drift loose. It travels bound to a carrier protein called transferrin."),
            (12.9, 16.8, "Each carrier has two places an iron atom can sit."),
            (17.0, 20.1, "Serum iron counts the seats that are taken."),
            (20.3, 24.3, "It rises after a meal, and drifts across the day."),
        ], out)

    S.outro(img, d, f, 32.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep02-serum-iron-ink", frame, DUR)
