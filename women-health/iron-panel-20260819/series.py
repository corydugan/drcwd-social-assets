#!/usr/bin/env python3
"""The IRON PANEL series kit: everything ten episodes share, in one place.

Palette, fonts, easing, the draw-on helper and the logo geometry are IMPORTED
from reels-20260818/build.py. They are not copied. Two files drawing the same
brand from two copies of the same constants is how the look drifts, and with ten
episodes coming that risk is ten times what it was with two reels.

Each episode is then a short file: a storyboard and a frame function. Anything
an episode does NOT define itself comes from here, so the series stays one thing.

Every episode:
  - opens on the same card, IRON PANEL and a two-digit number
  - closes on the same delta, wordmark and rule
  - carries no number, prevalence or threshold on screen, same as the reels
"""
import math
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "reels-20260818"))
import build as B                                   # noqa: E402

W, H, FPS = 1080, 1920, 30
OUTRO_LEN = 3.6          # from the delta starting to the rule finishing


def titlecard(d, f, num, title, sub, out=1.0):
    a = B.seg(f, 0.2, 1.4) * out
    if a > 0:
        d.text((W/2, 286), f"IRON PANEL   {num}", font=B.SANS_B(32),
               fill=B.mix(B.EYEBROW, a), anchor="ma")
    a = B.seg(f, 0.5, 1.9) * out
    if a > 0:
        # shrink to fit rather than clip. "Total iron-binding capacity" overruns
        # 1080 at the display size and would have been cut at both edges.
        fnt = B.SERIF(82)
        for size in (82, 74, 66, 58):
            fnt = B.SERIF(size)
            if d.textlength(title, font=fnt) <= W - 150:
                break
        d.text((W/2, 342), title, font=fnt, fill=B.mix(B.FG, a), anchor="ma")
    a = B.seg(f, 1.6, 2.8) * out
    if a > 0:
        d.text((W/2, 466), sub, font=B.SANS(38), fill=B.mix(B.FG_SUBTLE, a), anchor="ma")


def narrate(d, f, slots, out=1.0, y=1700):
    """The running line at the foot of frame. slots: (start, end, text)

    It WRAPS. The reels wrapped their narration and the first cut of this kit did
    not, so a line one word too long was silently clipped at both edges of the
    1080 frame instead of running to a second line."""
    fnt = B.SANS_M(40)
    for a0, b0, txt in slots:
        if a0 <= f/FPS < b0:
            al = min(B.smooth((f/FPS-a0)/0.5), B.smooth((b0-f/FPS)/0.5), 1.0) * out
            if al <= 0:
                continue
            lines = B.wrap(d, txt, fnt, W - 170)
            yy = y - 30 * (len(lines) - 1)
            for ln in lines:
                d.text((W/2, yy), ln, font=fnt, fill=B.mix(B.FG_MUTED, al), anchor="ma")
                yy += 58


def column(d, box, draw_p, fill_frac, alpha=1.0, accent=None):
    """A vertical store: an outline that draws on, and a level that rises or falls.

    box is (x0, ytop, x1, ybot). draw_p runs the outline on as a truncated
    polyline, the same trick the reels use for the curve and the delta."""
    x0, ytop, x1, ybot = box
    accent = accent or B.ACCENT
    if draw_p > 0:
        pts = [(x0, ybot), (x0, ytop), (x1, ytop), (x1, ybot), (x0, ybot)]
        path = B.partial(pts, draw_p)
        if len(path) > 1:
            d.line(path, fill=B.mix(B.FG_SUBTLE, alpha), width=4)
    if fill_frac > 0.001 and alpha > 0.01:
        h = (ybot - ytop) * min(fill_frac, 1.0)
        if h > 4:          # below this the level rectangle inverts and PIL raises
            d.rectangle([x0+5, ybot-h, x1-5, ybot-2], fill=accent + (int(235*alpha),))


def caplabel(d, box, big, sub, alpha):
    """the label under a column"""
    if alpha <= 0.01:
        return
    x0, _, x1, ybot = box
    cx = (x0 + x1) / 2
    d.text((cx, ybot + 26), big, font=B.SANS_B(38), fill=B.mix(B.FG, alpha), anchor="ma")
    d.text((cx, ybot + 76), sub, font=B.SANS(30), fill=B.mix(B.FG_SUBTLE, alpha), anchor="ma")


def outro(img, d, f, t0):
    """the delta, the wordmark and the rule, identical to the 18 Aug reels"""
    tri = [(B.ux(x), B.uy(y)) for x, y in B.DELTA_U]
    p = B.seg(f, t0, t0 + 1.2)
    if p > 0:
        path = B.partial(tri + [tri[0]], p)
        if len(path) > 1:
            d.line(path, fill=B.FG, width=6, joint="curve")
    fl = B.seg(f, t0 + 1.1, t0 + 1.7)
    if fl > 0:
        d.polygon(tri, fill=B.FG + (int(255*fl),))
    wm = B.seg(f, t0 + 1.6, t0 + 2.5)
    if wm > 0:
        tw, th = int(B.WM_U[2]*B.S), int(B.WM_U[3]*B.S)
        strip = B.WORDMARK.resize((tw, th), Image.LANCZOS)
        k = max(1, int(tw*wm)); c = strip.crop((0, 0, k, th))
        img.paste(c, (int(B.ux(B.WM_U[0])), int(B.uy(B.WM_U[1]))), c)
    rl = B.seg(f, t0 + 2.5, t0 + 3.2)
    if rl > 0:
        y = B.uy(B.WM_U[1] + B.WM_U[3]) + 44
        half = (B.CONTENT_W * B.S / 2) * rl
        d.line([(W/2 - half, y), (W/2 + half, y)], fill=B.EYEBROW, width=3)


# ============================================================== the timeline kit
#
# Added 19 Aug 2026. Before this, every beat in every episode was a bare
# B.seg(f, a, b) call with the numbers written inline, and every fade-in-then-out
# was seg(a,b) * (1 - seg(c,d)) spelled out by hand. Thirteen episodes in, the
# timings were the hardest thing to read and the easiest thing to get wrong.
#
# Nothing here replaces B.seg. Existing episodes keep working untouched. This is
# what new ones should use.

def _bounce_out(t):
    n, dd = 7.5625, 2.75
    if t < 1/dd:      return n*t*t
    if t < 2/dd:      t -= 1.5/dd;  return n*t*t + 0.75
    if t < 2.5/dd:    t -= 2.25/dd; return n*t*t + 0.9375
    t -= 2.625/dd;    return n*t*t + 0.984375


EASINGS = {
    "linear":      lambda t: t,
    "smooth":      lambda t: t*t*(3 - 2*t),          # the old B.seg curve
    "smoother":    lambda t: t*t*t*(t*(t*6 - 15) + 10),
    "in_quad":     lambda t: t*t,
    "out_quad":    lambda t: 1 - (1-t)**2,
    "in_out_quad": lambda t: 2*t*t if t < 0.5 else 1 - ((-2*t+2)**2)/2,
    "in_cubic":    lambda t: t**3,
    "out_cubic":   lambda t: 1 - (1-t)**3,
    "in_out_cubic":lambda t: 4*t**3 if t < 0.5 else 1 - ((-2*t+2)**3)/2,
    "out_quart":   lambda t: 1 - (1-t)**4,
    "out_expo":    lambda t: 1.0 if t >= 1 else 1 - 2**(-10*t),
    "in_expo":     lambda t: 0.0 if t <= 0 else 2**(10*t - 10),
    "out_back":    lambda t: 1 + 2.70158*(t-1)**3 + 1.70158*(t-1)**2,
    "in_back":     lambda t: 2.70158*t**3 - 1.70158*t*t,
    "out_elastic": lambda t: 1.0 if t >= 1 else (0.0 if t <= 0 else
                   2**(-10*t) * math.sin((t*10 - 0.75) * (2*math.pi/3)) + 1),
    "out_bounce":  _bounce_out,
    "out_sine":    lambda t: math.sin(t*math.pi/2),
    "in_sine":     lambda t: 1 - math.cos(t*math.pi/2),
}


def ramp(f, t0, t1, ease="smooth"):
    """B.seg with a choice of curve. 0 before t0, 1 after t1."""
    if t1 <= t0:
        return 1.0 if f/FPS >= t1 else 0.0
    t = max(0.0, min(1.0, (f/FPS - t0) / (t1 - t0)))
    return EASINGS[ease](t)


def pulse(f, t0, t1, t2=None, t3=None, ease="smooth"):
    """In at t0-t1, out at t2-t3. The seg(a,b) * (1 - seg(c,d)) idiom, named.
    With no t2 it never leaves."""
    a = ramp(f, t0, t1, ease)
    if t2 is None:
        return a
    return a * (1 - ramp(f, t2, t3 if t3 is not None else t2 + 0.4, ease))


class Timeline:
    """Beats declared as data, evaluated at a frame.

        tl = Timeline()
        tl.cue("title",  0.3, 1.9, ease="out_cubic")
        tl.cue("bar",    3.0, 5.2, out=(9.0, 9.8))
        tl.stagger("row", 7.4, 0.5, n=6, every=2.2)

        v = tl.at(f)
        if v["title"] > 0: ...
        for i in range(6):
            a = v[f"row{i}"]
    """

    def __init__(self):
        self._cues = {}

    def cue(self, name, t0, t1, ease="smooth", out=None):
        self._cues[name] = (t0, t1, ease, out)
        return self

    def stagger(self, prefix, t0, dur, n, every, ease="smooth", out=None):
        """n copies of the same beat, each starting `every` seconds after the
        last. Six symptom rows, eight carriers, eleven markers: this is the
        shape most of the series is made of."""
        for i in range(n):
            s = t0 + i * every
            o = None if out is None else (out[0] + i * every, out[1] + i * every)
            self.cue(f"{prefix}{i}", s, s + dur, ease, o)
        return self

    def value(self, f, name):
        t0, t1, ease, out = self._cues[name]
        return pulse(f, t0, t1, *(out if out else (None, None)), ease=ease)

    def at(self, f):
        return {k: self.value(f, k) for k in self._cues}

    def end(self):
        """The last moment anything is still moving. Useful for setting DUR
        from the storyboard rather than the other way round."""
        last = 0.0
        for t0, t1, _, out in self._cues.values():
            last = max(last, t1, out[1] if out else 0.0)
        return last


def render(here, stem, frame_fn, dur, motion_blur=1):
    """Clear the frame directory, draw every frame, encode.

    The clear is not optional. ffmpeg reads %05d.png until it hits a gap, so a
    previous longer render left in place gets read straight off the end of this
    one and into the old footage."""
    fr = os.path.join(here, f"frames-{stem}")
    os.makedirs(fr, exist_ok=True)
    for old in os.listdir(fr):
        os.remove(os.path.join(fr, old))
    n = int(FPS * dur)
    for f in range(n):
        if motion_blur > 1:
            # temporal supersampling: draw N sub-frames inside the frame's own
            # slice of time and average them. Frame functions take f as a float
            # already, because everything downstream divides it by FPS.
            acc = None
            for k in range(motion_blur):
                arr = np.asarray(frame_fn(f + k / motion_blur), dtype=np.float32)
                acc = arr if acc is None else acc + arr
            img = Image.fromarray((acc / motion_blur).astype(np.uint8))
        else:
            img = frame_fn(f)
        img.save(os.path.join(fr, f"{f:05d}.png"))
        if f % 200 == 0:
            print(f"  {f}/{n}", flush=True)
    mp4 = os.path.join(here, f"{stem}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", os.path.join(fr, "%05d.png"), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
                    mp4], check=True)
    print("wrote", mp4)
    return mp4
