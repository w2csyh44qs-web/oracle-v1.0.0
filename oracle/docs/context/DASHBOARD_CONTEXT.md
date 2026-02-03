# Dashboard Context Document

> **YOU ARE DASHBOARD** - Frontend development: app/frontend/. UI/UX, React components.

**Last Updated:** January 29, 2026 (DB8c - Navigation & UX Improvements)
**Session:** DB8c

---

## CURRENT DATE & SEASON

> **Today:** January 29, 2026
> **NFL Season:** 2025-2026 (Playoffs - Conference Championship)

---

## RESUME PROTOCOL

```
you are dashboard - read DASHBOARD_CONTEXT.md
```

### Rules
1. **Scope**: Only `app/frontend/` - don't modify `app/` backend or `scripts/`
2. **Test**: Backend (5001) + Frontend (5173)
3. **API-First**: Backend exposes REST APIs, frontend consumes

### Handoffs
```
Dash → Dev: custom_preset_request, api_change_request, backend_bug
Dev → Dash: new_feature_available, preset_added, api_updated
```

---

## TECH STACK

| Layer | Technology |
|-------|------------|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | Flask (V2 app/) |
| State | React Context (Auth, App, Job) |
| Real-time | Server-Sent Events (SSE) |

**Ports:** Backend 5001 (fallback 5002), Frontend 5173 (fallback 5174)

---

## CURRENT STATE

| Phase | Status |
|-------|--------|
| Phase 1: MVP Foundation | ✅ Complete |
| Phase 2: Core Functionality | In Progress |
| Phase A: L1 Fix | ✅ Complete |
| Phase B: Tool Standardization | ✅ Complete |
| Phase C: Admin Tool Manager | ✅ Complete |
| Phase D: Enhanced Preset Builder | ✅ Complete |
| Phase E: PresetBuilder Enhancements | ✅ Complete |
| Phase F: Data Source Fix + Naming | ✅ Complete |
| Phase G: Restore Truth Prompt Wrapper | ✅ Complete |
| Phase H: Truth Gallery + PresetBuilder Integration | ✅ Complete |
| Phase I: PresetBuilder Reorganization + Truth Extension | ✅ Complete |

---

## COMMANDS

```bash
# Start servers
python3 -m app.main              # Backend (5001)
cd app/frontend && npm run dev   # Frontend (5173)
```

---

## TOOL KEY SYSTEM (V2)

| Key | Layer | Purpose | Examples |
|-----|-------|---------|----------|
| `data_source` | L1 | Data fetching | goatedbets_api (primary), balldontlie_api |
| `enrichment` | L2 | Data enrichment | sportsblaze, stats_enricher |
| `llm_query` | L3 | LLM content | perplexity, gemini, gpt-4o, carousel_script |
| `tts` | L4 | Text-to-speech | elevenlabs, openai |
| `stt` | - | Speech-to-text | whisper_api, deepgram |
| `image_gen` | L5 | Image generation | nano_banana, flux, dalle3, imagen4 |
| `animation` | L6 | Video animation | ken_burns, carousel_assembly, pil_overlay |
| `music` | - | Background audio | suno_api, udio_free |

**L1 Data Sources:**
- `goatedbets_api` - PRIMARY for carousel presets (props/analysis)
- `balldontlie_api` - For game schedules/scores (fallback)
- `web_search` - For discovery mode trending topics
- `manual_input` - For presets without matchup requirements (static content)
- `manual_text_input` - Text-only manual content
- `manual_image_input` - Image-based manual content
- `manual_video_input` - Video-based manual content

**Backwards Compat:** Old keys work (`model`, `tts_tool`, `image_tool`, `animation_tool`)

---

## COMPONENTS

| Component | Purpose | Status |
|-----------|---------|--------|
| `SportSelection.jsx` | Sport picker | Ready |
| `MatchupSelection.jsx` | Matchup picker | Ready |
| `PresetSelection.jsx` | Preset browser + expandable cards | Ready |
| `PresetBuilder.jsx` | Custom preset form + tool overrides + assets | Ready |
| `PresetPreview.jsx` | Live mockup | Ready |
| `GenerationFlow.jsx` | Pipeline orchestration | Ready |
| `ProgressTracker.jsx` | SSE progress | Ready |
| `AssetPicker.jsx` | G Drive asset browser | Ready |
| `TruthGallery.jsx` | Truth reference management (Admin tab) | Ready |
| `LoginPage.jsx` | Google OAuth | Ready |

---

## API ENDPOINTS

```javascript
GET /sports                    // List sports
GET /sports/:sport/matchups    // Matchups for sport
GET /presets                   // List presets
POST /presets                  // Create preset
POST /jobs                     // Create job
GET /jobs/:id/stream           // SSE progress
GET /outputs/:job_id           // List outputs

// Assets (G Drive)
GET /assets/status             // Check G Drive connection
GET /assets/list               // List assets by subfolder
GET /assets/subfolders         // List available subfolders
POST /assets/upload            // Upload asset to G Drive
POST /assets/outputs/upload    // Upload generated output

// Truth Gallery (with ref_type: visual|layout)
GET /truth/sets                    // List truth sets
POST /truth/sets                   // Create truth set
GET /truth/sets/:preset/images     // List images (query: category, ref_type)
POST /truth/sets/:preset/images    // Upload truth image (form: category, ref_type)
PUT /truth/sets/:preset/images/:id/move  // Move image (body: ref_type)
DELETE /truth/sets/:preset/images/:id    // Delete image (query: ref_type)
GET /truth/sets/:preset/directives       // Get directives (nested visual/layout)
PUT /truth/sets/:preset/directives       // Save directives (nested structure)
POST /truth/sets/:preset/extract         // AI style extraction (body: ref_type)
```

---

## G DRIVE INTEGRATION

**Config:**
- `GDRIVE_SERVICE_ACCOUNT_PATH` - Path to service account JSON
- `GDRIVE_ROOT_FOLDER_ID` - Root folder ID for assets

**Folder Structure:**
```
GoatedBets/
├── Assets/
│   ├── backgrounds/
│   ├── logos/
│   ├── overlays/
│   ├── audio/
│   └── templates/
├── Outputs/
│   └── {preset_type}/{date}/
└── Truth/
    └── {preset}/
        ├── visual/
        │   ├── yes/
        │   ├── no/
        │   └── eh/
        ├── layout/
        │   ├── yes/
        │   ├── no/
        │   └── eh/
        └── style_directives.json  # Nested: {visual: {...}, layout: {...}}
```

**Auto-Upload:** Job outputs automatically upload to G Drive on completion.

---

## COLOR SYSTEM

```css
--goat-gold: #f59e0b;      /* Primary CTAs */
--goat-purple: #8b5cf6;    /* UI elements */
--success: #22c55e;        /* Selection states */
--bg-primary: #0f1419;     /* Main background */
```

| Layer | Hex |
|-------|-----|
| L1 | #3B82F6 |
| L3 | #A855F7 |
| L5 | #10B981 |
| L6 | #F97316 |
| L7 | #EF4444 |

---

## RECENT CHANGES

### January 29, 2026 (DB8c) - Navigation & UX Improvements
- **Enhanced Navigation System**
  - Added Home button (🏠) to header navigation across all pages
  - Added icons to all nav buttons: 🖼️ Gallery, 📅 Schedules, ⚙️ Admin
  - Home button calls `resetSelection()` and returns to media engine start
  - Improved visual consistency with flexbox layout and icon styling
- **Job-Based Workflow Skip Link**
  - Added "Skip to Presets →" link on Sport Selection page
  - Allows users to bypass sport/matchup selection for non-matchup content
  - Useful for manual input presets (banners, promos, static content)
- **Logo Overlay Opt-In System**
  - Logo overlay now OPT-IN instead of default in L6 assembly
  - Added Branding section to PresetBuilder with checkbox + dropdown
  - Logo options: Main_Logo, Logo_Sticker, Logo_Sticker_2
  - L6 `_resolve_logo_path()` method checks `package['logo']` or `settings['logo']`
- **Authentication Fix for Preset Visibility**
  - Removed `dev_user` fallback that caused string/integer user_id mismatch
  - Fixed `get_current_user_id()` to properly retrieve user from session token
  - User-created presets now correctly appear in preset list
- **L6 Carousel Assembly Fix**
  - Fixed routing for carousels without `has_reels` flag
  - Added dedicated path at lines 2804-2816 for non-reels carousels
  - Prevents fallthrough to video assembly which was causing failures
- **Future Architecture Plans**
  - Phase 1 (3-4 weeks): Reliability fixes - exception handling, validation, retry logic, thread safety
  - Phase 2 (3-4 weeks): Preview architecture - RecordRTC + html2canvas for Google AI Studio-like workflow
- **Files Modified:**
  - `app/core/pipeline/layers/_L6/L6_assembly.py` - Carousel routing, logo opt-in, _resolve_logo_path()
  - `app/frontend/src/components/PresetBuilder.jsx` - Logo UI (checkbox + dropdown)
  - `app/frontend/src/App.jsx` - Home button with icons, goHome() function
  - `app/frontend/src/styles/App.css` - Nav icon styling, home button colors
  - `app/frontend/src/components/SportSelection.jsx` - Skip link to presets
  - `app/frontend/src/components/SportSelection.css` - Skip section styling
  - `app/api/routes/presets.py` - Authentication fix, removed dev_user fallback

### January 18, 2026 (DB8b) - Manual Input Support
- **Manual Input Data Sources for Matchup-less Presets**
  - Added `manual_input`, `manual_text_input`, `manual_image_input`, `manual_video_input` to L1
  - Presets like "IG App Info Banner" can now run without matchup selection
  - L1 returns `NormalizedMatchup` with manual data instead of calling APIs
- **L1 Data Source Resolution Chain**
  - Fixed `_resolve_tool()` to check all code paths for manual input detection:
    1. Explicit L1_tool override
    2. Flat data_source field (after job_service flattening)
    3. Nested tools.data_source field
    4. Default to goatedbets_api
- **Frontend Manual Input Detection**
  - Added `isManualInputPreset()` helper in GenerationFlow.jsx
  - Skips matchup requirement for manual input presets
  - Shows "Manual Input (No matchup required)" in review UI
- **AI Preset Generation Guidance**
  - Updated ai_preset_service.py system prompt with "Data Source Selection Rules"
  - AI now correctly selects manual_input for non-matchup content
- **PresetBuilder Sync Fix**
  - Syncs `api_source` with `tools.data_source` when AI generates preset
  - Prevents mismatch between form state and generated config
- **Files Modified:**
  - `app/core/pipeline/layers/_L1/L1_data.py` - Added manual_data to DataContext, _fetch_manual_input(), fixed _resolve_tool()
  - `app/core/pipeline/adapters/l1_adapter.py` - Pass manual_data to DataContext
  - `config/tool_config.json` - Added manual_input options to data_source
  - `app/frontend/src/components/GenerationFlow.jsx` - isManualInputPreset() helper
  - `app/api/routes/jobs.py` - Pass manual_data through job config
  - `app/services/job_service.py` - Include manual_data in preset_config
  - `app/services/ai_preset_service.py` - Data source selection rules in prompt
  - `app/frontend/src/components/PresetBuilder.jsx` - Sync api_source with tools.data_source

### January 18, 2026 (DB8a) - Dashboard Sync & Tool Manager
- **Mouse-based drag-drop for Admin Tool Manager**
  - Replaced HTML5 drag API with mouse events (trackpad-friendly)
  - Supports cross-category moves AND within-category reordering
  - Uses `document.elementsFromPoint()` for drop target detection
- **Tool Integration Status Indicators**
  - Green ✓ for integrated tools, Gray ○ for non-integrated
  - Dashed border + reduced opacity for non-integrated
  - TOOL_METADATA in admin.py now has `integrated` field
- **Preset Generate/Discovery Tabs**
  - Added category filter in PresetSelection.jsx
  - Backend enriches presets with category field
- **Tool Config Updates**
  - Animation default changed to `rife_local`
  - Added ComfyUI, AnimateDiff, RIFE documentation
- **Removed Tool Reference section** from AdminPresetsReference.jsx
- **Files Modified:**
  - `AdminToolManager.jsx` - Complete drag-drop rewrite
  - `AdminToolManager.css` - Integration badges, drop indicators
  - `admin.py` - Added `integrated` to TOOL_METADATA
  - `tool_config.json` - animation.selected = rife_local

### January 8, 2026 (DB7) - Phase I Complete
- **Phase I: PresetBuilder Reorganization + Truth Extension**
  - I.D: Truth Extension Backend - Visual/Layout ref_type dimension
    - New folder structure: `Truth/{preset}/{ref_type}/yes|no|eh/`
    - Updated truth_service.py with ref_type parameter for all methods
    - Updated truth.py routes with ref_type query/body params
    - Nested directives schema: `{visual: {...}, layout: {...}}`
  - I.A: Quick/Advanced Mode Toggle
    - Added builderMode state with localStorage persistence
    - Mode toggle UI in PresetBuilder header
    - Advanced-only: Visual Reference, Layers, Tool Overrides
  - I.B/I.C: Section Reordering + Video Config
    - Added Video Settings section for video/animation output types
    - Duration, Pacing, Platform, Voice Preset fields
    - L4 layer suggestion for video content
    - Combined Data Source + Aspect Ratio side-by-side
- **Phase G/H Complete:** Truth Gallery + PresetBuilder Integration
  - TruthGallery.jsx with Visual/Layout tabs
  - Truth picker in PresetBuilder with drag-drop upload
  - Full truth management API with ref_type support
- **Files Modified:**
  - `app/services/truth_service.py` - ref_type dimension
  - `app/api/routes/truth.py` - ref_type params
  - `app/frontend/src/services/api.js` - refType params
  - `app/frontend/src/components/TruthGallery.jsx` - Visual/Layout tabs
  - `app/frontend/src/components/TruthGallery.css` - Tab styling
  - `app/frontend/src/components/PresetBuilder.jsx` - Mode toggle, video config
  - `app/frontend/src/components/PresetBuilder.css` - New section styling

### January 8, 2026 (DB6)
- **Phase F Complete:** Pipeline Data Source Fix + Naming Consistency
  - F.1: Created BalldontLie REST API service as fallback data source
  - F.2: Props enrichment deferred
  - F.3: Carousel presets use `goatedbets_api` for L1 (primary)
  - F.4: Renamed "illustrated" → "sketch" throughout codebase
  - F.5: Synced database preset names with all layer tools (L1-L6)
  - F.6: Cleaned stale cache files
- **L1 Data Sources:**
  - `goatedbets_api` = PRIMARY for carousel presets (props/analysis)
  - `balldontlie_api` = FALLBACK for game schedules/scores
- **Fallback Chain:** L1 tries goatedbets_api → balldontlie_api on failure
- **Preset Renames:**
  - `carousel_illustrated` → `carousel_sketch`
  - `illustrated_insights_carousel` → `sketch_insights_carousel`
  - `carousel_illustrated_pil` → `carousel_sketch_pil`
- **DB Presets Updated:** All system presets now have L1-L6 tools in `tools` object
- **PresetSelection:** Expanded cards show L1-L6 tools with layer prefixes

### January 8, 2026 (DB5)
- **Phase E Complete:** PresetBuilder enhancements
  - E.1: Tool override dropdowns in PresetBuilder
  - E.2: Clarified aspect ratio fields
  - E.3: G Drive asset integration (AssetPicker component)
  - E.4: Removed redundant audio checkbox
  - E.5: Added "Animation" output type
  - E.6: Expandable preset cards in PresetSelection
- **G Drive Service:** `gdrive_service.py` with service account auth
- **Assets API:** New `/assets/*` endpoints for browse/upload
- **Auto-Upload:** Job outputs auto-upload to G Drive on completion
- **Pipeline Fixes:**
  - Orchestrator now stops on adapter `success=False` (not just exceptions)
  - L5 validates cached data matches expected matchup/preset
  - Prevents stale cache from wrong matchup being used

### January 8, 2026 (DB4)
- Phase A Fix: job_service.py flattens tools, L1_data.py smart matchup default
- Phase B Standardization: New tool keys

### Earlier Sessions
- DB3: Context trimmed, cross-session handoffs
- DB2: PresetPreview component, server stability
- DB1: Dashboard scaffolding complete

---

## MANUAL INPUT PRESETS

**Purpose:** Support content creation without matchup requirements (e.g., "IG App Info Banner", promotional content, static graphics).

**Data Flow:**
```
1. User creates/selects preset with data_source=manual_input
2. GenerationFlow detects manual input → skips matchup selection
3. Job submitted with manual_data in config
4. job_service flattens tools → preset_config.data_source
5. L1Adapter passes manual_data to DataContext
6. L1_data._resolve_tool() detects manual input → returns _fetch_manual_input()
7. NormalizedMatchup created from manual_data without API calls
```

**Detection Logic (L1_data.py `_resolve_tool()`):**
```python
# Priority order:
1. Explicit L1_tool override
2. Flat data_source field (post-flattening)
3. Nested tools.data_source field
4. Default: goatedbets_api

# Manual input check at each level:
if tool_name.startswith('manual'):
    return 'manual_input'
```

**Frontend Helper (GenerationFlow.jsx):**
```javascript
const isManualInputPreset = (preset) => {
  const ds = preset?.tools?.data_source || preset?.api_source;
  return ds?.startsWith('manual') || false;
};
```

**Key Files:**
- `L1_data.py` - Manual input handler, tool resolution
- `l1_adapter.py` - Pass manual_data to DataContext
- `GenerationFlow.jsx` - Skip matchup for manual presets
- `PresetBuilder.jsx` - Sync api_source with tools.data_source

---

## PIPELINE CACHE VALIDATION

**Problem Solved:** Pipeline was using cached `ideas_approved.json` from different matchups/presets.

**Fix:**
1. `orchestrator.py` checks `AdapterResult.success` and stops on failure
2. `L5_media.py` validates cached data matches expected matchup/preset
3. Mismatched cache is rejected, forcing L3 to regenerate

**Key Files:**
- `app/core/pipeline/orchestrator.py` - Lines 289-304 (adapter success check)
- `app/core/pipeline/layers/_L5/L5_media.py` - `load_ideas_with_audio()` validation
- `app/core/pipeline/adapters/l5_adapter.py` - Passes matchup/preset to L5

---

## CROSS-SESSION FLAGS

**Status:** _(none)_

---

*Dashboard Context - Frontend development source of truth*
