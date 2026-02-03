# Pocket Context Document

> **YOU ARE POCKET** - Lightweight full-function session for portable workstation (MacBook Air). All capabilities, optimized for efficiency.

**Last Updated:** January 3, 2026 (O85 - P18 Main script rename)
**Session Count:** D101 / O88 / C10 / P20 / DB1
**Purpose:** Full workflow capability with resource-conscious execution

---

## CURRENT DATE & SEASON

> **Today's Date:** January 3, 2026
> **Current NFL Season:** 2025-2026 (NOT 2024-2025)
> **Current Week:** Week 18 NFL (Final Regular Season - Jan 4-5, 2026)

---

## POCKET SESSION PROTOCOL

### On Every Resume:
1. Read this file FIRST
2. Check what main sessions (D/O/C) have been doing
3. Execute task with efficiency in mind
4. Update this file + set handoff flags if needed

### Resume Prompt:
```
you are pocket - read POCKET_CONTEXT.md
```

---

## 📋 SESSION RULES (POCKET-SPECIFIC)

> 14 rules adapted from DEV/ORACLE for M1 MacBook Air constraints

### Core Philosophy Rules

1. **Context First Rule**: ALWAYS read POCKET_CONTEXT.md completely on resume. This is your memory.

2. **Autosave Rule**: Run `python3 maintenance/project_oracle.py autosave` before ending ANY session. Non-negotiable.

3. **Single-Task Focus Rule**: Complete one task fully before starting another. Pocket sessions are for focused work, not multi-tasking.

4. **Handoff Awareness Rule**: Flag heavy tasks for main workstation (Mac Studio) using Pocket Flags section. Heavy tasks include:
   - Full week batch generation (7+ matchups)
   - Video processing requiring significant RAM
   - Multi-hour pipeline runs
   - Tasks requiring GPU acceleration

### Resource-Conscious Rules (M1 Air Specific)

5. **Generation Limit Rule**: Maximum 3 media items per session to avoid thermal throttling and battery drain.
   - Single images: 3 max
   - Carousels: 1 matchup (6 slides) at a time
   - Video conversion: 1 at a time

6. **API Cost Awareness Rule**: Notify user before ANY paid API call. Prefer cost-efficient options:
   - Gemini (generous free tier)
   - Local processing (PIL, FFmpeg)
   - Mock data for testing

7. **Background Process Rule**: Avoid long-running background processes. M1 Air should run lean:
   - No health monitor daemon (run `status` manually if needed)
   - Complete processes before starting new ones
   - Check/kill orphaned processes at session start

### Context Preservation Rules

8. **Context Sync Rule**: After completing work, update POCKET_CONTEXT.md AND set appropriate flags:
   - `POCKET_COMPLETED: [task]` - Something main sessions should know
   - `NEEDS_MAIN_WORKSTATION: [task]` - Too heavy for pocket
   - Update session count in header

9. **Compaction Context Rule**: Before compaction, capture ALL ongoing context:
   - Current task in progress
   - Pending decisions
   - Files modified
   - Use todo list to track in-progress work

10. **Python3 Rule**: Always use `python3` for all script execution. M1 architecture requires explicit version.

### Quality Rules

11. **Output Review Rule**: Use Read tool to view generated images directly for quality feedback. Iterate based on visual inspection - Claude can see text rendering, layout, colors.

12. **Incremental Implementation Rule**: One action at a time, pause for confirmation. Allows compaction without losing work.

### Cross-Session Rules

13. **Cross-Session Communication Rule**: When handing off tasks, include ALL details:
    - Exact file paths, function names, parameter values
    - Design decisions, rationale
    - Error messages and solutions
    - Assume other session has NO memory

14. **Session Role Clarity Rule**:
    | Role | Pocket Approach |
    |------|-----------------|
    | Dev work | Full capability, prefer smaller edits |
    | Media generation | 1-3 items max |
    | Pipeline runs | Targeted layers only |
    | Oracle maintenance | Quick audits, doc updates |
    | Content cranking | 1 matchup at a time |

---

## CAPABILITY MATRIX

| Task | Pocket Approach | Notes |
|------|-----------------|-------|
| **Dev work** | Full capability | Prefer smaller edits over large refactors |
| **Media generation** | Single items | Avoid batch runs; do 1-3 at a time |
| **Pipeline runs** | Targeted layers | Run specific layers, not full L1-L8 |
| **Oracle maintenance** | Full capability | Quick audits, doc updates |
| **Content cranking** | Limited batches | 1 matchup at a time vs. full week |
| **Research/planning** | Full capability | Ideal for pocket - low resource use |
| **Git operations** | Full capability | Commits, PRs, branch management |

### Efficiency Guidelines
- **Prefer**: Quick edits, targeted generation, research, planning, reviews
- **Batch carefully**: Media generation (1-3 items), API calls (watch costs)
- **Handoff when**: Full week batch needed, heavy video processing, multi-hour tasks

---

## MULTI-MACHINE WORKFLOW

> **Project syncs via iCloud Drive** - No git needed for main project files

### Before Switching Machines
1. Run `autosave` to save context
2. Wait for iCloud sync icon ✅ (check Finder status)
3. Close Claude Code session

### After Switching Machines
1. Verify iCloud synced (files show cloud ✅ not downloading)
2. Start new session with resume prompt
3. Run `audit --quick` to verify state

### MacBook Air First-Time Setup
```bash
# 1. Generate SSH key (for GitHub/git operations)
ssh-keygen -t ed25519 -C "w2csyh44qs@privaterelay.appleid.com" -f ~/.ssh/id_ed25519 -N ""
ssh-keyscan github.com >> ~/.ssh/known_hosts
cat ~/.ssh/id_ed25519.pub | pbcopy
# Add to GitHub Settings > SSH Keys as "MacBook Air"

# 2. Configure git
git config --global user.name "w2csyh44qs-web"
git config --global user.email "w2csyh44qs@privaterelay.appleid.com"

# 3. Wait for iCloud to sync project folder
```

### Mac Mini First-Time Setup (M3/M4)
```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""
ssh-keyscan github.com >> ~/.ssh/known_hosts
cat ~/.ssh/id_ed25519.pub | pbcopy
# Add to GitHub Settings > SSH Keys as "Mac Mini"

# 2. Configure git
git config --global user.name "your-username"
git config --global user.email "your-email@example.com"

# 3. Wait for iCloud to sync project folder

# 4. Install OpenCV in project venv (for advanced motion tracking)
cd "/path/to/AutomationScript"
source venv/bin/activate
pip install opencv-python-headless
```

**TODO (Mac Mini):** Run step 4 above to install OpenCV when first accessing this context from Mac Mini.

---

## CROSS-SESSION SYNC

### Reading Other Sessions
- `DEV_CONTEXT.md` - Current dev state, pending features
- `ORACLE_CONTEXT.md` - Health status, maintenance needs
- `CRANK_CONTEXT.md` - Generation queue, content status

### Pocket Flags
Set in this section when handing off:

**Status:** _(none)_

<!--
Available flags:
- POCKET_COMPLETED: [task] - Pocket finished something main sessions should know
- NEEDS_MAIN_WORKSTATION: [task] - Too heavy for pocket, queue for main
- POCKET_IN_PROGRESS: [task] - Currently working on (for crash recovery)
-->

---

## QUICK COMMANDS

```bash
# Health check (lightweight)
python3 maintenance/project_oracle.py status

# Quick audit
python3 maintenance/project_oracle.py audit --quick

# Autosave (always do before ending)
python3 maintenance/project_oracle.py autosave

# Single matchup generation (example)
python3 scripts/content_pipeline.py --preset carousel_illustrated --matchup "SF @ ARI"

# Run specific layer only
python3 scripts/[layer_script].py --specific-args
```

---

## RECENT CHANGES

### December 27, 2025 - Session P17
**OpenCV Installation & Comparison Test:**
- Installed `opencv-python-headless` (v4.12.0.88) on MacBook Air M1
- Added Mac Mini setup instructions with TODO to install OpenCV
- **Comparison test:** Chargers wheelchair meme - FFmpeg vs OpenCV
  - FFmpeg (linear interpolation): 2.1 MB, clean motion, no drift
  - OpenCV (Lucas-Kanade optical flow): 2.7 MB, tracking drift (140px, 377.5px)
  - **Conclusion:** FFmpeg better for predictable/linear motion; OpenCV for erratic/complex motion
- **Decision:** Don't build OpenCV module yet - wait for patterns from 2-3 real use cases before abstracting
- Output files in `final/memes/`:
  - `chargers_wheelchair_meme.mp4` (FFmpeg - cleaner)
  - `chargers_wheelchair_opencv.mp4` (OpenCV - drift issues)

### December 27, 2025 - Session P16
**Chargers Wheelchair Meme (COMPLETE):**
- Created v13 with text at bottom, white background boxes, black text
- 2-line caption: "The most accurate leg" / "in the NFL"
- Chargers logo (180x90) tracking on torso, appearing at 1.3s
- Duration: 4.8s, audio preserved
- Output: `content/nfl/2025-2026/regular_season/week17/final/memes/chargers_wheelchair_meme.mp4`

### December 27, 2025 - Session P12
**Display Mode Registry - Versatility Refactor (COMPLETE):**

Extended P11 implementation to ensure all routing is **future-proofed** for adding new presets without hardcoded canonical names.

**New Config Properties Added to Registry:**
```python
"sketch_insights_carousel": {
    "skip_logo": True,           # Cleaner design without logo overlay
    "slide_count": 6,            # Cover + 5 props
    ...
},
"sketch_matchup_carousel": {
    "skip_logo": False,          # Logo on all slides
    "slide_count": 3,            # Cover, matchup, bonus
    ...
},
```

**New Helper Functions:**
```python
def skip_logo(mode: str) -> bool       # Check if mode skips logo overlay
def get_slide_count(mode: str) -> int  # Get slide count (0 for non-carousels)
def get_prompt_builder(mode: str) -> Optional[str]  # Get prompt builder function name
```

**Routing Pattern - Future-Proof Design:**

| File | Change | Pattern |
|------|--------|---------|
| `idea_creation.py` | Uses `get_prompt_builder()` for routing | Data-driven, not hardcoded names |
| `idea_creation.py` | `media_format = resolved_mode` | Dynamic canonical name |
| `assembly.py` | `skip_logo(resolved_mode)` instead of tuple check | Registry-based |
| `assembly.py` | Type markers use `resolve_mode(display_mode)` | Dynamic type names |
| `assembly.py` | Type checks use `is_carousel()` + `has_reels()` | Registry-based |
| `media_generation.py` | `has_audio(resolve_mode())` | Registry-based |
| `content_pipeline.py` | Manual ideas use `display_mode: resolved_display_mode` | Dynamic routing |

**Key P12 Principle:**
> **Never hardcode canonical names in routing logic.** Use registry functions (`get_prompt_builder()`, `is_carousel()`, etc.) and dynamic `resolved_mode` so new presets work automatically.

**Example - idea_creation.py carousel routing:**
```python
if is_carousel(resolved_mode):
    prompt_builder = get_prompt_builder(resolved_mode)
    if prompt_builder == 'build_insights_carousel_prompts':
        # 6-slide insights carousel (routes by prompt builder, not mode name)
        idea['media_format'] = resolved_mode  # Dynamic!
    else:
        # Other carousels (3-slide matchup, future presets)
        idea['media_format'] = resolved_mode  # Dynamic!
```

**Example - assembly.py logo skip:**
```python
# OLD (hardcoded tuple):
# skip_logo_modes = ('insights_carousel', 'sketch_insights_carousel')
# should_apply_logo = overlay.logo and resolved_mode not in skip_logo_modes

# NEW (registry-based):
should_apply_logo = overlay.logo and not skip_logo(resolved_mode)
```

**Files Modified in P12:**
- `config/display_modes.py` - Added `skip_logo`, `slide_count` configs + helpers
- `scripts/idea_creation.py` - Uses `get_prompt_builder()`, dynamic `resolved_mode`
- `scripts/assembly.py` - Uses `skip_logo()`, dynamic type markers
- `scripts/media_generation.py` - Uses `has_audio(resolve_mode())`
- `scripts/content_pipeline.py` - Manual ideas use `display_mode` from preset

---

### December 27, 2025 - Session P11
**Display Mode Registry Implementation (COMPLETE):**

Created `config/display_modes.py` - centralized handler registry replacing scattered if/elif checks across all layers.

**Naming Convention:** `{visual_style}_{content_type}_{output_format}`
- `sketch_insights_carousel` - Watercolor insights, multi-slide with reels
- `sketch_matchup_carousel` - Watercolor matchup, multi-slide with reels
- `dark_incentives_image` - Dark theme incentives, single image with reels

**Layers Updated (L0-L7):**
- L0 `content_pipeline.py` - Uses `is_carousel()`, `has_reels()` for flag routing
- L1 `data_source.py` - Import added for future use
- L2 `calendar_config.py` - Import added for future use
- L3 `idea_creation.py` - Uses `is_carousel()`, `is_single_image()`, `resolve_mode()`
- L4 `audio_sync.py` - Import added, `has_audio()` for future routing
- L5 `media_generation.py` - Uses registry for carousel/single_image routing
- L6 `assembly.py` - Uses `is_carousel()`, `has_reels()` for assembly routing
- L7 `distribution.py` - Already updated, uses registry throughout

**script_presets.json Updates:**
- `carousel_illustrated` → `display_mode: "sketch_matchup_carousel"`
- `illustrated_insights_carousel` → `display_mode: "sketch_insights_carousel"`
- `dark_incentives` → `display_mode: "dark_incentives_image"`

**Key Design:**
- `has_reels` = config property (carousel ALSO generates 9:16 reels)
- `is_reel` = category check (pure reel preset like future memes)
- Legacy aliases in registry handle backward compatibility

---

### December 27, 2025 - Session P10
**dark_incentives Pipeline Integration (COMPLETE):**
- **L0/L3 Manual Input** - `api_source: "manual_input"` presets with `_collect_manual_incentive_data()` + `_run_l3_manual()`
- **L5 Generation** - `_generate_dark_incentives_image()` method, dark_incentives added to infographic branch
- **L7 Distribution Fix** - Added `insights_carousel` to carousel_reels handling (copies slides + reels to final)
- **Prompt fix** - Removed text bullets from incentive format (money bags only via Gemini)

**Week 17 Saturday Content (COMPLETE):**
- HOU @ LAC insights_carousel (6 slides + 6 reels)
- BAL @ GB insights_carousel (6 slides + 6 reels)
- Keenan Allen incentives v2 (image + MP4)

**Display Mode Refactoring (P10 analysis → P11 implementation):**
- **Option B Selected**: Handler Registry for extensibility with future modes
- See **Display Mode Architecture** section below for full design

**Files modified**: content_pipeline.py, media_generation.py, api_utils.py, distribution.py

---

### December 26, 2025 - Session P9
**LLM-Powered Extraction Refactor:**
- **Regex → LLM migration** - Replaced 3 brittle regex functions with LLM-powered versions:
  - `extract_betting_thesis_llm()` - Identifies pass/run/situational thesis
  - `extract_cover_insight_llm()` - Generates 45-char setup/conflict/resolution bullets
  - `determine_predicted_winner_llm()` - Handles contrarian bets correctly
- **Smart wrapper functions** - `smart_extract_*()` wrappers auto-route to LLM or regex based on global toggle
- **Global toggle system** - `set_llm_extraction()` / `is_llm_extraction_enabled()` in api_utils.py
- **L0 menu integration** - Tool Configuration → [e] Toggle LLM Extraction
- **Session-level setting** - `ContentPipeline.use_llm_extraction` persists for session
- **Cost**: ~$0.0003/matchup (negligible), default ON for quality

**Files modified**:
- `scripts/api_utils.py` (lines 62-107 toggle, 903-1233 LLM functions, 1236-1324 smart wrappers)
- `scripts/content_pipeline.py` (import, init, menu, toggle method, execution calls)

---

### December 25, 2025 - Session P1
**illustrated_insights_carousel refinements:**
- **Player body coherence** - Added anatomical coherence instructions to prevent disjointed poses (head/legs facing different directions)
- **Defender colors fixed** - Defenders in RB/WR poses now correctly wear opposing team colors
- **Defender no football** - Added instruction that only ball carrier has the ball
- **Removed bold from headers** - Prop headers use regular weight font (highlights handle emphasis)
- **Logo removed from all slides** - insights_carousel now has no logo overlay (cleaner Christmas theme)
- **Cover text cleanup** - Removed quotation marks and parentheses from game info
- **Multi-word duplicate fix** - Added regex to catch 2-3 word phrase duplications from API
- **Highlight length limit** - Max 20 chars per highlight to prevent over-highlighting
- **"To Throw" pattern** - Added pattern to extract player names from INT props
- **Stale QB correction** - Upfront correction of outdated QB names using TEAM_QBS database (e.g., Sam Darnold → J.J. McCarthy)
- **Cleaner highlight phrases** - Added 'hot outlet', "'hot' outlet", removed generic terms like 'scheme', 'pass rush'
- **INT prop title cleanup** - Remove "(or Starting QB)" from bet line display

**Files modified**: `api_utils.py` (lines ~2395-2410, ~2956-3022, ~3132-3141, ~3188-3200, ~3247-3257)

---

## SMART TEXT ANALYSIS TOOLKIT (P9)

> **Location:** `scripts/api_utils.py` - Lines 144-790
> **Power:** Gemini Flash (fast, cheap ~$0.0001/call, text-only)

### Core Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `analyze_for_highlights(text, context, max_highlights, max_chars)` | Find key phrases for visual emphasis | `List[str]` of exact phrases |
| `analyze_for_buckets(text, bucket_definitions, return_sentences)` | Categorize text into themes | `Dict[str, List[str]]` |
| `analyze_for_sentiment(text, context)` | Detect bullish/bearish/neutral | `Dict` with sentiment, confidence, reasoning |
| `extract_entities(text, entity_types)` | Pull out players, teams, stats | `Dict[str, List[str]]` |
| `extract_key_stats(text, stat_types)` | Structured stat extraction | `List[Dict]` with value, type, subject, context |
| `summarize_to_length(text, max_chars, style)` | Condense text to fit | `str` within limit |

### analyze_for_highlights

Intelligently identifies key phrases worth highlighting. Context-aware - understands that "26 carries" matters for RB props.

```python
from scripts.api_utils import analyze_for_highlights

highlights = analyze_for_highlights(
    text="Woody Marks could see bell-cow usage with 26 carries expected...",
    context="betting_prop",  # betting_prop | game_preview | player_spotlight | incentive
    max_highlights=3,
    max_chars_per_highlight=20
)
# Returns: ['bell-cow usage', '26 carries']
```

**Context Options:**
- `betting_prop` - Focus on: projected stats, matchup advantages, game situation edges, usage indicators
- `game_preview` - Focus on: key matchups, injury impacts, coaching tendencies, historical edges
- `player_spotlight` - Focus on: career achievements, season stats, notable streaks
- `incentive` - Focus on: thresholds, current progress, remaining games, dollar amounts

### analyze_for_buckets

Categorizes text into predefined thematic buckets. Use predefined sets or custom.

```python
from scripts.api_utils import analyze_for_buckets, get_bucket_definitions

# Using predefined buckets
buckets = analyze_for_buckets(
    text=prop_reasoning,
    bucket_definitions=get_bucket_definitions("betting_prop")
)
# Returns: {'matchup_edge': [...], 'usage_role': [...], 'game_script': [...], ...}

# Custom buckets
buckets = analyze_for_buckets(
    text=game_analysis,
    bucket_definitions={
        "bullish_points": "Reasons to bet the over/favorite",
        "bearish_points": "Reasons for caution or underdog"
    }
)
```

### Predefined Bucket Sets

Use `get_bucket_definitions(name)` or `list_available_bucket_sets()` to access these programmatically.

```python
BETTING_PROP_BUCKETS = {
    "matchup_edge": "Opponent defensive weakness, coverage mismatch, or scheme advantage that benefits the player",
    "usage_role": "Expected touches, targets, snap count, workload share, or role in the offense",
    "game_script": "Game situation that favors this player - shootout potential, must-win game, garbage time, etc.",
    "stat_support": "Historical stats, recent trends, or season averages that support the bet",
    "risk_factors": "Concerns, injury notes, weather impact, or reasons for caution",
    "key_phrases": "The 2-3 most important short phrases that represent the core betting edge"
}

GAME_PREVIEW_BUCKETS = {
    "matchup_keys": "Critical X-factors and matchup advantages that will decide the game",
    "injury_impact": "Key injuries and how they affect each team's chances",
    "coaching_notes": "Coaching tendencies, scheme matchups, or strategic considerations",
    "weather_travel": "Weather conditions, travel fatigue, short week, or environmental factors",
    "historical_context": "Past meetings, revenge games, or relevant historical trends",
    "key_phrases": "The 2-3 most important short phrases that capture the game narrative"
}

PLAYER_ANALYSIS_BUCKETS = {
    "recent_form": "Last few games performance, hot/cold streaks, momentum",
    "season_trajectory": "How the season has gone overall, improvement or decline",
    "role_situation": "Current role, snap share, target share, touches - and any changes",
    "matchup_history": "Past performance against this opponent or similar matchups",
    "outlook_take": "Overall assessment and expectations going forward",
    "key_phrases": "The 2-3 most important short phrases about this player"
}

INCENTIVE_BUCKETS = {
    "threshold_status": "Current progress toward incentive threshold (yards, TDs, etc.)",
    "games_remaining": "How many games left and pace needed to hit the incentive",
    "motivation_level": "How likely the team/player is to prioritize hitting this incentive",
    "dollar_amount": "The monetary value of the incentive at stake",
    "hit_probability": "Assessment of likelihood to achieve the incentive",
    "key_phrases": "The 2-3 most important short phrases about this incentive situation"
}
```

### analyze_for_sentiment

Detects tone for color-coding decisions (green for bullish, red for bearish).

```python
from scripts.api_utils import analyze_for_sentiment

sentiment = analyze_for_sentiment(
    text="He's due for a breakout game against this weak defense",
    context="betting"  # betting | performance | matchup
)
# Returns: {'sentiment': 'bullish', 'confidence': 0.85, 'reasoning': 'Positive matchup outlook'}
```

### extract_entities

Pulls out named entities from text.

```python
from scripts.api_utils import extract_entities

entities = extract_entities(
    text="Patrick Mahomes threw for 350 yards against the Raiders",
    entity_types=["players", "teams", "stats"]  # Optional, defaults to all
)
# Returns: {'players': ['Patrick Mahomes'], 'teams': ['Raiders'], 'stats': ['350 yards']}
```

### extract_key_stats

Structured stat extraction with context.

```python
from scripts.api_utils import extract_key_stats

stats = extract_key_stats(
    text="Mahomes has thrown for 4,200 yards this season",
    stat_types=["yards", "touchdowns"]  # Optional filter
)
# Returns: [{'value': '4,200 yards', 'type': 'yards', 'subject': 'Mahomes', 'context': 'passing this season'}]
```

### summarize_to_length

Condense text to fit UI constraints.

```python
from scripts.api_utils import summarize_to_length

summary = summarize_to_length(
    text="Long prop reasoning text here...",
    max_chars=100,
    preserve_key_info=True,  # Keep player names, stats
    style="headline"  # concise | headline | bullet
)
# Returns: "Mahomes set for big game vs weak Raiders D"
```

### Internal Function

`_call_text_analyzer(prompt, model, temperature)` - Low-level Gemini Flash call. Presets should NOT call this directly.

---

## LLM-POWERED EXTRACTION (P9 REFACTOR)

> **Location:** `scripts/api_utils.py` - Lines 896-1180
> **Purpose:** Replace complex regex patterns with intelligent LLM analysis

These functions replace the legacy regex-based extraction with smarter LLM-powered versions that understand context better.

### extract_betting_thesis_llm

Identifies the primary thesis for why a pick should cover.

```python
from scripts.api_utils import extract_betting_thesis_llm

thesis = extract_betting_thesis_llm(
    reasoning="The Ravens run game has been dominant. The Texans run D ranks #26...",
    teams={'winner': 'Ravens', 'loser': 'Texans', 'winner_abbrev': 'BAL', 'loser_abbrev': 'HOU'}
)
# Returns: {'type': 'run_based', 'angle': 'run_d_vulnerable', 'confidence': 0.95}
```

**Thesis Types:**
- `pass_based`: Secondary weakness, aerial attack, coverage issues
- `run_based`: Run defense weakness, ground game dominance, clock control
- `situational`: Must-win, playoff implications, home field, motivation

### extract_cover_insight_llm

Extracts punchy 45-character insights for carousel bullets.

```python
from scripts.api_utils import extract_cover_insight_llm

# Follows narrative flow: setup → conflict → resolution
setup = extract_cover_insight_llm(reasoning, 'setup', teams, thesis)
# Returns: "BAL 10-5, playoff seeding at stake"

conflict = extract_cover_insight_llm(reasoning, 'conflict', teams, thesis)
# Returns: "HOU run D #26: 142.3 YPG allowed"

resolution = extract_cover_insight_llm(reasoning, 'resolution', teams, thesis)
# Returns: "BAL covers comfortably"
```

### determine_predicted_winner_llm

Analyzes reasoning to find the actual predicted winner (handles contrarian bets).

```python
from scripts.api_utils import determine_predicted_winner_llm

winner = determine_predicted_winner_llm(
    best_bet_desc="Green Bay Packers +3",  # Underdog bet
    best_bet_reasoning="...",
    away_team="Packers", home_team="Vikings",
    away_abbrev="GB", home_abbrev="MIN"
)
# Returns: "Vikings"  (actual predicted winner, not bet team)
```

### When to Use LLM vs Regex Versions

| Scenario | Use | Reason |
|----------|-----|--------|
| Production carousel generation | LLM versions | More accurate, context-aware |
| High-volume batch processing | Regex versions | Faster, no API calls |
| Testing/development | Either | LLM for quality, regex for speed |
| Offline/no API key | Regex versions | No network required |

### L0 Toggle (content_pipeline.py)

The LLM extraction toggle is accessible via the **Tool Configuration** menu:

```
[t] Tool Configuration
   → [e] Toggle LLM Extraction (thesis/insights)
```

**Session Setting:**
- Default: **ON** (LLM-powered, ~$0.0003/matchup)
- Toggle persists for the session
- Applied automatically before any pipeline execution

**How It Works:**
1. `ContentPipeline` stores `self.use_llm_extraction = True`
2. Before any execution (`_execute_generate`, `_execute_discovery`, `run_quick_carousel`), it calls `set_llm_extraction(self.use_llm_extraction)`
3. Smart wrapper functions (`smart_extract_betting_thesis()`, etc.) check `is_llm_extraction_enabled()` and route accordingly

**Presets don't need to know about the toggle** - they just call the smart wrappers which handle the routing internally.

---

## PRESET BUILDING RULES

> **Rule: Audit Tools First** - Before building ANY new preset, review available tools and utilize them smartly.

### Tool Audit Checklist

When creating a new preset, check:

1. **Smart Text Analysis (api_utils.py)**
   - [ ] Can `analyze_for_highlights()` identify key visual emphasis phrases?
   - [ ] Can `analyze_for_buckets()` organize content into sections?
   - [ ] Can `analyze_for_sentiment()` inform color/styling choices?
   - [ ] Can `extract_entities()` auto-populate player/team/stat fields?
   - [ ] Can `extract_key_stats()` structure statistical data?
   - [ ] Can `summarize_to_length()` fit text into space constraints?

2. **Team/Player Lookups (api_utils.py)**
   - [ ] `get_team_name(abbrev)` / `get_team_abbrev(name)` for team normalization
   - [ ] `get_player_position(name)` for pose/layout decisions
   - [ ] `get_player_team()` for color assignment
   - [ ] `TEAM_NAMES`, `PLAYER_TEAMS`, `TEAM_QBS` databases

3. **Color System (config/team_colors.py)**
   - [ ] `get_matchup_colors(away, home, league)` for team color palettes
   - [ ] `get_team_colors(abbrev, league)` for single team
   - [ ] `TEAM_COLORS` dict with primary/secondary/accent

4. **Prompt Building Patterns (api_utils.py)**
   - [ ] `build_insights_carousel_prompts()` - 6-slide carousel pattern
   - [ ] `build_dark_incentives_prompt()` - Single-page incentives pattern
   - [ ] `build_carousel_prompts()` - Standard carousel pattern
   - [ ] `get_position_pose()` - Athletic pose descriptions

5. **Data Transformation (api_utils.py)**
   - [ ] `transform_matchup_for_carousel()` - API → carousel data
   - [ ] `extract_betting_thesis_llm()` - LLM-powered betting thesis extraction
   - [ ] `extract_cover_insight_llm()` - LLM-powered 45-char insight extraction
   - [ ] `determine_predicted_winner_llm()` - LLM-powered winner prediction

6. **Asset Ingestion (asset_ingestion.py)**
   - [ ] Video/image download, segmentation, component extraction
   - [ ] Text removal tools: `--auto-crop`, `--crop-top`, `--find-original`

7. **Assembly Tools (assembly.py)**
   - [ ] `meme_mashup` - Multi-clip with text overlay
   - [ ] `meme_overlay` - Single clip with captions + logo
   - [ ] 9:16 video creation with padding

### Suggest New Tools

If existing tools don't cover a need, document the gap:

```
TOOL GAP: [description]
SUGGESTED FUNCTION: [name]
USE CASE: [preset(s) that would benefit]
INPUTS: [what it needs]
OUTPUTS: [what it returns]
```

Example gaps to consider:
- `generate_comparison_table()` - Side-by-side stat comparisons
- `validate_prop_data()` - Ensure prop has required fields
- `format_currency()` - Consistent money formatting
- `generate_trend_indicator()` - Up/down arrows based on data

### Preset Integration Pattern

```python
def build_new_preset_prompt(api_data: Dict, away: str, home: str) -> Dict[str, str]:
    """Build prompts for [preset_name].

    Uses:
        - analyze_for_highlights(): For key phrase emphasis
        - analyze_for_buckets(): For content organization
        - analyze_for_sentiment(): For color decisions
        - get_matchup_colors(): For team colors
        - summarize_to_length(): For space constraints
    """
    # 1. Get colors
    away_colors, home_colors = get_matchup_colors(away, home, 'NFL')

    # 2. Analyze content
    buckets = analyze_for_buckets(reasoning, get_bucket_definitions("betting_prop"))
    highlights = analyze_for_highlights(reasoning, context="betting_prop")
    sentiment = analyze_for_sentiment(reasoning, context="betting")

    # 3. Build structured prompt using analyzed data
    ...
```

---

## DISPLAY MODE ARCHITECTURE (P11/P12)

> **Location:** `config/display_modes.py`
> **Purpose:** Centralized registry for routing content through layers based on visual style and output format
> **Key Principle (P12):** Never hardcode canonical names - use registry functions for future-proof routing

### Naming Convention Rule

**Format:** `{visual_style}_{content_type}_{output_format}`

| Component | Description | Examples |
|-----------|-------------|----------|
| **visual_style** | The artistic/design treatment | `sketch`, `dark`, `minimal`, `photo`, `neon` |
| **content_type** | What the content is about | `insights`, `incentives`, `matchup`, `stats`, `infographic` |
| **output_format** | Final deliverable type | `carousel`, `image`, `reel`, `video` |

**Output Format Definitions:**
- `carousel` - Multi-slide images (may also generate reels via `has_reels` config)
- `image` - Single standalone image
- `reel` - Short-form video (<60s, 9:16 aspect ratio, for social platforms)
- `video` - Longer-form video (>60s, various aspect ratios, future presets)

**Examples:**
```
sketch_insights_carousel   → Watercolor/sketch style, betting insights, multi-slide carousel
dark_incentives_image      → Dark theme, player incentives, single image
minimal_stats_carousel     → Clean minimal style, statistics, multi-slide
photo_matchup_reel         → Photo-realistic, matchup preview, short-form video
```

### Handler Registry Design (P11 + P12 Extensions)

```python
DISPLAY_MODE_HANDLERS = {
    "sketch_insights_carousel": {
        "category": "carousel",
        "aspect_ratio": "1:1",
        "has_reels": True,        # L6 generates 9:16 reels from slides
        "has_audio": False,       # L4 skipped
        "skip_logo": True,        # P12: Cleaner design without logo overlay
        "slide_count": 6,         # P12: Cover + 5 props
        "layers": ["L3", "L5", "L6", "L7"],
        "prompt_builder": "build_insights_carousel_prompts",
        "description": "GoatedBets insights with watercolor illustrated players",
        "aliases": ["insights_carousel", "illustrated_insights_carousel"]
    },
    "sketch_matchup_carousel": {
        "category": "carousel",
        "aspect_ratio": "1:1",
        "has_reels": True,
        "has_audio": False,
        "skip_logo": False,       # P12: Logo on all slides
        "slide_count": 3,         # P12: Cover, matchup, bonus
        "layers": ["L3", "L5", "L6", "L7"],
        "prompt_builder": "build_carousel_prompts",
        "description": "3-slide matchup carousel with sketch/watercolor style",
        "aliases": ["carousel", "carousel_reels", "carousel_illustrated"]
    },
    "dark_incentives_image": {
        "category": "single_image",
        "aspect_ratio": "1:1",
        "has_reels": True,        # L6 converts to 9:16 video
        "has_audio": False,
        "layers": ["L3", "L5", "L6", "L7"],
        "prompt_builder": "build_dark_incentives_prompt",
        "description": "Player contract incentives on dark crumpled paper",
        "aliases": ["dark_incentives"]
    },
    # Future modes follow same pattern...
}
```

### Key Design Decisions

1. **`has_reels` is a config property, not a mode name suffix**
   - Wrong: `sketch_insights_carousel_reels` (don't suffix with output variants)
   - Right: `sketch_insights_carousel` with `has_reels: True`

2. **`has_audio` determines L4 execution**
   - Most current modes skip L4 (TTS/voiceover)
   - Future modes like `narrated_*` would have `has_audio: True`

3. **All layers (L0-L7) use the registry**
   - L0: Display mode selection in pipeline
   - L3: Data transformation routing
   - L4: Audio sync (if `has_audio: True`)
   - L5: Image/media generation routing
   - L6: Assembly (reels if `has_reels: True`)
   - L7: Distribution (folder routing by category)

4. **Display mode aligns with preset name**
   - The `display_mode` value should match or derive from the preset name
   - Enables consistent routing across all layers

5. **P12: Never hardcode canonical names in routing logic**
   - Use `get_prompt_builder()` for routing decisions (not mode name checks)
   - Use `resolved_mode` dynamically for `media_format` and type markers
   - This ensures new presets work automatically without code changes

### Helper Functions

```python
# Category checks
def is_carousel(mode: str) -> bool
def is_single_image(mode: str) -> bool
def is_reel(mode: str) -> bool
def is_video(mode: str) -> bool

# Config accessors
def has_reels(mode: str) -> bool
def has_audio(mode: str) -> bool
def skip_logo(mode: str) -> bool          # P12: Check if mode skips logo
def get_slide_count(mode: str) -> int      # P12: Get slide count (0 for non-carousels)
def get_aspect_ratio(mode: str) -> str
def get_layers(mode: str) -> List[str]
def get_prompt_builder(mode: str) -> str   # P12: For data-driven routing

# Layer routing
def needs_layer(mode: str, layer: str) -> bool
def get_category(mode: str) -> str

# Alias resolution
def resolve_mode(mode: str) -> str         # Convert legacy alias to canonical name
def is_known_mode(mode: str) -> bool       # Check if mode is registered
```

### P12 Routing Patterns

**Pattern 1: Route by prompt_builder (not mode name)**
```python
# In idea_creation.py - routes carousel types by prompt builder function
if is_carousel(resolved_mode):
    prompt_builder = get_prompt_builder(resolved_mode)
    if prompt_builder == 'build_insights_carousel_prompts':
        # 6-slide insights carousel
        idea['media_format'] = resolved_mode  # Dynamic canonical name
    else:
        # Other carousels (3-slide, future presets)
        idea['media_format'] = resolved_mode  # Dynamic canonical name
```

**Pattern 2: Use registry helpers (not hardcoded tuples)**
```python
# In assembly.py - logo skip decision
# OLD: skip_logo_modes = ('insights_carousel', 'sketch_insights_carousel')
# NEW:
should_apply_logo = overlay.logo and not skip_logo(resolved_mode)
```

**Pattern 3: Dynamic type markers**
```python
# In assembly.py - return type uses resolved mode
display_mode = package.get('display_mode', '')
type_name = resolve_mode(display_mode) if display_mode else 'carousel_with_reels'
return {'type': type_name, ...}  # Dynamic, not hardcoded
```

**Pattern 4: Registry-based audio check**
```python
# In media_generation.py
needs_audio = any(has_audio(resolve_mode(i.get('display_mode', ''))) for i in ideas)
```

### Current Display Modes (P12)

| Mode | Category | Reels | Audio | Logo | Slides | Prompt Builder |
|------|----------|-------|-------|------|--------|----------------|
| `sketch_insights_carousel` | carousel | ✓ | ✗ | ✗ | 6 | `build_insights_carousel_prompts` |
| `sketch_matchup_carousel` | carousel | ✓ | ✗ | ✓ | 3 | `build_carousel_prompts` |
| `dark_incentives_image` | single_image | ✓ | ✗ | - | - | `build_dark_incentives_prompt` |

### Future Modes (Planned)

| Mode | Category | Reels | Audio | Description |
|------|----------|-------|-------|-------------|
| `minimal_stats_image` | single_image | ✗ | ✗ | Clean stat infographic |
| `photo_highlight_reel` | reel | N/A | ✓ | Photo-real highlight with voiceover |
| `neon_promo_video` | video | N/A | ✓ | Longer promotional video |
| `meme_*_reel` | reel | N/A | ✗ | Meme-style short-form (future) |

### Adding New Presets (P12 Guide)

When adding a new display mode:

1. **Add to registry** (`config/display_modes.py`):
   ```python
   "new_style_content_format": {
       "category": "carousel|single_image|reel|video",
       "has_reels": True|False,
       "has_audio": True|False,
       "skip_logo": True|False,  # If carousel
       "slide_count": N,          # If carousel
       "prompt_builder": "build_new_prompt_function",
       "description": "...",
       "aliases": ["legacy_name"]  # If replacing old mode
   }
   ```

2. **Create prompt builder** (`scripts/api_utils.py`):
   - Function name must match `prompt_builder` value in registry

3. **No code changes needed in**:
   - `idea_creation.py` - Routes by `get_prompt_builder()` and category
   - `assembly.py` - Uses registry helpers (`skip_logo()`, `is_carousel()`, etc.)
   - `media_generation.py` - Uses `has_audio()` check
   - `content_pipeline.py` - Uses `display_mode` from preset config

4. **Add preset to `script_presets.json`**:
   ```json
   "new_preset_name": {
       "display_mode": "new_style_content_format",
       ...
   }
   ```

---

## CAROUSEL ARCHITECTURE REFERENCE

### Data Flow Differences

| Preset | Data Source | Props Field | Slide Count |
|--------|-------------|-------------|-------------|
| `carousel_illustrated` | `fetch_and_transform_matchup()` | `bonus_props` (3 max) | 3 slides |
| `insights_carousel` | `fetch_goatedbets_matchup()` (RAW) | `props`/`betting_insights` (5) | 6 slides |

**CRITICAL**: When regenerating `insights_carousel` slides manually:
- Use `fetch_goatedbets_matchup()` to get RAW API data (not transformed)
- RAW data has `props` or `betting_insights` key with 5 items
- Transformed data has `bonus_props` with only 3 items (for standard carousel)

### Regenerating Specific Slides
```python
from scripts.idea_creation import fetch_goatedbets_matchup
from scripts.api_utils import build_insights_carousel_prompts, get_team_name

# Get RAW API data (not transformed!)
away_team = get_team_name('DET')
home_team = get_team_name('MIN')
api_data = fetch_goatedbets_matchup(away_team, home_team)

# Build prompts - returns dict with 'cover', 'prop_1', 'prop_2', etc.
prompts = build_insights_carousel_prompts(api_data, 'DET', 'MIN')

# Then use Gemini to generate specific slides
```

**Christmas Day Carousels generated (P1-P2):**
- Cowboys @ Commanders (DAL_WAS_insights_carousel)
- Lions @ Vikings (DET_MIN_insights_carousel)
- Broncos @ Chiefs (DEN_KC_insights_carousel)

### December 24, 2025 - Ready for P1
**Recent main session updates to be aware of:**

**D100 (Dev - Dec 24)** - Carousel architecture simplified
- All carousels now output 9:16 MP4s (unified from 3 separate display modes)
- `carousel_illustrated_reels` preset removed, merged into `carousel_illustrated`
- Christmas Day variant added (auto-detects Dec 25 games, subtle festive accents)
- illustrated_insights_carousel refinements (6 tasks complete)

**O75 (Oracle - Dec 24)** - D100 cleanup complete + health improvements
- Health score improved: 5.7 → 8.4/10
- Verified carousel architecture cleanup
- Fixed CHANGELOG.md path, accepted unused imports/long functions
- Updated ARCHITECTURE.md with simplified carousel presets

**C10 (Crank - Dec 24)** - Week 16 complete, illustrated_insights_carousel tested
- Cowboys @ Commanders test (2 slides generated, data filtering limited output)
- Week 16 carousel_illustrated matchups all generated
- Awaiting Week 17 schedule

### December 23, 2025 - Session 0 (P0)
- **Initial Setup** - Created POCKET_CONTEXT.md (by O71)
- Defined as lightweight full-function session for MacBook Air
- Established capability matrix and efficiency guidelines

---

## PENDING TASKS

_(Tasks specifically for pocket sessions)_

- [x] Test single-matchup generation workflow on Air ✅
- [x] Verify oracle commands work on portable setup ✅
- [x] Generate Christmas Day carousels (DAL@WAS, DET@MIN) ✅
- [x] Final refinements on DET@MIN (prop_2, prop_4) ✅
- [x] Assemble and distribute both carousels ✅
- [x] Standardize output folder naming ✅
- [x] Generate DEN@KC insights_carousel ✅ (P2)
- [x] Create dark_incentives preset ✅ (P3)
- [x] Generate Deebo Samuel incentives page (Christmas theme) ✅ (P3)
- [x] Adjust Deebo jersey number to #1 ✅ (accepted v10 as final - jersey # minor detail)

---

## CURRENT STATE (P20)

**Session Status:** P20 - Week 17 Sunday Slate Complete

**Work Completed (Dec 28, 2025 - P20):**
1. ✅ Generated all 11 Sunday insights carousels (66 slides + 66 reels)
2. ✅ Toned down ink splatters permanently in `api_utils.py`:
   - Changed intensity from "30-100%" to "15-40%"
   - Changed style from "Dramatic ink splatter explosions" to "Subtle, refined watercolor washes"
   - Applied to both cover and prop slides

**Week 17 Sunday Carousels (all in `final/carousels/20251228_{matchup}/`):**
| # | Matchup | Predicted Winner | Best Bet |
|---|---------|------------------|----------|
| 1 | PIT @ CLE | Browns | Browns -2.5 |
| 2 | ARI @ CIN | Cardinals | Cardinals -2.5 |
| 3 | NO @ TEN | Titans | Titans -2.5 |
| 4 | SEA @ CAR | Panthers | Panthers -2.5 |
| 5 | JAX @ IND | Jaguars | Jaguars -2.5 |
| 6 | TB @ MIA | Dolphins | Dolphins -2.5 |
| 7 | NE @ NYJ | Jets | Jets -2.5 |
| 8 | NYG @ LV | Raiders | Raiders -2.5 |
| 9 | PHI @ BUF | Bills | Bills -1.5 |
| 10 | CHI @ SF | Bears | Bears -2.5 |
| 11 | LAR @ ATL | Falcons | Falcons -2.5 |

**Total Cost:** ~$0.132 (11 × $0.012)

**Previous Session Work (P19):**
- ✅ Generated all 6 incentive slides from IMG_0588 (1:1 + 9:16 reels)
- ✅ Updated PLAYER_TEAMS database (Diggs→Patriots, Darnold→Seahawks, Dowdle→Panthers)
- ✅ Fixed Gemini model association issue for traded players

**Previous Session Work (P18):**
- ✅ Documented Vision system design IN DETAIL in POCKET_CONTEXT.md
- ✅ Created Vision vs Display Mode conceptual separation
- ✅ Designed Control Point Hierarchy (Vision → Display Mode → Prompt Builder → Generation)
- ✅ Defined expanded Vision dataclass with 15+ fields
- ✅ Created 3 initial vision presets (analytical, hype, casual)

**Previous Session Work (P17):**
- ✅ Installed OpenCV (v4.12.0.88) on MacBook Air M1
- ✅ Added Mac Mini setup instructions with OpenCV TODO
- ✅ Ran OpenCV vs FFmpeg comparison on Chargers wheelchair meme
- ✅ Documented findings: FFmpeg better for linear motion, OpenCV for complex motion
- ✅ Decision: Don't abstract OpenCV to module yet - wait for patterns

**Previous Session Work (P15-P16):**
- ✅ Analyzed all scripts (27,433 total lines)
- ✅ Designed layer-based folder structure with `_L{n}/` implementation folders
- ✅ Planned api_utils.py decomposition into L0, L1, L3 components
- ✅ Documented naming conventions (A-E suggestions all implemented)
- ✅ Created 4-phase migration plan with risk mitigation
- ✅ Documented post-migration checklist
- ✅ **RENAMED:** `g_api_processor.py` → `goatedbets_api_processor.py`
- ✅ Chargers wheelchair meme v13 complete (FFmpeg version)

---

## 📁 SCRIPTS REORGANIZATION PLAN (P15)

> **Implementation:** After Week 17 Sunday content is generated
> **Risk Level:** Medium - 2-3 focused sessions, mostly import rewiring
> **Approach:** Phased migration (copy first → test → delete originals)

### Design Principles

1. **Layers ARE the Switchboards** - L0-L8 platform scripts serve as routing layers
2. **Implementation in `_L{n}/` folders** - Underscore = internal implementation
3. **L0 handles cross-layer data** - Teams, players, colors live in `_L0/`
4. **API/MCP naming convention** - `_api` and `_mcp` suffixes for clarity
5. **No hardcoded names** - Registry-based routing for extensibility

### Final Structure (5-Folder Symmetric Pattern)

**Subfolder Convention:** Every `_L{n}/` folder has the same 5 subfolders:
```
inputs/     ← Data coming in (fetchers, lookups, constants)
analysis/   ← Inspection, extraction, validation
processors/ ← Transformation, manipulation
outputs/    ← Builders, formatters, final results
utils/      ← Fallback for rare scripts (checkpoints, constants)
```

**Flow:** `inputs/ → analysis/ → processors/ → outputs/` (with `utils/` for edge cases)

```
scripts/
├── pipeline.py              ← L0 SWITCHBOARD: Entry + orchestration (v1.0)
│   └── _L0/
│       ├── __init__.py      ← Re-exports: get_team(), get_player(), run_pipeline()
│       ├── inputs/
│       │   ├── teams.py         ← Team names, abbrevs, colors (from api_utils)
│       │   └── players.py       ← Player database, positions (from api_utils)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L1_data.py               ← L1 SWITCHBOARD: External data inputs (v1.0)
│   └── _L1/
│       ├── __init__.py      ← Re-exports: fetch_matchup(), fetch_odds(), call_ai()
│       ├── inputs/
│       │   ├── goatedbets_api.py    ← GoatedBets API client
│       │   ├── balldontlie_mcp.py   ← Ball Don't Lie MCP client
│       │   ├── odds_api.py          ← OddsAPI client
│       │   ├── web_trends_api.py    ← Web trends/search API
│       │   ├── assets.py            ← Asset ingestion (from asset_ingestion.py)
│       │   ├── ai_models.py         ← AI model routing (from ai_models.py)
│       │   └── google_api.py        ← Google API client (from api_utils)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L2_calendar.py           ← L2 SWITCHBOARD: Scheduling (v1.0)
│   └── _L2/
│       ├── __init__.py      ← Future: get_week_games(), get_segment()
│       ├── inputs/              ← (empty initially)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L3_ideas.py              ← L3 SWITCHBOARD: Ideas + text + prompts (v1.0)
│   └── _L3/
│       ├── __init__.py      ← Re-exports: generate_ideas(), build_prompt()
│       ├── inputs/              ← (empty initially - data comes from L0/L1)
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── smart_text.py            ← Smart text functions (from api_utils)
│       │   ├── goatedbets_api_processor.py  ← RENAMED from g_api_processor.py
│       │   └── betting_thesis.py        ← Thesis extraction (from api_utils)
│       ├── processors/
│       │   └── transforms.py    ← Data transforms (from api_utils)
│       ├── outputs/
│       │   ├── __init__.py      ← Registry: get_prompt_builder()
│       │   ├── carousel.py              ← build_carousel_prompts()
│       │   ├── insights_carousel.py     ← build_insights_carousel_prompts()
│       │   ├── dark_incentives.py       ← build_dark_incentives_prompt()
│       │   └── poses.py                 ← get_position_pose()
│       └── utils/
│           └── approve.py       ← Checkpoint: approve_ideas.py
│
├── L4_audio.py              ← L4 SWITCHBOARD: Audio/TTS (v1.0)
│   └── _L4/
│       ├── __init__.py      ← Future: generate_audio(), expand_script()
│       ├── inputs/              ← (empty initially)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L5_media.py              ← L5 SWITCHBOARD: Media gen + processing (v1.0)
│   └── _L5/
│       ├── __init__.py      ← Re-exports: generate_image(), process_image()
│       ├── inputs/              ← (empty initially)
│       ├── analysis/            ← (empty initially)
│       ├── processors/
│       │   ├── pil_processor.py     ← PIL operations (keep name)
│       │   └── ffmpeg_processor.py  ← FFmpeg operations (keep name)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L6_assembly.py           ← L6 SWITCHBOARD: Assembly (v1.0)
│   └── _L6/
│       ├── __init__.py      ← Future: assemble_video(), apply_overlay()
│       ├── inputs/              ← (empty initially)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L7_distribution.py       ← L7 SWITCHBOARD: Distribution (v1.0)
│   └── _L7/
│       ├── __init__.py      ← Future: distribute(), get_platform_specs()
│       ├── inputs/              ← (empty initially)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
├── L8_analytics.py          ← L8 SWITCHBOARD: Analytics (v1.0)
│   └── _L8/
│       ├── __init__.py      ← Future: track_performance(), generate_report()
│       ├── inputs/              ← (empty initially)
│       ├── analysis/            ← (empty initially)
│       ├── processors/          ← (empty initially)
│       ├── outputs/             ← (empty initially)
│       └── utils/               ← (empty initially)
│
└── archive/                 ← Old scripts, deprecated code
```

### Layer Responsibilities (Reference)

| Layer | Role | Key Functions | Imports From |
|-------|------|---------------|--------------|
| L0 | Cross-layer + orchestration | `get_team()`, `get_player()`, `run_pipeline()` | L1-L8 |
| L1 | External data inputs | `fetch_matchup()`, `fetch_odds()`, `call_ai()`, `ingest_asset()` | L0 |
| L2 | Calendar/scheduling | `get_week_games()`, `get_segment()` | L0 |
| L3 | Ideas + text + prompts | `generate_ideas()`, `analyze_highlights()`, `build_prompt()`, `approve_ideas()` | L0, L1 |
| L4 | Audio/TTS | `generate_audio()`, `expand_script()` | L0, L3 |
| L5 | Media gen + processing | `generate_image()`, `process_image()`, `process_video()` | L0, L3 |
| L6 | Assembly | `assemble_video()`, `apply_overlay()` | L0, L5 |
| L7 | Distribution | `distribute()`, `get_platform_specs()` | L0 |
| L8 | Analytics | `track_performance()`, `generate_report()` | L0, L7 |

### File Migration Mapping

| Current File | Lines | Destination | Notes |
|--------------|-------|-------------|-------|
| `api_utils.py` | 4,763 | **SPLIT** → see below | Largest file, needs decomposition |
| `assembly.py` | 3,303 | `L6_assembly.py` | Becomes L6 switchboard |
| `media_generation.py` | 3,142 | `L5_media.py` | Becomes L5 switchboard |
| `content_pipeline.py` | 1,710 | `pipeline.py` (L0) | Becomes entry point |
| `idea_creation.py` | 1,722 | `L3_ideas.py` | Becomes L3 switchboard |
| `distribution.py` | 1,673 | `L7_distribution.py` | Becomes L7 switchboard |
| `pil_processor.py` | 969 | `_L5/processors/pil_processor.py` | Keep name |
| `ffmpeg_processor.py` | 969 | `_L5/processors/ffmpeg_processor.py` | Keep name |
| `audio_sync.py` | 879 | `L4_audio.py` | Becomes L4 switchboard |
| `asset_ingestion.py` | 618 | `_L1/inputs/assets.py` | Renamed |
| `ai_models.py` | 611 | `_L1/inputs/ai_models.py` | AI as input source |
| `g_api_processor.py` | 927 | `_L3/analysis/goatedbets_api_processor.py` | **RENAMED** - GoatedBets API data processor |
| `goatedbets.py` | 446 | `_L1/inputs/goatedbets_api.py` | API client |
| `approve_ideas.py` | 260 | `_L3/utils/approve.py` | Checkpoint in utils |
| `data_source.py` | 256 | Archive or merge into L1 | Evaluate usage |
| `calendar_config.py` | 172 | `L2_calendar.py` | Becomes L2 switchboard |
| `balldontlie_mcp.py` | 127 | `_L1/inputs/balldontlie_mcp.py` | MCP client |

### api_utils.py Decomposition (4,763 lines)

| Section | Lines | Destination |
|---------|-------|-------------|
| Team data (TEAM_NAMES, TEAM_COLORS, etc.) | ~200 | `_L0/inputs/teams.py` |
| Player data (PLAYER_TEAMS, TEAM_QBS, etc.) | ~150 | `_L0/inputs/players.py` |
| Smart text functions | ~650 | `_L3/analysis/smart_text.py` |
| Thesis extraction | ~300 | `_L3/analysis/betting_thesis.py` |
| Data transforms | ~400 | `_L3/processors/transforms.py` |
| Prompt builders | ~800 | `_L3/outputs/*.py` |
| Google API client | ~500 | `_L1/inputs/google_api.py` |
| Highlight analysis | ~300 | `_L3/analysis/smart_text.py` |
| LLM extraction functions | ~400 | `_L3/analysis/betting_thesis.py` |
| Remaining utilities | ~1,000+ | Distribute by function to appropriate subfolders |

### Naming Conventions

**A. Version in switchboard docstrings**
```python
"""L3_ideas.py - Ideas & Text Switchboard (v1.0)

Handles idea generation, text analysis, and prompt building.
Bump version on breaking changes.
"""
```

**B. Function naming convention**
| Prefix | Purpose | Example |
|--------|---------|---------|
| `get_*` | Retrieves existing data | `get_team()`, `get_player()` |
| `build_*` | Constructs new content | `build_carousel_prompts()` |
| `process_*` | Transforms input to output | `process_image()` |
| `extract_*` | Pulls structured data from unstructured | `extract_entities()` |
| `format_*` | Prepares for display | `format_for_layout()` |
| `fetch_*` | Gets data from external source | `fetch_matchup()` |
| `distribute_*` | Sends to destination | `distribute_to_platform()` |

**C. Registry pattern for prompts**
```python
# In _L3/prompts/__init__.py
PROMPT_BUILDERS = {
    "sketch_insights_carousel": build_insights_carousel_prompts,
    "sketch_matchup_carousel": build_carousel_prompts,
    "dark_incentives_image": build_dark_incentives_prompt,
    # Future modes added here...
}

def get_prompt_builder(display_mode: str):
    """Get prompt builder function for a display mode."""
    return PROMPT_BUILDERS.get(display_mode)
```

**D. display_modes.py stays at config level (cross-layer contract)**
- Location: `config/display_modes.py` (NOT inside any layer)
- It's the "contract" between layers - defines what each layer must support
- All layers import from it; it imports from none
- When adding new display modes, update registry here FIRST

**E. Layer boundaries in L0 docstring + ARCHITECTURE.md**

Layer boundaries documented in TWO places for drift prevention:

**E1. In pipeline.py (L0) docstring** - developers see rules when editing:
```python
"""
L0 SWITCHBOARD: Entry Point + Cross-Layer Orchestration (v1.0)

LAYER BOUNDARIES:
- L0 (this): Entry point, cross-layer data (teams/players), orchestration
- L1: External data inputs (APIs, MCPs, AI models, assets)
- L2: Calendar/scheduling
- L3: Ideas + text analysis + prompts (content creation)
- L4: Audio/TTS
- L5: Media generation + processing
- L6: Assembly
- L7: Distribution
- L8: Analytics

IMPORT RULES:
- Each layer can import from L0 (cross-layer data)
- Each layer can import from lower-numbered layers
- No layer imports from higher-numbered layers
- Example: L5 can import from L0, L1, L2, L3, L4 but NOT L6, L7, L8

This prevents circular dependencies and enforces clean architecture.
"""
```

**E2. In docs/ARCHITECTURE.md** - canonical reference for onboarding + Oracle audits:
- Add "Layer Architecture" section with layer responsibility table
- Include import rules diagram
- "When to add a new layer" guidance
- Link to display_modes.py as cross-layer contract

This dual placement ensures developers see rules when editing AND documentation stays canonical.

### Migration Phases

**Phase 1: Create Structure (Low Risk)**
- Create all `_L{n}/` folders
- Create `__init__.py` files with pass-through imports
- Copy files to new locations (don't delete originals)
- Test imports work

**Phase 2: Update Switchboards (Medium Risk)**
- Rename main scripts to `L{n}_*.py`
- Update imports in switchboard files
- Keep original files as fallback

**Phase 3: Update Callers (Medium Risk)**
- Update `content_pipeline.py` → `pipeline.py` imports
- Update preset configs to use new paths
- Test with existing presets

**Phase 4: Cleanup (Low Risk)**
- Verify all tests pass
- Delete original files
- Archive deprecated code

### 5-Folder Symmetric Pattern (All Layers)

**Principle:** Every `_L{n}/` folder has the same 5 subfolders for consistency. Create all subfolders upfront to prevent import path changes later (import paths are API contracts).

**The 5 Subfolders:**
```
inputs/     ← Data coming in (fetchers, lookups, constants, API clients)
analysis/   ← Inspection, extraction, validation (text analysis, parsing)
processors/ ← Transformation, manipulation (transforms, PIL/FFmpeg ops)
outputs/    ← Builders, formatters, final results (prompts, assemblers)
utils/      ← Fallback for rare scripts (checkpoints, constants, helpers)
```

**Flow:** `inputs/ → analysis/ → processors/ → outputs/` (with `utils/` for edge cases)

**Categorization Guidelines:**

| Subfolder | Contains | Examples |
|-----------|----------|----------|
| `inputs/` | Data sources, fetchers, lookups, constants | `teams.py`, `goatedbets_api.py`, `assets.py` |
| `analysis/` | Extraction, inspection, validation | `smart_text.py`, `betting_thesis.py` |
| `processors/` | Transformation, manipulation | `transforms.py`, `pil_processor.py` |
| `outputs/` | Builders, formatters, final generation | `carousel.py`, `dark_incentives.py` |
| `utils/` | **Rare fallback** - checkpoints, helpers | `approve.py` (checkpoint) |

**Discipline:** Stay disciplined with categorization. `utils/` is a fallback for scripts that genuinely don't fit the other 4 folders (like checkpoints and constants), NOT a dumping ground.

**Example: L3 (most populated layer):**
```
_L3/
├── __init__.py                      ← Re-exports from all subfolders
├── inputs/                          ← (empty - data comes from L0/L1)
├── analysis/
│   ├── __init__.py
│   ├── smart_text.py                ← Highlight extraction, bucketing
│   ├── goatedbets_api_processor.py  ← GoatedBets API data manipulation
│   └── betting_thesis.py            ← Thesis extraction (LLM + regex)
├── processors/
│   └── transforms.py                ← Data transforms (matchup, etc.)
├── outputs/
│   ├── __init__.py                  ← PROMPT_BUILDERS registry
│   ├── carousel.py                  ← build_carousel_prompts()
│   ├── insights_carousel.py         ← build_insights_carousel_prompts()
│   ├── dark_incentives.py           ← build_dark_incentives_prompt()
│   └── poses.py                     ← get_position_pose()
└── utils/
    └── approve.py                   ← Checkpoint handler
```

**Growth Pattern:**
- When a file exceeds ~500 lines → consider splitting
- When a subfolder exceeds ~10 files → consider nested subfolders
- Each subfolder gets `__init__.py` that re-exports key functions
- Switchboard stays thin - just imports from implementation folders
- Empty subfolders get just `__init__.py` (placeholder for future growth)

### Migration Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Import breakage** | Phase 1 copies files, keeps originals. Test imports before deleting. |
| **Circular imports** | Lazy imports already used. L0 only imported by L1+, not vice versa. |
| **Lost functionality** | Test with existing presets after each phase |
| **L3 growth** | Subfolder structure already planned |
| **IDE autocomplete** | Underscored folders may hide - acceptable tradeoff |

### Post-Migration Checklist

- [ ] All existing presets work (carousel_illustrated, insights_carousel, dark_incentives)
- [ ] Health check passes
- [ ] No circular import warnings
- [ ] API calls route correctly
- [ ] Distribution outputs to correct folders
- [ ] LAYERS.md created with boundary rules
- [ ] Version comments in all switchboards

---

## 🔧 POST-REORGANIZATION: QUALITY & AUTOMATION ROADMAP

> **When:** After scripts reorganization is complete
> **Goal:** Reduce iteration cycles, improve output quality, enable full automation

### Phase 1: Generation Quality Improvements

#### 1.1 Better Prompts
- **Structured sections** already implemented (P5): `[LOCKED]`, `[LAYOUT]`, `[CONTENT]`, `[ACCENTS]`
- **Next step:** Create prompt templates library in `_L3/outputs/templates/`
- **Pattern:** Lock visual elements that work, only vary content per generation

#### 1.2 Reference Image Support
```python
# Add to media_generation.py or new _L5/inputs/references.py
def generate_with_reference(prompt: str, reference_image: str, style_weight: float = 0.7):
    """Generate image using reference for style matching.

    Args:
        prompt: Text prompt for content
        reference_image: Path to example image for style
        style_weight: How closely to match reference (0.0-1.0)

    Use case: "Make it look like this example carousel"
    """
```
- Gemini supports image input for style guidance
- Store approved outputs as references for future generations

#### 1.3 Temperature Control
```python
# Add to ai_models.py or _L1/inputs/ai_models.py
GENERATION_TEMPERATURES = {
    'creative': 1.0,      # High variety (brainstorming)
    'balanced': 0.7,      # Default (good mix)
    'consistent': 0.4,    # Low variety (iteration refinement)
    'precise': 0.2,       # Minimal variation (final polish)
}

def get_temperature(mode: str = 'balanced') -> float:
    return GENERATION_TEMPERATURES.get(mode, 0.7)
```
- Lower temp = more consistent outputs between regenerations
- Use `precise` when iterating on specific element fixes

### Phase 2: Validation Layer (`_L5/analysis/`)

#### 2.1 Image Validator
```python
# _L5/analysis/image_validator.py

def validate_generated_image(image_path: str, requirements: dict) -> dict:
    """Auto-check image meets requirements before human review.

    Checks (using OpenCV + optional Gemini Vision):
    - aspect_ratio: Correct dimensions (1:1, 9:16, etc.)
    - text_readable: No cut-off text, correct placement
    - colors_match: Team palette verification
    - logo_visible: Logo in correct position and size
    - no_hallucinations: No phantom text/wrong player names
    - composition: Key elements in expected zones

    Returns:
        {
            'passed': bool,
            'score': float (0.0-1.0),
            'issues': ['logo_missing', 'text_cutoff'],
            'confidence': float,
            'recommendations': ['regenerate with logo emphasis']
        }
    """
```

#### 2.2 Gemini Vision QA
```python
# _L5/analysis/vision_qa.py

def ask_vision_about_image(image_path: str, question: str) -> str:
    """Use Gemini Vision to answer questions about generated image.

    Examples:
        ask_vision_about_image(img, "Is the logo visible in the bottom right?")
        ask_vision_about_image(img, "What text is shown on this image?")
        ask_vision_about_image(img, "Does the player appear to be wearing Chiefs colors?")

    Use for: Complex validation that OpenCV can't handle
    Cost: ~$0.001 per image (very cheap)
    """
```

#### 2.3 Validation Requirements Registry
```python
# _L5/analysis/validation_requirements.py

VALIDATION_REQUIREMENTS = {
    'sketch_insights_carousel': {
        'aspect_ratio': '1:1',
        'required_elements': ['player_figure', 'team_colors', 'prop_text'],
        'forbidden_elements': ['watermarks', 'stock_photo_text'],
        'text_zones': ['top_20%', 'bottom_30%'],  # Where text should appear
        'logo_required': False,  # skip_logo = True for this mode
    },
    'dark_incentives_image': {
        'aspect_ratio': '1:1',
        'required_elements': ['player_figure', 'money_bags', 'dollar_amounts'],
        'color_palette': ['black', 'dark_gray', 'green_accents'],
        'logo_required': False,
    },
    # ... other modes
}
```

### Phase 3: Preview System

#### 3.1 Thumbnail Preview
```python
# _L5/processors/preview.py

def generate_preview(prompt: str, size: tuple = (256, 256)) -> str:
    """Generate small preview before full resolution.

    Workflow:
    1. Generate 256x256 preview (~0.5s, ~$0.001)
    2. Run validation on preview
    3. If validation passes, generate full res
    4. If fails, adjust prompt and retry preview

    Saves: ~$0.01+ per failed generation at full res
    """
```

#### 3.2 Batch Preview Mode
```python
def preview_carousel(prompts: dict, validate: bool = True) -> dict:
    """Generate previews for all carousel slides at once.

    Returns:
        {
            'cover': {'preview': path, 'valid': True, 'issues': []},
            'prop_1': {'preview': path, 'valid': False, 'issues': ['text_cutoff']},
            ...
        }

    User reviews previews, approves or requests regeneration
    """
```

### Phase 4: Auto-Iteration Mode

#### 4.1 Smart Retry System
```python
# _L5/processors/auto_iterate.py

def generate_with_auto_retry(
    prompt: str,
    requirements: dict,
    max_attempts: int = 3,
    refinement_strategy: str = 'auto'
) -> dict:
    """Generate and auto-retry on validation failure.

    Strategies:
    - 'auto': Use Gemini to analyze failure and refine prompt
    - 'temperature': Lower temperature each attempt
    - 'emphasis': Add emphasis to failed requirements

    Flow:
    1. Generate image
    2. Validate against requirements
    3. If passed, return image
    4. If failed, analyze issues
    5. Refine prompt based on issues
    6. Retry (up to max_attempts)
    7. Return best attempt with validation report

    Returns:
        {
            'image_path': str,
            'attempts': int,
            'final_validation': dict,
            'refinement_history': [{'attempt': 1, 'issues': [...], 'fix': '...'}]
        }
    """
```

#### 4.2 Prompt Refinement Engine
```python
# _L3/processors/prompt_refiner.py

def refine_prompt_for_issues(original_prompt: str, issues: list) -> str:
    """Auto-adjust prompt to fix validation issues.

    Issue → Fix mapping:
    - 'logo_missing' → Add "[CRITICAL] Logo MUST appear in bottom right corner"
    - 'text_cutoff' → Add "Leave 15% margin around all text elements"
    - 'wrong_colors' → Strengthen team color references
    - 'hallucinated_text' → Add "NO text except: [exact text list]"

    Uses Gemini to intelligently merge fixes into prompt structure
    """
```

### Phase 5: Professional Tools Integration

#### 5.1 DaVinci Resolve Integration (Future)
```python
# _L5/processors/davinci_processor.py (or _L6/)

"""
DaVinci Resolve Python API Integration

Prerequisites:
- DaVinci Resolve installed (free version sufficient)
- Scripting enabled in Resolve preferences
- Python 3.6+ (Resolve requirement)

Capabilities:
- Color grading automation (LUTs, color wheels)
- Professional audio mixing (EQ, compression, limiting)
- Advanced transitions and effects
- Batch processing of video files
- Export with broadcast-quality settings

Use cases for GoatedBets:
- Apply consistent color grade across all carousel reels
- Professional audio normalization for TTS content
- Add broadcast-style lower thirds
- Generate color-matched variations for A/B testing
"""

class DaVinciProcessor:
    def __init__(self):
        # Import DaVinci scripting module
        # Requires Resolve to be running
        pass

    def apply_color_grade(self, video_path: str, lut_path: str) -> str:
        """Apply LUT color grade to video."""
        pass

    def normalize_audio(self, video_path: str, target_lufs: float = -14) -> str:
        """Normalize audio to broadcast standard."""
        pass

    def batch_process(self, videos: list, preset: str) -> list:
        """Apply preset to multiple videos."""
        pass
```

#### 5.2 OpenCV Processor (Ready to Build)
```python
# _L5/processors/opencv_processor.py

"""
OpenCV Integration - Computer Vision for Video/Image

Already installed: opencv-python-headless v4.12.0.88

Capabilities to build:
- Motion tracking (Lucas-Kanade, CSRT, KCF)
- Face/body detection for auto-placement
- Scene change detection
- Dominant color extraction
- Perspective transforms
- Video stabilization
- Frame quality analysis
"""

class OpenCVProcessor:
    # Motion Tracking
    def track_object(self, video: str, roi: tuple) -> list: ...
    def track_face(self, video: str) -> list: ...
    def stabilize_tracking(self, points: list) -> list: ...

    # Detection
    def detect_faces(self, frame) -> list: ...
    def detect_people(self, frame) -> list: ...
    def find_logo_placement_zone(self, frame) -> tuple: ...

    # Analysis
    def get_dominant_colors(self, frame, n: int = 3) -> list: ...
    def detect_scene_changes(self, video: str) -> list: ...
    def measure_motion_blur(self, frame) -> float: ...

    # Transforms
    def perspective_warp(self, overlay, surface_points: list): ...
    def match_lighting(self, overlay, background): ...
    def auto_mask_subject(self, frame): ...
```

#### 5.3 Audio Processors (Future)
```python
# _L4/processors/

# librosa_processor.py - Beat detection, tempo analysis
# Use case: Sync meme transitions to music beats

# whisper_processor.py - Transcription
# Use case: Auto-caption reels, extract quotes
```

### Implementation Priority

| Priority | Component | Layer | Effort | Impact |
|----------|-----------|-------|--------|--------|
| 1 | Image Validator | L5/analysis | Medium | High - catches failures early |
| 2 | Temperature Control | L1 | Low | Medium - reduces variation |
| 3 | Auto-Retry System | L5/processors | High | Very High - reduces manual iteration |
| 4 | Preview System | L5/processors | Medium | High - saves cost on failures |
| 5 | Reference Image Support | L5/inputs | Medium | High - style consistency |
| 6 | OpenCV Processor | L5/processors | Medium | Medium - advanced tracking |
| 7 | DaVinci Integration | L5 or L6 | High | Medium - pro finishing |
| 8 | Librosa/Whisper | L4 | Medium | Low initially - future features |

### Success Metrics

**Before (current state):**
- ~4-6 iterations per carousel slide to get right
- Manual review of every output
- No validation before human sees it

**After (target state):**
- ~1-2 iterations (auto-retry handles most issues)
- Only review outputs that pass validation
- Confidence score helps prioritize review time
- Full automation possible for high-confidence outputs

---

## 🎨 VISION SYSTEM DESIGN

> **Location:** `visions/` folder (outside scripts refactor scope)
> **Purpose:** Theme layer controlling tone, voice, messaging, and audience framing
> **Build Timing:** BEFORE scripts reorganization (lives in separate folder)

### Vision vs Display Mode: Conceptual Separation

**Vision** and **Display Mode** are orthogonal control layers:

| Aspect | Display Mode | Vision |
|--------|--------------|--------|
| **Controls** | WHAT we're making | HOW we communicate |
| **Focus** | Format, structure, layout | Tone, voice, messaging |
| **Examples** | carousel, image, reel, video | analytical, hype, casual |
| **Questions** | "What slides? What dimensions?" | "Who are we talking to? What's our voice?" |
| **Granularity** | Per-output (specific to content type) | Overall theme (applies across outputs) |

**Why Keep Separate:**
- Vision can change while display mode stays the same (same carousel, different voice)
- Display mode can change while vision stays the same (same voice, different format)
- Allows A/B testing of messaging without changing visual format
- Flexibility for platform-specific voice (Twitter hype vs LinkedIn analytical)

### Control Point Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                     VISION (Theme Layer)                     │
│         "Who are we talking to? What's our voice?"          │
│                                                              │
│  Injects: tone, brand_voice, messaging_themes, audience     │
└─────────────────────────┬───────────────────────────────────┘
                          │ Vision parameters flow down
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 DISPLAY MODE (Format Layer)                  │
│              "What are we making? What format?"             │
│                                                              │
│  Controls: category, aspect_ratio, slide_count, layers      │
└─────────────────────────┬───────────────────────────────────┘
                          │ Format + Vision merged
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 PROMPT BUILDER (Content Layer)               │
│         "How do we describe what we want generated?"        │
│                                                              │
│  Vision INJECTS HERE: tone phrases, audience framing,       │
│  messaging themes, caption style, temperature preference     │
└─────────────────────────┬───────────────────────────────────┘
                          │ Complete prompt with vision context
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 GENERATION (Execution Layer)                 │
│              "Create the actual content"                     │
│                                                              │
│  Temperature can be vision-influenced (hype=high, analytical=low)│
└─────────────────────────────────────────────────────────────┘
```

### Layer Integration Points

| Layer | Vision Integration |
|-------|-------------------|
| L0 (Pipeline) | Loads active vision, passes to L3 |
| L3 (Ideas) | Prompt builder injects vision tone/voice/messaging |
| L5 (Media) | Temperature setting influenced by vision |
| L7 (Distribution) | Caption style, hashtag selection from vision |
| L8 (Analytics) | Feedback loop: which vision performs best |

### Vision Data Structure

```python
# visions/vision_registry.py

@dataclass
class Vision:
    """Represents a creative vision/direction."""

    # Identity
    id: str                         # Unique identifier (e.g., "analytical")
    name: str                       # Display name (e.g., "Data-Driven Analyst")
    description: str                # What this vision is about
    active: bool = False            # Currently active vision?

    # Tone & Voice
    tone: str                       # analytical | hype | casual | educational
    brand_voice: str                # Full voice description for prompts
    caption_style: str              # How captions should read (short/punchy, detailed, etc.)

    # Visual Preferences
    visual_style: str               # illustrated | photorealistic | minimal | bold
    color_mood: str                 # vibrant | muted | dark | team-matched
    temperature: float = 0.7        # Generation temperature (0.2-1.0)

    # Content Focus
    content_focus: str              # What to emphasize (stats, matchups, narratives)
    target_audience: str            # Who we're speaking to
    messaging_themes: List[str]     # Core themes to reinforce

    # Platform Preferences (optional)
    preferred_platforms: List[str] = field(default_factory=list)
    posting_frequency: str = "standard"  # conservative | standard | aggressive
```

### Initial Vision Presets

#### 1. Analytical Vision (Default)
```python
Vision(
    id="analytical",
    name="Data-Driven Analyst",
    description="Expert sports betting analysis with statistical backing",
    tone="analytical_confident",
    brand_voice="Expert but accessible sports betting analysis. Lead with data, explain the edge, conclude with actionable insight.",
    caption_style="Stat-forward. '26 carries expected. #1 run defense. The math adds up.'",
    visual_style="illustrated",
    color_mood="team-matched",
    temperature=0.5,  # Lower for consistency
    content_focus="Statistical edges, matchup advantages, historical trends",
    target_audience="Sports bettors seeking data-driven insights, not gut feels",
    messaging_themes=["The edge is in the data", "Sharp analysis, smart bets", "Numbers don't lie"],
    preferred_platforms=["twitter", "instagram"],
    active=True
)
```

#### 2. Hype Vision
```python
Vision(
    id="hype",
    name="Game Day Energy",
    description="High-energy, excitement-driven content for engaged fans",
    tone="hype_exciting",
    brand_voice="ENERGY. Short punchy sentences. Exclamation points earned. Build anticipation. This is THE game.",
    caption_style="Short and punchy. 'LET'S EAT. 🔥' - max 10 words per line",
    visual_style="bold",
    color_mood="vibrant",
    temperature=0.8,  # Higher for creative variety
    content_focus="Big moments, player spotlights, game narratives",
    target_audience="Casual fans, engagement seekers, gameday scrollers",
    messaging_themes=["Can't miss this", "Game day energy", "Lock it in"],
    preferred_platforms=["instagram", "tiktok"],
    active=False
)
```

#### 3. Casual Vision
```python
Vision(
    id="casual",
    name="Sports Bar Friend",
    description="Conversational, relatable sports talk like a knowledgeable friend",
    tone="casual_friendly",
    brand_voice="Like explaining a bet to your friend at the bar. Conversational, relatable, no jargon. 'Here's the deal...'",
    caption_style="Conversational. 'Okay hear me out...' or 'Not gonna lie, this one's interesting'",
    visual_style="illustrated",
    color_mood="muted",
    temperature=0.7,
    content_focus="Storylines, simple explanations, relatable angles",
    target_audience="Recreational bettors, new to sports betting, casual fans",
    messaging_themes=["Smart bets made simple", "No overthinking", "Trust the process"],
    preferred_platforms=["twitter", "instagram"],
    active=False
)
```

### visions.json Config File

```json
{
    "visions": [
        {
            "id": "analytical",
            "name": "Data-Driven Analyst",
            "description": "Expert sports betting analysis with statistical backing",
            "tone": "analytical_confident",
            "brand_voice": "Expert but accessible sports betting analysis. Lead with data, explain the edge, conclude with actionable insight.",
            "caption_style": "Stat-forward. '26 carries expected. #1 run defense. The math adds up.'",
            "visual_style": "illustrated",
            "color_mood": "team-matched",
            "temperature": 0.5,
            "content_focus": "Statistical edges, matchup advantages, historical trends",
            "target_audience": "Sports bettors seeking data-driven insights",
            "messaging_themes": ["The edge is in the data", "Sharp analysis, smart bets"],
            "preferred_platforms": ["twitter", "instagram"],
            "active": true
        },
        {
            "id": "hype",
            "name": "Game Day Energy",
            "description": "High-energy, excitement-driven content",
            "tone": "hype_exciting",
            "brand_voice": "ENERGY. Short punchy sentences. Build anticipation.",
            "caption_style": "Short and punchy. Max 10 words per line.",
            "visual_style": "bold",
            "color_mood": "vibrant",
            "temperature": 0.8,
            "content_focus": "Big moments, player spotlights, game narratives",
            "target_audience": "Casual fans, engagement seekers",
            "messaging_themes": ["Can't miss this", "Game day energy"],
            "preferred_platforms": ["instagram", "tiktok"],
            "active": false
        },
        {
            "id": "casual",
            "name": "Sports Bar Friend",
            "description": "Conversational sports talk like a knowledgeable friend",
            "tone": "casual_friendly",
            "brand_voice": "Like explaining a bet to your friend at the bar.",
            "caption_style": "Conversational. 'Okay hear me out...'",
            "visual_style": "illustrated",
            "color_mood": "muted",
            "temperature": 0.7,
            "content_focus": "Storylines, simple explanations",
            "target_audience": "Recreational bettors, casual fans",
            "messaging_themes": ["Smart bets made simple", "Trust the process"],
            "preferred_platforms": ["twitter", "instagram"],
            "active": false
        }
    ]
}
```

### Prompt Injection Mechanism

```python
# visions/vision_prompts.py

from visions.vision_registry import VisionRegistry

def get_vision_prompt_context() -> dict:
    """Get current vision context for prompt building.

    Returns dict that prompt builders use to inject vision elements.
    """
    vision = VisionRegistry.get_active_vision()

    return {
        # For prompt preamble
        "voice_instruction": f"Voice: {vision.brand_voice}",
        "tone_instruction": f"Tone: {vision.tone.replace('_', ' ').title()}",

        # For caption/text generation
        "caption_style": vision.caption_style,
        "messaging_themes": vision.messaging_themes,

        # For generation settings
        "temperature": vision.temperature,
        "visual_style": vision.visual_style,

        # For content focus
        "content_focus": vision.content_focus,
        "audience_framing": f"Speaking to: {vision.target_audience}",
    }


def inject_vision_into_prompt(base_prompt: str, vision_context: dict = None) -> str:
    """Inject vision context into a prompt.

    Args:
        base_prompt: Original prompt from prompt builder
        vision_context: Optional override; uses active vision if None

    Returns:
        Prompt with vision context prepended
    """
    if vision_context is None:
        vision_context = get_vision_prompt_context()

    vision_preamble = f"""
[VISION CONTEXT]
{vision_context['voice_instruction']}
{vision_context['tone_instruction']}
{vision_context['audience_framing']}
Focus on: {vision_context['content_focus']}
"""

    return vision_preamble.strip() + "\n\n" + base_prompt


def get_caption_for_vision(content: str, platform: str = "instagram") -> str:
    """Generate platform-appropriate caption using active vision style.

    Uses Gemini to rewrite content in the vision's caption style.
    """
    vision = VisionRegistry.get_active_vision()

    # Would call Gemini with vision.caption_style as guidance
    # For now, returns content (placeholder for future implementation)
    return content
```

### Usage Pattern in Prompt Builders

```python
# In _L3/outputs/insights_carousel.py (future location)
# Or currently in api_utils.py

from visions.vision_prompts import get_vision_prompt_context, inject_vision_into_prompt

def build_insights_carousel_prompts(api_data: Dict, away: str, home: str) -> Dict[str, str]:
    """Build prompts for insights carousel with vision context."""

    # Get vision context once for all slides
    vision_ctx = get_vision_prompt_context()

    # Build base prompts as usual
    cover_prompt = _build_cover_base_prompt(api_data, away, home)

    # Inject vision context
    cover_prompt = inject_vision_into_prompt(cover_prompt, vision_ctx)

    # Use vision temperature for generation settings
    # (passed separately to generation call)

    return {
        'cover': cover_prompt,
        'temperature': vision_ctx['temperature'],
        # ... other slides
    }
```

### Folder Structure

```
visions/
├── __init__.py              # Re-exports: VisionRegistry, get_active_vision
├── vision_registry.py       # Vision dataclass + VisionRegistry class (exists)
├── vision_prompts.py        # Prompt injection helpers (to build)
└── visions.json             # Vision preset configs (to build)
```

**Note:** No complex subfolder structure needed. Vision is simpler than the pipeline - it's just:
1. Registry (dataclass + class) - already exists
2. JSON config file for presets
3. Prompts connector for injection

### Vision vs Display Mode: Per-Output Granularity

**Question:** Can vision have granular overrides per display mode?

**Answer:** Yes, but implement as optional overlay, not required:

```python
# visions.json - optional per-mode overrides
{
    "id": "analytical",
    "name": "Data-Driven Analyst",
    // ... base vision fields ...

    "display_mode_overrides": {
        "sketch_insights_carousel": {
            "caption_style": "Even more stat-heavy for carousel format"
        },
        "meme_overlay": {
            "tone": "casual_confident",  # Memes can be lighter
            "temperature": 0.9           # More creative for memes
        }
    }
}
```

**Get vision for specific mode:**
```python
def get_vision_for_mode(display_mode: str) -> Vision:
    """Get vision with any display-mode-specific overrides applied."""
    vision = VisionRegistry.get_active_vision()
    overrides = vision.display_mode_overrides.get(display_mode, {})

    # Return vision with overrides merged
    return vision.with_overrides(overrides)
```

### Build Order

1. **Expand Vision dataclass** - Add new fields (caption_style, temperature, messaging_themes, etc.)
2. **Create visions.json** - 3 initial presets (analytical, hype, casual)
3. **Build vision_prompts.py** - Injection helpers
4. **Update L0** - Load active vision at pipeline start
5. **Update L3 prompt builders** - Inject vision context
6. **Update L5** - Use vision temperature
7. **Update L7** - Caption style for distribution
8. **Future: L8 feedback** - Track which vision performs best

### Success Criteria

- [ ] Switching visions changes tone across all output types
- [ ] Same carousel, different voice when vision changes
- [ ] Temperature reflects vision preference (analytical=low, hype=high)
- [ ] Captions match vision style
- [ ] No code changes needed to add new vision presets (JSON only)

---

## P13-P14 WORK (COMPLETE - Reference)

**P13 Work (Dec 27):**
1. ✅ Added missing display modes to registry for unused presets
2. ✅ Fixed carousel distribution - slides AND reels now go to SAME folder
3. ✅ Created `animation` category for ken_burns + TTS presets
4. ✅ Renamed `static_videos` → `animations` folder in distribution.py
5. ✅ Updated `text_overlay` and `matchup_card` to use `animation` category
6. ✅ Added `is_animation()` helper function
7. ✅ Added `is_animation` import to L3, L5, L7

**New Display Mode Categories:**
```
Categories: carousel | single_image | animation | reel | video
```

**Display Modes by Category (P13):**
```python
# CAROUSEL (multi-slide images, may generate reels)
"sketch_insights_carousel"  # 6 slides + reels, skip logo
"sketch_matchup_carousel"   # 3 slides + reels
"carousel"                  # Generic legacy (no reels)

# SINGLE_IMAGE (standalone images)
"dark_incentives_image"     # Incentives, has reels
"minimal_stats_image"       # Clean stat infographic
"infographic"               # Generic infographic
"image_with_overlay"        # AI image + text at assembly

# ANIMATION (static image + ken_burns + TTS)
"text_overlay"              # Ken_burns + TTS voiceover
"matchup_card"              # Ken_burns + timed text reveals

# REEL (short-form video <60s, 9:16)
"meme_mashup"               # Multi-clip meme + transitions
"meme_overlay"              # Single clip + text/logo
"photo_highlight_reel"      # Photo-real highlight + voiceover

# VIDEO (longer-form >60s)
"neon_promo_video"          # Promo with neon aesthetics
```

**New Helper Functions (P13):**
```python
def is_animation(mode: str) -> bool   # Check if animation category
def get_animation_modes() -> set      # Get all animation modes
```

**Distribution Folder Structure:**
```
final/
├── carousels/          # Carousel slides + reels (together)
├── animations/         # Ken_burns + TTS animations (NEW!)
├── images/             # Standalone images
├── infographics/       # Infographic images
├── memes/              # Meme reels
└── universal (<60s)/   # Platform-ready videos
```

**Files Modified:**
- `config/display_modes.py` - Added animation category, 7 new modes, `is_animation()` helper
- `scripts/distribution.py` - Renamed static_videos → animations, fixed carousel routing
- `scripts/idea_creation.py` - Added `is_animation` import
- `scripts/media_generation.py` - Added `is_animation` import

---

**P12 Work (COMPLETE):**
- Alias removal migration complete, all JSON uses canonical names
- Added `skip_logo`, `slide_count` config properties + helpers
- Refactored all layers to use registry functions (no hardcoded names)

---

**P10/P11 Work (COMPLETE - Reference):**
- **dark_incentives Pipeline Integration** ✅
  - L0/L3: Manual input handling in content_pipeline.py
  - L5: `_generate_dark_incentives_image()` method in media_generation.py
  - Prompt fix: Removed text bullets (money bags only via Gemini)
- **Saturday Dec 27 Content** ✅
  - HOU @ LAC insights_carousel (6 slides + 6 reels)
  - BAL @ GB insights_carousel (6 slides + 6 reels)
  - Keenan Allen incentives v2 (image + MP4)
- **Display Mode Registry (P11)** ✅
  - Created `config/display_modes.py` centralized handler registry
  - Updated all layers (L0-L7) to use registry functions

**Output Locations:**
```
final/infographics/keenan_allen/
├── keenan_allen_incentives_v2.jpg
└── keenan_allen_incentives_v2.mp4

final/carousels/HOU_LAC_insights_carousel/  (6 slides)
final/carousels/BAL_GB_insights_carousel/   (6 slides)

assembled/idea_001/  (6 reels per matchup - 9:16 MP4s)
```

**O75 COMPLETE**: D100 carousel cleanup verified, health improved 5.7→8.4

**P8 Work (COMPLETE):**
- **Integrated cleaning tools into ingestion (L1)** ✅
  - All cleaning operations now part of `ingest()` method
  - CLI flags: `--auto-crop`, `--crop-top/bottom/left/right`, `--strip-subs`, `--find-original`
  - Removed standalone crop/clean modes - everything flows through ingestion
  - Example: `python3 asset_ingestion.py video.mp4 --type meme_template --auto-crop`
- **Tested on Tekken clip** ✅
  - Auto-crop removed 230px meme text from top
  - Cleaned video: `bro_crashed_out_after_losing_to_a_68_year_old_woman_in_tekke_clean.mp4`
- **Ran meme_overlay on cleaned clip** ✅
  - Output: `final/memes/overlay_20251226_175917_overlay.mp4` (38.96s, 13.56 MB)
- **Text removal strategy documented** in asset_ingestion.py docstring:
  1. Find original source (best - no info loss, free)
  2. Cropping (quick fix when original unavailable)
  3. Runway ML (~$15/mo or ~$0.05/sec API)
  4. ProPainter (future - requires NVIDIA GPU)

**P7 Work (COMPLETE):**
- **Tested both meme presets** ✅
  - meme_mashup: swift_locked_in.mp4 + hamm_disco.mp4 → `meme_20251226_164312_meme.mp4` (11.73s)
  - meme_overlay: Tekken clip + text + logo → `overlay_20251226_164410_overlay.mp4` (38.96s)
  - Output location: `final/memes/`

**P6 Work (COMPLETE):**
- **Automation with Granular Control Rule** - PHILOSOPHY.md §2.5-2.6
- **Preset Creation Rule** - PHILOSOPHY.md §2.6 (Pipeline-First + Layer Callability)
- **Layer Architecture (Canonical)**: L0-L8 defined
- **Asset Ingestion (L1)** - `scripts/asset_ingestion.py` ✅
- **meme_mashup preset** - `assembly.py` L6 ✅
  - CLI: `python3 assembly.py --meme-mashup --clips clip1.mp4 clip2.mp4 --text "..." --transition fade`
- **meme_overlay preset** - `assembly.py` L6 ✅
  - CLI: `python3 assembly.py --meme-overlay --clip clip.mp4 --text "..." --logo logo.png`
- **Archived meme_generator.py** → `archive/deprecated/`

**P5 Work (COMPLETE):**
- **Prompt Engineering Rules** - Formalized in STYLE_GUIDE.md, synced to all contexts
  - Structured sections: `[LOCKED]`, `[LAYOUT]`, `[CONTENT]`, `[ACCENTS]`
  - Overrides dict for design iteration
  - Post-generation tweaks via Gemini edit
  - Refactored `build_dark_incentives_prompt()` with new structure
- **L7 video/parent grouping fix**
  - Fixed `get_final_subfolder()` to keep videos with their parent images
  - Added `keep_with_parent: bool = True` parameter
  - Videos from infographics stay in `infographics/`, not `universal/`
- Moved Deebo Samuel files together:
  ```
  final/infographics/deebo_samuel/
  ├── deebo_samuel_incentives_v10_specks_gemini.jpg (724 KB)
  └── deebo_samuel_incentives_final.mp4 (209 KB)
  ```
- **Synced all contexts** - DEV, ORACLE, CRANK, POCKET all have Rule #16/20/8 for prompt engineering

**New Preset: dark_incentives** (P3-P4)
- Single-page player contract incentive graphics
- Black crumpled paper background
- Watercolor illustrated player with paint specks
- Red "$" with swoosh underline (signature element)
- Faded money bills in corners
- Green dollar amounts, money bag bullets
- Christmas variant available

**P4 Work:**
- Formalized 14 Pocket session rules (adapted from DEV/ORACLE for M1 Air)
- Discovered Gemini image editing for post-generation tweaks
- Added paint specks to v10 via Gemini edit → v10_specks_gemini.jpg = FINAL
- L6: Converted 1:1 → 9:16 MP4 with color-matched padding
- L7: Distributed to final folder
- **Fixed distribution.py** - Routes files to existing folder structure based on output type:
  - New methods: `get_final_subfolder(preset_name, file_path)`, `distribute_by_preset()`
  - Images (infographics, incentives) → `final/infographics/`
  - Carousels → `final/carousels/`
  - Videos stay with parent (not separate `universal/`)

**Image Iteration Strategies Learned:**
| Strategy | Use Case | Pros | Cons |
|----------|----------|------|------|
| **Gemini image editing** | Modify existing image (specks, jersey #) | Preserves original, targeted changes | May alter unintended areas |
| **PIL programmatic** | Add geometric effects (specks, overlays) | 100% predictable, preserves original | Less organic look |
| **Lower temperature** | More consistent regeneration | Less creative variation | Not yet tested |
| **Structured prompt sections** | Complex layouts | Clear hierarchy | Can still drift between calls |

**P3 Work:**
- Created `build_dark_incentives_prompt()` in api_utils.py
- Added preset config to script_presets.json
- Iterated through 10 versions refining style elements
- V10 selected as base, Gemini edit added paint specks

**P2 Work (DEN@KC):**
- Added R.J. Harvey to player database (Broncos, RB)
- Added Chris Oladokun as Chiefs QB (Mahomes torn ACL, Wentz benched)
- Added highlight keywords: "incentives", "ranks #1", "red-zone"
- Cover regenerated with anti-hallucination instructions (fixed "evens" text)
- All 6 slides + reels generated and distributed

**P1 Refinements (DET@MIN):**
- Prop 2: Defender body coherence improved
- Prop 4: J.J. McCarthy INT title cleaned (removed "(or Starting QB)")
- Model: `gemini-3-pro-image-preview`

---

## SESSION END CHECKLIST

1. Run `python3 maintenance/project_oracle.py autosave`
2. Update Recent Changes with what you did
3. Set handoff flags if main workstation needs to continue
4. Update session count in all context files touched

---

*Pocket Context - Full capability, efficient execution*
