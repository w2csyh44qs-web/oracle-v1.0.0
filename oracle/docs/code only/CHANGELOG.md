# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

> **Scope:** Raw session facts only. For design decisions and rationale, see [CODE_HISTORY.md](../overview/CODE_HISTORY.md).

---

### Recent Changes (Dec 18, 2025 - Session 56)
- **Refined carousel prompts to match original approved images** ✅
  - Rewrote all three prompts (cover, matchup, bonus) with exact layout specifications
  - Cover: Player name large on left, player illustration on right, three insight bullets with icons
  - Matchup: Two-column layout with helmets, orange/teal marker-style highlights, predicted winner
  - Bonus Props: Three rows with player illustrations LEFT, text RIGHT, italic bold names
- **Fixed API data parsing** - First prop is best bet, bonus props skip first prop (props[1:4])
- **Added new potential logo (Logo Option 2)** to `assets/branding/LOGO_REFERENCE.md`
- **Added Rule 18 (Code Optimization Rule)** - No hardcoded data, data flows from APIs
- **API-driven carousel generation** - `instagram_carousel_generator.py` uses `fetch_matchup_from_api()`
- **Tested with LAR @ SEA** - All three slides generating correctly in 1:1 format

### Recent Changes (Dec 18, 2025 - Session 55)
- **Added Image output type for non-infographic images** ✅
  - **New OUTPUT_TYPE category**: "Image" - AI-generated images where text is added at assembly (L6)
  - **Tool distinction**: Infographic uses Nano Banana (baked-in text), Image uses Imagen 4 (clean image)
  - **New presets**: `ai_image_matchup` (photorealistic matchup scene), `ai_image_player` (artistic player feature)
  - **Menu updated**: [1] Infographic, [2] Image, [3] Video
  - **Use case**: Generate beautiful AI images, add consistent text overlays with controlled fonts at assembly

### Recent Changes (Dec 18, 2025 - Session 54)
- **Implemented output type selection for Generate Mode** ✅
  - **New Generate Mode menu** with [1] Run, [2] Select Output Type & Preset, [3] Configure aspect ratio, [4] Configure tools
  - **Output type categories**: Infographic (image/carousel) and Video (short-form/long-form)
  - **Per-category preset display** with aspect ratio and style info
- **Updated default aspect ratio from 9:16 to 4:5** ✅
  - `media_generation.py`: VIDEO_FORMATS now defaults to "portrait" (4:5, 1080x1350)
  - `assembly.py`: Same VIDEO_FORMATS update
  - `platforms.py`: UNIVERSAL_LIMITS and instagram_reels updated to 4:5
  - Infographic prompts updated to use 4:5 portrait format
- **Created separate infographic presets** in `script_presets.json` ✅
  - `best_bets_matchup_infographic` - Generic/flexible (4:5 default)
  - `best_bets_single_image` - Single focused image with illustrated style (1:1 default)
  - `matchup_analysis_infographic` - Detailed matchup breakdown, dark style (1:1 default)
  - `instagram_carousel` - Multi-slide carousel (1:1 default)
  - Each preset has `aspect_ratio_options` for user adjustment
- **Added video placeholder presets** ✅
  - `short_form_video` - Under 60s, universal platform compatibility
  - `long_form_video` - Over 60s, user confirmation at content time
- **Added aspect ratio CLI argument** to `idea_creation.py` ✅
  - `--aspect-ratio` flag (1:1, 4:5, 9:16, 16:9)
  - Resolution order: CLI override → preset → resolution-based default
  - Flows through `platform_config` to downstream layers

### Recent Changes (Dec 18, 2025 - Session 53)
- **Created Instagram carousel generator for image posts** ✅
  - New script `scripts/instagram_carousel_generator.py` for image carousel posts
  - Formats: `portrait` (4:5), `square` (1:1, default)
  - Uses Nano Banana Pro (Gemini), consistent GoatedBets logo rendering
- **Generated 1:1 Instagram carousel** for LAR vs SEA matchup ✅

### Recent Changes (Dec 18, 2025 - Session 52)
- **Auto-update**: Modified docs: CHANGELOG.md
- **L6 video assembly now supports silent infographics** ✅
  - **Problem**: Infographic mode required audio file, but infographics are static images
  - **Solution**: Modified `assembly.py` to detect `display_mode: infographic` and use fixed duration
  - Duration defaults to 15s (from package or preset)
  - Ken Burns animation applied for subtle motion
  - Generated: `idea_001_vertical.mp4` (11.9 MB) - silent 15s video with Ken Burns
- **Pipeline fully tested for illustrated style** ✅
  - L5 → L6 flow working with `infographic_style: "illustrated"`
  - Logo specification from `LOGO_REFERENCE.md` embedded in prompt
  - Only one NFL matchup available (Rams @ Seahawks - TNF)

### Recent Changes (Dec 18, 2025 - Session 51)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Added illustrated infographic style** ✅
  - **New style**: `infographic_style: "illustrated"` - watercolor/sketch player with light background
  - **GoatedBets logo**: EXACT specification in `assets/branding/LOGO_REFERENCE.md`
    - Orange/gold goat head facing LEFT, flame mane, "GOATED" + "BETS" stacked below
    - Must be rendered identically every time
  - **Visual**: Cream/beige paper texture (#F5F2EB), watercolor player illustration
  - **Content**: Full reasoning paragraph displayed (not condensed bullets)
  - **Single graphic**: Illustrated style only generates best bet (no prediction)
- **Refined dark style** ✅
  - Mix of sharp (angled banners) and rounded (cards) shapes
  - Bordered logo frames in header with team colors
  - Diagonal accent lines, VS graphic, football icons
  - Color variety: gold best bet, cyan analysis, team colors for bonus props
- **File modified**: `scripts/media_generation.py` - `generate_nano_banana_infographic()` now accepts `visual_style` param
- **New file**: `assets/branding/LOGO_REFERENCE.md` - official logo specification

### Recent Changes (Dec 18, 2025 - Session 50)
- **Refined prediction infographic team edge bullets** ✅
  - **Problem**: Previous versions either truncated insights mid-sentence or lost valuable API analysis
  - **Solution**: `shorten_insight()` function with smart clause breaking + key term highlighting
  - **Word cap**: 25 words max (down from 35) for balanced visual layout
  - **Key term highlighting**: Football terms wrapped in `**bold**` markers for Nano Banana to render
    - Terms: safety rotations, check-downs, silent count, air yards, defensive line stunts, slide protections, etc.
  - **Clause breaking**: Finds natural break points (`, forcing`, `, causing`, `, suggesting`, etc.)
  - **Final output examples**:
    - "Mike Macdonald's defensive scheme relies heavily on post-snap **safety rotations** that are notoriously difficult to diagnose on a **short week**." (20 words)
    - "The Seahawks have consistently used interior **defensive line stunts** to exploit the Rams' aggressive **slide protections**." (16 words)
- **Updated prediction prompt**: Balanced columns with breathing room, explicit bold rendering instruction
- **File modified**: `scripts/media_generation.py` - `shorten_insight()` function at ~line 796

### Recent Changes (Dec 18, 2025 - Session 49)
- **Created global team colors config** ✅
  - New file: `config/team_colors.py` - shared color mapping for all sports
  - **8 leagues**: NFL (32), NBA (30), MLB (30), NHL (32), EPL (20), WNBA (12), NCAAF (70), NCAAB (30)
  - **~256 teams total** with cyberpunk-friendly colors for dark backgrounds
  - Functions: `get_team_colors(abbrev, sport)`, `get_matchup_colors(away, home, sport)`
  - Updated `media_generation.py` to import from shared config
  - Auto-detects sport from `api_data`, defaults to NFL

### Recent Changes (Dec 18, 2025 - Session 48)
- **Split infographic into 2 separate images** ✅
  - **Best Bet infographic** (`infographic_best_bet.png`): Main prop bet + short reasoning bullets + bonus props
  - **Prediction infographic** (`infographic_prediction.png`): Team edges + predicted winner
  - **Why**: Single infographic was cramped with competing focal points; 2 images = carousel or 2 posts
- **Fixed team color coding** ✅
  - Rams = orange/gold outline (not cyan)
  - Seahawks = green/cyan outline
  - Team color mapping in `media_generation.py` at line ~790
- **Fixed text cutoff issues** ✅
  - "Why This Hits" bullets: Template-based 5-6 word phrases (not truncated API text)
  - Team edge bullets: Template-based short phrases
  - Detects bet type (receptions, yards, rush, TD) and context (revenge game, short week)
- **Revenge game detection**: If reasoning contains "former team", uses:
  - "Revenge game vs former team"
  - "Knows defensive soft spots"
  - "Extra motivation expected"
- **Generated files**: `content/nfl/2025-2026/regular_season/week16/media/idea_001/`
  - `infographic_best_bet.png` (740 KB)
  - `infographic_prediction.png` (790 KB)

### Recent Changes (Dec 18, 2025 - Session 47)
- **Fixed Nano Banana to use Nano Banana Pro (gemini-3-pro-image-preview)** ✅
  - **Problem**: Imagen 4 produced garbled, unreadable text on infographics
  - **Solution**: Switched to **Nano Banana Pro** (`gemini-3-pro-image-preview`) via multimodal chat API
  - Model: `gemini-3-pro-image-preview` (not imagen-4.0 or gemini-2.0-flash)
  - Use `client.chats.create()` with `response_modalities=['TEXT', 'IMAGE']`
  - Extract image from `response.candidates[0].content.parts` via `inline_data`

### Recent Changes (Dec 18, 2025 - Session 46)
- **End-to-end test of best_bets_matchup_infographic preset (L3 + L5)**
  - **L3 test** ✅: Fixed `fetch_goatedbets_matchup()` in `scripts/idea_creation.py`:
    - API returns all sports at once (nfl, nba, etc.) - not per-matchup
    - API uses `betting_insights` with `prop`/`explanation` fields
    - Normalized to `props` with `description`/`reasoning` for internal use
    - Fixed f-string syntax error (backslash in list comprehension)
  - **L5 test** ✅: Fixed Nano Banana in `scripts/media_generation.py`:
    - Switched from deprecated `google.generativeai` to `google.genai` package
    - Changed from Imagen 3 to **Imagen 4** (`imagen-4.0-generate-001`)
    - Fixed safety filter: `BLOCK_LOW_AND_ABOVE` (not `BLOCK_ONLY_HIGH`)
    - Successfully generated 1MB infographic at `content/.../week16/media/idea_001/infographic.png`
  - **L6 skipped** per user request (Ken Burns can be tested later)
  - **Dependencies installed**: `pip install google-genai`

### Recent Changes (Dec 18, 2025 - Session 45)
- **Task #16: best_bets_matchup_infographic preset - COMPLETE** ✅
  - **Step 7** ✅: Added infographic handler to `scripts/assembly.py`:
    - Added `_handle_infographic_mode()` method - handles static infographic with Ken Burns animation
    - Updated `assemble_video()` to route to infographic handler when `display_mode == 'infographic'`
    - Updated `process_packages()` to check package's `display_mode` first (from L5), then preset
    - Pass through `api_data` from package to settings for logging
  - **Full pipeline**: L3 (API fetch + prop picker) → L5 (Nano Banana infographic) → L6 (Ken Burns video)

### Recent Changes (Dec 18, 2025 - Session 44)
- **Task #16: best_bets_matchup_infographic preset - Steps 5-6**
  - **Step 5** ✅: Added API fetch + prop picker to `scripts/idea_creation.py`:
    - Added `fetch_goatedbets_matchup(away_team, home_team)` function - calls GoatedBets API
    - Added `detect_week_from_commence_time(commence_time)` function - auto-detects NFL week
    - Added `PropPickerCheckpoint` class - interactive UI for selecting best bet from props
    - Added `auto_select` param to `IdeaCreation.__init__` and CLI (`--auto-select`)
    - Refactored `generate_from_preset()` to route to `_generate_from_api_preset()` or `_generate_from_ai_preset()`
    - New `_generate_from_api_preset()` method handles API-driven presets with prop picker
  - **Step 6** ✅: Added NanoBananaGenerator to `scripts/media_generation.py`:
    - Added `self.gemini_available` flag in `__init__`
    - Added Gemini API key check in `_init_clients()`
    - Added `generate_nano_banana_infographic(idea, output_path)` method - uses Gemini for infographics
    - Added `_generate_imagen_infographic(prompt, output_path)` fallback method
    - Updated `create_media_package()` to route to Nano Banana for `nano_banana` tool or `infographic` display mode
    - Pass through `display_mode` and `api_data` to media_package for L6

### Recent Changes (Dec 17, 2025 - Session 43)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Task #16: best_bets_matchup_infographic preset - Steps 1-4**
  - **Step 1** ✅: Added `GEMINI_API_KEY` to `.env` (Nano Banana for infographics)
  - **Step 2** ✅: Updated `config/tool_config.json`:
    - Added `nano_banana` to `image_gen.options`
    - Set as fallback for image_gen
    - Updated notes to mention text-heavy infographics
  - **Step 3** ✅: Renamed `single_matchup_card` → `matchup_card_video` in `script_presets.json`
  - **Step 4** ✅: Added `best_bets_matchup_infographic` preset to `script_presets.json`:
    - `api_source: "goatedbets_matchup_analysis"` - uses GoatedBets API
    - `use_web_context: false` - doesn't need web search
    - `image_tool: "nano_banana"` - Gemini for infographic generation
    - `display_mode: "infographic"` - new display mode
    - Template variables: `{away_team}`, `{home_team}`, `{week}`, `{best_bet_prop}`, etc.

### Recent Changes (Dec 17, 2025 - Session 42)
- **Task #17: Merge SourceConfig into ToolConfig - COMPLETE** ✅
  - **Steps 1-4** (Session 41): Updated tool_config.json, tool_resolver.py, web_search_trend_detector.py
  - **Step 5**: Updated `scripts/content_pipeline.py` Discovery Mode:
    - Changed `display_config()` to show `data_sources` instead of `web_search`
    - Removed `self.current_discovery_sources` session state
    - Updated `run_discovery_mode()` to show current data source from tool_resolver
    - Simplified `_configure_discovery()` (query + data source via tool config)
    - Deleted `_configure_discovery_tools()` method (no longer needed)
    - Updated `_load_discovery_preset()` and `_save_discovery_preset()` to not use SourceConfig
    - Updated `_execute_discovery()` - no longer passes source_config parameter
    - Updated `_show_all_tools_view()` to use `data_sources` instead of `web_search`
  - **Step 6**: Added L1 (Data Sources) to per-layer tool view with `--source` CLI arg
  - **Step 7**: Added `--source` CLI arg to `web_search_trend_detector.py`:
    - Choices: `tavily_websearch`, `perplexity_search`, `goatedbets_api`, `reddit_api`
  - **Step 8**: Simplified discovery presets in `script_presets.json`:
    - Removed old nested `sources` structure
    - Data source config now handled via `tool_config.json`
  - **Step 9**: Updated `tests/test_tool_resolver.py`:
    - Changed `web_search` to `data_sources` in parametrized test
    - Added `TestGetSourceConfig` class with 5 new tests
    - All 23 tests passing

### Recent Changes (Dec 17, 2025 - Session 41)
- **Task #17: Merge SourceConfig into ToolConfig - Steps 1-4**
  - **Step 1**: Updated `config/tool_config.json`:
    - Replaced `web_search` category with `data_sources`
    - Added nested `source_configs` with per-source settings (domain filters, endpoints)
    - Sources: `tavily_websearch`, `perplexity_search`, `goatedbets_api`, `reddit_api`, `action_network`
    - Bumped version to 1.1.0
  - **Step 2**: Updated `config/tool_resolver.py`:
    - Added `get_source_config(source_name)` method for nested config lookup
    - Updated class docstring with new `data_sources` category
  - **Step 3-4**: Updated `scripts/web_search_trend_detector.py`:
    - **DELETED** entire `SourceConfig` class (~118 lines removed)
    - Changed `__init__` param from `source_config: SourceConfig` to `source_override: str`
    - Now uses `tool_resolver.resolve_tool('data_sources')` for source selection
    - Now uses `tool_resolver.get_source_config(source_name)` for domain filtering

### Recent Changes (Dec 17, 2025 - Session 39)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Task #15: Tool Selection Enhancement - COMPLETE** ✅
  - **Step 1-4 (D37)**: Added CLI tool override args to all layer scripts:
    - `idea_creation.py`: `--model` (perplexity, gpt-4o, gpt-4o-mini)
    - `audio_sync.py`: `--tts-tool` (elevenlabs, openai, coqui)
    - `media_generation.py`: `--image-tool` (flux_fal, dalle3, pexels)
    - `assembly.py`: `--animation-tool` (kling_2.6, kling_turbo, ken_burns)
  - **Step 5**: Enhanced `[t]` Tool Configuration menu in `content_pipeline.py`:
    - New submenu: [1] Per-Layer View (L3-L6 with CLI args), [2] All Tools View
    - Per-Layer View shows: Layer, Script, Default, Fallback, Options, CLI override arg
  - **Step 6**: Added `tools` section to generate presets in `script_presets.json`:
    - Each preset can now specify: `model`, `tts_tool`, `image_tool`, `animation_tool`
    - `single_matchup_card` preset: uses `pexels` for images, `ken_burns` for animation
    - Tool flow: CLI override → Preset tools → tool_config.json → System defaults
  - Updated L4/L5/L6 to read `tools` from idea and pass to `get_effective_settings()`
  - Updated `tool_resolver.py` docstrings to clarify resolution order
  - **Design decision for Vision Orchestrator** (Task #13, future):
    - Current: CLI uses `vision_override` param (highest priority slot)
    - When Vision is built: CLI should still beat Vision (user typing now > batch config)
    - Proposed order: CLI → Vision → Preset → tool_config.json → System defaults
    - Rationale: Preset tools are part of the preset's identity; Vision is ambient preference

### Recent Changes (Dec 17, 2025 - Session 36)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Task 12: Automated Pytest Tests - COMPLETE** ✅
  - Created `pytest.ini` - pytest configuration
  - Created `tests/conftest.py` - shared fixtures (mock configs, temp dirs, env vars)
  - Created `tests/test_tool_resolver.py` - 18 tests for ToolResolver class
  - Created `tests/test_preset_managers.py` - 24 tests for all PresetManager classes (L3-L6)
  - Created `tests/test_nfl_calendar.py` - 19 tests for NFLCalendar module
  - Renamed `tests/test_layer2.py` → `tests/interactive_test_layer2.py` (interactive input breaks pytest)
  - Installed pytest: `pip3 install pytest --user`
  - **61 tests passing** - Run with `python3 -m pytest tests/ -v`

### Recent Changes (Dec 17, 2025 - Session 35)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Task 10: `single_matchup_card` Preset - COMPLETE** ✅
  - **Step 3**: Added `matchup_card` display_mode handler to `assembly.py`:
    - `_parse_matchup_card_content()` method (lines 1160-1214) - parses LLM structured output
    - `_add_matchup_card_overlays()` method (lines 1216-1382) - renders timed text overlays
    - Updated display_mode switch (line 1250) to route `matchup_card` → new handler
  - **Step 4**: Tested with Rams @ Seahawks matchup - **SUCCESS**
    - L3: Perplexity generated structured content with betting analysis
    - L4: ElevenLabs TTS created 51s audio (~$0.19)
    - L5: Placeholder background generated
    - L6: Matchup card rendered with timed reveals (Title/Week at 0s, THE PICK at 3s, Pick line at 3.5s, Reasoning at 5s, CTA at 12s)
    - Output: `content/nfl/2025-2026/regular_season/week15/assembled/idea_001_vertical.mp4` (12.4 MB)
  - **Bug fixes during testing**:
    - Fixed `get_content_preset()` in `idea_creation.py` to load from `generate_presets` (renamed from `content_presets` in Task 8)
    - Fixed `get_content_preset_settings()` in `assembly.py` to load from `generate_presets`
    - Fixed parser to handle `**THE PICK:**` bold format and clean Perplexity citations `[1][2]`

### Recent Changes (Dec 17, 2025 - Session 34)
- **Task 10: `single_matchup_card` Preset - Steps 1-2 COMPLETE** ✅
  - **Step 1**: Added presets to `config/script_presets.json`:
    - `single_matchup_card` generate preset with Perplexity model, matchup_card display_mode
    - `matchup_card_style` visual style (football field stadium dark)
    - `card_pace` pacing preset (timed reveals: intro 1.5s, pick 3s, reasoning 5s, CTA 12s)
    - `matchup_card` display_mode entry
  - **Step 2**: Added `--matchup` CLI arg to `scripts/idea_creation.py`:
    - Added `--matchup` argument to argparse
    - Added `matchup` parameter to `IdeaCreation.__init__`
    - Stored as `self.matchup`
    - Updated template formatting with `{matchup}` and `{week}` variables

### Recent Changes (Dec 17, 2025 - Session 33)
- **Auto-update**: Modified maintenance: project_oracle.py
- **Auto-update**: Modified scripts: idea_creation.py; docs: CHANGELOG.md
- **Task 9: Tool Configuration Integration COMPLETE** ✅
  - **Step 1**: Created `config/tool_resolver.py` (NEW FILE)
    - `ToolResolver` class with resolution order: vision > preset > tool_config.json > fallback > free_fallback
    - Methods: `resolve_tool()`, `get_fallback()`, `get_free_fallback()`, `try_with_fallback()`
    - Singleton `tool_resolver` instance for easy import across modules
  - **Step 2**: Updated `scripts/content_pipeline.py`
    - Imported `tool_resolver` singleton
    - `ToolConfigManager.get_tool()` now delegates to `tool_resolver.resolve_tool()`
    - `_save_config()` calls `tool_resolver.reload_config()` after saving
  - **Step 3**: Wired ToolResolver to L4 (`scripts/audio_sync.py`)
    - Imported `tool_resolver` from `config.tool_resolver`
    - Updated `get_effective_settings()` to use ToolResolver for TTS tool selection
    - Added `preset_override` parameter for future preset tool overrides
  - **Step 4**: Wired ToolResolver to L5 (`scripts/media_generation.py`)
    - Imported `tool_resolver` from `config.tool_resolver`
    - Updated `get_effective_settings()` to use ToolResolver for `image_gen` tool selection
    - Added `preset_override` parameter for future preset tool overrides
  - **Step 5**: Wired ToolResolver to L6 (`scripts/assembly.py`)
    - Imported `tool_resolver` from `config.tool_resolver`
    - Updated `get_effective_settings()` to use ToolResolver for `animation` tool selection
    - Added `preset_override` parameter for future preset tool overrides
  - **Step 6**: Wired ToolResolver to L3 (`scripts/idea_creation.py`)
    - Imported `tool_resolver` from `config.tool_resolver`
    - Updated `get_effective_settings()` to use ToolResolver for `content_generation` tool selection
    - Added `preset_override` parameter for future preset tool overrides

### Recent Changes (Dec 17, 2025 - Session 32)
- **Auto-update**: Modified scripts: content_pipeline.py, audio_sync.py; docs: CHANGELOG.md
- **Task 9: Tool Configuration Integration started** (Steps 1-3 completed)

### Recent Changes (Dec 17, 2025 - Session 31)
- **Task 8: Generate Mode Symmetry COMPLETE** ✅
  - **Renamed `content_presets` → `generate_presets`** in `config/script_presets.json`
    - Section note updated to reflect Generate Mode purpose
  - **Updated `GenerateModePresetManager`** to load from `generate_presets` section
  - **Refactored `run_generate_mode()`** with symmetric 1-4 menu:
    - [1] Run with current preset
    - [2] Configure tools (LLM model selection)
    - [3] Load Generate Preset
    - [4] Save current as preset (future placeholder)
    - [c] Cancel
  - **Added `_configure_generate_tools()`** - Tool selection for Generate Mode (LLM, TTS, image, animation)
  - **Added `_load_generate_preset()`** - Preset loading for Generate Mode
  - **Added `_configure_discovery_tools()`** - Tool selection for Discovery Mode (web search, LLM)
  - **Updated `_configure_discovery()`** with [3] Configure tools option
  - **Symmetric architecture achieved**: Both modes have same menu structure + access to tool config

### Recent Changes (Dec 17, 2025 - Session 30)
- **Task 7: Discovery Mode Enhancement COMPLETE** ✅
  - **Archived** `trend_detection.py` → `docs/archive/trend_detection_archived.py`
    - Preserved multi-source orchestration pattern for future reference
  - **Added `SourceConfig` class** to `web_search_trend_detector.py`:
    - Manages discovery sources (websearch, reddit_direct, action_network)
    - Each source toggleable with focus/exclude domain config
    - `display_menu()` for interactive source configuration
    - `to_dict()`/`from_dict()` for preset save/load
  - **Added `DiscoveryModePresetManager` class** to `content_pipeline.py`:
    - Parallel to `GenerateModePresetManager` for symmetric architecture
    - Loads/saves from `discovery_presets` section in script_presets.json
  - **Updated Discovery Mode menu** (symmetric 1-4 options):
    - [1] Run with current settings
    - [2] Configure search (query, sources)
    - [3] Load Discovery Preset
    - [4] Save current as preset
  - **Added `discovery_presets` section** to `config/script_presets.json`:
    - `nfl_betting_trends` - Default NFL betting trend search
    - `nfl_bad_beats` - Bad beats and upsets focus
  - **Updated docs**: ARCHITECTURE.md (file structure, L1 SourceConfig docs), README.md (L0 entry point)
- **L0 naming**: `ContentPipeline` docstring updated to "L0 Entry Point"

### Recent Changes (Dec 17, 2025 - Session 29)
- **Auto-update**: Modified docs: ARCHITECTURE.md, CHANGELOG.md
- **`single_matchup_card` preset PLANNED** - Full implementation spec documented
  - Card layout, content structure, implementation steps
  - Files to modify: script_presets.json, idea_creation.py, assembly.py
  - Usage: `--content-preset single_matchup_card --matchup "Rams @ Seahawks"`
  - Priority: After Discovery Mode Enhancement + Tool Config Integration
- **Class rename**: `ContentPresetManager` → `GenerateModePresetManager` in content_pipeline.py

### Recent Changes (Dec 17, 2025 - Session 28)
- **L1 Entry Point BUILT** - `scripts/content_pipeline.py` ✅
  - Mode selection menu: Discovery, Generate, and future modes (Hybrid, Scheduled, Manual, Remix)
  - **Discovery Mode**: Runs `web_search_trend_detector.py` (Tavily web search → trends)
  - **Generate Mode**: Runs `idea_creation.py --content-preset` (LLM-direct → ideas_approved.json)
  - **Tool Configuration**: Edit tool selections via interactive menu
    - Categories: web_search, content_generation, tts, image_gen, animation
    - Changes saved to `config/tool_config.json`
  - Preset browser shows available content presets with prompt_template
  - Classes: `ContentPipeline`, `ToolConfigManager`, `ContentPresetManager`
- **Usage**:
  ```bash
  python3 scripts/content_pipeline.py  # Interactive L1 entry point
  ```

### Recent Changes (Dec 17, 2025 - Session 27)
- **Context resume only** - Read both context files, confirmed pending tasks
- **L1 Module Selection Architecture** (finalized in O27):
  - Mode selection at L1 entry point: Discovery, Generate, Hybrid, Scheduled, Manual, Remix
  - Tool config via `config/tool_config.json` (placeholder created in O27)
  - Presets can save tool selections
  - See ORACLE_CONTEXT Session 35 (O27) for full architecture

### Recent Changes (Dec 16, 2025 - Session 26)
- **Auto-update**: Modified docs: CHANGELOG.md
- **Text-audio sync** implemented in `assembly.py`:
  - `_add_positioned_text_overlays()` now reads subtitle timings from `text_overlays.subtitles`
  - Builds timing map from numbered items (1., 2., etc.) to their audio start times
  - Each text overlay appears when the narrator starts reading that item
  - Falls back to staggered timing if no sync data available
  - Logs "🔊" indicator for items using audio sync
- **Heading styling** (gold + larger font) implemented in `assembly.py`:
  - Added `_parse_heading_and_body()` to extract `**bold**` markdown text as heading
  - Headings (e.g., "1. Los Angeles Rams at Seattle Seahawks") render in gold (#FFD700) at 28px
  - Body text (reasoning) renders in adaptive color at 24px below heading
  - Title also now renders in gold for consistency
  - Two-tier layout: heading above, body below with 45px vertical offset
- **Helper functions** added:
  - `_smart_wrap_text()` - Intelligent line breaking at punctuation
  - `_parse_heading_and_body()` - Extracts markdown bold as heading

### Recent Changes (Dec 16, 2025 - Session 25)
- **Text margin fix** in `assembly.py`:
  - Increased `x_margin` from 60px to 80px (160px total safe zone)
  - Reduced font sizes: title 52px, items 24px (from 56/28)
  - Renamed `x_padding` → `x_margin`, `text_area_width` for clarity
  - Increased `y_start` to 280px, `y_spacing` to 300px for better layout
- **Pexels stock image fallback** in `media_generation.py`:
  - Added `_search_pexels_images()` for image search (not just video)
  - Added `download_pexels_image()` to download stock images
  - Updated `create_media_package()` to fallback to Pexels when Flux fails
  - Uses visual style's `pexels_query` from content preset
  - Sets `background_type` to `pexels_stock` when using fallback
  - **Cost**: FREE (Pexels images are free to use)
- **L5 --ids filter** added to `media_generation.py`:
  - Added `--ids idea_001 idea_002` argument for testing
  - Filters ideas before processing to limit costs
- **Kling AI image animation integration** ✅:
  - Added `animation_models` section to `script_presets.json`:
    - `kling_standard`: $0.25/5s (default)
    - `kling_turbo`: $0.35/5s (faster)
    - `kling_master`: ~$1.00/video (best quality)
  - Added animation settings to visual styles in `script_presets.json`:
    - `animate_background`, `animation_model`, `animation_prompt` fields
    - New `sports_dynamic_animated` visual style for testing
  - Added `_animate_image_with_kling()` function in `assembly.py`:
    - Encodes image as base64, calls FAL AI Kling endpoint
    - Downloads animated video result, saves to disk
    - Returns path to animated video or None on failure
  - Updated `_create_background_clip()` to use animation when enabled:
    - Checks `animate_background` from visual style settings
    - Calls Kling animation, falls back to Ken Burns on failure
  - Added CLI flags `--animate` and `--animation-model` to force animation
  - Updated `run()` method with `force_animate` and `animation_model` params
  - **Cost**: ~$0.25-1.00 per animated background (Kling via FAL AI)
  - **Status**: Ready for testing with single video output

### Recent Changes (Dec 16, 2025 - Session 24)
- **Prompt accuracy fix**: Updated `best_bets_slate` prompt template
  - Added `{today_date}` placeholder for explicit date context
  - Tells Perplexity to verify current player team affiliations
  - Uses real-time injury reports and roster updates
  - Updated `idea_creation.py` to pass formatted date
- **Text readability improvements** in `assembly.py`:
  - Added `_analyze_background_for_text_colors()` - samples background luminance
  - Dynamic text/stroke colors based on background:
    - Dark bg (< 0.3): white text + black stroke
    - Light bg (> 0.6): dark text + white stroke
    - Medium bg: gold text + black stroke
  - Added stroke support to `_create_text_clip()` (3px default)
  - Better text wrapping at punctuation (` - `, `: `, ` | `)
  - Reduced font size (28px items) to prevent text cutoff
  - Layout: y_start=250, y_spacing=280, max 5 items
- **Voice preset integration** in `audio_sync.py`:
  - Added `get_voice_preset_from_content()` to AudioPresetManager
    - Reads `voice_preset` from content preset (e.g., `best_bets_slate` → `sports_authoritative`)
    - Looks up voice settings in `script_presets.json`'s `voice_presets` section
    - Returns voice_id, voice_name, stability, similarity_boost
  - Updated `generate_audio()` to apply voice preset when content_preset is set
    - Overrides default voice with preset's voice_id
    - Applies preset's stability and similarity_boost settings
  - Updated `_generate_elevenlabs()` to handle direct voice_id (not just key lookups)
  - **Result**: Content presets now control voice selection automatically
    - `best_bets_slate` → `sports_authoritative` → Adam voice with stability=0.5, similarity=0.75

### Recent Changes (Dec 16, 2025 - Session 23)
- **End-to-end preset generation test** ✅:
  - Ran full L3→L4→L5→L6 pipeline with Perplexity-generated betting picks
  - L3: Perplexity generated 5 picks ($0.0005)
  - L4: TTS text cleaned (1183→1161 chars), ElevenLabs audio ($0.35)
  - L5: Pillow placeholder (free)
  - L6: Video assembled with text overlays (12.1 MB, 94s)
  - **Total cost: ~$0.35**
- **Bug fixed**: L5 `media_generation.py` wasn't passing `generated_content` to packages
  - Added `'script_text'` and `'generated_content'` fields to `create_media_package()`
  - L6 now correctly renders 5 positioned text overlays for picks
- **All preset-driven features working**:
  - ✅ L3 uses preset's `preferred_model` (Perplexity) + `prompt_template`
  - ✅ L4 applies TTS text cleaning rules from preset
  - ✅ L6 uses `display_mode: text_overlay` from preset
  - ✅ L6 parses and renders listicle items with staggered timing

### Recent Changes (Dec 16, 2025 - Session 22)
- **L3 preset-driven content generation** ✅:
  - Integrated `AIModelCaller` into `idea_creation.py`
  - Added `generate_from_preset()` method for preset-driven generation
  - When `--content-preset` has `prompt_template`, L3 now uses:
    - Preset's `preferred_model` (Perplexity, Gemini, etc.) instead of hardcoded OpenAI
    - Preset's `prompt_template` for content generation
  - Preset-generated content auto-approves (saves to `ideas_approved.json` directly)
  - Standard segment-based generation unchanged (still uses OpenAI + trends)
- **Usage**:
  ```bash
  # Preset-driven generation (uses Perplexity + prompt_template)
  python3 scripts/idea_creation.py --content-preset best_bets_slate --no-checkpoint

  # Standard segment-based generation (uses OpenAI + trends)
  python3 scripts/idea_creation.py regular_season week16 --no-checkpoint
  ```

### Recent Changes (Dec 16, 2025 - Session 21)
- **End-to-end preset flow test** ✅:
  - Tested L3→L4→L5→L6 pipeline with `content_preset=best_bets_slate`
  - **Bug fixed**: `media_generation.py` wasn't passing `content_preset` to packages
    - Added `'content_preset': idea.get('content_preset')` to `create_media_package()`
  - **MoviePy upgraded**: 1.0.3 → 2.2.1 (required for direct imports)
  - Test cost: ~$0.14 (ElevenLabs TTS)
- **Verified working**:
  - ✅ L3: `--content-preset` flag stores preset in idea metadata
  - ✅ L4: TTS text cleaning applied ("TTS text cleaned" shown)
  - ✅ L5: `content_preset` now passed through to media packages
  - ✅ L6: Detects display_mode from content preset
- **Gap identified**: L3's `--content-preset` flag only sets metadata for downstream layers
  - It does NOT use the preset's `prompt_template` for content generation
  - For actual betting picks content, use `best_bets_workflow.py` (which does use Perplexity + prompt)
  - Future: L3 could use `prompt_template` when content preset specified

### Recent Changes (Dec 16, 2025 - Session 20)
- **ADR-014 Implementation COMPLETE** ✅:
  1. ✅ Added new fields to content_presets (`display_mode`, `voice_preset`, `visual_style`, `pacing_preset`, `tts_text_processing`)
  2. ✅ Added text overlay mode to `assembly.py`:
     - ImageMagick binary config for MoviePy TextClip
     - `get_content_preset_settings()` in AssemblyPresetManager
     - `_add_positioned_text_overlays()` for picks/listicles
     - `_parse_listicle_items()` helper
     - Display mode routing in `assemble_video()`
  3. ✅ Updated `audio_sync.py` for TTS text processing:
     - `get_tts_text_processing_rules()` - loads regex rules from preset
     - `apply_tts_text_processing()` - cleans text before TTS (e.g., `-110` → `minus 110`)
     - Auto-applies rules when `content_preset` set in idea metadata
  4. ✅ Updated `idea_creation.py` with `--content-preset` flag:
     - `--content-preset best_bets_slate` controls full L3-L6 pipeline
     - `--list-presets` shows available content presets
     - `get_content_preset()` and `get_all_content_presets()` methods added
  5. ✅ Content preset name stored in idea metadata (`idea['content_preset']`)
  6. ✅ Integration tests passed - preset flow verified L3 → L4 → L6
- **Usage**:
  ```bash
  python3 scripts/idea_creation.py --list-presets  # Show available presets
  python3 scripts/idea_creation.py --content-preset best_bets_slate  # Use preset
  ```

### Recent Changes (Dec 16, 2025 - Session 19)
- **ADR-014: Preset-Driven Workflow Architecture** documented in CODE_HISTORY.md:
  - Content presets control full L3-L6 production chain
  - Vision layer can override any preset setting
  - Hierarchy: Vision → Content Preset → User Overrides → System Defaults

### Recent Changes (Dec 16, 2025 - Session 18)
- **Best Bets workflow created** ✅ (`scripts/best_bets_workflow.py`):
  - Standalone script bypassing segment-based pipeline
  - Perplexity API for real-time 5 betting picks (~$0.001)
  - Pexels stock image or Pillow placeholder (free)
  - ElevenLabs TTS narration (~$0.44)
  - Text overlays (not subtitles) with staggered appearance
  - Output: `output/best_bets/[timestamp]/best_bets_video.mp4`
- **Dependencies installed**: ImageMagick (via Homebrew), mutagen
- **Test output**: 7.1 MB video, 122s, 1080x1920, 5 picks displayed
- **Pending improvements for next session**:
  1. Add ImageMagick config to workflow script
  2. Fix prompt for accurate current data (e.g., Kupp now on Seahawks)
  3. Adjust text font/colors for readability against background
  4. Change voice to be less robotic, don't speak syntax
  5. Integrate into established L3-L6 workflow for future flexibility
  6. Add image animation capability

### Recent Changes (Dec 16, 2025 - Session 17)
- **Full pipeline test (L1-L6)** ✅:
  - Ran complete test producing one piece of content
  - L1: Tavily web search - 20 results → websearch_trends.json
  - L2: Calendar config → week15 folder structure created
  - L3: Idea creation - generated 16 ideas, approved 1 (Bad Beats Monday)
  - L4: Audio generation - ElevenLabs TTS → idea_001.mp3 ($0.17)
  - L5: Media generation - FAL.AI balance exhausted, created Pillow placeholder
  - L6: Video assembly - MoviePy assembled → idea_001_vertical.mp4 (11.2 MB, 44s)
  - **Total cost**: ~$0.19 (Tavily ~$0.01, GPT ~$0.01, ElevenLabs $0.17)
- **Issues discovered**:
  - Wrong content type: Generated "Bad Beats Monday" instead of "Best Bets" picks
  - Used subtitles (word-by-word captions) instead of text overlay with 5 bets
  - Need free image tool (FAL exhausted)
- **Dependencies installed**: elevenlabs SDK, fal-client, pillow, moviepy
- **Output folder**: `content/nfl/2025-2026/regular_season/week15/`

### Recent Changes (Dec 16, 2025 - Session 16)
- **Best Bets content preset** ✅:
  - Added `content_presets` section to `config/script_presets.json`
  - `best_bets_game` - 5 picks for specific game with web context
  - `best_bets_slate` - Top picks across full slate
  - Prompt templates with `{game_matchup}` and `{web_context}` placeholders
- **Multi-model AI caller** ✅ (`scripts/ai_models.py`):
  - `AIModelCaller` class with unified interface for OpenAI, Perplexity, Gemini
  - `call()` - direct model call with cost tracking
  - `call_with_fallback()` - tries preferred model, falls back if unavailable
  - `get_best_bets_analysis()` - uses preset template
- **Perplexity API integrated** ✅:
  - `sonar` model with real-time web search and citations
  - Dramatically better quality than GPT-4o-mini for betting analysis
  - Cost: ~$0.0005 per analysis
- **AI models config** added to `script_presets.json`:
  - gpt-4o-mini, gpt-4o, gemini (pending key), perplexity
  - Cost estimates, strengths/weaknesses per model
- **IDEAS_BACKLOG.md updated** with YES tier items:
  - Intelligent tagging system (links to L8 analytics)
  - Poll generation capability
  - Gemini/Perplexity integrations
  - Midjourney/Hailuo AI research

### Recent Changes (Dec 14, 2025 - Session 15)
- **assembly.py refactored** ✅:
  - `assemble_video` function reduced from 241 lines → 40 lines (orchestrator)
  - Extracted 6 helper methods: `_load_audio_for_assembly`, `_create_background_clip`, `_create_image_sequence`, `_load_video_background`, `_add_text_overlay_clips`, `_render_final_video`
  - UX unchanged - all print statements and user messages preserved
  - Syntax verified, ready for testing
- **media_generation.py reviewed** ✅:
  - Already well-structured with helper extraction
  - 140-line checkpoint function is intentional UX pattern (per UX_RULES.md)
  - No refactoring needed
- **Module optimization complete** - Both L5/L6 scripts reviewed

### Recent Changes (Dec 8, 2025 - Session 14)
- **Python3 standardization** ✅:
  - All documentation now uses `python3` instead of `python`
  - Added Session Rule 9 (Python3 Rule) to both context files
  - Updated: README.md, ORACLE_README.md, WORKFLOW.md, ARCHITECTURE.md, both context files
- **Detailed Docs Update Protocol** ✅:
  - Added clear guidance on when to pull vs update detailed docs
  - Table mapping change types to affected docs
  - Checklist for doc updates after significant changes
  - Session Rule 10 added to ORACLE_CONTEXT.md
- **Context auto-update feature** ✅:
  - `ContextAutoUpdater` class added to `project_oracle.py`
  - Autosave now auto-appends file changes to Recent Changes section
  - Detects active session (dev/maintenance) by context file mtime
  - Session Rule 8 added: Context docs are Claude's memory, fully auto-managed
  - User no longer needs to manually maintain context docs - Claude handles all updates
- **Compaction risk indicator enhanced** ✅:
  - Now displays both qualitative level AND percentage (e.g., "Low (17%)")
  - `_get_compaction_risk()` returns dict with `percent`, `level`, `display` fields
  - Percentage 0-100% maps to thresholds: Low (<33%), Medium (34-66%), High (67-89%), Critical (90%+)
- **Dashboard "ok/new" format for warnings** ✅:
  - Long functions: Shows "10 ok, 0 new" format (accepted vs new)
  - Unused imports: Added `ACCEPTED_UNUSED_IMPORTS` set to project_oracle.py
  - Both warning types now tracked with ok/new counts in `.health_status.json`
  - Accepted items visible for awareness but don't lower health score
- **Dashboard readability improvements** ✅:
  - Added blank row before OPTIMIZATIONS and FILES WATCHED panels
  - Visual separation between code/docs metrics and utility panels
- **Session detection refresh** ✅:
  - Added manual session type toggle hotkeys: `d` (dev), `t` (maintenance), `0` (auto)
  - Dashboard shows "(manual)" indicator when override is active
  - User can now instantly switch session type without waiting for file changes
- **ORACLE_README.md documentation** ✅:
  - Added "Dashboard Panels" table documenting all panel information
  - Added "Acceptance Lists" section explaining ok/new tracking system

### Recent Changes (Dec 8, 2025 - Session 12)
- **Fixed false positive "documentation may need updating"** ✅:
  - Oracle now compares current state against session baseline (from `audit --quick`)
  - Only shows suggestions for files that **actually changed** during session
  - No more spurious doc update suggestions on autosave
- **Health monitor mode persistence** ✅:
  - Mode preference now saved to `maintenance/health_monitor_config.json`
  - Switch mode once with hotkey (f/c/s/m), starts in that mode next time
  - Truly "set and forget" - run once, never configure again
- **Clarified health monitor session compatibility**:
  - Works automatically for both dev AND maintenance sessions
  - Session-agnostic design - just run it in a dedicated terminal

### Recent Changes (Dec 8, 2025 - Session 11)
- **Oracle Health Monitor FULLY IMPLEMENTED** ✅ (`maintenance/health_monitor.py`):
  - **Phase 1**: Core dashboard with `rich` library - full/compact/split/minimized modes
  - **Phase 2**: File watching with `watchdog` library - monitors context/, scripts/, config/, docs/
  - **Phase 3**: Alerts & automation - keyboard input (termios/tty), escalating reminders
  - **Phase 4**: Oracle integration - writes `reports/.health_status.json` for real-time data
  - Dependencies: `pip install rich watchdog`
  - Usage: `python3 maintenance/health_monitor.py [--mode full|compact|split|min]`
- **Comprehensive documentation update** ✅:
  - Updated WORKFLOW.md with health monitor section and terminal layout
  - Added ADR-011 (Health Monitor), ADR-012 (Optimization System) to DECISIONS.md
  - Updated all timestamps, cross-references, and file structures

### Recent Changes (Dec 8, 2025 - Oracle Session 8)
- **Optimization Awareness System** ✅ - 30/70 hybrid detection:
  - Created `optimization/` folder with `OPTIMIZATION_LOG.md`, `IDEAS_BACKLOG.md`, `reports/`
  - Added `OptimizationDetector` class to oracle (~250 lines)
  - New `optimize` command with `--report` and `--log` flags
  - `audit --quick` and `autosave` now show optimization summaries
  - Added 🎯 Optimization Awareness sections to both context files
- **Future Planning consolidated** ✅:
  - All Future Planning content migrated to `optimization/IDEAS_BACKLOG.md`
  - Original sections in ORACLE_CONTEXT.md, PHILOSOPHY.md, DECISIONS.md, ARCHITECTURE.md now point to IDEAS_BACKLOG.md
  - Tiers: YES (approved), MAYBE (considering), NO (rejected), UNREVIEWED

### Recent Changes (Dec 8, 2025 - Oracle Session 4)
- **Oracle fixes** ✅:
  - Created `docs/CHANGELOG.md` (was referenced but missing)
  - Fixed health score calculation - warnings now capped at -3 points (was tanking score)
  - Added `PLANNED_FILES` list - future agent context files flagged as "info" not "critical"
  - Added `PLANNED_SCRIPTS` list - future scripts don't trigger warnings
  - Script reference checker now recognizes `maintenance/*.py` paths
  - Cross-reference checker now checks `context/` folder
- **File cleanup** ✅ - Keeps only last 5 of each:
  - `ORACLE_REPORT_*.md` - audit reports
  - `SNAPSHOT_*.md` - context snapshots
  - `SESSION_DIFF_*.md` - diff reports
- **Health improved**: 🟢 7.6/10 (0 critical, 24 warnings)
- **Documentation added**:
  - "How Oracle Works" section in ORACLE_README.md (execution model, automation flow)
  - Section 4.6-4.7 in WORKFLOW.md (automation flow, background monitor future spec)
  - Future Planning expanded in ORACLE_CONTEXT.md (background monitor, package architecture)

**Session 13 Status:**
- ✅ Reports subfolders created (audits/, diffs/)
- ✅ Oracle cross-session sync working
- ⏳ Manual module review (assembly.py, media_generation.py) - NEXT
- 📋 Automated pytest tests - deferred until after module optimization

### December 8, 2025 - Session 10
- **Oracle Health Monitor Phase 3-4 implemented**:
  - Phase 3: Alerts & Automation
    - `KeyboardReader` class for non-blocking keyboard input (termios/tty)
    - Escalating autosave reminders (gentle → nudge → urgent → critical)
    - `_check_alerts()` and `_handle_alert()` for alert management
    - Terminal bell alerts, macOS notifications for critical events
    - Hotkey handling now fully functional (a/h/o/f/c/s/m/r/?/q)
  - Phase 4: Oracle Integration
    - Oracle now writes `reports/.health_status.json` after audits/status checks
    - `write_health_status()` function in project_oracle.py
    - Health monitor reads real health score, issues, optimizations
    - Added `get_total_count()` to OptimizationDetector
- **Dependencies**: `pip install rich watchdog`
- **Usage**: `python3 maintenance/health_monitor.py [--mode full|compact|split|min]`

### December 8, 2025 - Session 9
- **Oracle Health Monitor Phase 1-2 implemented** (`maintenance/health_monitor.py`):
  - Phase 1: Core dashboard with `rich` library
    - Full, compact, split, minimized display modes
    - Health score, autosave timer, pipeline status, documentation staleness
    - Code bloat panel, optimizations panel, log panel
    - Hotkey display (a/h/o/c/s/m/q)
  - Phase 2: File watching with `watchdog` library
    - `HealthMonitorEventHandler` class for file system events
    - `FileWatcher` class to manage observers
    - Watches: context/, scripts/, config/, docs/, reports/, optimization/
    - Debouncing to prevent duplicate events
    - Auto-detects snapshot creation (autosave) and health status updates
  - Dependencies: `pip install rich watchdog`
  - Usage: `python3 maintenance/health_monitor.py [--mode full|compact|split|min]`
- **Added optimization files to oracle doc tracking**:
  - `optimization/OPTIMIZATION_LOG.md` and `IDEAS_BACKLOG.md` now tracked in staleness checks
  - Added `optimization_change` category to `DOC_CHANGE_MAP`

### December 8, 2025 - Session 8
- **Optimization Awareness System implemented**:
  - Created `optimization/` folder with `OPTIMIZATION_LOG.md`, `IDEAS_BACKLOG.md`, `reports/`
  - Added `OptimizationDetector` class (~250 lines) - detects code issues, doc staleness, placeholders, cost tracking
  - New `optimize` command with `--report` and `--log` flags
  - `audit --quick` now shows optimization summary
  - `autosave` now shows optimization count
  - Added 🎯 Optimization Awareness sections to DEV_CONTEXT.md and ORACLE_CONTEXT.md
  - Updated ORACLE_README.md with new Optimization System section
- **Future Planning consolidation**:
  - Migrated all Future Planning content from ORACLE_CONTEXT.md, PHILOSOPHY.md, DECISIONS.md, ARCHITECTURE.md
  - All now point to `optimization/IDEAS_BACKLOG.md`
  - IDEAS_BACKLOG.md has YES/MAYBE/NO/UNREVIEWED tiers plus Reference sections

### Recent Changes (Dec 8, 2025 - Oracle Session 3)
- **Oracle `autosave` command** ✅ - Streamlined checkpoint system:
  - Runs sync + snapshot with minimal output
  - Output: `💾 Autosaved. [health]. Snapshot: [file]`
  - Flags: `--archive-changes`, `--show-resume`
- **Oracle `audit --quick` now creates silent baseline** ✅ - Eliminates need for `diff --baseline`
- **Updated project_oracle.py paths** ✅ - All refs now use context/DEV_CONTEXT.md
- **Automation rules updated** ✅ - "Video game checkpoint" feel:
  - SESSION START: `audit --quick` (health + baseline)
  - EVERY ~10: `status` (silent unless issues)
  - EVERY ~20 / breakpoints: `autosave`
  - BEFORE COMPACTION: `autosave`

### December 8, 2025 - Session 7
- **Cross-session briefing implemented**:
  - New `CrossSessionBriefing` class in project_oracle.py
  - Auto-detects session type (dev vs maintenance) based on file access times
  - Dev session sees: oracle health findings, critical issues, maintenance changes
  - Maintenance session sees: layer changes, script modifications, task backlog
  - Shows at end of `audit --quick` output (session start)
  - New `briefing` command for standalone briefing: `python3 maintenance/project_oracle.py briefing`
  - `--session dev|maintenance` flag to override auto-detection
- Removed "Context/Oracle merge" from pending features (this IS that feature)

### Recent Changes (Dec 7, 2025 - Session 7)
- **Documentation restructured** ✅ - New organization:
  - Created `context/` folder for session state documents
  - Renamed CLAUDE_CONTEXT.md → context/DEV_CONTEXT.md
  - Created context/ORACLE_CONTEXT.md (maintenance session state)
  - Created docs/PHILOSOPHY.md (from PROJECT_OVERVIEW.md)
  - Created docs/WORKFLOW.md (operational processes, VS Code config, troubleshooting)
  - Created docs/DECISIONS.md (Architecture Decision Records)
  - Created docs/SETUP.md (placeholder)
  - Revised docs/ARCHITECTURE.md (technical only, removed philosophy overlap)
  - Revised README.md (fixed stale refs, added glossary)
  - Revised maintenance/ORACLE_README.md (user-facing only)
  - Deleted PROJECT_OVERVIEW.md (content moved to PHILOSOPHY.md)
- **Cross-session protocol added** ✅ - Dev ↔ Oracle communication documented

### December 8, 2025 - Session 6
- **Auto-archive Recent Changes**:
  - Autosave now auto-archives when sessions exceed 5 (MAX_RECENT_SESSIONS)
  - Keeps 5 most recent sessions in context file
  - Older sessions moved to CHANGELOG.md automatically
  - Manual `--archive-changes` flag still works for immediate archive
  - Output message shows "(auto-archived N old sessions)" when triggered
- **Dual context file syncing**:
  - Autosave now checks and archives BOTH DEV_CONTEXT.md and ORACLE_CONTEXT.md
  - Both files maintain max 5 sessions independently
  - Oracle works identically in both dev and maintenance sessions
- **Dynamic multi-agent support**:
  - Replaced hardcoded ORACLE_CONTEXT_FILE with CONTEXT_FILES list
  - Easy to add new agents: just add path to list and create context file
  - Autosave loops through all context files automatically

### Recent Changes (Dec 7, 2025 - Session 4)
- **Maintenance Agent (Project Oracle) created** ✅ - `maintenance/project_oracle.py`:
  - Parses DEV_CONTEXT.md as source of truth for configuration
  - Runs 5 auditors: Code, Docs, Layers, API, Context health
  - Generates optimization suggestions
  - Outputs detailed reports to `reports/ORACLE_REPORT_[timestamp].md`
  - Commands: `config -v`, `audit`, `audit --quick`, `report`, `sync --dry-run`
- **DEV_CONTEXT updated with maintenance documentation** ✅:
  - Added Project Oracle section with flow diagram
  - Added maintenance commands to Quick Commands
  - Added `reports/` and updated `maintenance/` in Special Folders

### December 8, 2025 - Session 5
- **Reports folder organization**:
  - Created `reports/audits/` for ORACLE_REPORT files
  - Created `reports/diffs/` for SESSION_DIFF files
  - Moved existing files to new locations
  - Updated all oracle paths to use new structure
- **Smart doc sync feature**:
  - Added `DOC_CHANGE_MAP` - maps change types to relevant docs
  - Added `ALL_REFERENCE_DOCS` - comprehensive list of all docs
  - Added `DocChangeDetector` class - analyzes changes and suggests updates
  - New command: `suggest-docs` - shows which docs need updating
  - New flag: `suggest-docs --staleness` - shows doc freshness
  - New flag: `autosave --suggest-docs` - combines autosave with doc suggestions
- **Documentation updated**:
  - ORACLE_README.md - new commands
  - ORACLE_CONTEXT.md - session 5 changes

### December 8, 2025 - Session 4
- **Bug fixes**:
  - Created `docs/CHANGELOG.md` (was referenced but missing)
  - Fixed health score calculation - warnings now capped at -3 points max
  - Added `PLANNED_FILES` set - future context files flagged as "info" not "critical"
  - Added `PLANNED_SCRIPTS` set - future/placeholder scripts don't trigger warnings
  - Script reference checker now recognizes `maintenance/*.py` paths
  - Cross-reference checker now checks `context/` folder
- **File cleanup**: Added `cleanup_old_files()` function
  - Keeps only last 5 `ORACLE_REPORT_*.md`, `SNAPSHOT_*.md`, `SESSION_DIFF_*.md`
  - Constants: `MAX_REPORTS = 5`, `MAX_SNAPSHOTS = 5`
- **Health improved**: 7.6/10 (was 0.0/10 due to warning penalty)
- **Documentation added**:
  - "How Oracle Works" section in ORACLE_README.md
  - Section 4.6-4.7 in WORKFLOW.md (automation flow diagram, background monitor spec)
  - Future Planning expanded (Background Health Monitor, Package Architecture)

### Recent Changes (Dec 7, 2025 - Session 3)
- **L3 preset integration COMPLETE** ✅ - ScriptPresetManager added to idea_creation.py:
  - Loads presets from config/script_presets.json (tone, format, length)
  - Integrates preset instructions into AI prompt generation
  - Adds script_preset metadata to each generated idea
  - Follows same pattern as L4 AudioPresetManager
  - script_presets.json status updated from PLACEHOLDER to ACTIVE
- **BIRDS_EYE_INPUT.md merged and deleted** ✅ - All content distributed without loss:
  - Full Bird's Eye system spec → ARCHITECTURE.md (Phase 5, comprehensive)
  - Build break checklist & recommendations → WORKFLOW.md
  - Context loss prevention strategy → WORKFLOW.md
  - UI patterns → UX_RULES.md
- **"Configurator" → "Orchestrator" rename COMPLETE** ✅ - All docs updated
- **UX_RULES.md moved to docs/** ✅ - All references updated
- **DEV_CONTEXT enhancements** ✅:
  - Added API Keys & MCPs section with status table
  - Added Preset vs Vision clarification table
  - Added Good Compaction Points section
  - Added Claude Desktop Offload guidance
  - Added Documentation Health Check section
  - Added DEV_CONTEXT Update Triggers section
  - Added Handling User Rejection Feedback section (prevents task loss)
  - Updated pending tasks (L3 preset before code review)

### December 8, 2025 - Session 3
- **Documentation restructure** - Moved from CLAUDE_CONTEXT.md to:
  - `context/DEV_CONTEXT.md` - Development session state
  - `context/ORACLE_CONTEXT.md` - Oracle/maintenance session state
  - `docs/PHILOSOPHY.md` - Replaced PROJECT_OVERVIEW.md
  - `docs/WORKFLOW.md` - Operational processes
  - `docs/DECISIONS.md` - Architecture Decision Records
- **Updated project_oracle.py paths** - All references now use new context/ and docs/ structure
- **NEW: `autosave` command** - Streamlined checkpoint system:
  - Runs sync + snapshot with minimal output
  - One-line result: "💾 Autosaved. [health]. Snapshot: [file]"
  - Flags: `--archive-changes`, `--show-resume`
  - No bloat check (Option A - keep it fast, ~1-2s)
- **MODIFIED: `audit --quick`** - Now silently creates baseline
  - Eliminates need for separate `diff --baseline` at session start
  - Health score stored in baseline for comparison
- **Updated automation rules** - New "video game checkpoint" feel:
  - Friendly language: "Autosaving...", "Quick health check..."
  - Simplified triggers: SESSION START, EVERY ~10, EVERY ~20, BEFORE COMPACTION

### December 7, 2025 - Session 2
- Added `snapshot` command - **recommended** for precompaction:
  - Combines current state + diff + resume prompt in single markdown file
  - Output: `reports/snapshots/SNAPSHOT_[timestamp].md`
  - Optional args: `--task`, `--file`, `--decisions`, `--blockers`
  - Auto-infers active task and last file from context
- Simplified session workflow:
  - `diff --baseline` for session start (lightweight)
  - `snapshot` for before compaction (full context)
  - Removed `--precompaction` flag (redundant with snapshot)
- Added `--prune-tasks` flag to sync command
- Detects completed tasks by: ✅ emoji, [x] checkbox, COMPLETE/DONE keywords
- Added internal diff tracking for snapshot comparison
- Added `status` command - quiet one-line health dashboard:
  - Shows: health score, critical/warning counts, task count, baseline age
  - Example: `🟢 Healthy: 8.2/10 | 0 critical | 3 warnings | 5 tasks | Baseline: 2h ago`
- Added `--archive-changes` flag to sync:
  - Moves old Recent Changes sections to `docs/CHANGELOG.md`
  - Keeps only the most recent section in DEV_CONTEXT.md
  - Creates CHANGELOG.md if it doesn't exist

### December 7, 2025 - Session 1
- Created project_oracle.py with full audit suite
- Implemented ContextParser for DEV_CONTEXT.md parsing
- Fixed layer output parsing (regex + MULTILINE flag)
- Fixed pending tasks parsing (numbered + bullet lists)
- Fixed "DEV_CONTEXT.md not loaded" bug
- Added DocSyncEngine with write capabilities
- Added sync for all 6 reference docs
- Added `--fix` mode for safe targeted updates
- Created ORACLE_README.md with session resume protocol

---

### Recent Changes (Dec 7, 2025 - Session 2)
- **L7 Distribution `--ids` filter added** ✅ - `distribution.py` now supports `--ids` filtering
- **L7 & L8 tested successfully** ✅ - All 3 test videos distributed to `universal (<60s)/` folder
- **Comprehensiveness rule added** - Documentation updates must never lose information

### Recent Changes (Dec 7, 2025 - Session 1)
- **L6 `--ids` filter FIXED** ✅ - Now properly filters packages before processing
  - `assembly.py run()` accepts `filter_ids` parameter
  - Command: `--ids idea_001 idea_002 idea_003` filters to only those packages
- **L7 Distribution optimized** - Single copy per video (no duplicates):
  - Videos MOVED (not copied) from `assembled/` to `final/`
  - Destination determined by duration:
    - ≤60s → `final/universal (<60s)/` (works on ALL platforms)
    - 61-90s → `final/instagram_reels (<90s)/`
    - 91-140s → `final/x_twitter (<140s)/`
    - 141-600s → `final/tiktok (<600s)/`
    - >600s → `final/youtube_long (no limit)/`
  - **Disk savings**: ~5x reduction (no more duplicate copies per platform)
  - `assembled/` is now a staging area (empty after L7 runs)
- **L6 Font Fix VERIFIED** ✅ - Full video assembly test completed successfully:
  - All 16 videos now render with proper text overlays
  - ✓ Hook overlays, ✓ Subtitles word-by-word, ✓ CTA overlays
  - Fix: `_create_text_clip()` detects already-resolved font paths and skips double resolution
  - Videos 13-70 MB (full quality with Ken Burns + overlays)
  - Render time: ~2.5 min/video with Ken Burns + image sequences
- **End-to-end pipeline test COMPLETED** - All L1-L8 layers run successfully
  - 16 videos generated, distributed to platform folders
  - Total cost: ~$3.26 (ElevenLabs $3.02, FAL AI images $0.24)
- **Video assembly improvements implemented**:
  - **Font fix**: `_get_font()` resolves font names to file paths
  - **Ken Burns effect**: `_apply_ken_burns()` with zoom_in, zoom_out, pan_left, pan_right, random
  - **Image sequences**: Videos cycle through all 5 AI-generated images
  - **Presets updated**: `assembly_presets.json` has `ken_burns` and `use_image_sequence` options
- **--no-checkpoint flags added** to ALL layers (L1-L8) for fully automated runs
- **Session rules documented** (see top of this file):
  - Testing: Top 3 ideas only (`--ids idea_001 idea_002 idea_003`)
  - Cost: Notify user before paid API calls
  - Compaction: Suggest good breakpoints

## [Unreleased]

### Added
- Initial project structure and documentation

---

## December 8, 2025 - Oracle Session 3

### Added
- `autosave` command - streamlined checkpoint system (sync + snapshot)
- Silent baseline creation in `audit --quick`
- New documentation structure:
  - `context/DEV_CONTEXT.md` - Development session state
  - `context/ORACLE_CONTEXT.md` - Oracle/maintenance session state
  - `docs/PHILOSOPHY.md` - Goals and principles
  - `docs/WORKFLOW.md` - Operational processes
  - `docs/DECISIONS.md` - Architecture Decision Records

### Changed
- Moved from single CLAUDE_CONTEXT.md to split context files
- Updated all oracle paths to use new structure
- Automation rules now use "video game checkpoint" terminology

---

## December 7, 2025 - Oracle Session 2

### Added
- `snapshot` command - unified context snapshot with resume prompt
- `status` command - one-line health dashboard
- `--prune-tasks` flag - remove completed tasks
- `--archive-changes` flag - move old changes to CHANGELOG.md
- Internal diff tracking for session comparison

### Changed
- Simplified session workflow (diff --baseline → snapshot)

---

## December 7, 2025 - Oracle Session 1

### Added
- Created `maintenance/project_oracle.py` with full audit suite
- ContextParser for DEV_CONTEXT.md parsing
- DocSyncEngine with write capabilities
- 5 Auditors: Code, Docs, Layers, API, Context health
- Reference doc checking for all 6 docs
- `--fix` mode for safe targeted updates
- Backup system (.backup files before writes)
- Dry-run default for preview before applying

### Fixed
- Layer output parsing (regex + MULTILINE flag)
- Pending tasks parsing (numbered + bullet lists)
- "DEV_CONTEXT.md not loaded" bug

---

*Archived changes from DEV_CONTEXT.md Recent Changes sections are appended here.*
