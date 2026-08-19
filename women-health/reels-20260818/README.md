# Reels, 18 Aug 2026

Minimalist animated explainers, 1080x1920, ink surface, with the logo outro.

    python3 build.py            → beat1-bloods-normal-ink.mp4   34s
    python3 build_symptoms.py   → beat-iron-symptoms-ink.mp4    34s

Frames are drawn with PIL, not rendered from a browser. A draw-on line is a
polyline truncated at frame n, so the whiteboard effect is exact and costs
about 30ms a frame instead of 2.7 seconds through headless Chrome.

`build_symptoms.py` IMPORTS the palette, easing, draw-on helper and the whole
outro from `build.py`. Do not copy them into a third file: two copies of the
same constants is how the look drifts.

Surface roles come from surface.ink in the design system's tokens.json v3.0.0,
not from inverting the paper palette. Ink is a peer surface there, not a dark
mode, so grape.800 never appears here: it dies on near-black. The curve takes
surface.ink.accent (grape.200) and the eyebrow takes grape.500.

`wordmark.png` is lockup-primary-delta-outlined.svg rendered white with the
delta polygon REMOVED, because the delta is animated in code from the lockup's
own coordinates. Regenerate it with wordmark.html through headless Chrome if
the lockup ever changes.

Needs: Pillow, numpy, ffmpeg, and DM Sans + DM Serif Display in ~/Library/Fonts.

NOT GATED. Neither reel has been through science-evidence-checker. Nothing on
screen carries a number, a prevalence or a threshold, which is deliberate, but
the symptom list is health content under Cory's name.
