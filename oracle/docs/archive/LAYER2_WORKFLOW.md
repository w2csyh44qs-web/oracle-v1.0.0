# Layer 2: Content Ideation Workflow

Complete guide to generating, approving, and organizing content ideas from trends.

---

## Overview

**Layer 2** transforms trend detection results (Layer 1) into production-ready content ideas organized by sport, season, week, and daily segments.

### The Flow:

```
LAYER 1: Trend Detection
    ↓
output/all_trends.json
    ↓
LAYER 2: Content Ideation
    ├─→ Generate Draft Ideas (AI)
    ├─→ Review & Approve (YOU - Checkpoint)
    ├─→ Organize by Segments
    └─→ Ready for Layer 3 (Video Production)
```

---

## Folder Structure

```
content/
└── nfl/
    └── 2025-2026/
        ├── preseason/
        │   └── week1/
        ├── regular_season/
        │   ├── week1/
        │   │   ├── trends.json              # Source trends from Layer 1
        │   │   ├── ideas_draft.json         # AI-generated ideas (pending approval)
        │   │   ├── ideas_approved.json      # YOUR approved ideas
        │   │   ├── segment_index.json       # Quick reference index
        │   │   └── segments/                # Organized by daily show
        │   │       ├── bad_beats_monday.json
        │   │       ├── upset_alert_tuesday.json
        │   │       ├── minigame_wednesday.json
        │   │       ├── lock_of_the_week.json
        │   │       ├── player_personality.json
        │   │       ├── big_kahuna.json
        │   │       ├── moneyline_minute.json
        │   │       └── betting_trends_recap.json
        │   ├── week2/
        │   └── ... (week 18)
        ├── playoffs/
        │   ├── wild_card/
        │   ├── divisional/
        │   ├── conference/
        │   └── super_bowl/
        ├── offseason/
        │   ├── draft/
        │   ├── free_agency/
        │   ├── training_camp/
        │   └── otas/
        └── special_events/
            ├── trade_deadline/
            └── pro_bowl/
```

---

## Complete Workflow

### Step 1: Run Trend Detection (Layer 1)

```bash
# Run trends for current week
python run_trends.py
# Choose option 2 (Reddit) or 4 (All Sources)
```

**Output:** `output/all_trends.json` (or individual source files)

---

### Step 2: Generate Draft Ideas

```bash
python scripts/content_ideation.py regular_season week1
```

**What it does:**
1. Reads trends from `output/all_trends.json`
2. Filters high-quality trends (meme_score >= 6)
3. Uses OpenAI GPT-4o-mini to generate 30 content ideas
4. Maps ideas to weekly segments (Bad Beats Monday, etc.)
5. Maintains 55% entertainment / 45% value split
6. Saves to `content/nfl/2025-2026/regular_season/week1/ideas_draft.json`

**Arguments:**
- `phase`: `preseason`, `regular_season`, `playoffs`, `offseason`, `special_events`
- `week`: `week1`, `week2`, etc.
- `--num-ideas`: Number of ideas to generate (default: 30)

**Example:**
```bash
# Generate 40 ideas for playoff wild card round
python scripts/content_ideation.py playoffs wild_card --num-ideas 40
```

**Output Structure:**
```json
{
  "status": "draft",
  "total_ideas": 30,
  "content_mix": {
    "entertainment": 17,
    "value": 13
  },
  "ideas": [
    {
      "id": "idea_001",
      "type": "entertainment",
      "segment_day": "monday",
      "segment_name": "Bad Beats Monday",
      "title": "The Five Stages of Grief: Missed PAT Edition",
      "hook": "Tell me you lost a parlay without telling me...",
      "concept": "Guy loses $2K parlay on missed PAT in OT...",
      "format": "reaction_video",
      "duration": "45s",
      "script_outline": [...],
      "source_trend": {...},
      "app_feature": null,
      "cta": null
    }
  ]
}
```

---

### Step 3: Review & Approve Ideas (CHECKPOINT)

```bash
python scripts/approve_ideas.py regular_season week1
```

**What it does:**
1. Loads `ideas_draft.json`
2. Shows each idea interactively
3. You decide: **Approve** or **Reject**
4. Saves approved ideas to `ideas_approved.json`

**Interactive Review:**
```
================================================================================
IDEA 1/30 - [ENTERTAINMENT]
================================================================================
Segment: Bad Beats Monday
Title: The Five Stages of Grief: Missed PAT Edition
Hook: Tell me you lost a parlay without telling me...

Concept:
  Guy loses $2K parlay because kicker missed PAT in overtime. Show the
  emotional journey through denial, anger, bargaining, depression, acceptance.

Format: reaction_video (45s)

Script Outline:
  - Hook: Text overlay 'When your 7-leg parlay comes down to an extra point...'
  - Denial: 'Wait, the game's not over right?'
  - Anger: 'ARE YOU KIDDING ME?!'
  - Bargaining: Checking if there's OT, refreshing app
  - Depression: Head in hands
  - Acceptance: Sardonic laugh, 'See you next week'

Notes: Pure entertainment. NO app mentions. Goal: Shares and relatability.

Source: reddit (score: 9)
  https://reddit.com/r/sportsbook/...

--------------------------------------------------------------------------------
Approve this idea? [y]es / [n]o / [e]dit / [q]uit:
```

**Commands:**
- `y` / `yes` - Approve and move to next
- `n` / `no` - Reject and move to next
- `e` / `edit` - Approve (you can edit JSON manually later)
- `q` / `quit` - Exit approval process

**Output:** `content/nfl/2025-2026/regular_season/week1/ideas_approved.json`

---

### Step 4: Organize Into Segments

```bash
python scripts/organize_segments.py regular_season week1
```

**What it does:**
1. Reads `ideas_approved.json`
2. Groups ideas by daily segment (monday, tuesday, etc.)
3. Creates individual JSON files for each segment
4. Creates `segment_index.json` for quick reference

**Output:**
```
content/nfl/2025-2026/regular_season/week1/segments/
├── bad_beats_monday.json          (4 ideas)
├── upset_alert_tuesday.json       (3 ideas)
├── minigame_wednesday.json        (4 ideas)
├── lock_of_the_week.json          (5 ideas)
├── player_personality.json        (4 ideas)
├── big_kahuna.json                (4 ideas)
├── moneyline_minute.json          (3 ideas)
└── betting_trends_recap.json      (3 ideas)
```

**Segment File Structure:**
```json
{
  "segment_name": "Bad Beats Monday",
  "segment_description": "Relatable betting losses and painful moments",
  "total_ideas": 4,
  "content_mix": {
    "entertainment": 3,
    "value": 1
  },
  "ideas": [...]
}
```

---

## Daily Segments Explained

### Monday: Bad Beats Monday
- **Type:** Entertainment
- **Focus:** Relatable betting losses, painful moments
- **Preferred Categories:** bad_beat, humor
- **Format:** Reaction videos, meme compilations

### Tuesday: Upset Alert Tuesday
- **Type:** Value
- **Focus:** Underdog opportunities, line value
- **Preferred Categories:** upset_alert, news
- **Format:** Analysis videos, stat graphics

### Wednesday: Minigame Wednesday
- **Type:** Entertainment
- **Focus:** Interactive content, polls, trivia
- **Preferred Categories:** humor, betting_strategy
- **Format:** Polls, smash-or-pass, trivia

### Thursday: Lock of the Week
- **Type:** Value
- **Focus:** Sharp money analysis, line movements
- **Preferred Categories:** betting_strategy, line_movement, analysis
- **Format:** Deep dives, stat graphics, tutorials

### Friday: Player Personality
- **Type:** Entertainment
- **Focus:** Player memes, personality-driven content
- **Preferred Categories:** humor, news
- **Format:** Meme compilations, rankings

### Saturday: Big Kahuna
- **Type:** Value
- **Focus:** Weekend preview, high-value bets
- **Preferred Categories:** winning_bet, upset_alert
- **Format:** Event previews, bet breakdowns

### Sunday AM: Moneyline Minute
- **Type:** Value
- **Focus:** Last-minute line movements
- **Preferred Categories:** line_movement, news
- **Format:** Quick hits, urgent updates

### Sunday PM: Betting Trends Recap
- **Type:** Entertainment
- **Focus:** Results recap, "ways the house won"
- **Preferred Categories:** analysis, humor
- **Format:** Compilation, commentary

---

## Configuration

### Customize NFL Calendar

Edit `config/nfl_calendar.py`:

**Add/Modify Segments:**
```python
WEEKLY_SEGMENTS = {
    'monday': {
        'name': 'Bad Beats Monday',
        'slug': 'bad_beats_monday',
        'preferred_categories': ['bad_beat', 'humor'],
        'content_type': 'entertainment',
        'description': 'Your custom description'
    }
}
```

**Adjust Content Mix by Phase:**
```python
CONTENT_MIX_BY_PHASE = {
    'regular_season': {
        'entertainment': 0.55,  # Adjust ratio
        'value': 0.45
    }
}
```

**Add Key Events:**
```python
KEY_EVENTS = {
    'super_bowl': {
        'date': '2025-02-09',
        'week': 'playoffs/super_bowl',
        'content_focus': 'Super Bowl props, party bets'
    }
}
```

---

## Common Workflows

### Weekly Content Cycle (Regular Season)

**Monday:**
```bash
# 1. Run trends over the weekend
python run_trends.py  # Option 2 (Reddit)

# 2. Generate ideas for the week
python scripts/content_ideation.py regular_season week5

# 3. Review and approve (15-30 min)
python scripts/approve_ideas.py regular_season week5

# 4. Organize into segments
python scripts/organize_segments.py regular_season week5
```

**Tuesday-Sunday:**
- Use segment files to guide video production (Layer 3)
- Each day's segment file contains ready-to-produce ideas

### Playoff Week

```bash
# Wild Card weekend
python scripts/content_ideation.py playoffs wild_card --num-ideas 40
python scripts/approve_ideas.py playoffs wild_card
python scripts/organize_segments.py playoffs wild_card
```

### Special Event (Trade Deadline)

```bash
python scripts/content_ideation.py special_events trade_deadline --num-ideas 20
python scripts/approve_ideas.py special_events trade_deadline
python scripts/organize_segments.py special_events trade_deadline
```

---

## Tips & Best Practices

### For Ideation:
- Run trend detection BEFORE ideation (fresh trends = better ideas)
- Higher meme scores (8-10) = entertainment content
- Medium scores (6-7) = value/educational opportunities

### For Approval:
- Don't overthink it - trust your gut
- Look for ideas that make you laugh or think "the boys will love this"
- Entertainment should feel shareable, value should feel helpful
- You can always edit the JSON manually after approval

### For Organization:
- Review `segment_index.json` for quick overview
- Each segment file is independent - easy to hand off to video editor
- Consistent structure makes automation easier down the line

---

## Next Steps: Layer 3 (Video Generation)

Once segments are organized, they're ready for:
- Motion Array video templates
- ElevenLabs AI voiceovers
- Automated video assembly
- Final human review before posting

**Future:** Direct integration with video generation tools reading from segment JSON files.

---

## Extending to Other Sports

### Coming Soon:

**NBA:**
```
content/nba/2025-2026/
├── preseason/
├── regular_season/
├── all_star/
├── playoffs/
└── offseason/
```

**Soccer/World Cup:**
```
content/soccer/
├── world_cup_2026/
├── premier_league/
└── champions_league/
```

**Tennis:**
```
content/tennis/
├── australian_open_2025/
├── french_open_2025/
├── wimbledon_2025/
└── us_open_2025/
```

Each sport will have its own calendar config and segment structure.

---

## Troubleshooting

**"Draft file not found"**
- Run `content_ideation.py` first to generate draft ideas

**"No trends found"**
- Run Layer 1 trend detection first: `python run_trends.py`

**"OpenAI error"**
- Check API key in `.env`
- Ensure you have credits: [platform.openai.com/settings/organization/billing](https://platform.openai.com/settings/organization/billing)

**Want to regenerate ideas?**
- Delete `ideas_draft.json` and run `content_ideation.py` again
- Draft is overwritten each time you run ideation

**Made a mistake during approval?**
- Edit `ideas_approved.json` manually (it's just JSON)
- Or delete it and run `approve_ideas.py` again

---

## Summary

**Layer 2 achieves:**
- ✅ Transforms raw trends into structured content ideas
- ✅ Checkpoint system for human oversight
- ✅ Organization by sport/season/week/segment
- ✅ Production-ready scripts and formats
- ✅ Scalable to multiple sports
- ✅ Maintains entertainment/value split automatically

**Your role:**
- Run 3 commands per week (~30 min total)
- Review and approve ideas (15-30 min)
- Focus on strategy, let AI handle ideation

**Next:** Build Layer 3 (Video Generation) to turn these ideas into finished videos.
