# DEV_CONTEXT.md - Backend Development Session

> **YOU ARE DEV** - Backend development: app/, scripts/, config/. NO dashboard/ changes.

**Last Updated:** January 18, 2026
**Session:** D107
**Purpose:** Single file for Dev session resume - read this FIRST

---

## Cross-Session Handoffs

**Handoffs TO Dev:**
- Dash: custom_preset_request, api_change_request, backend_bug
- Crank: bug_report (Crank reports, Dev fixes)

**Handoffs FROM Dev:**
- Dash: new_feature_available, preset_added, api_updated
- Crank: preset_fixed, new_preset

**Messaging:** `python3 oracle/daemon.py messages --context dev`

---

## Current Date & Season

> **Today:** January 18, 2026
> **NFL Season:** 2025-2026 (Playoffs - Divisional Round)
> **NBA Season:** 2025-2026 (In Progress)

---

## Session Rules

1. **Testing**: Use `--ids idea_001 idea_002 idea_003` to limit to 3 ideas
2. **Cost**: ALWAYS notify before API calls that cost money
3. **Compaction**: Suggest at natural breakpoints (task completion)
4. **Python3**: Always use `python3` for script execution
5. **Incremental**: One action at a time, pause for confirmation
6. **Documentation**: Never lose information when updating docs
7. **Cross-Session**: Include ALL details in handoffs (paths, code, rationale)

### Resume Protocol
```
you are dev - read @docs/context/DEV_CONTEXT.md
```

### On Every Resume:
1. Read this entire file
2. Check for pending handoff messages: `python3 oracle/daemon.py messages --context dev`
3. Review Pending Tasks below
4. Ask clarifying questions before making changes

---

## Pipeline Status

```
✅ L1: Trend Detection    → all_trends.json
✅ L2: Calendar Config    → segments_config.json
✅ L3: Idea Creation      → ideas_approved.json
✅ L4: Audio Generation   → audio/*.mp3
✅ L5: Media Components   → media/[idea_id]/
✅ L6: Video Assembly     → assembled/*.mp4
✅ L7: Distribution       → final/[platform]/
⬜ L8: Analytics          → analytics/*.json (placeholder)
```

### Quick Commands
```bash
# Activate environment
cd "/Users/Vanil/Library/Mobile Documents/com~apple~CloudDocs/VITAL SIGNS/LIFE/INVESTMENTS/Goated Bets/Marketing/AutomationScript"
source venv/bin/activate

# V2 Pipeline (scripts moved to app/core/pipeline/layers/)
# Playoffs - Wild Card Round (current)
python3 app/core/pipeline/layers/_L3/L3_ideas.py playoffs wild_card --matchup "TEAM @ TEAM" --content-preset carousel_illustrated --no-checkpoint
python3 app/core/pipeline/layers/_L5/L5_media.py playoffs wild_card --ids idea_001 --no-checkpoint --generate
python3 app/core/pipeline/layers/_L6/L6_assembly.py playoffs wild_card --ids idea_001 --no-checkpoint
python3 app/core/pipeline/layers/_L7/L7_distribution.py playoffs wild_card --ids idea_001 --carousels --no-checkpoint

# Health check
python3 oracle/project_oracle.py audit --quick

# Preset validation
python -m config.preset_validator --summary
```

---

## Pending Tasks

### Handoff Messages (Check on Resume)
- **From Dash:** "Need custom preset for playoff matchups" (2026-01-07) - ✅ Addressed with pokemon_battle_animated

### Active (Priority Order)
1. [x] **P29: Meme Support & Processor Restructure** - ✅ COMPLETE (D107)
   - Moved `pil_processor.py` and `ffmpeg_processor.py` from L5 to L6
   - Added `create_image_meme()` and `create_video_meme()` functions
   - Added `image_meme` preset to script_presets.json
   - L5/processors now re-exports from L6 with deprecation warning

2. [x] **P28: Preset Validator** - ✅ COMPLETE (D107)
   - `config/preset_validator.py` - validates presets have required fields per layer
   - Integrated into Oracle health audit (`oracle/maintenance/microglia.py`)
   - CLI: `python -m config.preset_validator --summary`
   - 4 failed presets: `pokemon_battle_animated`, `pokemon_battles`, `pipeline_test`, `screenshot_to_video`

3. [x] **P27: AnimateDiff + RIFE Hybrid** - ✅ COMPLETE (D106)
   - ComfyUI at `~/ComfyUI`, AnimateDiff-Evolved + RIFE VFI
   - `_L6/processors/animatediff_processor.py` - ComfyUI API integration

### Future
- [ ] L8 Analytics layer implementation

---

## Recent Changes

### Jan 18, 2026 (D107 - P29 Meme Support & P28 Preset Validator)
- **P29 Implementation Complete** - Meme Support & Processor Restructure
  - Moved `pil_processor.py` from `_L5/processors/` to `_L6/processors/`
  - Moved `ffmpeg_processor.py` from `_L5/processors/` to `_L6/processors/`
  - Rationale: PIL and FFmpeg are assembly tools, not generation tools
  - Added `create_image_meme()` - classic top/bottom text meme with Impact font
  - Added `create_video_meme()` - FFmpeg drawtext for video memes
  - L5/processors `__init__.py` now re-exports from L6 with deprecation warning
  - Added `image_meme` preset to `script_presets.json` (uses `single_image` display mode)
  - Tested: `output/test_meme.jpg` (133KB), `output/test_video_meme.mp4` (2.9MB)
  - Plan file: `oracle/docs/plans/P29_MEME_SUPPORT.md`

### Jan 18, 2026 (D107 - P28 Preset Validator)
- **P28 Implementation Complete** - Content Preset Validator
  - Created `config/preset_validator.py` - validates presets have all required fields
  - Checks layer requirements based on `display_mode` routing via `display_modes.py`
  - Validates references (voice_preset, pacing_preset exist)
  - CLI: `python -m config.preset_validator` or `python -m config.preset_validator carousel_sketch`
  - Results: 4 OK, 14 warnings, 4 failed (experimental presets)
  - Failed: `pokemon_battle_animated`, `pokemon_battles`, `pipeline_test`, `screenshot_to_video`
- **Integrated into Oracle health audit** (`oracle/maintenance/microglia.py`)
  - `run_audit()` now calls `_run_preset_validation()`
  - Failed presets appear as warnings in health score
  - Health score: 84 → 76 (4 preset warnings @ 2 points each)
- **Removed from Future list:**
  - AnimateDiff ComfyUI UI testing (handled by P27)
  - Unified Content Type System (replaced by validator-only approach)
- **Plan file:** `oracle/docs/plans/P28_UNIFIED_CONTENT_TYPES.md` (renamed to Preset Validator)

### Jan 9, 2026 (D106 - P27 AnimateDiff + RIFE Complete)
- **P27 Implementation Complete** - AnimateDiff + RIFE hybrid workflow
  - Installed Python 3.11 via Homebrew (ComfyUI requires 3.10+)
  - ComfyUI installed at `~/ComfyUI` with all dependencies
  - Custom nodes: AnimateDiff-Evolved, Frame-Interpolation, IP-Adapter, Manager
  - Models downloaded:
    - SD 1.5 checkpoint: `v1-5-pruned-emaonly.safetensors` (4.0GB)
    - Motion module: `mm_sd_v15_v2.ckpt` (1.7GB)
    - LCM LoRA: `lcm-lora-sdv1-5.safetensors` (128MB)
    - IP-Adapter: `ip-adapter_sd15.safetensors` (43MB)
- **New processor:** `_L6/processors/animatediff_processor.py`
  - ComfyUI API integration for battle animation generation
  - Workflow building, prompt queueing, completion polling
  - Segment-based AnimateDiff + RIFE upsampling pipeline
- **8-bit Audio sourced** from OpenGameArt (CC0 license)
  - Music: `battle_loop_8bit.mp3` (881KB, 1:15 loop)
  - SFX: attack_hit.wav, super_effective.wav, faint.wav, transition.wav
- **Full test successful:** `output/pokemon_battle_full.mp4` (1.3MB, 15s, video+audio)
- **ComfyUI launch command:** `cd ~/ComfyUI && source venv/bin/activate && python main.py --force-fp16 --highvram`

### Jan 9, 2026 (D105 - Pokemon Battle Animation Preset)
- **Created `pokemon_battle_animated` preset** - 4-slide battle animation
  - RIFE frame interpolation (crossfade transitions)
  - 8-bit battle audio mixing (music + timed SFX)
  - Output: 1080x1920 @ 30fps, ~15 seconds
- **New processors created:**
  - `_L6/processors/rife_interpolator.py` - RIFE-ncnn-vulkan integration
  - `_L4/processors/battle_audio_mixer.py` - 8-bit audio mixing
- **Installed rife-ncnn-vulkan** - `~/bin/rife-ncnn-vulkan` (Metal GPU on M2)
- **Config updates:**
  - Added `pokemon_battle_animated` to `script_presets.json`
  - Added `rife_local` to `tool_config.json`
- **Test video generated:** `output/jax_vs_buf_pokemon_battle.mp4` (1.2 MB, 14.4s)
- **P27 Plan created:** AnimateDiff + RIFE hybrid for true motion generation
  - Current RIFE-only creates crossfades, not attack motion
  - P27 adds ComfyUI + AnimateDiff for actual pounce/faint animation
  - See: `oracle/docs/plans/P27_ANIMATEDIFF_POKEMON_BATTLE.md`

### Jan 8, 2026 (D104 - V2 Fixes + Presets + Processors)
- **Fixed wild_card week parsing bug** - L3 now handles playoff week names
  - Added `parse_week_number()` and `get_week_display()` helper functions
  - Playoffs work: `python3 L3_ideas.py playoffs wild_card --matchup "LAC @ HOU"`
- **Created audio_processor.py** (`_L4/processors/`)
  - Whisper transcription (API and local)
  - Subtitle generation (SRT, VTT)
  - Silence detection and trimming
- **Created video_effects.py** (`_L6/processors/`)
  - Parallax multi-layer depth effect
  - Split screen layouts (horizontal, vertical, grid_2x2, focus)
  - Collage styles (grid_4, grid_6, pinterest, diagonal)

### Jan 8, 2026 (D104 - V2 Import Fixes + Preset Tests)
- **Fixed V2 layer script imports** - Oracle reorganized scripts to `app/core/pipeline/layers/`
  - All 8 layer scripts (L1-L8) now have correct `PROJECT_ROOT` path
  - Added `LAYERS_DIR` for cross-layer imports
  - Pipeline CLI works again from new locations
- **Fixed ai_models.py import path** - Was warning about missing config
  - `_L1/inputs/ai_models.py` now has correct 7-level PROJECT_ROOT calculation
  - All 4 AI models now loading correctly (gpt-4o-mini, gpt-4o, gemini, perplexity)
- **Fixed L5_media.py config paths** - SCRIPT_PRESETS_PATH and MEDIA_PRESETS_PATH now use PROJECT_ROOT
- **Tested remaining presets** - All working via Nano Banana:
  - `best_bets_matchup_infographic` ✅ (generates 2 infographics)
  - `ai_image_matchup` ✅ (routes to Nano Banana)
  - `carousel_dark` ✅ (3-slide watercolor carousel)
  - `dark_incentives` ⚠️ (requires manual player data - expected)
- **V2 Structure**: Scripts moved from `scripts/` to `app/core/pipeline/layers/_L*/`
  - Old scripts archived at `archive/v1/scripts_active_2026-01-07/`
  - Oracle did P23 Brain Cell Architecture (O97)

### Jan 7, 2026 (D103 - P20 Complete + Preset Validation)
- **P20 Complete**: Removed ~500 lines legacy carousel code from L5_media.py
- **carousel_illustrated preset validated**: Full L3→L5→L6→L7 pipeline works
- **P21 plan created**: Enhanced CodeOptimizer (handed to Oracle)

### Jan 7, 2026 (O91-O97 - Major Restructure)
- **P23 Brain Cell Architecture**: Oracle modularized into Microglia, Astrocytes, etc.
- **5-context system**: Oracle, Dev, Dash, Crank, Pocket
- **Context files moved** to `oracle/docs/context/`

### Jan 3, 2026 (D101)
- Week 18 carousel generation complete (CAR @ TB, SEA @ SF)
- Bug fix: Missing SCRIPT_PRESETS_PATH in media_generation.py
- PLAYER_TEAMS expanded to 208 players

### Jan 2, 2026 (O81-O83)
- P15/P16 Scripts Reorganization complete
- api_utils.py decomposed into 29 modules in `_L3/`

---

## Key Scripts

| Script | Layer | Purpose |
|--------|-------|---------|
| content_pipeline.py | L0 | Entry point |
| idea_creation.py | L3 | AI idea generation |
| media_generation.py | L5 | Image/video generation |
| assembly.py | L6 | Assembly + logo overlay |
| distribution.py | L7 | Platform distribution |

### Layer Tools (in `_L*/` subfolders)
- `_L1/inputs/` - odds_fetcher, web_search_trend_detector
- `_L2/processors/` - organize_segments
- `_L3/utils/` - api_utils modules (extraction, prompts, players)

---

## Config Files

| File | Purpose |
|------|---------|
| config/script_presets.json | Content presets (carousel, infographic, etc.) |
| config/tool_config.json | Tool selection & fallbacks |
| config/nfl_calendar.py | Season structure |

### Validated Presets (D104)
- `carousel_illustrated` ✅ - 3 slides, 1:1 → 9:16 MP4
- `carousel_dark` ✅ - 3-slide watercolor carousel
- `best_bets_matchup_infographic` ✅ - 2 Nano Banana infographics
- `ai_image_matchup` ✅ - Routes to Nano Banana
- `illustrated_insights_carousel` - 6 slides (cover + 5 props)
- `dark_incentives` ⚠️ - Requires manual player data

---

## Output Structure

```
content/nfl/2025-2026/[phase]/[week]/
├── ideas_approved.json
├── media/[idea_id]/          # L5 output (1:1 images)
├── final/
│   ├── carousels/            # 9:16 MP4s
│   ├── universal/            # Videos ≤60s
│   └── images/               # Infographics
└── distribution_manifest.json
```

---

## API Keys & Environment

| Key | Service | Status |
|-----|---------|--------|
| OPENAI_API_KEY | GPT-4o | ✅ |
| ELEVENLABS_API_KEY | TTS | ✅ |
| FAL_KEY | Flux images | ✅ |
| PEXELS_API_KEY | Stock media | ✅ |
| PERPLEXITY_API_KEY | AI search | ✅ |

**Virtual Environment:**
```bash
source venv/bin/activate
```

---

## Reference Documents

| Doc | Purpose |
|-----|---------|
| docs/overview/ARCHITECTURE.md | V2 architecture, layer flow, preset system |
| docs/overview/PHILOSOPHY.md | Design principles |
| docs/overview/TOOLS_REFERENCE.md | API pricing, tool options, Smart Text Toolkit |
| docs/overview/BRAND_RULES.md | Brand colors, logo usage |
| docs/overview/UX_RULES.md | Dashboard-first UI patterns |
| docs/overview/WORKFLOW.md | Cross-session handoffs, daemon commands |

---

## Milestone: First Full-Pipeline Preset (D68)

**`carousel_illustrated`** flows end-to-end through L3→L5→L6→L7:
- L3: Creates idea with `display_mode: carousel`
- L5: Generates 3 slides (cover, matchup, bonus)
- L6: Applies logo overlay via PIL
- L7: Organizes to `final/carousels/`

---

## Cross-Session Flags

**Status:** _(none)_

<!--
Available flags:
- 🚩 NEEDS_ORACLE_PASS - Dev sets before compact
- 🚩 NEEDS_DEV_ATTENTION: [reason] - Oracle sets if issues need dev input
-->

---

## Session End Checklist

1. Update "Recent Changes" with today's work
2. Update "Pending Tasks" (completed → remove, new → add)
3. If major changes: set 🚩 NEEDS_ORACLE_PASS flag
4. Send handoff if needed: `python3 oracle/daemon.py send dev dash "message"`
