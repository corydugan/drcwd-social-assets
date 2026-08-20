#!/usr/bin/env python3
"""IRON PANEL 03: transferrin saturation. Second appearance of THE FLEET.

THE ONE IDEA. Saturation is not an amount, it is a share: the seats that are
taken, over every seat there is. Episode 02 counted the taken ones. This one
lines up all of them beside each other and reads the ratio off.

Auerbach, DeLoughery and Tirnauer, JAMA 2025;333(20):1813-1823, PMID 40159291,
gives the diagnosis of iron deficiency to serum ferritin or to transferrin
saturation, which is why saturation gets an episode and serum iron alone does
not. Checked through pubmed.py.

The fleet and its loading come from bio.py. The ratio on screen is the same five
seats in sixteen that episode 02 drew. If they ever disagree, the fault is that
someone gave an episode its own copy of FILL.

AU spelling throughout. No number, prevalence or threshold on screen: the share
is shown as a picture and never written down.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 29

SEATS = 2 * len(bio.FLEET)
TAKEN = sum(bio.FILL)


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 24.0, 24.8)

    if out > 0.01:
        S.titlecard(d, f, "03", "Transferrin saturation", "How full the transport is", out)

        bio.fleet(d, draw_p=B.seg(f, 3.0, 5.6), alpha=out,
                  seat_a=B.seg(f, 5.0, 6.6), load_a=B.seg(f, 6.2, 8.0), stagger=0.4)

        bio.tickbar(d, 1120, SEATS, TAKEN, p=B.seg(f, 8.6, 11.6), alpha=out)

        a = B.seg(f, 12.4, 13.4) * out
        if a > 0:
            d.text((S.W/2, 1064), "EVERY SEAT IN THE FLEET, TAKEN AND EMPTY",
                   font=B.SANS_B(30), fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 16.4, 17.4) * out
        if a > 0:
            d.text((S.W/2, 1212), "SATURATION  =  THE SHARE THAT IS TAKEN",
                   font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 21.6, 22.8) * out
        if a > 0:
            d.line([(110, 1320), (110 + (S.W-220)*B.seg(f, 21.4, 22.4), 1320)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1358), "Not how much iron.",    font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1430), "How full the transport is.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.4,  "The same carriers, and the same two seats on each."),
            (8.6,  12.8, "Line every seat up, taken and empty alike."),
            (13.0, 18.0, "Saturation is the share of them that is taken."),
            (18.2, 21.2, "A low share is one of the two ways deficiency is called."),
        ], out)

    S.outro(img, d, f, 25.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep03-tsat-ink", frame, DUR)
