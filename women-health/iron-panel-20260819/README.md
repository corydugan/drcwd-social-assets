# IRON PANEL, a ten-part series. Started 19 Aug 2026.

One episode per biomarker, 1080x1920, ink surface, same open and same outro.

    python3 ep01_ferritin.py     → ep01-ferritin-ink.mp4      29s
    python3 ep02_serum_iron.py   → ep02-serum-iron-ink.mp4    29s
    python3 ep03_tsat.py         → ep03-tsat-ink.mp4          29s
    python3 ep04_tibc.py         → ep04-tibc-ink.mp4          30s
    python3 ep05_transferrin.py  → ep05-transferrin-ink.mp4   30s
    python3 ep06_haemoglobin.py  → ep06-haemoglobin-ink.mp4   31s
    python3 ep07_stfr.py         → ep07-stfr-ink.mp4          31s
    python3 ep08_mcv.py          → ep08-mcv-ink.mp4           31s
    python3 ep09_hepcidin.py     → ep09-hepcidin-ink.mp4      31s
    python3 ep10_zpp.py          → ep10-zpp-ink.mp4           31s
    python3 ep11_crp.py          → ep11-crp-ink.mp4           31s

`wrap.py` top-and-tails ANY hero clip with Cory's format, 19 Aug:

    python3 wrap.py <hero.mp4> <marker 1-11> -o out.mp4

    hook  ->  the eleven listed  ->  a box round this one  ->  hero  ->  the mark

It conforms the hero to 1080x1920 at 30fps, pads to the ink field, gives it a
stereo track whether or not it had one, and crossfades rather than cuts. A hard
cut from a lit photoreal hero to a black ink outro reads as a fault.

This format supersedes the cold title-card opening the eleven ink episodes use.
It places every episode inside the whole panel instead of announcing itself.

`bio.py` holds the biological primitives: THE FLEET, the red cell, the receptor
cell and the tick bar. It is the BioRender layer for this pipeline, drawn from
the ink palette so a schematic is made of the same lines as the charts.

`series.py` holds everything the episodes share: the title card, the running
narration line, the column primitive, the outro and the renderer. It imports the
palette, fonts, easing and logo geometry from `../reels-20260818/build.py`
rather than copying them. With ten episodes coming, a second copy of the brand
constants would drift ten times faster than it did with two reels.

`series.render()` CLEARS the frame directory before drawing. ffmpeg reads
%05d.png until it hits a gap, so a previous longer render left in place gets
read straight off the end of the new one.

## Standing rules for the series

- No number, prevalence or threshold on screen. Same as the reels.
- AU spelling. haemoglobin, anaemia, coeliac. The brief was written US and the
  series is BRAND lane, so it is converted, not copied.
- Every claim about staging or interpretation carries a PMID in the episode
  docstring, checked through `~/.claude/scripts/pubmed.py`, never taken from a
  Gemini Notebook corpus. That corpus returned three fabricated PMIDs during the
  18 Aug gate.

## Anchors used so far

- Auerbach, DeLoughery, Tirnauer. JAMA 2025;333(20):1813-1823. PMID 40159291.
  Iron deficiency progresses from low stores to anaemia, which is the staging
  episode 01 is built on. Also names fatigue, pica and restless legs as symptoms
  for which testing is indicated on their own.
- Nemeth et al. Science 2004. PMID 15514116. Hepcidin binds ferroportin and
  induces its internalisation. For episode 09.
- Ganz T. Physiol Rev 2013. PMID 24137020. Systemic iron homeostasis.
- Camaschella C. Haematologica 2020. PMID 31949017. Iron metabolism revisited.

## The eleven, in panel order. Cory's call, 19 Aug.

    01  Serum ferritin                  BUILT   the store, and what empties first
    02  Serum iron                      BUILT   fleet 1 of 4: the seats that are taken
    03  Transferrin saturation          BUILT   fleet 2 of 4: taken as a share of all
    04  Total iron-binding capacity     BUILT   fleet 3 of 4: capacity rises as iron falls
    05  Transferrin                     BUILT   fleet 4 of 4: one protein, three numbers
    06  Haemoglobin                     BUILT   the last thing in the sequence to move
    07  Soluble transferrin receptor    BUILT   cells putting up antennae
    08  Mean corpuscular volume         BUILT   cells built short, and it shows late
    09  Hepcidin                        BUILT   the switch on the gut door
    10  Zinc protoporphyrin             BUILT   the wrong metal in the seat
    11  C-reactive protein              BUILT   ADDED 19 Aug. Why a normal ferritin
                                                can still be a deficient one.

    All eleven built 19 Aug 2026. None published. They sit in
    CAREER/Business/CONTENT/2-DRAFT/ pending Cory's review.

## Two series, not one

Cory's call, 19 Aug: the ink episodes and the photoreal Gemini heroes are two
versions of similar content, and both stand. wrap.py frames either.

A note on the heroes. The Gemini clip carries Google's provenance sparkle at the
bottom right and it is LEFT ALONE. Covering it does not remove the provenance,
because SynthID is embedded regardless; it only removes the visible signal of
it. Generate without the mark, or disclose. For a scientist the disclosure is
worth more than the concealment.

TWO THINGS TO CHECK BEFORE ANY HERO SHIPS. The ferritin clip labels iron-FILLED
ferritin in the bloodstream as "Serum ferritin". Intracellular ferritin is
iron-rich; whether circulating ferritin carries a full core is a different
question and three PubMed passes did not settle it. The one paper that surfaced
points the other way: Renaud et al, J Submicrosc Cytol Pathol 1991, PMID 1764677,
on apoferritin, the iron-FREE form, in the hepatocyte secretory pathway.
UNVERIFIED, and it needs settling. Second, the hero carries its own captions in
its own typeface. Generating the hero WITHOUT text and adding brand-styled
labels would make it his rather than the generator's.

## Two drawing treatments, and the line between them

Cory's call, 19 Aug: organs looser and more organic. So:

    RULED     carriers, columns, tick bars, the sequence line, the door frame.
              Anything that is machinery or measurement.
    ORGANIC   liver, gut, cells, red cells, the porphyrin ring. Anything alive.

The organic bodies come from bio.blob, whose wobble is three fixed harmonics
keyed off a seed and never random. A random outline would redraw differently
every render, so reshooting one episode would stop it matching the frame beside
it in the next.

Organic bodies carry a soft grape wash at about 0.15 alpha. Drawn as bare
outlines they read as unfinished beside the filled red cells.

CRP is the eleventh on Cory's call. Ferritin is an acute phase reactant, so
episode 01 cannot be taken at face value without it, and the brief's line about
ferritin showing "exactly" how much iron is stored was dropped for that reason.
Episode 11 is where that debt is paid.

THE FLEET was Cory's call over the brief's three competing metaphors. The brief
used buses for saturation, trucks for capacity and boats for transferrin, for
what is one protein measured four ways. One fleet now runs across 02 to 05,
redrawn each time with a different part lit. Two seats a carrier, because
transferrin binds up to two atoms of ferric iron.

## The style gate

The first pass over episode 01 was run by hand, case-sensitively, and missed a
banned word at the start of a sentence. It is a script now:

    python3 ~/.claude/scripts/style_gate.py . --au

It exits non-zero on a hit, so it cannot scroll past unnoticed the way the grep
did. A line carrying the marker the script names is exempt, and that exists for
documentation and for verbatim quotation, not for convenience.

Quotations are not an exemption from AU spelling. Three paraphrases of the JAMA review carried US
spelling on 19 Aug and were rewritten rather than quoted, so nothing on the page
is US-spelled. Cory's call the same day: all AUS spelling, everywhere.
