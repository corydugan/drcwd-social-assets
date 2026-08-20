# drCWDugan video branding: the opening and closing requirement

Paste this into the Google AI Studio app as a standing requirement. It describes
the two things every video the app produces must carry, and it is written so a
code-generating model can implement it without seeing the brand repo.

Every value below is taken from `drcwd-design-system/colors_and_type.css`, which
is the single source for the brand. Nothing here is approximate.

---

## 1. THE RULE

**Every video opens on a title card and closes on the logo lockup.** No
exceptions, no "just this once". A clip that ships without both is not finished.

The opening card states what the viewer is about to watch. The closing lockup is
the signature, and it is the same four beats every time so that people come to
recognise it before the name is legible.

---

## 2. THE SURFACE

Video uses the INK surface, never the paper one. Ink is a peer surface in this
brand, not a dark mode, so do not derive it by inverting light values.

    field / background      #0B0B0C     ink-max
    primary text            #FFFFFF     paper
    secondary text          #E4E5E7     ink-200
    tertiary / captions     #C8CACE     ink-300
    hairline rules          #2A2A2D     ink-900
    accent, TYPE ONLY       #D8CFE7     grape-200
    eyebrow micro-caps      #8A6FB8     grape-500
    the logo lockup         #FFFFFF     paper

**grape-800 #352051 is the primary brand grape on the paper surface and it must
never appear on ink.** It dies on a near-black field. On ink the accent is
grape-200 and the eyebrow is grape-500, and grape-500 is the rare colour, spent
by hand rather than sprinkled.

When a colour fades, fade it toward the FIELD colour, not toward white or toward
transparent-over-white. On a near-black field that difference is the difference
between a fade and a glow.

---

## 3. THE TYPE

    display / headlines     DM Serif Display, regular weight, tracking -0.02em
    everything else         DM Sans, regular / medium / bold
    figures and numerals    IBM Plex Sans

Both DM faces are on Google Fonts. **DM Sans has no tabular-figures table**, so
any `font-variant-numeric: tabular-nums` on it is a silent no-op and columns of
numbers will not line up. Set numerals in IBM Plex Sans.

Never letterspace DM Serif Display positive. Never use DM Serif Display below
about 36px on a 1080-wide frame; it is a display face and it falls apart small.

---

## 4. THE OPENING CARD

Canvas 1080 x 1920, field #0B0B0C. Three elements, stacked, centred.

    EYEBROW     y 286   DM Sans Bold 32px   #8A6FB8   uppercase
                        e.g. "IRON PANEL   01"
    TITLE       y 342   DM Serif Display 82px   #FFFFFF
                        The subject. One line.
    SUBTITLE    y 466   DM Sans regular 38px   #C8CACE
                        One short line saying what it is in plain words.

**The title must shrink to fit, never clip.** Try 82px, then 74, then 66, then
58, and use the first size whose measured width is under 930px. A title such as
"Total iron-binding capacity" overruns at the display size and getting cut at
both edges is the failure this rule exists to stop.

Timing, in seconds from the start of the card:

    0.2 - 1.4   eyebrow fades in
    0.5 - 1.9   title fades in
    1.6 - 2.8   subtitle fades in
    hold, then the card clears over 0.5s before the content starts

Use a smoothstep curve for every fade, `t * t * (3 - 2t)`. Nothing in this brand
moves linearly and nothing bounces.

---

## 5. THE CLOSING LOCKUP

This is the signature and it is FOUR BEATS, always in this order. It runs 3.6
seconds. The field is #0B0B0C and nothing else is on screen.

### Beat 1, the triangle draws itself, 1.2s

An equilateral-ish triangle, drawn as a single continuous white stroke that
travels around its own outline from one vertex, back to where it began. It is
not a fade-in and it is not a scale-up. It is a line being drawn.

Geometry, in the lockup's own coordinate space, then multiplied by a scale of
1.56 to reach the video frame:

    vertex A    (32, 38)      the apex
    vertex B    (9, 80)       lower left
    vertex C    (55, 80)      lower right

Stroke 6px, colour #FFFFFF, round joins. Implement the draw-on by walking the
closed path, measuring cumulative segment length, and truncating at the fraction
of total length the beat has reached. Do not fake it with a mask wipe; the
travelling endpoint is the whole point.

### Beat 2, the triangle fills, 0.6s, overlapping beat 1 by 0.1s

The outline becomes a solid white triangle. Fill alpha ramps 0 to 255 on a
smoothstep. The stroke stays underneath.

### Beat 3, the wordmark wipes in, 0.9s

To the right of the triangle, on the same optical baseline, the name wipes in
left to right. It is a **wipe**, revealing the mark column by column, not a fade
and not a slide.

The wordmark sits at (77.3, 36.3) in lockup units, 432.3 wide and 59.0 tall,
before the 1.56 scale. Set in DM Serif Display, white.

    The name reads   Dr. Cory Dugan

Render the wordmark once as a white image with the triangle REMOVED from it, and
animate the triangle separately in code. If both the image and the code carry a
triangle they will fight over alignment and the result is a double delta.

### Beat 4, the rule expands, 0.7s

A 3px rule in #8A6FB8 grows outward from the centre point, symmetrically in both
directions, until it spans the full width of the triangle-plus-wordmark group.
It sits 44 units below the wordmark's baseline box, before scaling.

Then hold. The last frame of every video is the completed lockup on the field.

### Summary of the closing timeline

    0.0 - 1.2   triangle outline draws
    1.1 - 1.7   triangle fills solid
    1.6 - 2.5   wordmark wipes in
    2.5 - 3.2   grape rule expands from the centre
    3.2 - 3.6   hold on the finished lockup

The whole group is centred horizontally in the 1080 frame and sits at about 46%
of frame height, which keeps it clear of a phone's bottom UI.

---

## 6. HANDING OVER TO AND FROM THE CONTENT

Do not hard-cut between the content and either card. **Crossfade 0.4 seconds.** A
hard cut from lit footage to a near-black field reads as a fault rather than a
transition.

If the content carries audio and the cards do not, give the cards a silent
stereo track at 48kHz before joining, or the concatenation will refuse the
mismatched stream layout.

---

## 7. HARD RULES THAT APPLY TO EVERYTHING ON SCREEN

- **No em dashes and no en dashes.** Anywhere. Use a comma, brackets, or a full
  stop.
- **Never the words** prove, proven, fact, absolute.  <!-- style-gate-allow: names them to ban them -->
- **Australian spelling.** haemoglobin, anaemia, coeliac, colour, organise.
- **No number, prevalence, percentage or threshold on screen** unless it has been
  checked against a named source. A picture of a direction beats a figure that
  has to be defended.
- Every scientific claim carries a citation in the source file, even though the
  citation never appears on screen.

---

## 8. ACCEPTANCE CHECKS

A video is finished when all of these pass:

1. Frame is 1080 x 1920. Output frame rate is stated and consistent.
2. The opening card's title is fully visible, not clipped at either edge.
3. The closing lockup runs all four beats, in order, and the final frame is the
   completed lockup.
4. No grape-800 #352051 appears anywhere on the ink field.
5. Every transition into and out of a card is a crossfade, not a cut.
6. A text search of every string in the video finds no em dash, no en dash, and
   none of the four banned words.
