#!/usr/bin/env python3
"""Top and tail any hero clip with the IRON PANEL frame. Cory's format, 19 Aug.

    python3 wrap.py <hero.mp4> <marker number 1-11> [-o out.mp4]

    hook       "Ever had a blood test for iron and not been told what the
               markers were?"                      Cory's words, 19 Aug
    the panel  all eleven markers listed
    the box    wraps the one this episode is about, the rest dim
    the hero   the clip plays, conformed to 1080x1920 at 30fps
    the mark   the delta and the wordmark

WHY THIS EXISTS. The eleven ink episodes each open cold on their own title,
which tells a viewer what they are watching but not where it sits. Cory's
structure opens on the viewer's own experience and then shows them the whole
panel with one marker ringed, so every episode places itself. It is the better
format and it now wraps both series: the ink diagrams and the photoreal heroes
are two versions of the same content, Cory's call, and this frames either.

CONFORMING THE HERO. Heroes arrive at whatever the generator produced. The
Gemini ferritin clip is 720x1280 at 24fps with an AAC track; the ink episodes are
1080x1920 at 30fps and silent. Both are scaled into a 1080x1920 ink-coloured
frame, resampled to 30fps, and given a stereo 48kHz track, silent if they had
none, because the concat filter refuses a mismatched stream layout.

NOT DONE, and deliberately. The Gemini clip carries Google's provenance sparkle
bottom right and it is left alone. Covering it does not remove the provenance,
since SynthID is embedded regardless. It only removes the visible signal.
"""
import os
import subprocess
import sys
from PIL import Image, ImageDraw
import series as S
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = "Ever had a blood test for iron and not been told what the markers were?"

MARKERS = ["Serum ferritin", "Serum iron", "Transferrin saturation",
           "Total iron-binding capacity", "Transferrin", "Haemoglobin",
           "Soluble transferrin receptor", "Mean corpuscular volume",
           "Hepcidin", "Zinc protoporphyrin", "C-reactive protein"]

INTRO_DUR, OUTRO_DUR = 8.4, 4.4
XFADE = 0.4          # hard cuts from a lit photoreal hero to ink read as a fault
ROW0, ROWH = 776, 62
FADE = 0.72


def intro_frame(pick):
    def frame(f):
        img = Image.new("RGB", (S.W, S.H), B.FIELD)
        d = ImageDraw.Draw(img, "RGBA")
        out = 1 - B.seg(f, 7.9, 8.4)

        a = B.seg(f, 0.3, 1.9) * out
        if a > 0:
            fnt = B.SERIF(58)
            y = 296
            for ln in B.wrap(d, HOOK, fnt, S.W - 190):
                d.text((S.W/2, y), ln, font=fnt, fill=B.mix(B.FG, a), anchor="ma")
                y += 76

        a = B.seg(f, 2.2, 3.0) * out
        if a > 0:
            d.text((S.W/2, 690), "THE IRON PANEL", font=B.SANS_B(32),
                   fill=B.mix(B.EYEBROW, a), anchor="ma")

        dim = B.seg(f, 6.0, 6.9)
        for i, name in enumerate(MARKERS):
            t = 2.9 + i * 0.19
            av = B.seg(f, t, t + 0.5) * out
            keep = 1.0 if i == pick else 1 - FADE * dim
            av *= keep
            if av <= 0.01:
                continue
            y = ROW0 + i * ROWH
            d.text((178, y), f"{i+1:02d}", font=B.SANS_B(30),
                   fill=B.mix(B.EYEBROW, av), anchor="lm")
            d.text((252, y), name, font=B.SANS_M(42),
                   fill=B.mix(B.FG, av), anchor="lm")

        # the box around the one this episode is about
        p = B.seg(f, 5.6, 6.6)
        if p > 0 and out > 0.01:
            y = ROW0 + pick * ROWH
            box = [(150, y+27), (150, y-27), (938, y-27), (938, y+27), (150, y+27)]
            path = B.partial(box, p)
            if len(path) > 1:
                d.line(path, fill=B.mix(B.ACCENT, out), width=4, joint="curve")

        a = B.seg(f, 7.0, 7.6) * out
        if a > 0:
            d.text((S.W/2, 1508), "This one.", font=B.SERIF(56),
                   fill=B.mix(B.FG, a), anchor="ma")
        return img
    return frame


def outro_frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    S.outro(img, d, f, 0.5)
    return img


def encode(frames_dir, mp4, dur):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-framerate", str(S.FPS), "-i", os.path.join(frames_dir, "%05d.png"),
                    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                    "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-c:a", "aac", "-b:a", "128k", mp4], check=True)


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                        "-show_entries", "stream=codec_type", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return "audio" in r.stdout


def conform(hero, out):
    vf = ("scale=1080:1920:force_original_aspect_ratio=decrease,"
          "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x0B0B0C,fps=30,setsar=1")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", hero]
    if not has_audio(hero):
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-shortest"]
    cmd += ["-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", out]
    subprocess.run(cmd, check=True)


def render_dir(name, frame_fn, dur):
    fr = os.path.join(HERE, name)
    os.makedirs(fr, exist_ok=True)
    for old in os.listdir(fr):
        os.remove(os.path.join(fr, old))
    for f in range(int(S.FPS * dur)):
        frame_fn(f).save(os.path.join(fr, f"{f:05d}.png"))
    return fr


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(args) < 2:
        print(__doc__); return 2
    hero, pick = args[0], int(args[1]) - 1
    if not 0 <= pick < len(MARKERS):
        print("marker number must be 1 to 11"); return 2
    out = (sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv
           else os.path.join(HERE, f"wrapped-{pick+1:02d}.mp4"))

    tmp = os.path.join(HERE, ".wrap")
    os.makedirs(tmp, exist_ok=True)
    print(f"  marker {pick+1:02d}  {MARKERS[pick]}")
    print("  intro"); encode(render_dir("frames-intro", intro_frame(pick), INTRO_DUR),
                             f"{tmp}/intro.mp4", INTRO_DUR)
    print("  outro"); encode(render_dir("frames-outro", outro_frame, OUTRO_DUR),
                             f"{tmp}/outro.mp4", OUTRO_DUR)
    print("  hero");  conform(hero, f"{tmp}/hero.mp4")
    print("  join")
    # crossfade rather than cut. The offsets are measured off the conformed hero
    # rather than assumed: a generator rarely returns the duration it advertises.
    hd = duration(f"{tmp}/hero.mp4")
    off1 = INTRO_DUR - XFADE
    off2 = INTRO_DUR + hd - 2 * XFADE
    fc = (f"[0:v][1:v]xfade=transition=fade:duration={XFADE}:offset={off1:.3f}[v01];"
          f"[v01][2:v]xfade=transition=fade:duration={XFADE}:offset={off2:.3f}[v];"
          f"[0:a][1:a]acrossfade=d={XFADE}[a01];[a01][2:a]acrossfade=d={XFADE}[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", f"{tmp}/intro.mp4", "-i", f"{tmp}/hero.mp4", "-i", f"{tmp}/outro.mp4",
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out], check=True)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
