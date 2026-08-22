# reel-sources

The build source for each reel in `../reels/`. One generator per reel.

Before 2026-08-22 none of the fifteen finished videos under
`CAREER/Business/CONTENT/` had a source. Every one of them was unrebuildable:
changing a single word meant starting over. This directory exists so that
never happens again.

## How a generator works

    python3 beat1-bloods-normal-ink.gen.py A ../reels/beat1-bloods-normal-ink.mp4

It emits one SVG per frame, rasterises each with `rsvg-convert`, and stitches
them with ffmpeg at 25fps. No browser and no Node. Fonts come from the local
system, so DM Serif Display and DM Sans must be installed.

The argument is the typeface variant: `A` is DM Serif Display, which is the
brand face and the one used. `B` is Chalkduster and was rejected.

Every timing in the piece is a number in the file. Changing one is an edit,
not a rebuild.

## The rule that stops the bug this file was born from

Three elements once shared the caption slot at y=1560 and two shared the
headline slot at y=360. The first caption had no exit at all, so every later
line drew on top of it. Anything sharing a screen position MUST go through
`seg(t, in0, in1, out0, out1)`, which gives it an explicit exit. Verify by
sampling the slot between occupants: it has to read zero.

The wipe spans the content column, not the screen. Starting at x=0 left
centred text invisible until the mask had crossed the margin.
