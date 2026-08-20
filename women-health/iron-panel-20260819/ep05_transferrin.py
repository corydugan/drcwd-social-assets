#!/usr/bin/env python3
"""IRON PANEL 05: transferrin. THE FLEET, fourth and last appearance.

THE ONE IDEA, and it is the payoff for the four-part arc: three of the numbers
on the panel are readings of this one protein. Serum iron is the seats taken,
saturation is the share taken, capacity is every seat there is. Learn the
carrier and three lines of the report stop being separate things to remember.

Transferrin being a liver protein carrying up to two atoms of ferric iron is the
definition Cory supplied. Camaschella, Haematologica 2020, PMID 31949017, and
Ganz, Physiol Rev 2013, PMID 24137020, carry the physiology. Checked through
pubmed.py.

The liver is drawn with bio.liver, which is loose and lobed rather than ruled.
Cory's call, 19 Aug: organs looser and more organic than the machinery. The
carriers stay ruled because they are machinery.

AU spelling throughout. No number on screen.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 30

ROAD_Y = 900
READS = [("SERUM IRON",  "the seats that are taken"),
         ("SATURATION",  "the share of them taken"),
         ("CAPACITY",    "every seat there is")]


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 25.0, 25.8)

    if out > 0.01:
        S.titlecard(d, f, "05", "Transferrin", "The carrier itself", out)

        bio.liver(d, S.W/2, 700, 196, alpha=out, draw_p=B.seg(f, 3.0, 5.8),
                  label="LIVER", label_a=B.seg(f, 5.4, 6.4) * out)

        # the carriers it builds, rolling out below it
        cp = B.seg(f, 6.8, 10.8)
        for i, x in enumerate(bio.COL_X):
            p = max(0.0, min(1.0, cp * 4 - i * 0.5))
            bio.carrier(d, x, ROAD_Y, filled=bio.FILL[i], draw_p=p, alpha=out,
                        seat_a=B.seg(f, 9.0, 10.6), load_a=B.seg(f, 10.0, 11.6))
        bio.road(d, ROAD_Y + bio.TRUCK_H + 21, cp, out)

        # the three readings, all of the same fleet
        for i, (big, sub) in enumerate(READS):
            a = B.seg(f, 13.4 + i * 1.4, 14.4 + i * 1.4) * out
            if a > 0:
                y = 1150 + i * 66
                d.ellipse([150, y+10, 168, y+28], fill=B.mix(B.ACCENT, a))
                d.text((200, y), big, font=B.SANS_B(38), fill=B.mix(B.FG, a))
                d.text((520, y + 6), sub, font=B.SANS(32), fill=B.mix(B.FG_SUBTLE, a))

        a = B.seg(f, 22.6, 23.8) * out
        if a > 0:
            d.line([(110, 1400), (110 + (S.W-220)*B.seg(f, 22.4, 23.4), 1400)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1438), "One protein.",  font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1510), "Three numbers.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.0,  "Your liver builds the carrier that moves iron around."),
            (8.2,  12.8, "Each one holds up to two atoms of iron, and no more."),
            (13.0, 18.4, "Three lines on your panel are readings of this one protein."),
            (18.6, 22.2, "Learn the carrier and three of them stop being separate."),
        ], out)

    S.outro(img, d, f, 26.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep05-transferrin-ink", frame, DUR)
