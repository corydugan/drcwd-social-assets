# Regenerating the heroes with no text

Both clips carry the generator's captions in the generator's typeface, and they
are the loudest thing on screen. Text baked into a finished render cannot be
removed cleanly, so the fix is upstream: generate with no text at all, and let
`short01_ferritin_vs_iron.py` and `wrap.py` lay brand-styled labels over it.

Two reasons beyond the look.

**The captions are wrong in one place.** The ferritin clip labels the blue
spheres "Iron atoms (Fe3+)". Fe3+ is an ION. An atom is neutral by definition,
and a ferric ion is not one. Nobody outside the field will notice, and every
haematologist will.

**The labels are not yours to defend.** Anything on screen reads as Cory's claim
once his mark is on the end of it. A caption he did not write and cannot cite is
a liability in a way that a caption in DM Sans, written against a PMID, is not.

Ask for **9:16, 1080x1920, at least 30fps** as well. Both current clips came back
720x1280 at 24fps, which means every one gets upscaled and resampled.

---

## Hero 01, serum ferritin

    A photoreal 3D medical animation, vertical 9:16, 1080x1920, 30fps, no text,
    no labels, no captions, no lettering of any kind anywhere in the frame.

    A single ferritin protein shell fills the centre of frame, its cage-like
    surface catching warm light. The camera pushes slowly through an opening in
    the shell to reveal the packed iron core inside: hundreds of small dark
    spheres, densely stacked, filling the cavity completely.

    Hold on the full core. Then the core slowly EMPTIES from the centre outward
    until the shell stands almost hollow, with only a scatter of spheres left
    against its inner wall.

    Warm amber and bronze palette, shallow depth of field, no on-screen text.

The empty ending matters. There is no shot of a depleting store in the current
clip, and that is the one image the whole argument turns on.

## Hero 02, serum iron

    A photoreal 3D medical animation, vertical 9:16, 1080x1920, 30fps, no text,
    no labels, no captions, no lettering of any kind anywhere in the frame.

    Inside a blood vessel, red blood cells drift past. Scattered single ions
    glint in the plasma between them. Transferrin proteins move through frame
    and the ions dock into them, TWO ions to each protein, never more.

    The camera holds while proteins pass, some carrying two, some carrying one,
    some carrying none.

    Cool blue accents against warm vessel walls, shallow depth of field, no
    on-screen text.

Two ions per protein is not decoration. Transferrin binds up to two atoms of
ferric iron, and the ink series counts it that way in every fleet diagram, so
the photoreal version has to agree with it.

## The provenance mark

If the tier in use stamps the sparkle bottom right, it stays. Covering it does
not remove the provenance, because SynthID is embedded regardless; it removes
only the visible signal of it. Generate without the mark, or disclose that the
3D sequence is AI-generated and clinically reviewed. For a scientist the
disclosure is worth more than the concealment.

---

# What happened when these were run, 19 Aug 2026

Both prompts were run through `veo.py` on veo-3.1-fast at 1080x1920, 8 seconds,
$0.96 each. The API delivered exactly what it promised on format: 1080x1920,
NO visible sparkle. It did not deliver on content.

**Hero A came back half right.** The shell and the packed core are strong for
the first three seconds. Then it blows out into a white light source and the
camera flies through a glowing tunnel. The core never empties. The one shot the
whole argument needs is the one that did not arrive.

**Hero B failed.** The blue forms read as bacteria rather than ions docking into
a carrier, nothing shows two per protein, and the palette came back pink instead
of a warm vessel with cool accents.

## The diagnosis, and it is a prompt problem not a model problem

Both prompts asked for a SEQUENCE: hold on the full core, THEN empty it. Pass
through frame, THEN dock. An eight second generation does not reliably execute
staged direction; it renders one continuous motion and picks whichever stage it
likes. The instruction that gets dropped is always the second one.

Three fixes, in order of how likely they are to work:

1. **One state per clip.** Generate FULL as its own clip and EMPTY as its own
   clip, then cut between them. Two clips at $0.96 rather than one that tries to
   be both.
2. **First and last frame control.** The Gemini API takes a first frame and a
   last frame and interpolates between them. Give it the full core and the empty
   shell as stills and the emptying becomes an instruction it cannot drop.
3. **Reference images**, up to three, so the second clip matches the first
   rather than inventing a new palette. That is what fixed nothing about hero B
   being pink.

Until one of those is tried, Cory's original web-UI clips are the better
footage. They are lower resolution and they carry captions, and they are still
clearer.
