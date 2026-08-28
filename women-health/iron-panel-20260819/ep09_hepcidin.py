#!/usr/bin/env python3
"""IRON PANEL 09: hepcidin.

THE ONE IDEA, and it is the one with clinical teeth. Hepcidin is the switch on
the gut door, and it answers to inflammation, not to how much iron you need. So
in an inflamed patient the door shuts on iron that is wanted, and the ferritin
reading rises at the same time. Episodes 09 and 11 are the same problem seen
from two ends.

Nemeth, Tuttle, Powelson, Vaughn, Donovan, Ward, Ganz and Kaplan, Science 2004,
PMID 15514116: hepcidin binds ferroportin and induces its internalisation, which
is the door closing. Ganz, Physiol Rev 2013, PMID 24137020, for the systemic
picture. Both checked through pubmed.py.

Ferroportin is not named on screen. The exporter is the door, and naming the
protein would cost the beat without adding anything a lay viewer can use.

AU spelling throughout.
"""
import os
from PIL import Image, ImageDraw
import series as S
import bio
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 38
GUT_Y = 1030
DOOR_X, DOOR_W = 540, 116


def frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 32.6, 33.4)

    if out > 0.01:
        S.titlecard(d, f, "09", "Hepcidin", "The switch on the door", out)

        bio.liver(d, 430, 716, 158, alpha=out, draw_p=B.seg(f, 10, 12.8),
                  label="LIVER", label_a=B.seg(f, 12.4, 13.4) * out)
        bio.gut(d, 110, 970, GUT_Y, amp=44, alpha=out, draw_p=B.seg(f, 12.6, 15.4))
        a = B.seg(f, 15, 16) * out
        if a > 0:
            d.text((110, GUT_Y + 92), "GUT", font=B.SANS_B(30), fill=B.mix(B.EYEBROW, a))

        # iron crossing the wall while the door is open
        shut = B.seg(f, 23.6, 26)
        for j in range(4):
            t = 9.4 + j * 0.7
            rise = B.seg(f, t, t + 2.6)
            if 0 < rise < 1:
                fade = B.seg(f, t, t + 0.6) * (1 - B.smooth(max(0.0, (rise-0.6)/0.4))) * (1 - shut)
                if fade > 0.01:
                    d.ellipse([DOOR_X-11 - 26 + j*18, GUT_Y - 30 - 120*rise - 11,
                               DOOR_X+11 - 26 + j*18, GUT_Y - 30 - 120*rise + 11],
                              fill=B.mix(B.ACCENT, fade * out))

        # the door frame, then the bar across it
        a = B.seg(f, 16, 17) * out
        if a > 0:
            for x in (DOOR_X - DOOR_W//2, DOOR_X + DOOR_W//2):
                d.line([(x, GUT_Y - 34), (x, GUT_Y + 34)], fill=B.mix(B.FG_SUBTLE, a), width=4)
        if shut > 0.01:
            d.line([(DOOR_X - DOOR_W//2, GUT_Y), (DOOR_X - DOOR_W//2 + DOOR_W*shut, GUT_Y)],
                   fill=B.mix(B.EYEBROW, out), width=13)

        # hepcidin travelling from liver to door
        for j in range(3):
            t = 13.4 + j * 0.8
            trip = B.seg(f, t, t + 2.8)
            if 0 < trip < 1:
                x = 430 + (DOOR_X - 430) * trip
                y = 716 + 112 + (GUT_Y - 40 - 828) * trip
                fa = B.seg(f, t, t + 0.5) * (1 - B.smooth(max(0.0, (trip-0.72)/0.28)))
                if fa > 0.01:
                    d.ellipse([x-10, y-10, x+10, y+10], fill=B.mix(B.EYEBROW, fa * out))

        a = B.seg(f, 26.2, 27.2) * out          # stays: the closing frame is a shut door
        if a > 0:
            d.text((S.W/2, GUT_Y + 92), "SHUT", font=B.SANS_B(32),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")

        a = B.seg(f, 30, 31.2) * out
        if a > 0:
            d.line([(110, 1240), (110 + (S.W-220)*B.seg(f, 29.8, 30.8), 1240)],
                   fill=B.mix(B.RULE, a), width=4)
            d.text((S.W/2, 1278), "The switch answers", font=B.SERIF(56), fill=B.mix(B.FG, a), anchor="ma")
            d.text((S.W/2, 1350), "to inflammation, not to need.", font=B.SERIF(52), fill=B.mix(B.FG, a), anchor="ma")

        S.narrate(d, f, [
            (2.6, 8.2, "Hepcidin is a hormone your liver makes to control how much iron gets into your body."),
            (8.4, 12.9, "It acts on the gut wall, where iron from food is taken up."),
            (13.1, 15.9, "While you need iron, that door stays open."),
            (16.1, 18.6, "Raise the hormone and the door shuts."),
            (18.8, 23.0, "Inflammation raises it, whether or not you need what is behind it."),
        ], out)

    S.outro(img, d, f, 33.8)
    return img


if __name__ == "__main__":
    S.render(HERE, "ep09-hepcidin-ink", frame, DUR)
