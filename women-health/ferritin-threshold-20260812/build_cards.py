#!/usr/bin/env python3
"""Cards 1 and 5 of the ferritin threshold set. Ink surface.

WHY THIS FILE EXISTS. The 12 Aug set shipped as PNGs with no generator, so it
could not be edited, only replaced. This rebuilds the two cards that changed and
gives the set a source again. Cards 2, 3 and 4 are unchanged and still have no
generator; rebuild them here when they next need editing.

WHAT CHANGED, and why, 2026-08-18. Benchmark research against high-performing
iron content found the set answered a question nobody had asked out loud. The
diagnosis was framing, not density: a consultant haematologist posting correct
thresholds drew 31 reactions in the same week an ADHD coach posting her own
infusion story drew 369. So card 1 stopped being a headline and became a claim,
and card 5 stopped issuing an academic instruction and became something a reader
can do on Monday. Cards 2 to 4 were left alone; the 83.6% card is the best in
the set.

EVERY NUMBER VERIFIED 2026-08-18 against the open-access full text at
PMC10300696, not against a summary:
    Weyand AC, Chaitoff A, Freed GL, Sholzberg M, Choi SW, McGann PT.
    JAMA. 2023;329(24):2191-2193. PMID 37367984. n = 3,490.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2160, 2700
OUT = os.path.dirname(os.path.abspath(__file__))
FIELD=(11,11,12); FG=(255,255,255); SUBTLE=(200,202,206); MUTED=(228,229,231)
RULE=(42,42,45); ACCENT=(216,207,231); EYEBROW=(138,111,184); GRAPE=(107,79,158)
DIM=(120,121,128)
F=os.path.expanduser("~/Library/Fonts")
def f(n,s): return ImageFont.truetype(os.path.join(F,n),s)
SERIF=lambda s: f("DMSerifDisplay-Regular.ttf",s)
SANS =lambda s: f("DMSans-Regular.ttf",s)
SANS_M=lambda s: f("DMSans-Medium.ttf",s)
SANS_B=lambda s: f("DMSans-Bold.ttf",s)
M=140

def lockup(d, y=2592):
    wm="Dr. Cory Dugan"; w=d.textlength(wm,font=SERIF(44))
    tx=W-M; dx=tx-w-70
    d.polygon([(dx+26,y-34),(dx,y+20),(dx+52,y+20)],fill=FG)
    d.text((tx,y-36),wm,font=SERIF(44),fill=FG,anchor="ra")

def card1():
    img=Image.new("RGB",(W,H),FIELD); d=ImageDraw.Draw(img,"RGBA")
    d.text((M,150),"EVIDENCE · IRON DEFICIENCY",font=SANS_B(38),fill=EYEBROW)
    d.text((M,240),"“Iron deficient” is not",font=SERIF(116),fill=FG)
    d.text((M,378),"one measurement.",font=SERIF(116),fill=FG)
    d.text((M,556),"It is a line somebody chose.",font=SANS(50),fill=SUBTLE)

    figs=[("17%","below 15 µg/L","95% CI 15.4 to 19.2",False),
          ("38.6%","below 25 µg/L","95% CI 35.8 to 40.9",True),
          ("77.5%","below 50 µg/L","95% CI 75.7 to 79.3",False)]
    x=M
    for val,lab,ci,hi in figs:
        d.text((x,860),val,font=SANS_B(140),fill=ACCENT if hi else FG)
        d.text((x,1030),lab,font=SANS_M(40),fill=SUBTLE)
        d.text((x,1084),ci,font=SANS(32),fill=DIM)
        x+=640

    d.line([(M,1240),(W-M,1240)],fill=RULE,width=4)
    d.rectangle([M,1360,W-M,1640],fill=GRAPE)
    d.text((M+52,1404),"Move that line by 35 µg/L",font=SERIF(74),fill=FG)
    d.text((M+52,1500),"and the number goes from 17% to 77%.",font=SERIF(74),fill=FG)

    d.text((M,1760),"Same 3,490 girls and young women. Same blood. Same assay.",
           font=SANS_M(44),fill=MUTED)
    d.text((M,1830),"Nobody was re-tested.",font=SANS_M(44),fill=MUTED)

    d.text((M,2380),"NHANES 2003 TO 2020 · US FEMALES AGED 12 TO 21 · MEDIAN AGE 16 (IQR 14 TO 18)",
           font=SANS_B(30),fill=DIM)
    d.text((M,2428),"n = 3,490 · ferritin not measured 2011 to 2014",font=SANS(30),fill=DIM)
    d.text((M,2492),"Weyand AC et al. JAMA. 2023;329(24):2191-2193. PMID 37367984.",
           font=SANS(30),fill=DIM)
    d.text((M,2560),"SWIPE · 1 OF 5",font=SANS_B(32),fill=EYEBROW)
    lockup(d)
    p=os.path.join(OUT,"s1-hook.png"); img.save(p); return p

def card5():
    img=Image.new("RGB",(W,H),FIELD); d=ImageDraw.Draw(img,"RGBA")
    d.text((M,150),"WHAT TO DO WITH THIS",font=SANS_B(38),fill=EYEBROW)
    d.text((M,250),"Ask for the number,",font=SERIF(116),fill=FG)
    d.text((M,388),"not the verdict.",font=SERIF(116),fill=FG)

    d.text((M,600),"Then ask which line they are measuring it against.",
           font=SANS(52),fill=SUBTLE)

    d.rectangle([M,780,W-M,1080],fill=GRAPE)
    d.text((M+52,824),"Those are two different questions,",font=SERIF(72),fill=FG)
    d.text((M+52,920),"and you are owed both answers.",font=SERIF(72),fill=FG)

    d.text((M,1240),"A reference range is not a health target.",font=SANS_M(48),fill=MUTED)
    d.text((M,1316),"It describes the group that was tested. If a large share of",font=SANS(44),fill=SUBTLE)
    d.text((M,1380),"them were already deficient, their results sit inside the",font=SANS(44),fill=SUBTLE)
    d.text((M,1444),"range you are being measured against.",font=SANS(44),fill=SUBTLE)

    d.line([(M,1600),(W-M,1600)],fill=RULE,width=4)
    d.text((M,1660),"If you are still exhausted after being told you are fine,",font=SANS_M(48),fill=MUTED)
    d.text((M,1728),"that is information, not a contradiction.",font=SANS_M(48),fill=MUTED)

    d.text((M,2428),"Weyand AC, Chaitoff A, Freed GL, Sholzberg M, Choi SW, McGann PT.",font=SANS(30),fill=DIM)
    d.text((M,2472),"JAMA. 2023;329(24):2191-2193. PMID 37367984. NHANES 2003 to 2020, n = 3,490.",font=SANS(30),fill=DIM)
    d.text((M,2560),"5 OF 5",font=SANS_B(32),fill=EYEBROW)
    lockup(d)
    p=os.path.join(OUT,"s5-position.png"); img.save(p); return p

if __name__=="__main__":
    for p in (card1(), card5()): print("wrote", p)
