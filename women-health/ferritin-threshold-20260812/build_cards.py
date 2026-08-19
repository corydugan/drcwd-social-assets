#!/usr/bin/env python3
"""The ferritin threshold set. Five carousel cards plus the LinkedIn chart.

REBUILT CLEAN 2026-08-18. The 12 Aug set shipped as PNGs with no generator, so
it could only be replaced, never edited. Worse, cards 2 to 4 drew a HOLLOW
outline delta. That mark does not exist in the logo set: logo/lockup-primary
defines one delta and it is filled. On a swipe the reader passed a filled logo,
three hollow ones, then a filled one. Everything now comes out of this file, so
the lockup cannot drift again.

The 12 Aug PNGs are preserved in git at ac3c080 and nothing was deleted.

ONE SURFACE. The old set alternated ink, paper, paper, paper, ink. Now all ink,
matching the reels. Flip SURFACE below to go back to paper.

EVERY NUMBER VERIFIED 2026-08-18 against the open-access full text at
PMC10300696, not against a summary of it:
    Weyand AC, Chaitoff A, Freed GL, Sholzberg M, Choi SW, McGann PT.
    Prevalence of Iron Deficiency and Iron-Deficiency Anemia in US Females
    Aged 12-21 Years, 2003-2020. JAMA. 2023;329(24):2191-2193. PMID 37367984.
    n = 3,490 of 4,052 eligible. Ferritin not measured 2011 to 2014.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2160, 2700
OUT = os.path.dirname(os.path.abspath(__file__))
SURFACE = "ink"

INK  = dict(field=(11,11,12), fg=(255,255,255), muted=(228,229,231),
            subtle=(200,202,206), rule=(42,42,45), accent=(216,207,231),
            eyebrow=(138,111,184), panel=(107,79,158), dim=(120,121,128),
            logo=(255,255,255))
PAPER= dict(field=(255,255,255), fg=(28,28,30), muted=(74,74,79),
            subtle=(110,111,117), rule=(228,229,231), accent=(53,32,81),
            eyebrow=(107,79,158), panel=(53,32,81), dim=(156,160,166),
            logo=(53,32,81))
C = INK if SURFACE=="ink" else PAPER

F=os.path.expanduser("~/Library/Fonts")
def f(n,s): return ImageFont.truetype(os.path.join(F,n),s)
SERIF =lambda s: f("DMSerifDisplay-Regular.ttf",s)
SANS  =lambda s: f("DMSans-Regular.ttf",s)
SANS_M=lambda s: f("DMSans-Medium.ttf",s)
SANS_B=lambda s: f("DMSans-Bold.ttf",s)
M=140
CITE="Weyand AC et al. JAMA. 2023;329(24):2191-2193. PMID 37367984."
METHOD="NHANES 2003 TO 2020 · US FEMALES AGED 12 TO 21 · MEDIAN AGE 16 (IQR 14 TO 18) · n = 3,490"

def new():
    img=Image.new("RGB",(W,H),C["field"]); return img, ImageDraw.Draw(img,"RGBA")

def chrome(d, eyebrow, page):
    """The parts every card shares. ONE definition, so they cannot drift."""
    d.text((M,150),eyebrow,font=SANS_B(38),fill=C["eyebrow"])
    d.text((M,2492),CITE,font=SANS(30),fill=C["dim"])
    d.text((M,2560),page,font=SANS_B(32),fill=C["eyebrow"])
    # the delta is FILLED, from logo/lockup-primary-delta-outlined.svg
    wm="Dr. Cory Dugan"; w=d.textlength(wm,font=SERIF(44))
    tx=W-M; dx=tx-w-70
    d.polygon([(dx+26,2558),(dx,2612),(dx+52,2612)],fill=C["logo"])
    d.text((tx,2556),wm,font=SERIF(44),fill=C["logo"],anchor="ra")

def panel(d, y0, lines, h=None, size=72):
    h = h or (len(lines)*96+64)
    d.rectangle([M,y0,W-M,y0+h],fill=C["panel"])
    yy=y0+44
    for ln in lines:
        d.text((M+52,yy),ln,font=SERIF(size),fill=(255,255,255)); yy+=96

# ---------------------------------------------------------------- card 1
def card1():
    img,d=new(); chrome(d,"EVIDENCE · IRON DEFICIENCY","SWIPE · 1 OF 5")
    d.text((M,240),"“Iron deficient” is not",font=SERIF(116),fill=C["fg"])
    d.text((M,378),"one measurement.",font=SERIF(116),fill=C["fg"])
    d.text((M,556),"It is a line somebody chose.",font=SANS(50),fill=C["subtle"])
    x=M
    for val,lab,ci,hi in [("17%","below 15 µg/L","95% CI 15.4 to 19.2",False),
                          ("38.6%","below 25 µg/L","95% CI 35.8 to 40.9",True),
                          ("77.5%","below 50 µg/L","95% CI 75.7 to 79.3",False)]:
        d.text((x,860),val,font=SANS_B(140),fill=C["accent"] if hi else C["fg"])
        d.text((x,1030),lab,font=SANS_M(40),fill=C["subtle"])
        d.text((x,1084),ci,font=SANS(32),fill=C["dim"]); x+=640
    d.line([(M,1240),(W-M,1240)],fill=C["rule"],width=4)
    panel(d,1360,["Move that line by 35 µg/L","and the number goes from 17% to 77%."],280,74)
    d.text((M,1760),"Same 3,490 girls and young women. Same blood. Same assay.",font=SANS_M(44),fill=C["muted"])
    d.text((M,1830),"Nobody was re-tested.",font=SANS_M(44),fill=C["muted"])
    d.text((M,2380),METHOD,font=SANS_B(28),fill=C["dim"])
    d.text((M,2428),"ferritin not measured 2011 to 2014",font=SANS(30),fill=C["dim"])
    return img,"s1-hook.png"

# ---------------------------------------------------------------- the curve
def curve(d, top, bot, left, right, big=True):
    """Three published points. The line between them is drawn straight and the
    caption says so, because the paper reports three cut-offs, not a curve."""
    pts=[(15,17.0),(25,38.6),(50,77.5)]
    def px(v): return left+(right-left)*(v-5)/50.0
    def py(v): return bot-(bot-top)*(v/100.0)
    d.line([(left,bot),(right,bot)],fill=C["rule"],width=4)
    d.line([(left,bot),(left,top)],fill=C["rule"],width=4)
    for gy in (0,40,100):
        d.line([(left,py(gy)),(right,py(gy))],fill=C["rule"],width=2)
        d.text((left-24,py(gy)),str(gy),font=SANS(34),fill=C["dim"],anchor="rm")
    path=[(px(x),py(y)) for x,y in pts]
    for i in range(len(path)-1):
        x1,y1=path[i]; x2,y2=path[i+1]; n=26
        for k in range(n):
            if k%2: continue
            a=k/n; b=(k+1)/n
            d.line([(x1+(x2-x1)*a,y1+(y2-y1)*a),(x1+(x2-x1)*b,y1+(y2-y1)*b)],
                   fill=C["accent"],width=6)
    for (xv,yv),(pxx,pyy) in zip(pts,path):
        hi = xv==25
        r = 22 if hi else 15
        d.ellipse([pxx-r,pyy-r,pxx+r,pyy+r],fill=C["accent"] if hi else C["fg"])
        d.text((pxx,pyy-74),f"{yv:g}%",font=SANS_B(60 if big else 48),
               fill=C["fg"],anchor="ma")
        d.text((pxx,bot+26),str(xv),font=SANS(36),fill=C["subtle"],anchor="ma")
    d.text(((left+right)/2,bot+96),"FERRITIN CUT-OFF, µg/L",font=SANS_B(30),
           fill=C["dim"],anchor="ma")
    d.text((left,top-64),"PERCENT BELOW THE CUT-OFF",font=SANS_B(30),fill=C["dim"])

def card2():
    img,d=new(); chrome(d,"FERRITIN · THE MECHANISM","2 OF 5")
    d.text((M,250),"The prevalence is just",font=SERIF(104),fill=C["fg"])
    d.text((M,378),"where you read the axis.",font=SERIF(104),fill=C["fg"])
    curve(d,700,1700,M+90,W-M-40)
    d.text((M,1960),"One curve. Three readings. The line is drawn straight between the",font=SANS(42),fill=C["subtle"])
    d.text((M,2016),"three published cut-offs, because the paper reports those three",font=SANS(42),fill=C["subtle"])
    d.text((M,2072),"and not a distribution.",font=SANS(42),fill=C["subtle"])
    d.text((M,2380),METHOD,font=SANS_B(28),fill=C["dim"])
    return img,"s2-curve.png"

# ---------------------------------------------------------------- card 3
def card3():
    img,d=new(); chrome(d,"HAEMOGLOBIN · DEFINING ANAEMIA","3 OF 5")
    d.text((M,250),"The anaemia line has",font=SERIF(104),fill=C["fg"])
    d.text((M,378),"the same problem.",font=SERIF(104),fill=C["fg"])
    d.text((M,556),"IRON-DEFICIENCY ANAEMIA, FERRITIN HELD BELOW 25 µg/L",font=SANS_B(32),fill=C["dim"])
    rows=[("Haemoglobin below 12.0","6.3%","95% CI 5.2 to 7.4",False),
          ("Haemoglobin below 12.5","11.0%","95% CI 9.5 to 12.6",False),
          ("Haemoglobin below 13.0","17.2%","95% CI 15.3 to 19.1",True)]
    y=700
    for lab,val,ci,hi in rows:
        d.line([(M,y),(W-M,y)],fill=C["rule"],width=3)
        d.text((M,y+52),lab,font=SANS_M(52),fill=C["fg"])
        # measure, do not guess: a fixed x put g/dL on top of the number
        d.text((M+d.textlength(lab,font=SANS_M(52))+16,y+70),"g/dL",
               font=SANS(36),fill=C["dim"])
        d.text((W-M,y+30),val,font=SANS_B(96),fill=C["accent"] if hi else C["fg"],anchor="ra")
        d.text((W-M,y+146),ci,font=SANS(32),fill=C["dim"],anchor="ra")
        y+=250
    d.line([(M,y),(W-M,y)],fill=C["rule"],width=3)
    panel(d,y+120,["12.0 is the WHO line for women.","13.0 is the line used for men."],280,68)
    d.text((M,y+470),"A 1.0 g/dL move nearly triples the count, in the same blood.",font=SANS_M(44),fill=C["muted"])
    d.text((M,2380),METHOD,font=SANS_B(28),fill=C["dim"])
    return img,"s3-haemoglobin.png"

# ---------------------------------------------------------------- card 4
def card4():
    img,d=new(); chrome(d,"THE FINDING","4 OF 5")
    d.text((M,250),"Most iron deficiency",font=SERIF(104),fill=C["fg"])
    d.text((M,378),"never becomes anaemia.",font=SERIF(104),fill=C["fg"])
    d.text((M,760),"83.6%",font=SANS_B(400),fill=C["accent"])
    d.line([(M,1290),(M+520,1290)],fill=C["rule"],width=4)
    d.text((M,1340),"of those with iron deficiency did NOT have",font=SANS_M(50),fill=C["muted"])
    d.text((M,1406),"iron-deficiency anaemia",font=SANS_M(50),fill=C["muted"])
    d.text((M,1490),"95% CI 80.8 to 86.4",font=SANS(36),fill=C["dim"])
    panel(d,1700,["A pathway that starts at haemoglobin","sees the last sixth of the problem."],280,70)
    d.text((M,2060),"and calls the other five sixths normal.",font=SANS_M(46),fill=C["muted"])
    d.text((M,2380),METHOD,font=SANS_B(28),fill=C["dim"])
    return img,"s4-83pc.png"

# ---------------------------------------------------------------- card 5
def card5():
    img,d=new(); chrome(d,"WHAT TO DO WITH THIS","5 OF 5")
    d.text((M,250),"Ask for the number,",font=SERIF(116),fill=C["fg"])
    d.text((M,388),"not the verdict.",font=SERIF(116),fill=C["fg"])
    d.text((M,600),"Then ask which line they are measuring it against.",font=SANS(52),fill=C["subtle"])
    panel(d,780,["Those are two different questions,","and you are owed both answers."],300,72)
    d.text((M,1240),"A reference range is not a health target.",font=SANS_M(48),fill=C["muted"])
    for i,ln in enumerate(["It describes the group that was tested. If a large share of",
                           "them were already deficient, their results sit inside the",
                           "range you are being measured against."]):
        d.text((M,1316+i*64),ln,font=SANS(44),fill=C["subtle"])
    d.line([(M,1600),(W-M,1600)],fill=C["rule"],width=4)
    d.text((M,1660),"If you are still exhausted after being told you are fine,",font=SANS_M(48),fill=C["muted"])
    d.text((M,1728),"that is information, not a contradiction.",font=SANS_M(48),fill=C["muted"])
    return img,"s5-position.png"

# ---------------------------------------------------------------- linkedin
def linkedin():
    img,d=new(); chrome(d,"FERRITIN · THE MECHANISM","")
    d.text((M,250),"The prevalence is just",font=SERIF(104),fill=C["fg"])
    d.text((M,378),"where you read the axis.",font=SERIF(104),fill=C["fg"])
    curve(d,700,1700,M+90,W-M-40)
    d.text((M,1960),"One curve. Three readings. Nobody was re-tested; only the",font=SANS(42),fill=C["subtle"])
    d.text((M,2016),"cut-off moved.",font=SANS(42),fill=C["subtle"])
    d.text((M,2380),METHOD,font=SANS_B(28),fill=C["dim"])
    return img,"linkedin-curve.png"

if __name__=="__main__":
    for fn in (card1,card2,card3,card4,card5,linkedin):
        img,name=fn(); p=os.path.join(OUT,name); img.save(p); print("wrote",name)
