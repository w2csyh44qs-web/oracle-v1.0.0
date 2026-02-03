# GOATED Media Engine - Brand Rules

**Last Updated:** January 7, 2026
**Purpose:** Brand identity guidelines for the Goated Bets marketing media engine.

---

## Brand Colors

### Primary Palette

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Goat Gold** | `#f59e0b` | `--goat-gold` | Primary CTAs, logo glow, emphasis |
| **Goat Gold Light** | `#fbbf24` | `--goat-gold-light` | Hover states, highlights |
| **Goat Gold Dark** | `#d97706` | `--goat-gold-dark` | Active states, shadows |

### Secondary Palette

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Goat Purple** | `#8b5cf6` | `--goat-purple` | UI elements, indicators, badges |
| **Goat Purple Light** | `#a78bfa` | `--goat-purple-light` | Hover states |
| **Goat Purple Text** | `#c4b5fd` | `--goat-purple-text` | Readable purple on dark backgrounds |

### Accent Colors

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Success Green** | `#22c55e` | `--success` | Selection states, confirmations, positive indicators |
| **Error Red** | `#ef4444` | `--error` | Errors, warnings, negative states |
| **Info Blue** | `#3b82f6` | `--info` | Informational elements |

### Background Colors

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Primary BG** | `#0f1419` | `--bg-primary` | Main app background |
| **Secondary BG** | `#1a1f2e` | `--bg-secondary` | Cards, containers |
| **Tertiary BG** | `#2d3748` | `--bg-tertiary` | Elevated elements, hovers |

---

## Color Distribution Rules

### Dashboard UI

| Element Type | Color |
|--------------|-------|
| **Primary CTA Buttons** | Gold (`--goat-gold`) |
| Generate, Build, Submit | Gold background with dark text |
| **Step Indicators** | Purple (`--goat-purple`) |
| Progress dots, current step | Purple fill |
| **Filter Tabs** | Purple (`--goat-purple`) |
| Active filters, toggles | Purple highlight |
| **Selection States** | Green (`--success`) |
| Card hover, selected items | Green border/background |
| **Secondary Actions** | Purple outline or purple-text |
| Clone, Customize, Cancel | Purple styling |
| **Download Actions** | Green (`--success`) |
| Download buttons | Green background |

### Generated Content

| Content Type | Primary Color | Accent |
|--------------|---------------|--------|
| **Carousel Covers** | Team colors | Gold highlights |
| **Prop Slides** | Team colors | Green/red sentiment |
| **Incentive Images** | Gold emphasis | Dark backgrounds |
| **Matchup Previews** | Team home/away | Purple dividers |

---

## Logo Usage

### Logo Assets

| File | Location | Usage |
|------|----------|-------|
| `welcome_logo.png` | `dashboard/frontend/public/assets/branding/logos/` | Dashboard header |
| Favicon | `dashboard/frontend/public/` | Browser tab |

### Logo Styling

```css
/* Header logo with glow effect */
.dashboard-header .logo {
    height: 60px;
    filter: drop-shadow(0 0 20px rgba(245, 158, 11, 0.4));
}
```

### Logo Placement Rules

1. **Dashboard Header** - Left-aligned with title, gold glow effect
2. **Generated Content** - Bottom-right corner (except `skip_logo` presets)
3. **Login Page** - Centered with larger size
4. **Favicon** - Standard favicon placement

### Logo Don'ts

- Don't stretch or distort the logo
- Don't place on busy backgrounds without contrast
- Don't use on light backgrounds without dark mode variant
- Don't change the logo colors

---

## Typography

### Dashboard Typography

```css
.dashboard-header h1 {
    text-transform: uppercase;
    font-style: italic;
    letter-spacing: 2px;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
```

### Font Stack

```css
:root {
    --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}
```

---

## Team Color System

### Usage

```python
from config.team_colors import get_matchup_colors, get_team_colors

# Get both team palettes for a matchup
away_colors, home_colors = get_matchup_colors('DET', 'MIN', 'NFL')

# Get single team colors
team_colors = get_team_colors('KC', 'NFL')
# Returns: {'primary': '#E31837', 'secondary': '#FFB612', 'accent': '#FFFFFF'}
```

### Team Color Structure

Each team has:
- **Primary** - Main team color (jerseys, dominant)
- **Secondary** - Complementary color (accents, numbers)
- **Accent** - Third color (highlights, trim)

### Color Application in Content

| Element | Color Source |
|---------|--------------|
| Background gradients | Team primary + secondary |
| Player name labels | Team primary |
| Stat highlights | Team secondary |
| Borders/dividers | Team accent |
| Text on team bg | Contrast-aware white/black |

---

## Visual Style Guidelines

### Generated Content Styles

| Style | Description | Use Case |
|-------|-------------|----------|
| **Sketch/Watercolor** | Hand-drawn, artistic feel | Insights carousels, player features |
| **Dark/Dramatic** | High contrast, moody | Incentives, dramatic moments |
| **Minimal/Clean** | Simple, data-focused | Stats, infographics |
| **Photo-Realistic** | Photography-based | Matchup previews, highlights |

### Carousel Design Principles

1. **Cover Slide** - Bold, attention-grabbing, matchup-focused
2. **Content Slides** - Readable, data-rich, team-colored
3. **CTA Slide** - Brand-focused, engagement-driving
4. **Consistent Margins** - 40px safe zone on all edges

### Image Aspect Ratios

| Format | Ratio | Use |
|--------|-------|-----|
| Square | 1:1 | Instagram feed, carousels |
| Portrait | 9:16 | Reels, Stories, TikTok |
| Landscape | 16:9 | YouTube thumbnails, banners |

---

## Content Tone & Voice

### Brand Personality

- **Confident** - Strong opinions backed by data
- **Sharp** - Quick, punchy analysis
- **Informed** - Deep sports knowledge
- **Relatable** - Sports fan language, not corporate

### Writing Guidelines

| Do | Don't |
|----|-------|
| Use action verbs | Use passive voice |
| Be specific with stats | Vague generalizations |
| Take clear positions | Hedge everything |
| Use sports vernacular | Overly formal language |

### Example Copy Patterns

**Prop Headlines:**
- "Woody Marks OVER 74.5 rushing yards"
- "3 Reasons to Hammer the Under"

**Insight Bullets:**
- "26 carries expected in bell-cow role"
- "Texans run D ranks #26 (142.3 YPG)"

**CTA Text:**
- "Lock it in"
- "Smash the over"
- "Fade the public"

---

## Platform Specifications

### Instagram

| Format | Size | Notes |
|--------|------|-------|
| Feed Post | 1080x1080 | Square, carousel support |
| Story/Reel | 1080x1920 | 9:16, <60s |
| Profile | 320x320 | Logo only |

### TikTok

| Format | Size | Notes |
|--------|------|-------|
| Video | 1080x1920 | 9:16, <3min |
| Profile | 200x200 | Logo only |

### Twitter/X

| Format | Size | Notes |
|--------|------|-------|
| Image | 1200x675 | 16:9 preferred |
| Card | 800x418 | Link preview |

---

## CSS Variables Reference

```css
:root {
    /* Brand Colors */
    --goat-gold: #f59e0b;
    --goat-gold-light: #fbbf24;
    --goat-gold-dark: #d97706;
    --goat-purple: #8b5cf6;
    --goat-purple-light: #a78bfa;
    --goat-purple-text: #c4b5fd;

    /* Semantic Colors */
    --success: #22c55e;
    --error: #ef4444;
    --warning: #f59e0b;
    --info: #3b82f6;

    /* Backgrounds */
    --bg-primary: #0f1419;
    --bg-secondary: #1a1f2e;
    --bg-tertiary: #2d3748;

    /* Text */
    --text-primary: #ffffff;
    --text-secondary: #9ca3af;
    --text-muted: #6b7280;

    /* Borders */
    --border-default: #374151;
    --border-focus: #8b5cf6;
}
```

---

## Quick Reference

### Button Colors
- **Primary Action**: Gold background, dark text
- **Secondary Action**: Purple outline/text
- **Success/Download**: Green background
- **Danger/Delete**: Red background

### State Colors
- **Hover**: Lighter variant of base color
- **Active**: Darker variant of base color
- **Disabled**: 50% opacity
- **Focus**: Purple ring outline

### Content Priorities
1. **Gold** - Most important (CTAs, key stats)
2. **Green** - Positive/success (winning bets, good matchups)
3. **Purple** - UI elements, secondary info
4. **Red** - Warnings, negative sentiment

---

*This document defines the visual identity of the Goated Bets brand. All generated content and UI should follow these guidelines.*
