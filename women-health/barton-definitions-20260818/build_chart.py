#!/usr/bin/env python3
"""One cohort, three definitions. The annotated chart, ink surface.

Every figure verified 2026-08-18 against the PubMed abstract via
~/.claude/scripts/pubmed.py, NOT against a summary of it:
    Barton JC, Wiener HW, Barton JC, Acton RT.
    Prevalence of Iron Deficiency Using 3 Definitions Among Women in the US
    and Canada. JAMA Netw Open. 2024;7(6):e2413967. PMID 38848068.

The argument is Martens and DeLoughery's (ASH 2023, PMID 38066931): do not
argue for a better number, show that the current one is an artefact of its own
construction. So the chart holds the POPULATION fixed and moves only the line.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2160, 2700
OUT = os.path.dirname(os.path.abspath(__file__))
FIELD=(11,11,12); FG=(255,255,255); MUTED=(228,229,231); SUBTLE=(200,202,206)
RULE=(42,42,45); ACCENT=(216,207,231); EYEBROW=(138,111,184); GRAPE=(107,79,158)
F=os.path.expanduser("~/Library/Fonts")
def f(n,s): return ImageFont.truetype(os.path.join(F,n),s)
SERIF=lambda s: f("DMSerifDisplay-Regular.ttf",s)
SANS =lambda s: f("DMSans-Regular.ttf",s)
SANS_M=lambda s: f("DMSans-Medium.ttf",s)
SANS_B=lambda s: f("DMSans-Bold.ttf",s)

# One short line each. The first build overflowed the right edge and pushed two
# of the three counts off the card; the explanation moved below the axis.
BARS=[("HEIRS", "TSAT <10% AND ferritin <15",  3.12, "1,957 women"),
      ("WHO",   "ferritin <15",                7.43, "4,659 women"),
      ("IDE",   "ferritin <25",               15.33, "9,611 women")]

img=Image.new("RGB",(W,H),FIELD); d=ImageDraw.Draw(img,"RGBA")
M=140
d.text((M,150),"EVIDENCE · IRON DEFICIENCY",font=SANS_B(38),fill=EYEBROW)
d.text((M,230),"Same 62,685 women.",font=SERIF(120),fill=FG)
d.text((M,370),"Three answers.",font=SERIF(120),fill=FG)
d.text((M,545),"Nobody was re-tested. Only the definition changed.",font=SANS(46),fill=SUBTLE)

TOP,BOT = 760, 1960
MAXV=16.0
BW=380; GAP=(W-2*M-3*BW)//2
for i,(name,defn,val,n) in enumerate(BARS):
    x=M+i*(BW+GAP)
    h=int((BOT-TOP)*(val/MAXV))
    # sequential ramp, grape 700/500/200, monotonic in lightness and validated
    # for CVD separation. The old grey base sat at 1.55:1 against the field and
    # nearly vanished.
    col = [(74,47,112),(138,111,184),(216,207,231)][i]
    d.rectangle([x,BOT-h,x+BW,BOT],fill=col)
    # "Text wears text tokens, never the series color." The bar carries  style-gate-allow: quotes the design system verbatim
    # identity; the number does not repeat it.
    d.text((x,BOT-h-118),f"{val:.2f}%",font=SANS_B(96),fill=FG)
    d.text((x,BOT+34),name,font=SANS_B(52),fill=FG)
    d.text((x,BOT+108),defn,font=SANS(36),fill=SUBTLE)
    d.text((x,BOT+160),n,font=SANS(34),fill=(120,121,128))
d.line([(M,BOT),(W-M,BOT)],fill=RULE,width=4)
d.text((M,BOT+250),"IDE is the ferritin level below which the marrow is already short of iron for making red cells.",
       font=SANS(34),fill=SUBTLE)

# measured, not hardcoded: the first version pinned the box at 170px and
# started the text 34px down, which left the block high and a gap beneath it
_h1,_h2 = SERIF(64), SANS_M(38)
_l1,_l2 = "Nothing about these women changed.", "The prevalence rose 4.9-fold, 95% CI 4.7 to 5.2, P<.001."
_pad, _gap = 44, 20
_b1 = _h1.getbbox(_l1); _b2 = _h2.getbbox(_l2)
_block = (_b1[3]-_b1[1]) + _gap + (_b2[3]-_b2[1])
_top = 2300; _bh = _block + _pad*2
d.rectangle([M,_top,W-M,_top+_bh],fill=GRAPE)
_y = _top + _pad
d.text((M+44,_y-_b1[1]),_l1,font=_h1,fill=FG); _y += (_b1[3]-_b1[1]) + _gap
d.text((M+44,_y-_b2[1]),_l2,font=_h2,fill=(232,226,242))
d.text((M,2545),"Barton JC, Wiener HW, Barton JC, Acton RT. JAMA Netw Open. 2024;7(6):e2413967. PMID 38848068.",
       font=SANS(30),fill=(110,111,117))
d.text((M,2592),"HEIRS screening study, 5 field centres, US and Canada. Women aged 25 and over, mean age 49.6.",
       font=SANS(30),fill=(110,111,117))
# right-align the lockup as a GROUP: measure the wordmark, then place the delta
# to its left. The first build drew the delta on top of the text.
_wm="Dr. Cory Dugan"; _w=d.textlength(_wm,font=SERIF(44))
_tx=W-M; _dx=_tx-_w-70
d.polygon([(_dx+26,2558),(_dx,2612),(_dx+52,2612)],fill=FG)
d.text((_tx,2556),_wm,font=SERIF(44),fill=FG,anchor="ra")

p=os.path.join(OUT,"barton-three-definitions.png")
img.save(p); print("wrote",p,img.size)
