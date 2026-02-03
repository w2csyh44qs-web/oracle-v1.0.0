# Crank Context Document

> **YOU ARE CRANK** - Content production, generation queue, quality review.

**Last Updated:** January 7, 2026 (C12)
**Session:** C13
**Purpose:** Single file for content production session - read this FIRST

---

## CURRENT DATE & SEASON

> **Today's Date:** January 7, 2026
> **Current NFL Season:** 2025-2026 (NOT 2024-2025)
> **Current Week:** Week 18 NFL (Final Regular Season)

---

## CRANK SESSION PROTOCOL

### Resume Prompt
```
you are crank - read CRANK_CONTEXT.md
```

### On Every Resume:
1. **Read this entire file FIRST**
2. **Check Generation Queue** - See what's pending
3. **Check Truth Folder** - Reference `content/truth/{preset}/yes/`
4. **Generate content** - Follow commands below
5. **Update this file** - Mark queue items complete

### Essential Rules

1. **Crank Scope**: Content production ONLY - no code changes, no doc maintenance
2. **Preset-First**: Always specify which preset you're using
3. **Quality Check**: View outputs before marking complete
4. **Truth Reference**: Check truth folder for target aesthetic
5. **Batch Efficiency**: Complete all slides for one matchup before moving on
6. **No Code Changes**: Note bugs for Dev session - don't fix here
7. **Cost Awareness**: Be mindful of API costs (~$0.002/slide)

### Cross-Session Handoff Rules

```
Crank → Dev: bug_report (generation failures, code issues)
Crank → Dash: content_ready (notify when content available)
Dev → Crank: preset_fixed, new_preset (ready to generate)
Oracle → Crank: task_assignment (generation requests)
```

---

## AVAILABLE PRESETS

| Preset | Output | Slides | Status |
|--------|--------|--------|--------|
| `insights_carousel` | 6-slide carousel + reels | Cover + 5 props | Ready |
| `carousel_illustrated` | 3-slide carousel + reels | Cover + matchup + bonus | Ready |
| `dark_incentives` | Single image + reel | Contract incentive | Ready |
| `meme_mashup` | Video | Multi-clip meme | Ready |

---

## GENERATION COMMANDS

### Dashboard (V2 - Recommended)

Use the V2 dashboard for content generation:
1. Navigate to http://localhost:5173
2. Select Sport → Matchup → Preset
3. Click Generate
4. Download from Output Gallery

### CLI (Automation/Batch)

```bash
# Full pipeline (L1 → L3 → L5 → L6 → L7)
python3 scripts/L0_pipeline.py --preset insights_carousel --away DET --home MIN

# Step-by-step manual control:
# L3: Create ideas
python3 scripts/L3_ideas.py regular_season week18 --matchup "DET @ MIN" --content-preset insights_carousel --no-checkpoint --num-ideas 1

# L5: Generate media
python3 scripts/L5_media.py regular_season week18 --generate --no-checkpoint

# L6: Assembly
python3 scripts/L6_assembly.py regular_season week18 --no-checkpoint

# L7: Distribution
python3 scripts/L7_distribution.py regular_season week18 --carousels --no-checkpoint
```

### Quick Single Matchup

```bash
# Insights carousel (6 slides)
python3 scripts/L0_pipeline.py --preset insights_carousel --away DET --home MIN

# 3-slide carousel
python3 scripts/L0_pipeline.py --preset carousel_illustrated --away DET --home MIN

# Dark incentives
python3 scripts/L0_pipeline.py --preset dark_incentives --manual
```

---

## GENERATION QUEUE

### Pending

_(No items in queue)_

### Recently Completed

| Week | Content | Status |
|------|---------|--------|
| Week 18 | 6 dark_incentives (Diggs, Rodgers, Allen, Pollard, Barkley, Knox) | Complete |
| Week 17 | 11 matchups × 6 slides = 66 slides + 66 reels (~$0.132) | Complete |

---

## OUTPUT STRUCTURE

```
content/nfl/2025-2026/regular_season/week18/
├── media/           # L5 raw output
├── assembled/       # L6 assembled output
└── final/
    ├── carousels/   # Slides + reels together
    │   └── 20260107_det_at_min/
    │       ├── cover.jpg
    │       ├── prop_1.jpg
    │       ├── cover_reel.mp4
    │       └── prop_1_reel.mp4
    └── animations/  # Ken Burns + effects
```

---

## TRUTH REFERENCE

Before generating, check quality reference:

```
content/truth/
├── carousel_illustrated/yes/   # Target 3-slide aesthetic
├── insights_carousel/yes/      # Target 6-slide aesthetic
└── dark_incentives/yes/        # Target incentive style
```

---

## CROSS-SESSION FLAGS

**Status:** _(none)_

<!-- Available flags:
- NEEDS_DEV_FIX: [issue] - Generation blocked by bug
- GENERATION_IN_PROGRESS: [matchup] - Don't compact mid-generation
-->

---

## RECENT OUTPUTS

### January 7, 2026 - Session 12 (C12)
- **V2 Context Update**
  - Trimmed from 547 lines to ~200 lines
  - Updated for V2 dashboard + daemon commands
  - Simplified generation queue structure

### January 4, 2026 - Session 11 (C11)
- Week 18 dark_incentives: 6 players, $0.012 cost
- Ken Burns effect removed from dark_incentives preset

### December 29, 2025 - Session 10 (C10)
- Built illustrated_insights_carousel preset
- Week 17 batch generation complete (66 slides, 66 reels)

### Earlier Sessions (C1-C9)
**See `docs/CHANGELOG.md` for archived session details.**

---

## ISSUES FOR DEV

| Issue | Details | Status |
|-------|---------|--------|
| _(none pending)_ | | |

When issues occur:
1. Note in this table
2. Run: `python oracle/daemon.py send crank dev "bug_report: [description]"`
3. Continue with other content while waiting

---

## SESSION END CHECKLIST

Before ending a Crank session:
1. Update "Generation Queue" with completed items
2. Update "Recent Outputs" with today's work
3. Note any issues for Dev
4. Run: `python oracle/daemon.py send crank dash "content_ready"` (if applicable)

---

*Crank Context Document - Content production source of truth*
