#!/usr/bin/env python3
"""IRON PANEL 04: total iron-binding capacity. Third appearance of THE FLEET.

THE ONE IDEA, and it is the counter-intuitive one in the whole panel. Capacity
is not the iron, it is the room for it. And when iron runs short the liver
builds MORE carriers, so capacity goes UP while the iron on board does not. The
bar grows, the taken seats do not move, and the share visibly falls.

That is the single most useful thing to know about TIBC, because a rising number
reads like an improvement to anyone who has not been told otherwise.

Transferrin rises in iron deficiency: Lopez, Cacoub, Macdougall and Peyrin-
Biroulet, Iron deficiency anaemia, Lancet 2016, PMID 26314490, and Camaschella,
Haematologica 2020, PMID 31949017. Both checked through pubmed.py. Transferrin
being made by the liver is in the definition Cory supplied.

The bar growing from sixteen seats to twenty-six is a picture of a direction,
not a measurement. No number is shown, and none should be added: the real ratio
depends on the assay and on how far the deficiency has run.

AU spelling throughout.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 37

SEATS = 2 * len(bio.FLEET)
TAKEN = sum(bio.FILL)
GROWN = 26


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 32, 32.8)

    if out > 0.01:
        S.titlecard(d, f, "04", "Total iron-binding capacity", "Every seat, taken or not", out)

        bio.fleet(d, draw_p=B.seg(f, 10, 12.6), alpha=out,
                  seat_a=B.seg(f, 12, 13.6), load_a=B.seg(f, 13.2, 15), stagger=0.4)

        # the bar grows while the taken seats stay exactly where they were
        grow = B.seg(f, 21, 25)
        n = int(round(SEATS + (GROWN - SEATS) * grow))
        bio.tickbar(d, 1120, n, TAKEN, p=B.seg(f, 15.6, 18.6), alpha=out)

        a = B.seg(f, 19, 20) * (1 - B.seg(f, 21, 21.8)) * out
        if a > 0:
            d.text((S.W/2, 1064), "CAPACITY  =  ALL THE SEATS THERE ARE",
                   font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 25.4, 26.4) * out
        if a > 0:
            d.text((S.W/2, 1064), "MORE SEATS.  THE SAME IRON.",
                   font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 29.4, 30.6) * out
        if a > 0:
            d.line([(110, 1320), (110 + (S.W-220)*B.seg(f, 29.2, 30.2), 1320)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1358), "The capacity rises",   font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1430), "as the iron runs out.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (2.6, 7.9, "Total iron-binding capacity measures how much iron your blood could carry if every carrier were full."),
            (8.1, 12.5, "It is a count of the room, not a count of the iron."),
            (12.7, 16.7, "Every seat in the fleet, counted whether or not it is used."),
            (16.9, 20.2, "Run short of iron and the liver builds more carriers."),
            (20.4, 24.4, "So the room goes up while the iron on board does not."),
        ], out)

    S.outro(img, d, f, 33.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep04-tibc-ink", frame, DUR)
