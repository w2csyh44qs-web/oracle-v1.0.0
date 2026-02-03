# GOATED Brand Style Guide

**Last Updated:** December 25, 2025 (P5 - Added Prompt Engineering Rules)
**Purpose:** Visual brand standards for all generated content - carousels, infographics, thumbnails, and social media assets.

---

## Table of Contents

1. [Brand Identity](#brand-identity)
2. [Color Palette](#color-palette)
3. [Typography](#typography)
4. [Visual Styles](#visual-styles)
5. [Layout Patterns](#layout-patterns)
6. [Logo Usage](#logo-usage)
7. [Content-Specific Guidelines](#content-specific-guidelines)
8. [Do's and Don'ts](#dos-and-donts)
9. [Prompt Engineering Rules](#prompt-engineering-rules) ← **P5: TRANSFER TO ALL CONTEXTS**

---

## Brand Identity

### Brand Voice
- **Confident** - We know our stuff
- **Accessible** - Sports betting for everyone, not just sharps
- **Playful** - Fun with sports, not gambling addiction
- **Data-driven** - Analysis over gut feelings

### Brand Promise
Transform trending sports narratives into engaging, shareable content that makes betting insights accessible.

---

## Color Palette

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Gold** | `#D4822C` | Primary brand color, headlines, CTAs |
| Gold Light | `#E59A3F` | Highlights, hover states |
| Gold Dark | `#B56A1A` | Shadows, depth |

### Background Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Cream** | `#F5F2EB` | Illustrated style background |
| Cream Light | `#F8F5F0` | Secondary backgrounds |
| **Charcoal** | `#1a1a2e` | Dark style gradient start |
| **Navy** | `#16213e` | Dark style gradient end |

### Text Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Black | `#000000` | Primary text (light backgrounds) |
| Dark Gray | `#333333` | Body text |
| Medium Gray | `#666666` | Secondary text |
| Light Gray | `#999999` | Captions, metadata |
| White | `#FFFFFF` | Primary text (dark backgrounds) |

### Accent Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Teal** | `#2D8B8B` | Illustrated style highlights, data viz |
| Orange Highlight | `#E59A3F` | Attention, warnings |
| **Neon Green** | `#39FF14` | Dark style highlights, "live" indicators |

---

## Typography

### Font Stack

| Purpose | Primary Font | Fallback | Weight |
|---------|--------------|----------|--------|
| **Headlines** | Bebas Neue | Impact, Arial Black | Regular (400) |
| **Body Text** | Inter | Helvetica, Arial | Regular (400), SemiBold (600), Bold (700) |
| **Data/Stats** | Inter | Helvetica Neue | SemiBold (600) |

### Size Scale (Carousel/Infographic)

| Element | Size (px) | Line Height |
|---------|-----------|-------------|
| Hero Headline | 72-96 | 1.0 |
| Section Header | 48-60 | 1.1 |
| Card Title | 36-42 | 1.2 |
| Body Text | 24-28 | 1.4 |
| Caption/Meta | 18-20 | 1.3 |
| Fine Print | 14-16 | 1.3 |

### Text Styling Rules

1. **Headlines:** ALL CAPS for Bebas Neue, sentence case for Inter
2. **Player Names:** ALL CAPS, Gold accent color
3. **Team Names:** ALL CAPS
4. **Stats/Numbers:** SemiBold weight, larger than surrounding text
5. **Odds:** Monospace appearance, clear +/- formatting

---

## Visual Styles

### Illustrated Style (Primary)

The signature GOATED look - warm, approachable, premium feel.

```
Background: Cream (#F5F2EB)
Text Primary: Black (#000000)
Text Accent: Gold (#D4822C)
Highlights: Teal (#2D8B8B)
```

**Characteristics:**
- Clean, editorial feel
- Hand-drawn illustration elements optional
- Generous white space
- Soft shadows (if any)
- Rounded corners (8-16px radius)

**Best for:** Carousels, infographics, educational content, matchup previews

### Dark Style (Secondary)

Bold, energetic, game-day intensity.

```
Background: Gradient from Charcoal (#1a1a2e) to Navy (#16213e)
Text Primary: White (#FFFFFF)
Text Accent: Gold (#D4822C)
Highlights: Neon Green (#39FF14)
```

**Characteristics:**
- High contrast
- Glowing/neon effects for emphasis
- Sharp edges
- Bold, aggressive typography
- Minimal gradients beyond background

**Best for:** Live game content, urgent picks, hype pieces, night games

---

## Layout Patterns

### Carousel Slides (1080x1350px - 4:5 ratio)

#### Slide 1: Cover
```
┌─────────────────────────────────┐
│                                 │
│         [MATCHUP BADGE]         │
│                                 │
│    TEAM A                       │
│      vs                         │
│    TEAM B                       │
│                                 │
│    [Date/Time]                  │
│                                 │
│              [LOGO]             │
└─────────────────────────────────┘
```

#### Slide 2-N: Content
```
┌─────────────────────────────────┐
│  [Section Header]               │
│  ─────────────────              │
│                                 │
│  • Key point one                │
│  • Key point two                │
│  • Key point three              │
│                                 │
│  ┌─────────────────────────┐    │
│  │   STAT HIGHLIGHT BOX    │    │
│  │   72.4%                 │    │
│  │   Win rate description  │    │
│  └─────────────────────────┘    │
│                                 │
│              [LOGO]             │
└─────────────────────────────────┘
```

#### Final Slide: CTA
```
┌─────────────────────────────────┐
│                                 │
│     THE GOATED PICK             │
│     ─────────────               │
│                                 │
│     [Team/Player]               │
│     [Bet Type] [Line]           │
│                                 │
│     "Tagline or reasoning"      │
│                                 │
│     Follow for more picks       │
│              [LOGO]             │
└─────────────────────────────────┘
```

### Spacing Guidelines

| Element | Margin/Padding |
|---------|----------------|
| Slide edges | 48-64px |
| Between sections | 32-48px |
| Between text lines | 16-24px |
| Logo from bottom | 48px |
| Card internal padding | 24-32px |

---

## Logo Usage

### Placement
- **Bottom center** of every slide/asset
- Consistent position across carousel
- Never in corners (gets cropped)

### Size
- Carousel: 80-120px width
- Thumbnail: 60-80px width
- Video watermark: 40-60px width

### Clear Space
- Minimum 24px padding around logo
- Never overlap with text or key elements

### Logo Variations
- Full color on cream backgrounds
- White/gold on dark backgrounds
- Never distort, rotate, or recolor

---

## Content-Specific Guidelines

### Matchup Carousels

**Required Elements:**
- Both team names/logos
- Game date and time
- Spread/total lines
- Key stats (3-5 per slide)
- Clear pick recommendation
- GOATED logo on each slide

**Team Colors:**
- Use official team primary colors for accents
- Apply to: team name backgrounds, stat highlights, dividers
- Keep brand colors dominant (gold, cream/charcoal)

**Predicted Winner Indicator:**
- Subtle gold glow or border on predicted winner
- Crown icon optional
- Never use red/green (gambling connotations)

### Best Bets Posts

**Structure:**
1. Hook headline
2. The pick (team, line, odds)
3. Supporting reasoning (2-3 points)
4. Key stat
5. Confidence indicator (optional)

### Stats Infographics

**Data Visualization:**
- Use teal for positive trends
- Use gold for neutral/brand
- Use muted colors for comparison data
- Always cite source in fine print
- Round percentages to 1 decimal

---

## Do's and Don'ts

### Do

- Maintain consistent margins across slides
- Use the brand gold as primary accent
- Keep text readable (high contrast)
- Include logo on every asset
- Use team colors as secondary accents
- Leave breathing room around elements
- Test on mobile (most users view on phones)

### Don't

- Use red/green for win/loss (colorblind unfriendly, gambling vibes)
- Overcrowd slides with text
- Use more than 3 fonts
- Place important content in corners (gets cropped)
- Use pure white backgrounds (too harsh)
- Mix illustrated and dark styles in same carousel
- Forget the logo

---

## Quick Reference

### Illustrated Style Starter
```
Background: #F5F2EB
Headlines: Bebas Neue, #000000
Body: Inter, #333333
Accent: #D4822C
Highlight: #2D8B8B
```

### Dark Style Starter
```
Background: linear-gradient(#1a1a2e, #16213e)
Headlines: Bebas Neue, #FFFFFF
Body: Inter, #FFFFFF
Accent: #D4822C
Highlight: #39FF14
```

---

## Prompt Engineering Rules

> **TRANSFER TO ALL CONTEXTS** - These rules apply to all AI image generation prompts.

### P5 Structured Prompt Pattern

When building prompts for AI image generation (Gemini, etc.), use structured sections:

| Section | Purpose | Modifiable? |
|---------|---------|-------------|
| `[LOCKED STYLE]` | Core visual identity - fonts, colors, proportions | ❌ Never after design finalized |
| `[LOCKED *]` | Specific locked elements (header, footer, player style) | ❌ Never after design finalized |
| `[LAYOUT]` | Positions, sizes, spacing | ⚠️ Via overrides during iteration |
| `[CONTENT]` | Dynamic data (player name, stats, text) | ✅ Always dynamic |
| `[ACCENTS]` | Optional additions (Christmas, effects) | ✅ Toggle on/off |
| `[ANTI-HALLUCINATION]` | What NOT to generate | ❌ Keep comprehensive |

### Iteration Strategies

| Strategy | When to Use | Preserves Original? |
|----------|-------------|---------------------|
| **Gemini image editing** | Minor tweaks to existing image (add specks, change detail) | ✅ Yes |
| **PIL programmatic** | Geometric effects (overlays, shapes) | ✅ Yes |
| **Overrides dict** | Layout adjustments during design phase | N/A - regenerates |
| **Full regeneration** | Only when starting fresh or major changes needed | ❌ No |

### Key Rules

1. **Never paraphrase locked sections** - Copy exact wording that produced good results
2. **Use overrides, not inline edits** - Pass `overrides={'title_size': 'small'}` instead of editing prompt
3. **Post-generation tweaks via Gemini edit** - Don't regenerate to fix minor issues
4. **Scan verbose output** - Review generated images for drift before finalizing
5. **Document what worked** - When a version is accepted, note the exact prompt state

### Example: Overrides Usage

```python
# Design iteration - try smaller title
prompt = build_dark_incentives_prompt(
    player_data,
    overrides={'title_size': 'small', 'add_paint_specks': True}
)

# Production - no overrides, uses locked defaults
prompt = build_dark_incentives_prompt(player_data)
```

### Anti-Pattern: What Broke dark_incentives v11-v13

When we asked for "title size change + specks" by editing the prompt inline:
- Gemini re-interpreted the entire 150-line prompt
- Lost font consistency, proportions, style elements
- Each regeneration drifted further from v10

**Fix**: Use structured sections + Gemini image editing for post-generation tweaks.

---

## Related Files

- `assets/branding/brand_colors.json` - Machine-readable color definitions
- `assets/branding/fonts/` - Font files for PIL overlay
- `config/script_presets.json` - Preset configurations with style settings
- `scripts/api_utils.py` - Prompt builder functions with structured sections

---

*GOATED Brand Style Guide - Ensuring consistent, professional visual identity across all generated content.*
