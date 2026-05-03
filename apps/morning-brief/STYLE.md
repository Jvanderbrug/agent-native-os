# AI Build Lab Design Aesthetic. Source of Truth

**Purpose.** Vibe baseline for any Sunday capstone artifact (morning-brief Vercel app, dashboards, blueprint pages). Not a content spec, a visual direction spec.

**Reference mockup.** [MOCKUP-2026-05-02.html](./MOCKUP-2026-05-02.html) (open in browser). This is a marketing-site shape not a product UI, but the design tokens, materials, and personality transfer.

**Companion sources.**
- `~/GitHub/aibuild-lab/the-studio/` (canonical design assets, design-system, slides)
- `~/GitHub/foundations-2.0/brand/AI-Build-Lab-Brand/` (brand guidance)
- `~/GitHub/agent-native-os-hq/playbook/design-aesthetic/MOCKUP-2026-05-02.html` (this folder)

## Personality (in three words)

**Field manual. Personnel file. Scratched-up notebook.**

Brutalist edges, paper texture, lime accents, mono labels, slight rotations like things were taped to a board. Built-by-operators-not-designers but on purpose. Confident, not corporate.

## Design Tokens

```
Surfaces
  --paper:        #F5F2EB   (warm off-white, primary canvas)
  --paper-2:      #EBE7DE   (one step deeper)
  --paper-3:      #DDD7CA   (two steps deeper)
  --surface:      #FFFFFF   (cards on paper)
  --terminal-bg:  #080808   (code/blueprint blocks)

Ink
  --ink:    #0F0F0F  (body)
  --ink-2:  #4A4A52  (secondary)
  --ink-3:  #7A7A85  (tertiary, mono labels)
  --border: #0F0F0F  (always near-black)

Accents
  --lime:       #C8FF00  (signature highlight)
  --lime-dim:   #A8D600  (hover state)
  --caution:    #FF3300  (CTAs, urgency, section labels)
  --blueprint:  #0055FF  (Sara, schema, secondary accent)
  --success:    #00D084  (live dot, verified stamps)

Shadows (offset, never blurred)
  --shadow-sm:  3px 3px 0 var(--border)
  --shadow:     5px 5px 0 var(--border)
  --shadow-lg:  9px 9px 0 var(--border)

Background
  Subtle 46px grid:
  background-image:
    linear-gradient(rgba(15,15,15,0.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(15,15,15,0.055) 1px, transparent 1px);
  background-size: 46px 46px;
```

Dark mode keeps the lime/caution/blueprint accents and switches paper to ~#0F1115 with the same grid texture at lower opacity (see CSS in mockup).

## Typography

```
Display:  'Space Grotesk' weight 700, letter-spacing -0.04em to -0.055em, line-height 1.05-1.10
Body:     'Inter' weight 400-600, line-height 1.55-1.60
Mono:     'JetBrains Mono' weight 600-700 for labels, code, badges, stamps
```

Headlines lean tight and large. Body breathes. Mono is the connective tissue (every label, every kicker, every stat tag).

## Material Rules

1. **Borders are thick and almost-black.** 2px or 3px solid `var(--border)`. Never gray-on-gray.
2. **Shadows are hard offsets, never blurred.** A card sits on the page like a stack of paper.
3. **Cards rotate slightly (-0.45deg to +0.45deg).** Just enough to feel taped down.
4. **Tape elements at top of cards.** Two yellow strips with low-opacity black border.
5. **Highlight phrases with `.highlight`.** Lime background, near-black text, inline-block. Used on key noun phrases in headlines.
6. **Section labels are mono caps with offset shadow.** Color is caution-red.
7. **Stamps and pills always have white-space-nowrap.** No clipped text ever.

## Components You Will Reuse on the Morning Brief App

- **Hero kicker.** White surface, 2px border, 3x3 shadow, mono font, live-dot indicator, status text.
- **Hero board.** White surface with tape strips, 3px border, 9x9 shadow, slight rotation, holds video or hero artifact.
- **Stat cards.** 2px border, paper-2 background, 100px min-height, large display number + mono label.
- **Manifest strip.** Lime band with scrolling marquee of taglines separated by `◆`.
- **Section label + title + sub.** Three-element block at the top of every section.
- **File-tab card.** Lime tab at top-left says `PERSONNEL FILE / 001` style. Used for founder cards, can be repurposed as `BRIEF / 2026-05-04` for the morning brief.
- **Terminal blueprint block.** Black bg, lime headlines, 4-column flow nodes for showing system pipelines.
- **Verified stamp.** Hand-drawn-feel border, slight rotation, success-green or caution-red.

## Morning Brief App Translation

The mockup is a marketing site. The morning-brief app is a product surface. Translation rules:

- **Keep:** color palette, typography, border + shadow language, grid background, mono labels, lime highlight on key phrases, file-tab framing.
- **Adapt:** density. Product UI gets tighter padding (paper feel persists, but card padding drops from ~1.45rem to ~1rem in dense data views).
- **Drop:** scrolling marquee, large hero-board video, founder cards. Replace with: brief-of-the-day card, source registry table, delivery log, agent run timeline.
- **New patterns to invent:** brief feed (timeline of past briefs), source toggle controls, delivery channel status pills, "build now" CTA.

## Brand Logo

Logo file referenced as `/assets/aibuildlab-logo.png`. Resolve from:
1. `~/GitHub/aibuild-lab/the-studio/assets/`
2. `~/GitHub/foundations-2.0/brand/AI-Build-Lab-Brand/`

Fallback rendering provided in mockup CSS (`.logo-fallback`): black background, lime forward-slash + dim-lime pipe, "buildlab" wordmark in Space Grotesk 700.

## Voice and Tone in UI Copy

- Imperative, lowercase-ish, terse. "build morning brief", "ship it", "next run in 4h 12m".
- Never marketing-glossy. Never enterprise-blandsy. Never cute.
- Mono for system messages and status. Sans for human-reading prose.
- Caution-red for destructive actions and urgency only. Lime for success and primary affordances. Blueprint-blue is reserved (Sara's track, schema views).

## Anti-Patterns (Do Not)

- Soft drop shadows.
- Gradient buttons.
- Rounded-everything (radii are 0 for cards, full for live-dot only).
- Generic stock-photo hero. If you need an image, treat it grayscale + contrast-bumped.
- Em dashes. Periods, commas, parens, hyphens for compound words. Workshop-wide rule.
- Centered-everything. Asymmetric layouts. Things lean.

## When in Doubt

Ask: would this look at home thumbtacked to a corkboard in a workshop with a roll of yellow tape, a paint marker, and a notebook full of PRDs? If yes, ship it. If no, sand it down.
