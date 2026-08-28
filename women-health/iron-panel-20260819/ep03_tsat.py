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
DUR = 36

SEATS = 2 * len(bio.FLEET)
TAKEN = sum(bio.FILL)


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 31.0, 31.8)

    if out > 0.01:
        S.titlecard(d, f, "03", "Transferrin saturation", "How full the transport is", out)

        # ONE carrier first, while the voice explains what transferrin is.
        # Without it the frame held a title, a line of narration at the foot,
        # and seven seconds of nothing in between, which reads as a fault
        # rather than a rest. It also earns the next line: you can only say
        # "each carrier has two seats" over a picture of the two seats.
        solo = B.seg(f, 3.4, 4.6) * (1 - B.seg(f, 9.4, 10.0)) * out
        if solo > 0.01:
            bio.carrier(d, (S.W - bio.TRUCK_W) / 2, 800, filled=2,
                        draw_p=B.seg(f, 3.4, 4.6), alpha=solo,
                        seat_a=B.seg(f, 5.0, 6.0), load_a=B.seg(f, 7.4, 8.6))
            bio.road(d, 800 + bio.TRUCK_H + 21, B.seg(f, 3.4, 4.6), solo)
            a = B.seg(f, 4.8, 5.8) * solo
            if a > 0:
                d.text((S.W/2, 700), "TRANSFERRIN,  THE CARRIER",
                       font=B.SANS_B(30), fill=B.mix(B.EYEBROW, a), anchor="ma")

        # then the one becomes many. The fleet arrives AFTER transferrin has
        # been named, not before.
        bio.fleet(d, draw_p=B.seg(f, 10.2, 12.8), alpha=out,
                  seat_a=B.seg(f, 12.2, 13.8), load_a=B.seg(f, 13.4, 15.2), stagger=0.4)

        # the label sits ABOVE the fleet. At y=992 it ran straight through the
        # second road line and the wheels of the second row.
        a = B.seg(f, 12.8, 13.8) * (1 - B.seg(f, 22.0, 22.8)) * out
        if a > 0:
            d.text((S.W/2, 640), "EIGHT CARRIERS,  TWO SEATS EACH",
                   font=B.SANS_B(30), fill=B.mix(B.EYEBROW, a), anchor="ma")

        bio.tickbar(d, 1120, SEATS, TAKEN, p=B.seg(f, 15.6, 18.6), alpha=out)

        a = B.seg(f, 19.4, 20.4) * out
        if a > 0:
            d.text((S.W/2, 1064), "EVERY SEAT IN THE FLEET, TAKEN AND EMPTY",
                   font=B.SANS_B(30), fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 23.4, 24.4) * out
        if a > 0:
            d.text((S.W/2, 1212), "SATURATION  =  THE SHARE THAT IS TAKEN",
                   font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 28.6, 29.8) * out
        if a > 0:
            d.line([(110, 1320), (110 + (S.W-220)*B.seg(f, 28.4, 29.4), 1320)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1358), "Not how much iron.",    font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1430), "How full the transport is.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (2.6,  6.2,  "Transferrin is the protein that carries iron around your body."),
            (6.4,  10.2, "Think of it as iron's ride. It picks iron up in the blood and drives it to where it is needed."),
            (10.4, 14.8, "Iron has to be in its ferric form to board. Each carrier has two seats."),
            (15.0, 18.8, "So the same carriers, and the same two seats on each."),
            (19.0, 22.6, "Line every seat up, taken and empty alike."),
            (22.8, 27.8, "Saturation is the share of them that is taken. It reads how much of the transport is in use, not how much iron there is."),
            (28.0, 31.0, "A low share is one of the two ways deficiency is called."),
        ], out)

    S.outro(img, d, f, 32.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep03-tsat-ink", frame, DUR)
