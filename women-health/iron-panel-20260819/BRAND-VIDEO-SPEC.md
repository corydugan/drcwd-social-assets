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

---

## 10. THE CLOSING LOCKUP, RESOLVED TO ABSOLUTE PIXELS

Section 5 describes the lockup in lockup-SVG units. This section is the same
lockup with every unit resolved to pixels on the 1080 x 1920 frame, derived from
`reels-20260818/build.py` and `series.py`. It is written to be pasted whole into
any tool that has to reproduce the animation without reading the repo.

### Canvas and field

    Frame          1080 x 1920, portrait
    Frame rate     30 fps
    Field colour   #0B0B0C, filling the whole frame, nothing else on screen
    Ink white      #FFFFFF
    Grape rule     #8A6FB8
    Address grey   #E4E5E7

### Easing, applied to all five beats

    smoothstep:  p = t * t * (3 - 2t),  where t is 0 at the beat's start
                 and 1 at its end, clamped to that range.

No other curve appears in the closing. No bounce, no elastic, no overshoot.

### Geometry, in pixels, fixed

    Triangle       apex          (185.4,  882.7)
                   bottom left   (149.5,  948.2)
                   bottom right  (221.3,  948.2)
                   stroke 6px, joint "curve", colour #FFFFFF
                   71.8 wide, 65.5 tall

    Wordmark box   x 256.1, y 880.0, width 674.4, height 92.0
                   the words "Dr. Cory Dugan" set in DM Serif Display, white
                   supplied as a PNG with the triangle REMOVED from it

    Grape rule     y 1016.0, from x 149.5 to x 930.5 at full extent
                   780.9 long, 3px, colour #8A6FB8

    Address line   centred on x 540, baseline 40px below the rule
                   DM Sans Regular, 34px minimum, #E4E5E7, tracking 0.08em

The whole group spans x 149.5 to x 930.5 and is centred horizontally. It sits at
about 46 percent of frame height, which keeps it clear of a phone's bottom UI.

### Beat 1, the triangle draws itself. 0.0 to 1.2 seconds.

A single continuous white stroke travels around the triangle's own outline and
returns to where it began. It is not a fade and not a scale.

Path, in this order:

    start at the APEX      (185.4, 882.7)
    down and left to       (149.5, 948.2)
    across to              (221.3, 948.2)
    back up to the APEX    (185.4, 882.7)

**Truncate the path by ARC LENGTH, not by vertex count.** At eased progress p,
draw the first p of the total 221.2px perimeter. The three sides are 74.7,
71.8 and 74.7 pixels, so the pen crosses the first corner at p = 0.338 and the
second at p = 0.662. Truncating per-vertex instead makes the pen hesitate at the
corners, which is the single most visible way to get this wrong.

### Beat 2, the triangle fills. 1.1 to 1.7 seconds, overlapping beat 1 by 0.1s.

The solid white triangle fades up underneath the stroke, alpha 0 to 255 on the
same smoothstep. The outline is still being completed as the fill begins. Do not
wait for the outline to close.

### Beat 3, the wordmark wipes in. 1.6 to 2.5 seconds.

A left-to-right column reveal of the wordmark image. At eased progress p, show
the leftmost round(674.4 x p) pixel columns of the 674.4-wide image and none of
the rest.

**Hard edge. No feather, no fade, no slide.** The letters do not move; they are
uncovered where they already are. The reveal edge is a vertical cut.

### Beat 4, the rule expands from the centre. 2.5 to 3.2 seconds.

A 3px #8A6FB8 line grows outward from x 540, symmetrically both ways, at
y 1016.0. At eased progress p it spans from 540 - 390.5p to 540 + 390.5p,
reaching x 149.5 and x 930.5 at completion.

It grows from the middle. It does not sweep from one side.

### Beat 5, the address settles in. 3.2 to 4.0 seconds.

    drcorydugan.com

Fades up, the only fade in the closing. DM Sans Regular, #E4E5E7, 34px minimum,
centred on x 540, 40px below the rule. See section 9 for why it is a bare domain.

### Hold

4.0 to 4.6 seconds. Nothing moves. The final frame of every video is the
completed sign-off: filled triangle, full wordmark, full rule, address.

### The whole timeline

    0.00 - 1.20   triangle outline draws, apex first, by arc length
    1.10 - 1.70   triangle fills, overlapping
    1.60 - 2.50   wordmark wipes left to right, hard edge
    2.50 - 3.20   grape rule grows from the centre
    3.20 - 4.00   address fades up
    4.00 - 4.60   hold

Total 4.6 seconds. Crossfade 0.4 seconds into it from the content, never a cut.
Nothing is spoken over any of it.

---

## 11. THE OPENING QUESTION

The opening card names the subject. It does not say why anyone should stay, and
in a vertical feed the first two seconds are the whole retention problem.

**Do not read the card aloud.** The eyebrow, title and subtitle are on screen,
large, for three seconds. Speaking them is the same redundancy as speaking the
name over the lockup.

Instead, ask ONE question over the card. It is spoken, never on screen, so the
card stays clean and the viewer gets two channels rather than one.

### Placement, and why it is free

    0.0 - 3.0   the opening card, currently SILENT
    0.5 - 2.8   the question, spoken over it
    3.0         narration begins as it already does

No re-timing is needed. The room already exists. This is the one addition in the
whole series that costs nothing.

### The rule for writing one

- It is a QUESTION, and the episode answers it. If the episode does not answer
  it, it is a hook and hooks are not this brand.
- It comes out of that episode's own closing line, worked backwards. The closing
  line is the answer, so the question is whatever that answer settles.
- No number, no prevalence, no threshold. Section 7 applies to spoken words too.
- Second person. "Your iron", not "the patient's iron".
- One sentence. Two at the absolute limit, and then only if the first is short.
- Do not answer it in the question. "Did you know ferritin falls first?" is a
  statement wearing a question mark.

### The eleven

| Ep | Spoken over the card |
|---|---|
| 01 ferritin | When your iron starts running out, which number moves first? |
| 02 serum iron | Why can the same blood give two different iron results in one day? |
| 03 TSAT | Your iron is being carried somewhere. How much of that carrying is actually being used? |
| 04 TIBC | Why does one number on your iron panel go up when you are running out? |
| 05 transferrin | Three lines on your panel are readings of the same protein. Which three? |
| 06 haemoglobin | If your haemoglobin came back normal, are you in the clear? |
| 07 sTfR | Which iron marker still works when you are inflamed? |
| 08 MCV | What does the size of a red cell tell you about the iron that built it? |
| 09 hepcidin | What decides whether the iron you swallow ever gets in? |
| 10 ZPP | What does a red cell do when it cannot find the iron it needs? |
| 11 CRP | Your ferritin came back normal. Can you trust it? |

Each is answered inside its own episode by the closing line in section 9.

### Acceptance check, added

9. If the file carries audio, exactly one question is spoken over the opening
   card, it is not printed on screen, and the episode answers it.

---

## 12. THE VOICE DECISION, 19 August 2026

Researched across three passes: platform landscape, licensing of free tiers, and
the evidence on accent and gender. Recorded here so it is not re-litigated.

### The platform

**Google Cloud Text-to-Speech, Chirp 3 HD, en-AU female.** Fourteen genuine
Australian female voices: Achernar, Aoede, Autonoe, Callirrhoe, Despina,
Erinome, Gacrux, Kore, Laomedeia, Leda, Pulcherrima, Sulafat, Vindemiatrix,
Zephyr.

Free allowance is 1,000,000 characters a month, resetting monthly. This series
is about 4,000 characters, so 0.4% of one month. Commercial use is explicit in
Google's docs, the output is yours, and no attribution is required.

It needs OAuth, not an API key: `gcloud auth application-default login`.

Fallback with equally clean terms: **Amazon Polly "Olivia"**, native en-AU,
100,000 generative characters a month free.

### Ruled out, and why

| Platform | Reason |
|---|---|
| ElevenLabs free | Non-commercial by its own terms, and requires "elevenlabs.io" IN THE TITLE of the post. Upgrading later does not clear audio made on the free tier. |
| Azure Speech F0 | Product terms grant output rights to the paid tier only. |
| Murf free | Cannot export a file at all. |
| Coqui XTTS, F5-TTS | Weights are non-commercial even though the code is permissive. |
| Kokoro, Piper | Licences are clean, but neither ships an Australian voice. |
| Gemini TTS | No free tier. Whether the Gemini API free tier covers TTS is ambiguous, and on the free tier Google states human reviewers may read inputs and outputs. |

### The accent

**General Australian.** In a study of 138 Australian listeners rating 12 English
accents, General Australian scored positively across both status and solidarity,
and the authors conclude it now functions as both norms. Broad Australian and L2
accents rated more negatively. So the contrast that matters is General versus
Broad, not Australian versus British versus American.

Do not over-invest in this. The founding accent-and-credibility result did not
replicate, and the mechanism with the best support is processing fluency, which
argues for audio clarity rather than for a nationality.

### The female voice

The evidence is thin and contested. One conference paper of 120 participants
found a female voice assistant raised anthropomorphism, which raised perceived
credibility. Single study, unreplicated, not a health outcome.

**Do not treat "women trust women's voices" as established.** The choice is
defensible on brand grounds. It is not evidence-based, and the file should say so.

### THE FINDING THAT SHOULD BE ACTED ON FIRST

Every comparable channel that works uses a named human on camera, not a
synthetic narrator. The AMA NSW list of Australian doctor creators is three
humans presenting to camera. A content analysis of 700 contraception videos with
1.18 billion views found clinicians made 19.3% of videos and drew 41.3% of views,
concentrated in six identifiable faces.

The assumption worth breaking is not which synthetic voice. It is synthetic voice
versus Cory's face.

Second to that: caption quality has real peer-reviewed support for comprehension
and retention, and accent does not. Hand-corrected captions beat voice selection
as an investment.

### What to test rather than assume

- Same script, three voices: General Australian, British, General American.
  Measure three-second hold, average watch time, saves.
- General Australian versus Broad Australian, which the AU data says matters more.
- Synthetic narrator versus Cory on camera.
- Hand-written captions versus auto-captions, voice held constant.
