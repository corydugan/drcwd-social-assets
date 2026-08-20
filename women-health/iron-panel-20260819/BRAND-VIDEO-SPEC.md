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

### Beat 5, the address settles in, 0.8s

The lockup names him. This beat is the only part of the closing that does
business, and it is deliberately quiet: an address, not a call to action. A
shouted CTA on all eleven episodes of a series turns a body of work into an
advert.

Below the grape rule, on the same centre line, one line of text fades up. It is a
**fade**, the only one in the closing, which is what makes it read as a settling
rather than another beat of the animation.

    The line reads   drcorydugan.com

Set in **DM Sans Regular**, not the serif. The serif is the wordmark and nothing
else on this card may share it. Colour is `#E4E5E7`, not pure white, so it sits
clearly below the name in the hierarchy rather than competing with it. Set the
tracking open, about 0.08em, because a lowercase URL at small size closes up.

Size no smaller than **34px on the 1080 frame**. The design system floor is 32px
for anything intended to be read; a URL is the one string on screen a viewer may
try to type, so it clears the floor rather than sitting on it.

It sits 40 units below the grape rule, before the 1.56 scale.

**Use the bare domain.** Not a path, not a campaign URL, not a redirect.
`drcorydugan.com/iron-protocol` currently serves a redirect to the iron guide,
and a redirect baked into eleven permanent videos is a broken link waiting for a
site tidy-up. The bare domain cannot rot.

**No handle.** Handles differ per platform and these files are cut once and
posted everywhere.

### The campaign variant, used sparingly

For a video that carries a real offer, and for no more than one video in any
series, the address line may carry a destination in front of it:

    The iron guide  ·  drcorydugan.com

Same type, same colour, same size. The separator is a middot with a space either
side. Never an em dash or an en dash. If this variant is used, Beat 5 runs 1.0s
rather than 0.8s to let the extra words land.

### Revised closing timeline

    0.0 - 1.2   triangle outline draws
    1.1 - 1.7   triangle fills solid
    1.6 - 2.5   wordmark wipes in
    2.5 - 3.2   grape rule expands from the centre
    3.2 - 4.0   the address fades up
    4.0 - 4.6   hold on the finished sign-off

Total 4.6 seconds, or 4.8 with the campaign variant. The last frame of every
video is the completed sign-off: triangle, wordmark, rule, address.

### Summary of the closing timeline (superseded, see the revised timeline above)

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
3. The closing lockup runs all five beats, in order, and the final frame is the
   completed sign-off including the address line.
7. The address line reads a bare domain, resolves without a redirect, and is set
   in DM Sans at 34px or larger.
4. No grape-800 #352051 appears anywhere on the ink field.
5. Every transition into and out of a card is a crossfade, not a cut.
6. A text search of every string in the video finds no em dash, no en dash, and
   none of the four banned words.

---

## 9. VOICE OVER, AND THE LAST SECONDS

The eleven episodes ship silent. `S.narrate()` in `series.py` is on-screen
captions with start and end times, not audio, which means **the script and its
timings already exist**. A voice track is a read of those slots, not a new
writing job.

### Whose voice

Cory's own, recorded. A synthetic read on a video whose entire claim is
"a health scientist explains your blood panel" undercuts the claim. Text to
speech is acceptable for a rough cut to check timing, never for a shipped file.

A Google Cloud TTS key is on file if a rough cut is wanted. Use an Australian
English voice, never a US one, on a channel whose spelling is already AU.

### THE RULE FOR THE LAST SECONDS

**Nothing is spoken over the closing lockup. Not the name, not the address.**

The lockup is a signature, and a signature is silent. Speaking the name while
the name is being drawn is redundant, and speaking a URL is the one thing that
turns the sign-off from an address into an advert, which Beat 5 was written to
avoid. Nobody has ever typed a URL they heard.

So the last seconds run:

    the final narrated line       spoken
    the on-screen closing card    spoken, after a pause of about 0.4s
    a beat of silence             about 0.4s
    the closing lockup            SILENT, all five beats

If a music bed is used it may continue under the lockup and should resolve on
the final frame. It must not start there, because a bed arriving at the sign-off
reads as an advert break.

### Episode 1, written out

    18.2 - 21.4   "Haemoglobin only falls once the store is gone."
    21.8 - 24.8   "The store runs down, long before the blood does."
    24.8 - 25.2   silence
    25.2 - 29.8   lockup, silent

The line at 21.8 is the one already on screen as the closing card. Speaking it
is the only doubling permitted in the whole video, because it is the thesis and
it is the line people screenshot.

### The closing line of every episode

Each is already written and on screen. This is the last thing said in each file.

| Episode | The line |
|---|---|
| 01 ferritin | The store runs down, long before the blood does. |
| 02 serum iron | It rises after a meal, and drifts across the day. |
| 03 TSAT | A low share is one of the two ways deficiency is called. |
| 04 TIBC | So the room goes up while the iron on board does not. |
| 05 transferrin | Learn the carrier and three of them stop being separate. |
| 06 haemoglobin | Anaemia is where the shortage ends, not where it starts. |
| 07 sTfR | It is less disturbed by inflammation than ferritin is. |
| 08 MCV | A red cell lives for months, so this one moves last of all. |
| 09 hepcidin | Inflammation raises it, whether or not you need what is behind it. |
| 10 ZPP | The wrong molecule builds up, and counting it is the test. |
| 11 CRP | CRP is what tells you which of the two you are looking at. |

### Reading direction

Read down, not up. These are statements of how something works, not
announcements. The last word of each line is where the pitch drops. Leave the
pause before the closing line longer than feels comfortable, because that pause
is what makes the line land rather than merely arrive.

### Acceptance check, added

8. If the file carries audio, the closing lockup is silent of speech, and the
   final narrated word ends at least 0.3 seconds before the lockup begins.
