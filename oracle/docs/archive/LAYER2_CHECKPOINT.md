# Layer 2: Calendar Configuration Checkpoint

## Overview

Layer 2 provides visibility and configuration for the NFL season calendar structure. This checkpoint allows you to review and modify:
- Season phases and weeks
- Daily content segments (Bad Beats Monday, etc.)
- Key events (Super Bowl, Trade Deadline, etc.)
- Content mix ratios (entertainment vs value)

## When It Runs

The Layer 2 checkpoint appears **before** Layer 3 (Idea Creation) when you run:

```bash
python scripts/idea_creation.py regular_season week1
```

You'll see:
```
📅 LAYER 2 CHECKPOINT: NFL Calendar Configuration

Review calendar configuration? [y/N]:
```

Press **N** (or Enter) to skip and continue with current configuration.
Press **Y** to enter the configuration menu.

## Skip the Checkpoint

If you want to bypass the checkpoint entirely:

```bash
python scripts/idea_creation.py regular_season week1 --skip-calendar
```

## Configuration Menu Options

### Main Menu

```
[c] Continue with current configuration
[v] View detailed calendar structure
[s] View/edit segments (daily shows)
[e] View/edit key events
[w] View week structure by phase
[m] View content mix ratios
[q] Quit
```

### View Detailed Structure (`v`)

Shows complete season breakdown:
- All phases (preseason, regular_season, playoffs, offseason, special_events)
- Week counts per phase
- Content mix ratios per phase

### Manage Segments (`s`)

View and customize your daily content segments:

**Default Segments:**
- Monday: Bad Beats Monday (entertainment)
- Tuesday: Upset Alert Tuesday (value)
- Wednesday: Minigame Wednesday (entertainment)
- Thursday: Lock of the Week (value)
- Friday: Player Personality (entertainment)
- Saturday: Big Kahuna (value)
- Sunday AM: Moneyline Minute (value)
- Sunday PM: Betting Trends Recap (entertainment)

**Actions:**
- `[a]` Add new custom segment
- `[e]` Edit segment (custom only)
- `[d]` Delete custom segment
- `[b]` Back to main menu

**Adding a Custom Segment:**
You'll be prompted for:
- Segment name (e.g., "Rivalry Week")
- Slug (e.g., "rivalry_week")
- Day/time slot (e.g., "thursday_pm")
- Type (entertainment or value)
- Description
- Categories (comma-separated)

Custom segments are saved to `config/custom_segments.json`.

### Manage Key Events (`e`)

View scheduled NFL events:
- Season Opener
- Trade Deadline
- Thanksgiving
- Playoff Clinching
- Super Bowl
- NFL Draft

**Future Features:**
- `[r]` Refresh dates from ESPN/SportsData API
- `[a]` Add custom events

### View Week Structure (`w`)

Displays all weeks organized by phase in a grid format.

### View Content Mix (`m`)

Shows entertainment/value split for each phase:
```
REGULAR_SEASON
  Entertainment: 55% ███████████
  Value:         45% █████████
```

These ratios guide AI content generation in Layer 3.

## Files and Configuration

### Main Calendar Config
`config/nfl_calendar.py` - Core season structure, segments, events

### Custom Segments
`config/custom_segments.json` - Your custom segments (created on first add)

### Example Custom Segment
```json
{
  "rivalry_week": {
    "name": "Rivalry Week",
    "day": "thursday_pm",
    "content_type": "entertainment",
    "description": "Historic rivalry games and trash talk",
    "preferred_categories": ["humor", "news", "analysis"]
  }
}
```

## Standalone Usage

You can also run the calendar checkpoint independently:

```bash
python scripts/configure_calendar.py
```

This is useful for:
- Reviewing calendar structure before a new week
- Adding segments for special events
- Updating configurations mid-season

## Integration with Layer 3

After confirming your calendar configuration, Layer 3 (Idea Creation) will:
1. Use the configured segments to organize content
2. Apply the content mix ratios for the target phase
3. Map generated ideas to your daily segments
4. Structure output folders according to season/week hierarchy

## Tips

1. **First Time Setup**: Press `[y]` to review segments and familiarize yourself with the structure
2. **Weekly Routine**: Press `[N]` to skip - configuration rarely changes week-to-week
3. **Special Events**: Press `[y]` to add custom segments for rivalry weeks, playoff pushes, etc.
4. **Content Mix**: If you want more entertainment or value content, note the ratios and edit `config/nfl_calendar.py` manually

## Future Enhancements

Planned features:
- **API Integration**: Auto-fetch NFL schedule from ESPN or SportsData
- **Week Detection**: Auto-detect current week based on date
- **Multi-Sport**: Extend to NBA, Soccer, Tennis calendars
- **Custom Events**: Add one-off events (draft day, awards shows)
- **Segment Templates**: Pre-built segment packs for different sports

## Workflow Example

```bash
# Week 5 content planning

$ python scripts/idea_creation.py regular_season week5

🚀 GOATED IDEA CREATION LAYER Starting...

Target: regular_season / week5

================================================================================
📅 LAYER 2 CHECKPOINT: NFL Calendar Configuration
================================================================================

Review calendar configuration? [y/N]: y

================================================================================
📅 LAYER 2: NFL CALENDAR CONFIGURATION
================================================================================

Season: 2025-2026
Current Week: regular_season / week1

📊 Season Structure:
  • Preseason: 3 weeks
  • Regular Season: 18 weeks
  • Playoffs: 4 weeks
  • Offseason: 4 weeks
  • Special Events: 2 weeks

📺 Daily Segments: 8 configured
🗓️  Key Events: 6 scheduled

================================================================================
🛑 CHECKPOINT: Review Calendar Configuration
================================================================================

Options:
  [c] Continue with current configuration
  [v] View detailed calendar structure
  [s] View/edit segments (daily shows)
  [e] View/edit key events
  [w] View week structure by phase
  [m] View content mix ratios
  [q] Quit

Choose an option: c

✅ Continuing with current calendar configuration...

✓ Loaded 20 trends from 1 approved source(s)
✓ Filtered to 8 high-strength trends (score >= 6)

🤖 Generating 30 content ideas...
...
```

## Summary

**Layer 2 achieves:**
- ✅ Visibility into season structure before content generation
- ✅ Ability to customize segments without editing code
- ✅ Clear understanding of content mix ratios
- ✅ Checkpoint consistency across all layers
- ✅ Foundation for multi-sport expansion

**Your role:**
- Review calendar on first run or when adding special events
- Skip checkpoint during regular weekly workflows
- Customize segments as your content strategy evolves
