# Changelog

Archived Recent Changes from context files.

---

## January 2026

### January 18, 2026 - Dashboard Sync & Tool Manager (DB8)
- **Mouse-based drag-drop for Tool Manager** - Replaced HTML5 drag API with mouse events
  - HTML5 drag API doesn't work reliably on Mac trackpads
  - New approach: `onMouseDown` + `document.mousemove/mouseup` events
  - Uses `document.elementsFromPoint()` for detecting drop targets
  - Works for both cross-category moves AND within-category reordering
- **Integration status indicators** - Shows which tools are integrated in pipeline
  - Green ✓ badge for integrated tools (actually hooked up to pipeline)
  - Gray ○ badge for non-integrated tools (installed but not connected)
  - Dashed border + reduced opacity for non-integrated tools
  - Added `integrated` field to TOOL_METADATA in admin.py
- **Preset categorization with Generate/Discovery tabs** (from earlier in session)
  - Added category field to normalized preset data in preset_service.py
  - New filter tabs in PresetSelection.jsx for Generate vs Discovery
- **Removed Tool Reference section** from AdminPresetsReference.jsx
- **Updated tool_config.json** - Animation selected: `rife_local` (was ken_burns)
- **Files Modified:**
  - `app/frontend/src/components/AdminToolManager.jsx` - Complete drag-drop rewrite
  - `app/frontend/src/styles/AdminToolManager.css` - Drop indicators, integration badges
  - `app/frontend/src/components/AdminPresetsReference.jsx` - Removed tool reference section
  - `app/api/routes/admin.py` - Added `integrated` field to TOOL_METADATA
  - `config/tool_config.json` - Changed animation.selected to rife_local

### January 8, 2026 - V2 First Output Milestone (O101)
- **🎉 FIRST V2 OUTPUT SUCCESS** - Carousel generated via dashboard
  - Used `carousel_illustrated` preset (intended: `illustrated_insights_carousel`)
  - Full pipeline: Dashboard → Backend → L1 → L3 → L5 → L6 → L7
  - First end-to-end V2 dashboard generation

### January 8, 2026 - Dashboard Session DB4
- **Phase A Fix:** job_service.py flattens tools, L1_data.py smart matchup default
- **Phase B Tool Standardization:** New tool keys (data_source, llm_query, tts, image_gen, animation, music)
- Files: tool_config.json V2, tool_resolver.py aliases, script_presets.json, presets.py, layer adapters, oracle.db

### January 8, 2026 - Dev Session D104
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
- **Fixed V2 layer script imports** - All 8 layer scripts (L1-L8) now have correct `PROJECT_ROOT` path
- **Fixed ai_models.py import path** - All 4 AI models now loading correctly
- **Fixed L5_media.py config paths** - SCRIPT_PRESETS_PATH and MEDIA_PRESETS_PATH now use PROJECT_ROOT
- **Tested remaining presets** - All working via Nano Banana:
  - `best_bets_matchup_infographic` - 2 infographics
  - `ai_image_matchup` - Routes to Nano Banana
  - `carousel_dark` - 3-slide watercolor carousel
  - `dark_incentives` - Requires manual player data (expected)

### January 8, 2026 - Oracle Session O99
- **Fixed sEEG monitor display bug**: Brain cells and API connections showing errors
  - Root cause: `seeg.py` missing `sys.path.insert(0, str(PROJECT_ROOT))`
  - Without this, `from oracle.maintenance import microglia` failed silently
  - Added sys.path fix at line 85 of `seeg.py`
- **Fixed stale health status**: Added missing `write_health_status()` function
  - Function was lost during P23 refactoring
  - Added to `microglia.py` and called from `run_audit()`
  - Now updates `.health_status.json` after each audit

### January 8, 2026 - Oracle Session O98
- **P24 sEEG Modernization COMPLETE**
  - Brain Cells + API Connections display in sEEG monitor
  - New methods: `_get_brain_cell_status()`, `_get_api_status()`, `_get_context_status()`
  - Display: DOCUMENTATION → BRAIN CELLS, OPTIMIZATIONS → API CONNECTIONS
  - Hotkeys: Added [b]rain diagnostics, removed [y]history

### January 8, 2026 - Oracle Session O97
- **P23 Brain Cell Architecture COMPLETE** - All 8 phases finished
  - Phase 8.1: Glial Functions in `microglia.py`
  - Phase 8.2: Synapses Functions in `oligodendrocytes.py`
  - Phase 8.3: Moved ORACLE_README.md to `oracle/` root
  - Context organization: Kept 4 files separate (Option A)

### January 7, 2026 - Oracle Sessions O92-O96
- **O96**: Presets Reference System + balldontlie API Key Fallback
- **O95**: P22 Phase 2 V2 Consolidation COMPLETE
- **O94**: P21 CodeOptimizer Enhancement
- **O93**: Workflow Simplification (manual session spawning preferred)
- **O92**: V2 Context & Reference Docs Overhaul (15 phases)

### January 7, 2026 - Dev Session D103
- **P20 Complete**: Removed ~500 lines legacy carousel code from L5_media.py
- **carousel_illustrated preset validated**: Full L3→L5→L6→L7 pipeline works
- **P21 plan created**: Enhanced CodeOptimizer (handed to Oracle)

### January 3, 2026 - Dev Session D101
- Week 18 carousel generation complete (CAR @ TB, SEA @ SF)
- Bug fix: Missing SCRIPT_PRESETS_PATH in media_generation.py
- PLAYER_TEAMS expanded to 208 players

### January 2, 2026 - Oracle Sessions O81-O83
- P15/P16 Scripts Reorganization complete
- api_utils.py decomposed into 29 modules in `_L3/`

---

## December 2025

### Recent Changes (Dec 24, 2025 - Session D99)
- **illustrated_insights_carousel fixes - all 6 tasks complete**
  - **Logo placeholder removed** (`api_utils.py` lines 2987-2990, 3070-3074)
    - Changed from reserved white box to cream background extending to all edges
    - Logo now added via PIL overlay in L6 (cleaner approach)
  - **PLAYER_TEAMS updated for 2025 mid-season trades** (`api_utils.py` lines 2047-2133, 2182-2194)
    - George Pickens: Steelers → Cowboys
    - Deebo Samuel: 49ers → Commanders
    - Javonte Williams: Broncos → Cowboys (also updated TEAM_RBS)
  - **Data flow fixed for insights_carousel** (`idea_creation.py` 1106-1112, `api_utils.py` 2897-2943)
    - Now passes raw `api_data` instead of filtered `carousel_data` to `build_insights_carousel_prompts()`
    - No more team filtering - uses all props from API's `betting_insights` directly
    - Should generate all 6 slides instead of only 2
  - **Player name extraction improved** (`api_utils.py` 3037-3059)
    - Added spread/moneyline/total bet detection
    - Uses team name for non-player props instead of "Player"
  - **Game metadata parsing enhanced** (`api_utils.py` 2974-2998)
    - Added error handling for `commence_time` parsing
    - Stadium/venue detection with dome stadium logic
    - Graceful fallback if no venue data
  - **Assembly & distribution list path bugs fixed** (`assembly.py` 2254-2277, `distribution.py` 458-477)
    - Added `insights_carousel` to carousel type checks
    - Enhanced `get_media_info()` to handle list vs single paths
    - No more TypeErrors when processing carousel slides

  - **Additional bugs found during testing**:
    - Fixed API field name mismatch in `api_utils.py` (line 2931-2940)
      - API uses `'props'` (normalized by idea_creation.py) not `'betting_insights'`
      - Reads from `api_data.get('props')` instead of `api_data.get('betting_insights')`
    - Fixed additional list path bug in `distribution.py:move_to_distribution_folder()` (line 625-628)
      - Added early return for carousel paths (list) - handled by separate `distribute_carousel()` function

**Why**: C10 built and tested illustrated_insights_carousel but only generated 2/6 slides due to PLAYER_TEAMS filtering out 2025 trades (Pickens, Deebo, Williams to Cowboys/Commanders). D99 fixes all data flow and metadata issues.

**Test Results** (Cowboys @ Commanders):
- ✅ Generated all 6 slides (cover + 5 props) instead of 2
- ✅ All props from API appeared (no filtering issues)
- ✅ George Pickens prop included (Cowboys trade recognized)
- ✅ Logo overlay applied to all slides via PIL
- ✅ No TypeErrors in assembly or distribution
- ✅ Cover shows "Game Day TBD" (API didn't provide `commence_time` - graceful fallback working)
- ✅ Prop slide shows full reasoning text with player illustration
- ✅ Total cost: $0.012 (~$0.002 per slide)
- ✅ Final output: `content/.../final/carousels/20251224_idea_001/` (6 slides numbered 01-06)

**Status**: illustrated_insights_carousel preset is now fully functional end-to-end (L3→L5→L6→L7). Ready for minor refinements and production use.

**Next**: Minor adjustments to prompt refinement, then ready for posting.

---

### Recent Changes (Dec 22, 2025 - Session D98)
- **Fixed animations distribution** (`distribution.py`)
  - P13: `find_animations()` now looks up matchup from `ideas_approved.json`
  - Previously just parsed folder name (`idea_001` → `idea 001`) which didn't work
  - Now: `idea_001` → looks up `carousel_data.away_team/home_team` → `49ers @ Colts`
  - P13: Carousel with reels goes to `final/carousels/{timestamp}_{matchup}/` (slides + reels together)
- **Verified truth_prompt_wrapper integration** ✅
  - Confirmed wrapper IS being applied in `build_carousel_prompts()` (api_utils.py lines 2876-2886)
  - All key directives present: INK SPLATTER, DRIPS, paint explosion, 30/100% intensity, grass/turf spray, motion blur
  - **Archived** `truth_prompt_wrapper.py` → `scripts/archive/` (with d98_truth_wrapper_archive_note.md)
  - Mined future bucket ideas: `VISUAL_STYLE_BUCKETS` for ink_effects, environmental, motion, saturation

**D98 STATUS: COMPLETE**
- Distribution fix done
- Truth wrapper verified and archived

**Next Tasks:**
1. **[CRANK C10]** Test O67 pipeline end-to-end (carousel_illustrated_reels) - SF @ IND
2. **[DEV D99]** Integrate meme_mashup preset into O67 architecture

---

### Recent Changes (Dec 22, 2025 - Session D97)
- **O67 Platform Architecture IMPLEMENTED**
  - Created `scripts/data_source.py` - L1 platform for unified data fetching
    - `DataSourcePlatform` class routes to appropriate tool based on preset's `L1_tool`
    - `DataContext` and `NormalizedMatchup` dataclasses for cross-tool normalization
    - Supports: goatedbets_api, web_search, local_assets, balldontlie, odds_api
  - Created `PipelineOrchestrator` class in `content_pipeline.py`
    - `PipelineContext` dataclass: mode, phase, week, preset, matchup, l1_data, etc.
    - Reads preset's `layers` array and calls each layer sequentially
    - Layer runners: `_run_l1()` through `_run_l8()`
    - Falls back to legacy flow for presets without `layers` array
  - Updated presets with O67 fields (`config/script_presets.json`):
    - `carousel_illustrated`: `["L1", "L2", "L3", "L5", "L6", "L7"]` - skips L4 (no audio)
    - `carousel_illustrated_reels`: same layers + L6_tool=reel_converter
    - `best_bets_dark`: same layers + output_type=infographic
    - `short_form_video`: `["L1", "L2", "L3", "L4", "L5", "L6", "L7"]` - includes L4 (TTS)
    - `long_form_video`: same as short_form_video
  - Updated `_execute_generate()` and `_execute_discovery()` to use orchestrator
  - Both modes now symmetric: O67 path if preset has layers, legacy path otherwise
- **Added infographics distribution**
  - Added `--infographics` flag to `distribution.py`
  - Added `find_infographics()` and `distribute_infographic()` methods
  - Infographics → `final/infographics/` (separate from carousels)
  - Orchestrator's `_run_l7()` now passes correct flag based on `output_type`

**D97 STATUS: O67 COMPLETE** - Platform architecture in place

---

### Recent Changes (Dec 22, 2025 - Session D96)
- **Auto-update**: Modified scripts: data_source.py; docs: CHANGELOG.md
- **Fixed prompt leak on matchup slide** - "NFL logo Ided to essing" text was bleeding into image
  - Simplified `logo_prompt` in `api_utils.py` to single sentence
  - Removed explicit "LOGO AREA (TOP-LEFT CORNER)" sections from all slide prompts
  - Result: Clean images with no instruction text visible
- **Fixed discolored logo block** - Removed "RESERVED zone" language that AI interpreted as colored area
  - Cover, matchup, bonus prompts all simplified
  - Background now uniform cream across entire image
- **Removed team abbreviations from matchup edges** - Column header already shows team
  - `g_api_processor.py`: `select_best_entity()` no longer prefixes with team abbrev
  - `g_api_processor.py`: `_get_thesis_fallbacks()` returns phrases without team prefix
  - `api_utils.py`: Legacy fallbacks and variety pools updated (no team prefix)
  - Before: "SF 28% targets" → After: "28% targets"
  - Before: "IND home cooking" → After: "Home cooking"
- **Centered matchup header** - Removed left-margin positioning instructions
- **Full pipeline test** - SF @ IND carousel verified all fixes
  - Cost: $0.012 (2 regenerations)

**D96 STATUS: COMPLETE** - Prompt fixes and edge cleanup done

---

### Recent Changes (Dec 26, 2025 - Session P9)

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

**Smart Text Analysis Toolkit:**
- `analyze_for_highlights()` - Find key phrases for visual emphasis
- `analyze_for_buckets()` - Categorize text into themes (betting_prop, game_preview, etc.)
- `analyze_for_sentiment()` - Detect bullish/bearish/neutral for color coding
- `extract_entities()` - Pull out players, teams, stats
- `extract_key_stats()` - Structured stat extraction with context
- `summarize_to_length()` - Condense text to fit UI constraints

**Files modified**:
- `scripts/api_utils.py` (Smart Text Toolkit lines 144-790, LLM extraction lines 896-1324)
- `scripts/content_pipeline.py` (import, init, menu, toggle method, execution calls)

---

### Recent Changes (Dec 26, 2025 - Session P8)

**Asset Ingestion Text Removal Tools:**
- Integrated cleaning tools into ingestion (L1):
  - All cleaning operations now part of `ingest()` method
  - CLI flags: `--auto-crop`, `--crop-top/bottom/left/right`, `--strip-subs`, `--find-original`
  - Removed standalone crop/clean modes - everything flows through ingestion
- Text removal strategy documented:
  1. Find original source (best - no info loss, free)
  2. Cropping (quick fix when original unavailable)
  3. Runway ML (~$15/mo or ~$0.05/sec API)
  4. ProPainter (future - requires NVIDIA GPU)

**Files modified**: `scripts/asset_ingestion.py`

---

### Recent Changes (Dec 22, 2025 - Session D95)
- **Auto-update**: Modified scripts: api_utils.py, g_api_processor.py
- **Created `scripts/g_api_processor.py`** - GoatedBets API Processor (L3 layer)
  - Structured text extraction pipeline replacing ad-hoc patterns
  - Stage 1: Entity extraction (players, coaches, teams, stats from sentences)
  - Stage 2: Bucket organization (offense/defense/situational per team)
  - Stage 3: Layout formatting (30 char edges, 45 char cover insights)
  - Thesis alignment scoring for prioritizing relevant stats
  - Dataclasses: `ExtractedEntity`, `Stat`, `TeamBucket`, `MatchupBuckets`, `FormattedOutput`
- **Pre-refactor snapshot created:** `scripts/archive/d94_extraction_snapshot/`
- **New Rule #25 added:** "Pre-Refactor Snapshot Rule" - archive before major refactors
- **D95 Integration COMPLETE:**
  - Added `_get_g_api_processor()` lazy import in `api_utils.py`
  - Integrated into `transform_matchup_for_carousel()` with fallback to legacy extraction
  - Fixed sentence splitting to handle semicolons (proper player attribution)
  - Tested with real GoatedBets API (NE @ BAL):
    ```
    Cover Insights:
      1. Stakes high for BAL
      2. BAL matchup edge
      3. BAL covers the spread
    Matchup Edges:
      Away: ['NE 300 yds', 'NE tightens up', 'NE urgent mode']
      Home: ['Flowers 100 targets', 'BAL makes plays', 'BAL December form']
    ```
  - Compared with D94 snapshot - key patterns preserved (thesis alignment, attribution, char limits)

**D95 STATUS: COMPLETE** - Structured extraction pipeline integrated and tested

- **Fixed `fetch_goatedbets_matchup()` abbreviation matching** (idea_creation.py)
  - Added `abbrev_to_names` mapping for all 32 NFL teams
  - `matches_team()` helper expands abbreviations before matching
  - SF @ IND, JAX @ DEN, KC @ TEN, TB @ CAR all now work with abbreviations

---

### Recent Changes (Dec 21, 2025 - Session D94)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Auto-update**: Modified scripts: api_utils.py, assembly.py
- **All C7 Crank issues resolved** - See section above for details
- **Universal enhancements** - Changes apply to ALL presets using GoatedBets API:
  - PLAYER_TEAMS reference dict used for player attribution
  - team_cities mapping for city-to-team resolution
  - No preset-specific hardcoding - modular design

---

