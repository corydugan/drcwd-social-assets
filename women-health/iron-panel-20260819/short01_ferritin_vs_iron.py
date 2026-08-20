#!/usr/bin/env python3
"""SHORT 01: serum ferritin against serum iron. Cory's script, 19 Aug.

    hook    "Ever wondered the difference between serum ferritin and serum iron?"
    hero A   the ferritin clip, trimmed, with a brand caption band
    hero B   the serum iron clip, trimmed, with a brand caption band
    turn    "So why do doctors care about ferritin, and not iron?"
    bank     the savings account and the wallet, and which one empties
    mark     the delta and the wordmark

THE ONE CHANGE I MADE TO THE SCRIPT, and it is worth reading. Cory's analogy was
savings against spending. The sharper version is savings against THE WALLET,
because it answers his own question exactly: serum iron is what is in your
wallet at this moment, and it moves with lunch and with the time of day. So the
wallet bar does not drain in the animation, it OSCILLATES while the savings bar
empties underneath it. A wallet that still has money in it is not evidence of
being solvent, and that is the whole reason the ferritin is the number ordered.

Circadian movement in plasma iron: Cao et al, Biol Trace Elem Res 2012, PMID
22198869. Stores emptying before anaemia: Auerbach, DeLoughery and Tirnauer,
JAMA 2025;333(20):1813-1823, PMID 40159291. Both checked through pubmed.py.

THE HERO TRIMS. Cory asked to drop the hepatocyte, so hero A starts after it, on
the shell opening to the iron core. The trim also stops before the clip labels
iron-filled ferritin in the bloodstream as "serum ferritin", which is the claim
this folder's README records as unverified.

THE BAKED CAPTIONS. Both clips carry the generator's own text in the generator's
own typeface and it cannot be removed cleanly from a finished render. The brand
caption band is laid over the bottom of frame where it does the most good. The
real fix is regenerating both with no text at all, and PROMPTS.md holds the
prompts for that.

AU spelling throughout.
"""
import os
import subprocess
import sys
from PIL import Image, ImageDraw
import series as S
import bio
import build as B
import wrap as W

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, ".short01")
XF = 0.4

# FOUR heroes now, generated through veo.py at 1080x1920 with no visible mark.
# One STATE per clip, which is what fixed the first attempt: an 8 second
# generation will not execute "hold, then empty", it renders one continuous
# thing and drops the second instruction. Two states asked for separately both
# arrive.
H = os.path.join(HERE, "_heroes")
# All four are STILLS with a camera move put over them in code, not generated
# clips. Nine Veo attempts never produced a full store and an empty store that
# were the same object; two stills with the first passed in as a reference did
# it on the first try. The iron pair went the same way and it fixed the defect
# Veo would not: its transferrin read as a red blood cell cradling two spheres,
# which in a video about transferrin says the wrong thing entirely. Naming what
# the protein must NOT look like, in a reference-pinned still, fixed it.
#
# COST, verified against Google pricing 19 Aug. Four 2K images at $0.134 is
# $0.536 for the set. The same four shots cost $5.76 across six Veo attempts.
#
# What is lost: the Veo clips carried generated audio and these are silent.
UP = "/Users/corydugan/.claude/uploads/6d9f78d0-740a-42eb-9fc1-bf177df085d1"

# The hook now sits OVER the opening footage rather than on a black card. Six
# seconds of static text before anything moves is exactly where a feed viewer
# leaves, and the words did not need to change to fix it.
#
# Each hero also carries its narration burned in, because most social video is
# watched muted. The solid plate that ate the bottom quarter of frame is gone;
# a gradient scrim carries the text instead.
HEROES = [
    # Cory's original web-UI clip. It establishes that ferritin is something
    # measured IN THE CIRCULATION before the store shots say what it measures.
    # Lower resolution than the rest, and it carries the generator's captions
    # and sparkle; kept because nothing else shows ferritin in the blood.
    # The bloodstream beat does not start until 6.0s in the source, and there
    # are only 4.4 seconds of it. A first cut trimmed from 4.0 and opened on the
    # IRON CORE instead, which is not what Cory asked for. Those 4.4 seconds are
    # stretched to 6.0 so the hook has room to breathe over them. Smooth CG
    # slowed by a third reads as deliberate rather than as slow motion.
    dict(src=f"{UP}/b632b4d0-gemini_generated_video_7D053AFD.mp4", trim=(5.6, 4.4),
         out_len=6.0, num="01", name="SERUM FERRITIN",
         cap="Measured in your blood.", hook=True),
    dict(src=f"{H}/a1-store-full-still.mp4", trim=None,
         num="01", name="SERUM FERRITIN", cap="What it measures is the store."),
    dict(src=f"{H}/a2-store-empty-still.mp4", trim=None,
         num="01", name="SERUM FERRITIN", cap="The same store, run down."),
    dict(src=f"{H}/b1-iron-loose-still.mp4", trim=None,
         num="02", name="SERUM IRON", cap="Iron loose in the plasma, right now."),
    # Transferrin is HELD for the next video, Cory's call 19 Aug. The still is
    # generated and sitting in _stills/b2-carried.png, ready.
]


HOOK = "Ever wondered the difference between serum ferritin and serum iron?"

SAV = (150, 620, 490, 1180)      # the bank: big
WAL = (590, 900, 930, 1180)      # the wallet: small, on purpose


# ------------------------------------------------------------------ the hook
def hook_frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 5.5, 6.0)
    a = B.seg(f, 0.3, 1.9) * out
    if a > 0:
        fnt = B.SERIF(60)
        y = 640
        for ln in B.wrap(d, HOOK, fnt, S.W - 190):
            d.text((S.W/2, y), ln, font=fnt, fill=B.mix(B.FG, a), anchor="ma")
            y += 80
    a = B.seg(f, 2.4, 3.4) * out
    if a > 0:
        d.text((S.W/2, 990), "Both say iron. Only one is ordered.",
               font=B.SANS_M(40), fill=B.mix(B.EYEBROW, a), anchor="ma")
    a = B.seg(f, 4.2, 5.2) * out
    if a > 0:
        d.text((S.W/2, 1100), "Here is what each one is.",
               font=B.SANS(38), fill=B.mix(B.FG_SUBTLE, a), anchor="ma")
    return img


# ------------------------------------------------------------------ the turn
def turn_frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 5.5, 6.0)
    a = B.seg(f, 0.3, 1.6) * out
    if a > 0:
        d.text((S.W/2, 700), "So why do doctors care",     font=B.SERIF(62), fill=B.mix(B.FG, a), anchor="ma")
        d.text((S.W/2, 786), "about ferritin, and not iron?", font=B.SERIF(62), fill=B.mix(B.FG, a), anchor="ma")
    a = B.seg(f, 2.2, 3.2) * out
    if a > 0:
        d.text((S.W/2, 930), "It is iron either way.", font=B.SANS_M(42),
               fill=B.mix(B.FG_SUBTLE, a), anchor="ma")
    a = B.seg(f, 3.8, 4.8) * out
    if a > 0:
        d.text((S.W/2, 1060), "THE FIRST THING YOU LOSE IS THE STORE",
               font=B.SANS_B(32), fill=B.mix(B.EYEBROW, a), anchor="ma")
    return img


# ------------------------------------------------------------------ the bank
def bank_frame(f):
    import math
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    out = 1 - B.seg(f, 11.5, 12.0)
    t = f / S.FPS

    drain = B.seg(f, 4.6, 8.6)
    sav_fill = B.seg(f, 1.4, 2.6) - 0.88 * drain
    # the wallet does not drain, it MOVES. That is the whole point of it.
    wob = 0.13 * math.sin(t * 2.7) + 0.07 * math.sin(t * 5.3 + 1.1)
    wal_fill = B.seg(f, 1.8, 3.0) * (0.80 + wob)

    S.column(d, SAV, B.seg(f, 0.2, 1.4), max(sav_fill, 0.0), out)
    S.column(d, WAL, B.seg(f, 0.6, 1.8), max(wal_fill, 0.0), out)
    S.caplabel(d, SAV, "THE BANK", "ferritin", B.seg(f, 2.6, 3.4) * out)
    S.caplabel(d, WAL, "THE WALLET", "serum iron", B.seg(f, 2.8, 3.6) * out)

    a = B.seg(f, 8.8, 9.6) * out
    if a > 0:
        d.text((320, 576), "EMPTIES FIRST", font=B.SANS_B(30),
               fill=B.mix(B.EYEBROW, a), anchor="ma")
        d.text((760, 856), "STILL LOOKS FINE", font=B.SANS_B(30),
               fill=B.mix(B.EYEBROW, a), anchor="ma")

    a = B.seg(f, 9.8, 10.8) * out
    if a > 0:
        d.line([(110, 1390), (110 + (S.W-220)*B.seg(f, 9.6, 10.4), 1390)],
               fill=B.mix(B.RULE, a), width=4)
        d.text((S.W/2, 1428), "Check the bank.", font=B.SERIF(62), fill=B.mix(B.FG, a), anchor="ma")
        d.text((S.W/2, 1512), "Not the wallet.", font=B.SERIF(62), fill=B.mix(B.FG, a), anchor="ma")

    S.narrate(d, f, [
        (0.4, 4.4, "Serum iron is what is in your wallet today."),
        (4.6, 8.8, "Ferritin is what is in the bank."),
        (9.0, 11.4, "In any shortage, the savings go first."),
    ], out)
    return img


def outro_frame(f):
    img = Image.new("RGB", (S.W, S.H), B.FIELD)
    d = ImageDraw.Draw(img, "RGBA")
    S.outro(img, d, f, 0.5)
    return img


# ------------------------------------------------- the brand overlay on a hero
def scrim(d, y0, y1, top_down=False, strength=232):
    """A gradient wash so type stays legible over footage without a solid plate.
    The plate this replaces covered the bottom quarter of every shot."""
    for y in range(int(y0), int(y1)):
        t = (y - y0) / max(1.0, (y1 - y0))
        a = int(strength * ((1 - t) if top_down else t) ** 1.4)
        d.line([(0, y), (S.W, y)], fill=B.FIELD + (a,))


def overlay_frames(spec, dur, out_dir):
    """One RGBA frame per video frame: the scrim, the eyebrow, the burned-in
    caption, and on the first hero the hook laid over the footage."""
    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, f))
    n = int(S.FPS * dur)
    for i in range(n):
        img = Image.new("RGBA", (S.W, S.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img, "RGBA")

        if spec.get("hook"):
            a = S.pulse(i, 0.3, 1.7, 4.0, 4.8)
            if a > 0.01:
                scrim(d, 120, 900, top_down=True, strength=int(238 * a))
                fnt = B.SERIF(58)
                y = 300
                for ln in B.wrap(d, HOOK, fnt, S.W - 300):
                    d.text((S.W/2, y), ln, font=fnt, fill=B.mix(B.FG, a), anchor="ma")
                    y += 78
                b = S.pulse(i, 1.9, 2.9, 4.0, 4.8)
                if b > 0.01:
                    d.text((S.W/2, y + 26), "Both say iron. Only one is ordered.",
                           font=B.SANS_M(38), fill=B.mix(B.EYEBROW, b), anchor="ma")
            lab_in = 4.6
        else:
            lab_in = 0.5

        a = S.pulse(i, lab_in, lab_in + 0.7, dur - 0.7, dur - 0.1)
        if a > 0.01:
            scrim(d, 1420, S.H, strength=int(236 * a))
            d.text((110, 1530), f"{spec['num']}   {spec['name']}",
                   font=B.SANS_B(34), fill=B.mix(B.EYEBROW, a))
            fnt = B.SANS_M(46)
            y = 1592
            for ln in B.wrap(d, spec["cap"], fnt, S.W - 220):
                d.text((110, y), ln, font=fnt, fill=B.mix(B.FG, a))
                y += 58
        img.save(os.path.join(out_dir, f"{i:05d}.png"))
    return n


def hero(spec, out):
    src, trim = spec["src"], spec["trim"]
    src_len = W.duration(src) if trim is None else trim[1]
    dur = spec.get("out_len", src_len)
    stretch = dur / src_len
    start = 0.0 if trim is None else trim[0]
    ov = os.path.join(TMP, "ov-" + os.path.basename(out).replace(".mp4", ""))
    overlay_frames(spec, dur, ov)

    vf = (f"setpts={stretch:.5f}*PTS," if abs(stretch - 1) > 0.01 else "") + \
         ("scale=1080:1920:force_original_aspect_ratio=decrease,"
          "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x0B0B0C,fps=30,setsar=1")
    # a stretched clip takes its audio from the bed, not from itself: retiming
    # video and audio together is a second problem for no gain here
    silent = (not W.has_audio(src)) or abs(stretch - 1) > 0.01
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-ss", str(start), "-t", str(src_len), "-i", src,
           "-framerate", str(S.FPS), "-i", os.path.join(ov, "%05d.png")]
    if silent:
        cmd += ["-f", "lavfi", "-i",
                "anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd += ["-filter_complex", f"[0:v]{vf}[base];[base][1:v]overlay=0:0[v]",
            "-map", "[v]", "-map", "2:a" if silent else "0:a",
            "-t", str(dur),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", out]
    subprocess.run(cmd, check=True)


def section(name, fn, dur):
    fr = W.render_dir(f"frames-{name}", fn, dur)
    mp4 = f"{TMP}/{name}.mp4"
    W.encode(fr, mp4, dur)
    return mp4, dur


def main():
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(HERE, "short01-ferritin-vs-iron.mp4")

    print("  heroes")
    hero_clips = []
    for i, spec in enumerate(HEROES):
        out_i = f"{TMP}/hero{i}.mp4"
        hero(spec, out_i)
        hero_clips.append((out_i, W.duration(out_i)))
    print("  turn");  c, dc = section("turn", turn_frame, 6.0)
    print("  bank");  e, de = section("bank", bank_frame, 12.0)
    print("  outro"); g, dg = section("outro", outro_frame, 4.4)

    clips = hero_clips + [(c, dc), (e, de), (g, dg)]

    print("  join")
    inputs, parts, run, prev = [], [], 0.0, "0:v"
    apart, aprev = [], "0:a"
    for i, (p, dur) in enumerate(clips):
        inputs += ["-i", p]
    for i in range(1, len(clips)):
        run = (clips[0][1] if i == 1 else run) + (clips[i-1][1] if i > 1 else 0) - XF
        tag = f"[v{i}]" if i < len(clips)-1 else "[v]"
        parts.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={XF}:offset={run:.3f}{tag}")
        prev = tag.strip("[]")
        atag = f"[a{i}]" if i < len(clips)-1 else "[a]"
        apart.append(f"[{aprev}][{i}:a]acrossfade=d={XF}{atag}")
        aprev = atag.strip("[]")
    fc = ";".join(parts + apart)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs +
                   ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out],
                  check=True)
    # THE BED. Before this, sound arrived at 4s and vanished at 10s: peak 20793
    # then thirty-three seconds of nothing, which reads worse than silent
    # throughout. The ambience from the opening clip is looped under the whole
    # piece at low level so it never drops out. It is the sound Cory already
    # picked, just continuous.
    print("  bed")
    total = sum(d for _, d in clips) - XF * (len(clips) - 1)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", HEROES[0]["src"], "-vn", "-ac", "2", "-ar", "48000",
                    f"{TMP}/bed.wav"], check=True)
    bedded = out.replace(".mp4", "-bedded.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out,
                    "-stream_loop", "-1", "-i", f"{TMP}/bed.wav",
                    "-filter_complex",
                    # the opening clip's own audio is the SOURCE of the bed, so
                    # leaving it at full doubled it: 20980 peak for six seconds
                    # against 8800 for the rest. Ducked so the level is even.
                    f"[0:a]volume=0.30[src];"
                    f"[1:a]volume=0.50,atrim=0:{total:.2f},asetpts=N/SR/TB,"
                    f"afade=in:st=0:d=1.2,afade=out:st={total-2.0:.2f}:d=2.0[bed];"
                    f"[src][bed]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                    bedded], check=True)
    os.replace(bedded, out)
    print("wrote", out)


if __name__ == "__main__":
    main()
