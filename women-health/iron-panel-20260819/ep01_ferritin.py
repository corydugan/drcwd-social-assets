#!/usr/bin/env python3
"""IRON PANEL 01: serum ferritin.

THE ONE IDEA. Ferritin is the store, haemoglobin is the iron in use, and the
store empties first. Two columns, one drains, then the other. That single
picture is why a full blood count can look normal in a woman who is deficient,
and it is the spine the other nine episodes hang off.

The staging is not a stylistic choice. Auerbach, DeLoughery and Tirnauer, JAMA
2025;333(20):1813-1823, PMID 40159291, describes iron deficiency as running from
low iron stores through to iron deficiency anaemia. Ferritin falls, then
haemoglobin. Paraphrased and not quoted, so the page stays AU throughout.

WHAT IS DELIBERATELY NOT SAID. The brief called ferritin an indicator of
"exactly how much iron your body has saved up". That word is dropped. Ferritin
is an acute phase reactant and rises with inflammation, so a normal ferritin in
an inflamed patient does not settle the question. The word "exactly" would be
the first thing a haematologist attacked, and it is not needed for the point.
The inflammation caveat gets its own episode alongside hepcidin rather than a
rushed half sentence here.

No number, prevalence or threshold appears on screen. Same rule as the reels.
"""
import os
from PIL import Image, ImageDraw
import series as S
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 29

FERR = (250, 640, 470, 1180)     # x0, ytop, x1, ybot
HAEM = (610, 640, 830, 1180)


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 24.0, 24.8)

    if out > 0.01:
        S.titlecard(d, f, "01", "Serum ferritin", "The iron you are not using yet", out)

        # the store
        fdraw = B.seg(f, 3.0, 5.2)
        ffill = B.seg(f, 5.4, 8.4) - 0.88 * B.seg(f, 13.4, 17.4)
        S.column(d, FERR, fdraw, max(ffill, 0.0), out)
        S.caplabel(d, FERR, "FERRITIN", "what is stored", B.seg(f, 6.0, 7.0) * out)

        # the iron in use
        hdraw = B.seg(f, 9.0, 10.6)
        hfill = B.seg(f, 10.6, 13.0) - 0.40 * B.seg(f, 18.2, 20.6)
        S.column(d, HAEM, hdraw, max(hfill, 0.0), out)
        S.caplabel(d, HAEM, "HAEMOGLOBIN", "what is working", B.seg(f, 10.8, 11.8) * out)

        # the order of events, marked on the falling column
        a = B.seg(f, 15.0, 16.0) * (1 - B.seg(f, 21.0, 21.8)) * out
        if a > 0:
            d.text((360, 596), "FALLS FIRST", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")
        a = B.seg(f, 19.4, 20.4) * (1 - B.seg(f, 21.0, 21.8)) * out
        if a > 0:
            d.text((720, 596), "FALLS LAST", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 21.6, 22.8) * out
        if a > 0:
            d.line([(110, 1360), (110 + (S.W-220)*B.seg(f, 21.4, 22.4), 1360)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1398), "The store runs down",     font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1470), "long before the blood does.", font=B.SERIF(58), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.8,  "Ferritin is where your body keeps the iron it is not using."),
            (9.0,  13.2, "Haemoglobin is the iron already at work, carrying oxygen."),
            (13.4, 18.0, "Lose iron, and the store is what empties."),
            (18.2, 21.4, "Haemoglobin only falls once the store is gone."),
        ], out)

    S.outro(img, d, f, 25.2)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep01-ferritin-ink", frame, DUR)
