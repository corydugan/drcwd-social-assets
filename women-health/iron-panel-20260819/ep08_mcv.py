#!/usr/bin/env python3
"""IRON PANEL 08: mean corpuscular volume.

THE ONE IDEA. MCV is the size the cells come out, and it changes LATE. A red
cell already in circulation does not shrink; only newly built ones are smaller.
So a low MCV says the shortage has been running for a long time, and a normal
MCV says almost nothing about a recent one.

Microcytosis arriving late in longstanding deficiency is the definition Cory
supplied. Lopez, Cacoub, Macdougall, Peyrin-Biroulet, Lancet 2016, PMID
26314490, carries the picture. Checked through pubmed.py.

AU spelling throughout. No number on screen: the two rows are compared by
bracket width, never by a figure.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 31
XS = (380, 545, 710, 875)   # moved right: the row labels were clipped at x=0
BIG_Y, BIG_R = 726, 76
SML_Y, SML_R = 906, 50


def bracket(d, cx, y, half, a):
    if a <= 0.01:
        return
    d.line([(cx-half, y), (cx+half, y)], fill=B.mix(B.EYEBROW, a), width=3)
    for x in (cx-half, cx+half):
        d.line([(x, y-11), (x, y+11)], fill=B.mix(B.EYEBROW, a), width=3)


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 25.6, 26.4)

    if out > 0.01:
        S.titlecard(d, f, "08", "Mean corpuscular volume", "The size the cells come out", out)

        for i, cx in enumerate(XS):
            p = max(0.0, min(1.0, B.seg(f, 3.0, 6.6) * 4 - i * 0.5))
            bio.red_cell(d, cx, BIG_Y, BIG_R, alpha=out, draw_p=p, seed=0.4 + i)
            q = max(0.0, min(1.0, B.seg(f, 8.6, 12.4) * 4 - i * 0.5))
            bio.red_cell(d, cx, SML_Y, SML_R, alpha=out, pale=0.58, draw_p=q, seed=2.1 + i)

        a = B.seg(f, 6.4, 7.4) * out
        if a > 0:
            d.text((110, BIG_Y), "IRON ENOUGH", font=B.SANS_B(24),
                   fill=B.mix(B.EYEBROW, a), anchor="lm")
        a = B.seg(f, 12.0, 13.0) * out
        if a > 0:
            d.text((110, SML_Y), "IRON SHORT", font=B.SANS_B(24),
                   fill=B.mix(B.EYEBROW, a), anchor="lm")

        ba = B.seg(f, 14.2, 15.4) * out
        bracket(d, XS[0], BIG_Y + BIG_R + 30, BIG_R, ba)
        bracket(d, XS[0], SML_Y + SML_R + 30, SML_R, B.seg(f, 15.4, 16.6) * out)

        a = B.seg(f, 23.0, 24.2) * out
        if a > 0:
            d.line([(110, 1220), (110 + (S.W-220)*B.seg(f, 22.8, 23.8), 1220)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1258), "Small cells mean it has",   font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1330), "been going on a long time.", font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.2,  "Every red cell is built to a size."),
            (8.4,  13.6, "Build them short of iron and they come out smaller and paler."),
            (13.8, 18.4, "That is all a low MCV is: cells built short."),
            (18.6, 22.4, "A red cell lives for months, so this one moves last of all."),
        ], out)

    S.outro(img, d, f, 26.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep08-mcv-ink", frame, DUR)
