import os, sys, math, subprocess, shutil
MODE = sys.argv[1]                      # 'A' or 'B'
OUT  = sys.argv[2]
FPS, DUR = 25, 34.0
W, H = 1080, 1920
D = os.path.dirname(OUT)
FR = os.path.join(D, f"frames{MODE}")
shutil.rmtree(FR, ignore_errors=True); os.makedirs(FR)

INK="#0B0B0C"; PAPER="#FFFFFF"; GRAPE="#8a6fb8"; GRAPEF="#6b4f9e"; MUTED="#8C8E94"
if MODE=="A":
    HEAD="DM Serif Display"; BODY="DM Sans"; HW=0
else:
    HEAD="Chalkduster"; BODY="Chalkduster"; HW=1

def ease(t):                              # smooth 0..1
    return 0 if t<=0 else 1 if t>=1 else t*t*(3-2*t)
def win(t,a,b):
    return ease((t-a)/(b-a)) if b>a else (1.0 if t>=a else 0.0)
def seg(t,i0,i1,o0,o1):
    """opacity envelope: fades IN over i0..i1, OUT over o0..o1. Every element
    that shares a screen position with another MUST use this, or they stack."""
    return win(t,i0,i1)*(1.0-win(t,o0,o1))

# bell curve, y down
def bell(x, mu=540, sd=150, amp=430, base=1180):
    return base - amp*math.exp(-((x-mu)**2)/(2*sd*sd))
PTS=[(x, bell(x)) for x in range(120, 961, 6)]
CURVE="M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in PTS)
CLEN=sum(math.dist(PTS[i],PTS[i+1]) for i in range(len(PTS)-1))

L, R = 110, 970                            # the content column
def wipe(idx, p):
    """Clip rect that grows L->R across the CONTENT COLUMN, not the screen.
    Starting at x=0 meant centred text stayed invisible until the mask had
    crossed ~200px of empty margin, so lines appeared to arrive late and then
    snap in. Spanning L..R makes the reveal track the actual glyphs."""
    return f'<clipPath id="w{idx}"><rect x="{L}" y="0" width="{(R-L)*p:.1f}" height="{H}"/></clipPath>'

def frame(t):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{INK}"/>')
    defs=[]; body=[]
    # --- headline ---
    p1=win(t,0.15,1.9); p2=win(t,1.5,3.1); p3=win(t,2.7,3.9)
    fade = 1.0 - win(t,9.0,10.2)          # fully out, it shares y=360 with NORMAL FERRITIN
    hcol = PAPER
    hsize = 86 if MODE=="A" else 74
    defs += [wipe(1,p1), wipe(2,p2), wipe(3,p3)]
    body.append(f'<g opacity="{fade:.2f}" fill="{hcol}" font-family="{HEAD}" font-size="{hsize}" text-anchor="middle">')
    body.append(f'<g clip-path="url(#w1)"><text x="540" y="360">“Your bloods came</text></g>')
    body.append(f'<g clip-path="url(#w2)"><text x="540" y="460">back normal.”</text></g></g>')
    body.append(f'<g opacity="{fade:.2f}" clip-path="url(#w3)"><text x="540" y="540" fill="{MUTED}" font-family="{BODY}" font-size="34" text-anchor="middle">What that sentence actually means</text></g>')
    # --- curve ---
    pc=win(t,4.0,8.6)
    if pc>0:
        off=CLEN*(1-pc)
        body.append(f'<path d="{CURVE}" fill="none" stroke="#d8cfe7" stroke-width="4" stroke-linecap="round" stroke-dasharray="{CLEN:.0f}" stroke-dashoffset="{off:.1f}"/>')
        body.append(f'<line x1="120" y1="1180" x2="960" y2="1180" stroke="#3A3A40" stroke-width="3" opacity="{pc:.2f}"/>')
    p4=win(t,5.0,7.0); o4=seg(t,5.0,7.0,9.4,10.2); defs.append(wipe(4,p4))
    body.append(f'<g clip-path="url(#w4)" opacity="{o4:.2f}"><text x="540" y="1560" fill="{PAPER}" font-family="{BODY}" font-size="38" text-anchor="middle">A reference range is built by testing</text>'
                f'<text x="540" y="1612" fill="{PAPER}" font-family="{BODY}" font-size="38" text-anchor="middle">a population.</text></g>')
    # --- verticals + labels ---
    pv=win(t,10.2,11.4)
    if pv>0:
        for X in (300, 780):
            body.append(f'<line x1="{X}" y1="{1180-540*pv:.0f}" x2="{X}" y2="1180" stroke="{GRAPE}" stroke-width="5" stroke-linecap="round"/>')
    p5=win(t,10.6,12.2); p6=win(t,11.0,12.6); defs += [wipe(5,p5), wipe(6,p6)]
    if p5>0:
        body.append(f'<g clip-path="url(#w5)"><text x="540" y="360" fill="{PAPER}" font-family="{BODY}" font-weight="700" font-size="52" text-anchor="middle" letter-spacing="2">“NORMAL FERRITIN”</text></g>')
    if p6>0:
        body.append(f'<g clip-path="url(#w6)"><text x="540" y="424" fill="{MUTED}" font-family="{BODY}" font-size="34" text-anchor="middle">the middle 95% of a group assumed healthy</text></g>')
    p7=win(t,11.6,13.6); defs.append(wipe(7,p7))
    o7=seg(t,11.6,13.6,15.4,16.2)
    if o7>0.01:
        body.append(f'<g clip-path="url(#w7)" opacity="{o7:.2f}"><text x="540" y="1560" fill="{PAPER}" font-family="{BODY}" font-size="38" text-anchor="middle">A line is drawn around the middle of them.</text></g>')
    # --- grape fill on the left shoulder ---
    pf=win(t,16.2,17.8)
    if pf>0:
        xe=300+(540-300)*pf
        pl=[(x,bell(x)) for x in range(300, int(xe)+1, 4)] or [(300,bell(300))]
        d="M300,1180 L"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pl)+f" L{xe:.1f},1180 Z"
        body.append(f'<path d="{d}" fill="{GRAPEF}" opacity="0.85"/>')
    p8=win(t,16.6,18.8); p9=win(t,18.4,20.2); defs += [wipe(8,p8), wipe(9,p9)]
    o8=seg(t,16.6,18.8,21.4,22.2)
    if o8>0.01:
        body.append(f'<g clip-path="url(#w8)" opacity="{o8:.2f}"><text x="540" y="1560" fill="{PAPER}" font-family="{BODY}" font-size="38" text-anchor="middle">But a large share of the women tested</text>'
                    f'<text x="540" y="1612" fill="{PAPER}" font-family="{BODY}" font-size="38" text-anchor="middle">were already deficient.</text></g>')
    o9=seg(t,18.4,20.2,29.4,30.2)
    if o9>0.01:
        body.append(f'<g clip-path="url(#w9)" opacity="{o9:.2f}"><text x="150" y="1268" fill="{GRAPE}" font-family="{BODY}" font-size="30">already iron deficient,</text>'
                    f'<text x="150" y="1308" fill="{GRAPE}" font-family="{BODY}" font-size="30">and inside the range</text></g>')
    # --- closing ---
    pa=win(t,22.4,24.4); pb=win(t,23.4,25.6); defs += [wipe(10,pa), wipe(11,pb)]
    if pa>0:
        body.append(f'<line x1="120" y1="1430" x2="960" y2="1430" stroke="#3A3A40" stroke-width="2" opacity="{pa:.2f}"/>')
        body.append(f'<g clip-path="url(#w10)"><text x="540" y="1520" fill="{PAPER}" font-family="{HEAD}" font-size="{46 if MODE=="A" else 40}" text-anchor="middle">Normal describes the population.</text></g>')
    if pb>0:
        body.append(f'<g clip-path="url(#w11)"><text x="540" y="1580" fill="{PAPER}" font-family="{HEAD}" font-size="{46 if MODE=="A" else 40}" text-anchor="middle">It does not describe a healthy person.</text></g>')
    # --- signoff ---
    ps=win(t,30.0,31.6)
    if ps>0:
        o=ps
        # SIGNOFF is the BRAND mark, not the personal name. Changed 2026-08-27,
        # Cory's call: the voiceover is a female TTS voice, and closing on
        # "Dr Cory Dugan" implied the narrator was him. The brand mark does not
        # make that claim. Matches the .brandbar lockup on the concept cards.
        body.append(f'<g opacity="{o:.2f}"><polygon points="392,980 424,1032 360,1032" fill="{PAPER}"/>'
                    f'<text x="452" y="1032" fill="{PAPER}" font-family="{HEAD}" font-size="58">drCWDugan</text></g>')
        # dim everything else
        s.append(f'<rect width="{W}" height="{H}" fill="{INK}" opacity="{o*0.97:.2f}"/>')
        s.append(f'<g opacity="{o:.2f}"><polygon points="392,980 424,1032 360,1032" fill="{PAPER}"/>'
                 f'<text x="452" y="1032" fill="{PAPER}" font-family="{HEAD}" font-size="58">drCWDugan</text></g>')
        s.append('</svg>'); return "".join(s[:2]+["<defs>"+"".join(defs)+"</defs>"]+body+s[2:])
    s.append("<defs>"+"".join(defs)+"</defs>")
    s.extend(body); s.append('</svg>')
    return "".join(s)

N=int(FPS*DUR)
for i in range(N):
    t=i/FPS
    p=os.path.join(FR,f"f{i:05d}.svg")
    open(p,"w").write(frame(t))
print("svg frames:",N)
subprocess.run(f'cd "{FR}" && for f in *.svg; do rsvg-convert -w {W} -h {H} "$f" -o "${{f%.svg}}.png"; done', shell=True, check=True)
print("png done")
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),
                "-i",os.path.join(FR,"f%05d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","20",OUT],check=True)
print("video:",OUT)
