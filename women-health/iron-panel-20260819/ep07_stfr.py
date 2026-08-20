#!/usr/bin/env python3
"""IRON PANEL 07: soluble transferrin receptor.

THE ONE IDEA. Ferritin reports the store. This reports the demand: cells short
of iron put up more receptors, pieces of those receptors break off into the
blood, and the count of the pieces is how loudly the cells are asking.

WHAT WAS TONED DOWN, and it is the reason this docstring exists. The source
brief said sTfR reveals cellular iron hunger "regardless of inflammation". That
is an overclaim. sTfR is LESS disturbed by inflammation than ferritin is, which
is the useful and defensible version, and it is what the narration says.

Lopez, Cacoub, Macdougall, Peyrin-Biroulet, Lancet 2016, PMID 26314490.
Camaschella, Haematologica 2020, PMID 31949017. Both checked through pubmed.py.

AU spelling throughout. No number on screen.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 31
CELLS = [(272, 858), (540, 858), (808, 858)]
R = 112


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 25.6, 26.4)

    if out > 0.01:
        S.titlecard(d, f, "07", "Soluble transferrin receptor",
                    "What the cells are asking for", out)

        grow = B.seg(f, 7.0, 11.5)
        n = 1 + int(round(4 * grow))
        for i, (cx, cy) in enumerate(CELLS):
            p = max(0.0, min(1.0, B.seg(f, 3.0, 6.4) * 3 - i * 0.5))
            bio.cell(d, cx, cy, R, alpha=out, draw_p=p,
                     antennae=n, ant_a=grow, seed=0.6 + i * 1.3)

        # The pieces that snap off and are counted in the blood.
        # They rise into the band between the cells and the subtitle and FADE OUT
        # there. The first cut sent them to y=522, straight through the subtitle,
        # and never faded them, so by the payoff the frame was full of debris.
        for i, (cx, _) in enumerate(CELLS):
            for j in range(3):
                t = 13.6 + j * 0.9 + i * 0.35
                rise = B.seg(f, t, t + 3.4)
                if rise <= 0 or rise >= 1:
                    continue
                x = cx - 46 + j * 46
                y = 700 - 108 * rise
                fade = B.seg(f, t, t + 0.7) * (1 - B.smooth(max(0.0, (rise - 0.55) / 0.45)))
                if fade > 0.01:
                    d.ellipse([x-8, y-8, x+8, y+8], fill=B.mix(B.ACCENT, fade * out))
        a = B.seg(f, 17.0, 18.0) * (1 - B.seg(f, 21.6, 22.4)) * out
        if a > 0:
            d.text((S.W/2, 560), "COUNTED IN THE BLOOD", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 23.0, 24.2) * out
        if a > 0:
            d.line([(110, 1200), (110 + (S.W-220)*B.seg(f, 22.8, 23.8), 1200)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1238), "Ferritin says what is stored.", font=B.SERIF(52), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1308), "This says what the cells want.", font=B.SERIF(52), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (3.0,  8.2,  "Cells take iron in through receptors on their surface."),
            (8.4,  13.2, "Run them short, and they put up more of them."),
            (13.4, 18.6, "Pieces snap off into the blood, and those are what is counted."),
            (18.8, 22.4, "It is less disturbed by inflammation than ferritin is."),
        ], out)

    S.outro(img, d, f, 26.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep07-stfr-ink", frame, DUR)
