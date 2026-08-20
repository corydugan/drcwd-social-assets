# Reels, 18 Aug 2026

Minimalist animated explainers, 1080x1920, ink surface, with the logo outro.

    python3 build.py            → beat1-bloods-normal-ink.mp4   34s
    python3 build_symptoms.py   → beat-iron-symptoms-ink.mp4    38s

build_symptoms.py clears frames2/ before it renders. build.py does NOT, so if it
is ever shortened, delete the directory first: ffmpeg reads %05d.png until it
hits a gap and would run off the end of the new render into the old one.

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

GATED 2026-08-18 by science-evidence-checker. Nine edits applied, all label
swaps. Reel 1 is now anchored to FERRITIN, because the reference-range argument
holds there and not for haemoglobin: Braat 2024, Lancet Haematol PMID 38432242,
screened reference populations properly and the female haemoglobin limit barely
moved. Reel 2 now says "energy" rather than "oxygen", because four of its six
branches are not oxygen-transport stories. "finding words" and "brittle nails"
were deleted as unsupported; pica replaced the latter.

Nothing on screen carries a number, a prevalence or a threshold. That is
deliberate and it should stay that way.

THAT OBJECTION IS NOW CLOSED, 2026-08-19. The differential beat was built. Reel
2 ran 34s and now runs 38s: at 20s every symptom dims and the four conditions
they also fit are named, and at 25s the three that are on their own an
indication to test come back with a ring on the dot.

Those three are fatigue, restless legs and pica, which is rows 0, 4 and 5. They
are not a judgement call. Auerbach, DeLoughery and Tirnauer, JAMA
2025;333(20):1813-1823, PMID 40159291, says testing is indicated for patients
with anaemia and/or symptoms of iron deficiency, naming those three. PMID checked
through pubmed.py, not taken from a corpus.

The reel is STILL HELD. The differential answered the clinical objection; the
lane objection in the HOLD note is a separate call and is untouched.

STANDING WARNING. The Gemini Notebook `Iron: Diagnosis` corpus returned three
FABRICATED PMIDs during this gate. The papers were real, the identifiers were
not. Run any corpus-supplied PMID through `~/.claude/scripts/pubmed.py exists`
before it enters copy.
