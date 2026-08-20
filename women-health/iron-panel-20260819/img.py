#!/usr/bin/env python3
"""Generate a still through the Gemini image models, then move a camera over it.

    python3 img.py --prompt-file p.txt --out shot.png [--model flash|pro|banana]
    python3 img.py --animate shot.png --out shot.mp4 --seconds 5 [--move push|drift]

WHY THIS EXISTS. Nine Veo clips cost $8.00 and six were binned, because every
failure was a TIME failure: an 8 second generation will not perform "hold, then
empty", it renders one continuous thing and drops the second instruction.

A still has no time in it. The two shots this series actually needs, a ferritin
store full and the same store empty, are both static states. Nothing has to
move. So generate the state as an image, and put the movement in code where it
is deterministic and free to change.

Iteration cost is the thing that matters, not unit cost. A clip you bin costs a
dollar; a still you bin costs cents.

The camera move uses series.ramp, so it eases the same way everything else in
this series eases.

VERIFIED PRICES, read from ai.google.dev/gemini-api/docs/pricing on 2026-08-19.
Not estimated, not remembered.

    gemini-3-pro-image      1K or 2K   $0.134    4K   $0.24
      the same, batch tier  1K or 2K   $0.067    4K   $0.12
    gemini-3.1-flash-image  1K $0.067   2K $0.101   4K $0.151
    gemini-2.5-flash-image  1K $0.039   batch $0.0195

    veo-3.1 at 1080p, per second   standard $0.40   fast $0.12   lite $0.08
      so an 8 second clip           $3.20            $0.96        $0.64

The matched ferritin pair that finally worked cost $0.268 as two 2K pro images.
The same pair cost $3.84 across four Veo attempts and never matched. Fourteen
times the price for a worse result, and that ratio is the whole argument for
generating a state rather than a change.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

BASE = "https://generativelanguage.googleapis.com/v1beta"
MODELS = {"flash": "gemini-3.1-flash-image",
          "pro": "gemini-3-pro-image",
          "banana": "nano-banana-pro-preview"}


def key():
    with open(os.path.expanduser("~/.claude/secrets/google-ai.env")) as fh:
        for line in fh:
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("GEMINI_API_KEY not found")


def generate(prompt, model, out, ref=None, size=None):
    """ref pins the new image to an existing one. This is the whole reason a
    still beats a clip here: the full store and the empty store have to be the
    SAME shell, and a reference image makes that an instruction rather than a
    hope. Veo has the same feature; at a dollar a try it is expensive to use."""
    k = key()
    parts = [{"text": prompt}]
    if ref:
        parts.insert(0, {"inlineData": {"mimeType": "image/png",
                                        "data": base64.b64encode(open(ref, "rb").read()).decode()}})
    cfg = {"aspectRatio": "9:16"}
    if size:
        cfg["imageSize"] = size
    req = urllib.request.Request(
        f"{BASE}/models/{MODELS[model]}:generateContent?key={k}",
        data=json.dumps({
            "contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": cfg},
        }).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}\n{e.read().decode()[:800].replace(k, '<KEY>')}",
              file=sys.stderr)
        sys.exit(2)
    for part in d.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        blob = part.get("inlineData") or part.get("inline_data")
        if blob:
            with open(out, "wb") as fh:
                fh.write(base64.b64decode(blob["data"]))
            print("wrote", out, os.path.getsize(out), "bytes")
            return 0
    print(json.dumps(d)[:900]); sys.exit("no image in response")


def animate(src, out, seconds, move, fps=30):
    """A slow camera over a still. The crop rect shrinks (push) or slides
    (drift) across the source, and every frame is resampled to 1080x1920."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import subprocess
    from PIL import Image
    import series as S

    im = Image.open(src).convert("RGB")
    W, H = im.size
    n = int(fps * seconds)
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), ".kb")
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))

    for i in range(n):
        p = S.ramp(i, 0.0, seconds, ease="in_out_cubic")   # no jolt at either end
        if move == "push":
            z = 1.0 - 0.16 * p                 # 16% in over the shot
            cw, ch = W * z, H * z
            x, y = (W - cw) / 2, (H - ch) / 2
        else:                                   # drift, right to left
            z = 0.88
            cw, ch = W * z, H * z
            x = (W - cw) * (1 - p)
            y = (H - ch) / 2
        im.crop((int(x), int(y), int(x + cw), int(y + ch))) \
          .resize((1080, 1920), Image.LANCZOS) \
          .save(os.path.join(tmp, f"{i:05d}.png"))

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-i", os.path.join(tmp, "%05d.png"),
                    "-f", "lavfi", "-i",
                    "anullsrc=channel_layout=stereo:sample_rate=48000",
                    "-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", "-c:a", "aac", "-b:a", "128k", out], check=True)
    print("wrote", out)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--animate")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="flash", choices=list(MODELS))
    ap.add_argument("--seconds", type=float, default=5.0)
    ap.add_argument("--move", default="push", choices=["push", "drift"])
    ap.add_argument("--ref", help="an existing image the new one must match")
    ap.add_argument("--size", choices=["1K", "2K", "4K"])
    a = ap.parse_args()
    if a.animate:
        return animate(a.animate, a.out, a.seconds, a.move)
    return generate(a.prompt or open(a.prompt_file).read().strip(), a.model,
                    a.out, a.ref, a.size)


if __name__ == "__main__":
    sys.exit(main())
