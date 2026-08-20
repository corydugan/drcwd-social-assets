#!/usr/bin/env python3
"""Generate a hero clip with Veo through the Gemini API, not the web page.

    python3 veo.py --prompt-file p.txt --out hero.mp4 [--model lite|fast|standard]
                   [--seconds 8] [--resolution 1080p] [--aspect 9:16] [--dry-run]

WHY. The web UI stamps a visible sparkle on the output and returns 720x1280 at
24fps. The API returns the same model with NO visible mark, at 1080p or 4K, and
takes reference images so clips can be made to match each other.

SynthID is still embedded, invisibly, on every tier including this one. It is not
removable and removing it is not permitted. "No watermark" means no VISIBLE mark.

COST, from Google's pricing page, per second of output:
    lite      $0.08      standard 1080p   $0.40
    fast      $0.12      standard 4K      $0.60

Every run prints the estimate BEFORE it submits, and --dry-run stops there. This
spends real money on Cory's account and a silent spend is not acceptable.

The key comes from ~/.claude/secrets/google-ai.env, which is the derived cache;
Bitwarden is the source of truth. The key is never printed, never logged, and
never written into an output file.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE = "https://generativelanguage.googleapis.com/v1beta"
MODELS = {
    "lite":     ("veo-3.1-lite-generate-preview", 0.08),
    "fast":     ("veo-3.1-fast-generate-preview", 0.12),
    "standard": ("veo-3.1-generate-preview",      0.40),
}


def key():
    env = os.path.expanduser("~/.claude/secrets/google-ai.env")
    with open(env) as fh:
        for line in fh:
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("GEMINI_API_KEY not found in " + env)


def post(url, payload, k):
    req = urllib.request.Request(
        f"{url}?key={k}", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:900]
        # the key can appear in a URL echoed back; never let it reach a log
        print(f"HTTP {e.code}\n{body.replace(k, '<KEY>')}", file=sys.stderr)
        sys.exit(2)


def get(url, k):
    sep = "&" if "?" in url else "?"
    with urllib.request.urlopen(f"{url}{sep}key={k}", timeout=120) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="fast", choices=list(MODELS))
    ap.add_argument("--seconds", type=int, default=8)
    ap.add_argument("--resolution", default="1080p")
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    prompt = a.prompt or open(a.prompt_file).read().strip()
    model, rate = MODELS[a.model]
    print(f"model      {model}")
    print(f"clip       {a.seconds}s  {a.resolution}  {a.aspect}")
    print(f"ESTIMATE   ${rate * a.seconds:.2f} USD at ${rate:.2f}/second")
    if a.dry_run:
        print("dry run, nothing submitted")
        return 0

    k = key()
    op = post(f"{BASE}/models/{model}:predictLongRunning",
              {"instances": [{"prompt": prompt}],
               "parameters": {"aspectRatio": a.aspect,
                              "resolution": a.resolution,
                              "durationSeconds": a.seconds}}, k)
    name = op.get("name")
    if not name:
        print(json.dumps(op)[:800]); sys.exit("no operation returned")
    print("submitted, polling")

    for i in range(120):
        time.sleep(10)
        st = get(f"{BASE}/{name}", k)
        if st.get("done"):
            if "error" in st:
                print(json.dumps(st["error"])[:800]); sys.exit(3)
            resp = st.get("response", {})
            vids = (resp.get("generateVideoResponse", {}).get("generatedSamples")
                    or resp.get("generatedSamples") or resp.get("videos") or [])
            if not vids:
                print(json.dumps(resp)[:1200]); sys.exit("no video in response")
            uri = (vids[0].get("video", {}).get("uri") or vids[0].get("uri"))
            req = urllib.request.Request(f"{uri}{'&' if '?' in uri else '?'}key={k}")
            with urllib.request.urlopen(req, timeout=600) as r, open(a.out, "wb") as fh:
                fh.write(r.read())
            print("wrote", a.out, os.path.getsize(a.out), "bytes")
            return 0
        print(f"  {(i+1)*10}s", flush=True)
    sys.exit("timed out")


if __name__ == "__main__":
    sys.exit(main())
