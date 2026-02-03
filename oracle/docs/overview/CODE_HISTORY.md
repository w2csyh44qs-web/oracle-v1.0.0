# Code History

> Technical decisions, design evolution, and rejected approaches.
> For project goals and principles, see PHILOSOPHY.md.

**Last Updated:** January 7, 2026 (O92 - V2 Docs Overhaul)
**Session Count:** D102 (Dev), O92 (Oracle), C12 (Crank), P21 (Pocket), DB3 (Dashboard)

> **Note:** P18 (O85) renamed main scripts: `content_pipeline.py` → `L0_pipeline.py`, etc. Historical references below use original names as they existed at the time.

---

## Architecture Decision Records (ADRs)

### Index

| ID | Decision | Status | Date | Session | Impact |
|----|----------|--------|------|---------|--------|
| ADR-001 | 8-Layer Pipeline | Accepted | Dec 2025 | D1 | Architecture |
| ADR-002 | Vision Above Layers | Accepted | Dec 2025 | D1 | Architecture |
| ADR-003 | Preset Hierarchy | Accepted | Dec 2025 | D1 | Architecture |
| ADR-004 | Single-Copy Distribution | Accepted | Dec 2025 | D1 | Workflow |
| ADR-005 | ElevenLabs Primary TTS | Accepted | Dec 2025 | D1 | Tooling |
| ADR-006 | MoviePy for Composition | Accepted | Dec 2025 | D1 | Tooling |
| ADR-007 | Checkpoint-Based Control | Accepted | Dec 2025 | D1 | Workflow |
| ADR-008 | Context File as Source | Accepted | Dec 2025 | D3 | Documentation |
| ADR-009 | Oracle Agent | Accepted | Dec 2025 | D4, O1 | Tooling |
| ADR-010 | Separate Context Files | Accepted | Dec 2025 | D7, O3 | Documentation |
| ADR-011 | Health Monitor | Accepted | Dec 2025 | D9-D10, O7 | Tooling |
| ADR-012 | Optimization System | Accepted | Dec 2025 | D8 | Workflow |
| ADR-013 | Code History System | Accepted | Dec 2025 | O9 | Documentation |
| ADR-014 | Preset-Driven Workflow | Accepted | Dec 2025 | D19 | Architecture |
| ADR-015 | L0 Mode Selection Entry Point | Accepted | Dec 2025 | D28-D30 | Architecture |
| ADR-016 | Unified Tool Configuration (data_sources) | Accepted | Dec 2025 | D41-D42 | Architecture |
| ADR-017 | First Publishable Output (Infographic Preset) | Accepted | Dec 2025 | D47-D50 | Milestone |
| ADR-018 | Static Team Colors + Dynamic MCP Data | Accepted | Dec 2025 | O46 | Architecture |
| ADR-019 | L6 Processor Expansion (Phase 1-3) | Accepted | Dec 2025 | O52-O54 | Architecture |
| ADR-020 | Pipeline Orchestrator (O67 Platform Architecture) | Accepted | Dec 2025 | O67, D95-D97 | Architecture |
| ADR-021 | V2 Oracle Daemon + 5-Context System | Accepted | Jan 2026 | O89-O92 | Architecture |
| ADR-022 | V2 Context Consolidation | Accepted | Jan 2026 | O92 | Documentation |

---

### ADR-001: 8-Layer Pipeline Architecture

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Architecture

#### Context
Need a content automation system that can be developed incrementally, tested in isolation, and maintained by potentially multiple people.

#### Options Considered
1. **Monolithic script** - Single script handles everything
2. **3-Layer architecture** - Input, Processing, Output
3. **8-Layer pipeline** - Granular separation by function
4. **Microservices** - Fully decoupled services

#### Decision
Adopted 8-layer pipeline architecture:
1. Trend Detection
2. Calendar Configuration
3. Idea Creation
4. Audio Generation
5. Media Generation
6. Video Assembly
7. Distribution
8. Analytics

#### Rationale
- **Testability**: Each layer can be tested independently
- **Debuggability**: Issues isolated to specific layer
- **Flexibility**: Can skip/rerun individual layers
- **Maintainability**: Clear ownership boundaries
- **Extensibility**: Easy to add new layers or modify existing

#### Consequences
- More files to manage
- Need clear input/output contracts between layers
- Requires documentation of layer interactions
- Enables parallel development of different layers

---

### ADR-002: Vision System Above Technical Layers

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Architecture

#### Context
Need creative flexibility to produce different styles of content (generic, character-based, trend-informed) without duplicating the technical pipeline.

#### Options Considered
1. **Per-layer configuration** - Each layer has its own style settings
2. **Global config file** - Single config applied everywhere
3. **Vision layer above pipeline** - Creative direction informs all layers
4. **Templates per content type** - Pre-built templates for each style

#### Decision
Vision system sits above the technical layers and influences all of them.

#### Rationale
- Same technical pipeline, different creative outputs
- Toggleable visions allow experimentation
- Trend-informed visions enable organic brand evolution
- Clear separation of creative vs technical concerns

#### Consequences
- Vision metadata must flow through all layers
- Need vision registry and management
- Slightly more complex architecture
- Enables A/B testing of different creative approaches

---

### ADR-003: Preset Hierarchy System

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Architecture

#### Context
Need to balance consistency (brand voice) with flexibility (per-content customization) without requiring manual configuration for every video.

#### Options Considered
1. **Fixed presets** - Unchangeable system defaults
2. **User overrides only** - No defaults, always configure
3. **Hierarchy system** - Layered defaults with override capability
4. **AI-only** - Let AI decide everything

#### Decision
Preset hierarchy: Vision > Segment > Script Analysis > User Defaults > System Defaults

#### Rationale
- Sensible defaults reduce configuration burden
- Higher-level settings can override lower-level
- Segment type informs but doesn't restrict
- User preferences persist across sessions

#### Consequences
- Need preset config files for each layer
- Must document hierarchy clearly
- Presets are suggestions, not restrictions
- Enables both consistency and customization

---

### ADR-004: Single-Copy Distribution (No Duplicates)

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Workflow

#### Context
Initially, distribution created copies of each video for every compatible platform. This wasted significant disk space.

#### Options Considered
1. **Full copies** - Copy to each platform folder
2. **Symlinks** - Link to single source file
3. **Single copy with manifest** - One file, metadata tracks compatibility
4. **Cloud-first** - Upload directly, no local copies

#### Decision
Single copy distribution with duration-based folder routing. Videos are MOVED (not copied) to one folder based on duration. Manifest tracks platform compatibility.

#### Rationale
- 5x disk space savings
- Simpler file management
- Manifest provides all platform info needed
- Duration naturally determines platform compatibility

#### Consequences
- assembled/ becomes staging area (empty after L7)
- Must consult manifest for platform info
- Cannot have platform-specific versions (acceptable for MVP)
- Clear folder structure by duration

---

### ADR-005: ElevenLabs as Primary TTS

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Tooling

#### Context
Need high-quality text-to-speech for engaging content. Multiple TTS providers available at various price points.

#### Options Considered
1. **OpenAI TTS** - $15/1M chars, consistent but limited
2. **ElevenLabs** - $0.20/1K chars, best quality
3. **Coqui TTS** - Free/local, good but requires GPU
4. **Google Cloud TTS** - $16/1M Neural, enterprise-grade

#### Decision
ElevenLabs as primary TTS provider.

#### Rationale
- Best naturalness (MOS 4.2-4.5)
- Voice cloning capability
- Emotion control
- 82% pronunciation accuracy (vs 77% OpenAI)
- Python SDK available

#### Consequences
- Higher per-unit cost
- Dependency on external service
- Need to manage API credits
- Quality justifies cost for content focus

---

### ADR-006: MoviePy for Video Composition

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Tooling

#### Context
Need programmatic video generation and composition for automated pipeline.

#### Options Considered
1. **MoviePy** - Python-native, good for composition
2. **FFmpeg directly** - Most powerful but complex syntax
3. **Remotion** - React-based, excellent but JS
4. **OpenCV** - Low-level, best for processing

#### Decision
MoviePy for video composition with FFmpeg bundled via imageio_ffmpeg.

#### Rationale
- Pure Python (matches rest of stack)
- Good documentation
- Handles common use cases well
- FFmpeg bundled for encoding
- Active community

#### Consequences
- CPU-bound (no GPU acceleration)
- Some limitations on complex effects
- Sufficient for current needs
- Can shell out to FFmpeg for edge cases

---

### ADR-007: Checkpoint-Based User Control

**Status:** Accepted
**Date:** December 2025
**Session:** D1
**Impact:** Workflow

#### Context
Need to balance automation with user control. Fully automated risks expensive mistakes; fully manual is too slow.

#### Options Considered
1. **Full automation** - Run everything without stopping
2. **Full manual** - Approve every step
3. **Checkpoints** - Key review points with skip option
4. **Batch approval** - Review batches, not individuals

#### Decision
Checkpoint at each layer with --no-checkpoint flag for auto-mode.

#### Rationale
- Catch errors before expensive operations
- User maintains creative control
- Can skip checkpoints when confident
- Multi-user friendly (non-technical can review)

#### Consequences
- Slightly slower than full automation
- Must implement consistent checkpoint UX
- Need --no-checkpoint flag on all scripts
- Enables confidence-based automation

---

### ADR-008: DEV_CONTEXT.md as Source of Truth

**Status:** Accepted
**Date:** December 2025
**Session:** D3
**Impact:** Documentation

#### Context
Claude Code context compaction loses information. Need a way to quickly resume sessions without re-explaining the project.

#### Options Considered
1. **README only** - Single doc for everything
2. **Many small docs** - Fragmented information
3. **Context file + references** - Summary doc with links to details
4. **Database** - Structured storage

#### Decision
DEV_CONTEXT.md as session source of truth, with detailed reference docs pulled when needed.

#### Rationale
- Single file to read on resume
- Contains current state, not just static info
- References prevent duplication
- Can be updated frequently
- Human and AI readable

#### Consequences
- Must keep DEV_CONTEXT.md updated
- Risk of context file going stale
- Need discipline to update after changes
- Enables Oracle auto-configuration

---

### ADR-009: Oracle Agent for Project Health

**Status:** Accepted
**Date:** December 2025
**Session:** D4, O1
**Impact:** Tooling

#### Context
Manual code review and documentation updates are tedious and often skipped. Need automated health monitoring.

#### Options Considered
1. **Manual review only** - Scheduled human review
2. **Linter/CI** - Standard code quality tools
3. **Custom oracle agent** - Project-specific health monitoring
4. **External service** - Third-party code quality

#### Decision
Custom Oracle agent that reads DEV_CONTEXT.md for configuration and monitors code, documentation, and workflow health.

#### Rationale
- Auto-configures from existing documentation
- Project-specific checks (layers, presets, etc.)
- Runs in separate Claude Code session
- Generates actionable reports
- Supports context snapshots

#### Consequences
- Another tool to maintain
- Must keep Oracle updated as project evolves
- Enables proactive health monitoring
- Reduces manual review burden

---

### ADR-010: Separate Context Files per Session Type

**Status:** Accepted
**Date:** December 2025
**Session:** D7, O3
**Impact:** Documentation

#### Context
Development and maintenance sessions have different concerns. Mixing them in one context file creates confusion and bloat.

#### Options Considered
1. **Single context file** - Everything in one place
2. **Session-specific files** - DEV_CONTEXT.md, ORACLE_CONTEXT.md
3. **Database with views** - Structured with filtered access
4. **No context files** - Rely on chat history

#### Decision
Separate context files per session type, stored in context/ folder:
- DEV_CONTEXT.md - Development session state
- ORACLE_CONTEXT.md - Maintenance session state
- Future: CONTENT_CONTEXT.md, ANALYTICS_CONTEXT.md

#### Rationale
- Clear separation of concerns
- Each session reads only what it needs
- Scales to multiple agents
- Cross-session protocol enables communication

#### Consequences
- Multiple files to maintain
- Need cross-session communication protocol
- Cleaner per-session context
- Enables future agent expansion

---

### ADR-011: Oracle Health Monitor Architecture

**Status:** Accepted
**Date:** December 2025
**Session:** D9-D10, O7
**Impact:** Tooling

#### Context
Session rules require Claude to run oracle commands at intervals, but there's no persistent visibility into project health. Users want real-time feedback without relying solely on Claude's memory.

#### Options Considered
1. **Status bar widget** - VS Code extension showing health in status bar
2. **Popup notifications** - System notifications on health changes
3. **Dashboard in terminal** - Rich TUI running in dedicated terminal
4. **Web dashboard** - Local web server with health UI

#### Decision
Standalone Python dashboard using `rich` library, running in a dedicated VS Code terminal, reading shared state from oracle via JSON file.

#### Rationale
- Independent of Claude Code sessions
- Real-time visibility into health score, autosave timing, file changes
- Configurable display modes (full, compact, split, minimized)
- Integrates with existing oracle commands via shared `.health_status.json`
- No additional VS Code extension needed
- Cross-platform (macOS, Linux)

#### Consequences
- Requires terminal space in VS Code layout
- Additional process to run (optional but recommended)
- `watchdog` and `rich` dependencies required
- Enables proactive health management
- Escalating alerts prevent context loss

---

### ADR-012: Optimization Awareness System

**Status:** Accepted
**Date:** December 2025
**Session:** D8
**Impact:** Workflow

#### Context
Optimization opportunities (long functions, stale docs, placeholders) accumulate silently. Need systematic detection and tracking without overwhelming users with suggestions.

#### Options Considered
1. **Full automation** - Auto-fix all detected issues
2. **Report-only** - Generate reports but no tracking
3. **Hybrid 30/70** - Automated detection (30%) + Claude judgment (70%)
4. **Manual review** - User-driven optimization sessions

#### Decision
Hybrid 30/70 system: Oracle detects quantifiable patterns (30%), Claude adds context and prioritization (70%). Tracked in dedicated `optimization/` folder.

#### Rationale
- Leverages Claude's judgment for context-dependent decisions
- Quantifiable patterns (long functions, stale dates) automated
- Single source of truth for future ideas (IDEAS_BACKLOG.md)
- Source tracking ([O], [CD], [CO], [U]) enables analysis
- Non-intrusive: surfaces at natural breakpoints
- User controls disposition (accept, backlog, decline)

#### Consequences
- New `optimization/` folder structure
- Auto-updates during autosave
- Future Planning consolidated from multiple docs
- Enables pattern analysis over time
- Respects user autonomy (recommendations, not mandates)

---

### ADR-013: Code History System

**Status:** Accepted
**Date:** December 2025
**Session:** O9
**Impact:** Documentation
**Related:** ADR-008, ADR-010, ADR-012

#### Context
Architectural decisions and design discussions happen during sessions but get lost to context compaction. DECISIONS.md existed but lacked structure for discussions, rejected approaches, and session tracking.

#### Options Considered
1. **Keep DECISIONS.md** - Status quo, ADRs only
2. **Create separate HISTORY.md** - Discussions in new file, ADRs in DECISIONS.md
3. **Merge into CODE_HISTORY.md** - Single file with ADRs, discussions, rejected approaches
4. **Fully automatic extraction** - Oracle auto-creates complete ADRs

#### Decision
Merge DECISIONS.md into CODE_HISTORY.md with expanded structure:
- ADRs section (existing + new)
- Design Discussions section (technical conversations)
- Rejected Approaches section (what we didn't do and why)
- Session Reference (D#/O# mapping)

Add `suggest-code-history` command for pattern detection, but Claude completes manually (no draft system).

#### Rationale
- Single location for "why is the code this way"
- Session numbering (D#/O#) enables cross-reference
- Rejected approaches prevent repeating discussions
- Pattern detection catches forgotten decisions
- Manual completion preserves context quality (30/70 split)

#### Consequences
- DECISIONS.md deprecated (content migrated)
- New command: `suggest-code-history`
- Session headers updated with D#/O# format
- CHANGELOG.md scoped to raw facts only
- CODE_HISTORY.md becomes technical decision archive

#### Implementation Details (O10)

**Command Spec:** `suggest-code-history`
```bash
python3 maintenance/project_oracle.py suggest-code-history
```

**Pattern Matching:**
- ADR indicators: "decisions?", "decided", "chose", "selected", "went with", "architecture", "approach", "ADR"
- Discussion indicators: "considered", "debated", "discussed", "explored", "option", "tradeoff"
- Rejection indicators: "rejected", "declined", "not pursuing", "abandoned", "instead"

**Sources Scanned:**
- `context/DEV_CONTEXT.md` - Recent Changes section
- `context/ORACLE_CONTEXT.md` - Recent Changes section
- (Optimization files excluded to avoid duplicate detection)

**Health Monitor Integration:**
- `[y]` hotkey runs `suggest-code-history` command
- Added to footer in all display modes (full, compact, split)

**Design Decisions:**
- Hotkey: `[y]` for code history (not `[d]` - conflicts with session type display)
- Session numbering: D# for dev, O# for oracle (retroactively assigned)
- Draft system deferred to IDEAS_BACKLOG.md (user reviews at own pace)

---

### ADR-014: Preset-Driven Workflow Architecture

**Status:** Accepted
**Date:** December 2025
**Session:** D19
**Impact:** Architecture
**Related:** ADR-002, ADR-003

#### Context
Need to support different content types (Best Bets, Bad Beats, Player Props, etc.) with different AI models, display modes, voice styles, and visual treatments—all flowing through the same L3-L6 pipeline.

#### Options Considered
1. **Standalone scripts per content type** - Separate workflow for each (e.g., best_bets_workflow.py)
2. **Layer-level configuration** - Configure each layer independently per run
3. **Preset-driven with Vision override** - Content preset controls full pipeline, Vision can influence
4. **Template-based** - Pre-built templates with no flexibility

#### Decision
Preset-driven workflow architecture where content presets define the full production chain, with Vision layer able to influence/override preset selections.

```
HIERARCHY (top to bottom, each can override below):
┌─────────────────────────────────────────┐
│ VISION (Creative Direction)             │
│ - Brand voice, visual identity, tone    │
│ - Can override any preset setting       │
│ - Example: "Gil & Goldie" character     │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ CONTENT PRESET (Production Chain)       │
│ - AI model for content generation       │
│ - Display mode (text_overlay/subtitles) │
│ - Voice preset for TTS                  │
│ - Visual style for backgrounds          │
│ - Pacing preset for video assembly      │
│ - TTS text processing rules             │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ USER CHECKPOINT OVERRIDES               │
│ - Per-idea adjustments at each layer    │
│ - "Apply to all" option                 │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ SYSTEM DEFAULTS                         │
│ - Fallback values from config files     │
└─────────────────────────────────────────┘
```

#### Content Preset Structure
```json
{
  "best_bets_slate": {
    "name": "Best Bets - Full Slate",
    "description": "5 betting picks across NFL slate",

    // L3: Content Generation
    "preferred_model": "perplexity",
    "fallback_model": "gpt-4o-mini",
    "prompt_template": "...",
    "output_type": "betting_picks",

    // L4: Audio
    "voice_preset": "sports_authoritative",
    "tts_text_processing": "clean_syntax",

    // L5: Media
    "visual_style": "sports_dynamic",
    "image_source": "pexels",

    // L6: Assembly
    "display_mode": "text_overlay",
    "pacing_preset": "measured_pace",
    "caption_style": null
  }
}
```

#### How It Flows
1. **L3 idea_creation.py** - Reads `--content-preset best_bets_slate`
   - Uses `preferred_model` (Perplexity) for AI generation
   - Stores preset name in idea metadata
   - Output: `ideas_approved.json` with `content_preset: "best_bets_slate"`

2. **L4 audio_sync.py** - Reads idea's preset
   - Uses `voice_preset` for ElevenLabs voice selection
   - Uses `tts_text_processing` to clean syntax before TTS
   - Example: "clean_syntax" strips `**`, `[]`, formats odds naturally

3. **L5 media_generation.py** - Reads idea's preset
   - Uses `visual_style` for background generation
   - Uses `image_source` preference (Pexels, Pillow, FAL)

4. **L6 assembly.py** - Reads idea's preset
   - Uses `display_mode` to choose rendering approach:
     - `text_overlay`: Positioned text blocks (for picks, bullet points)
     - `subtitles`: Word-by-word captions (for narrative content)
   - Uses `pacing_preset` for timing

#### Vision Override Example
```json
// Vision: "Sharp Insider"
{
  "vision_id": "sharp_insider",
  "overrides": {
    "voice_preset": "confident_whisper",
    "visual_style": "dark_premium",
    "tone": "exclusive_insider"
  }
}
```
When "Sharp Insider" vision is active, these override the content preset defaults, but the preset still provides the base structure.

#### Rationale
- **Single pipeline, multiple outputs** - No code duplication
- **Granular control** - Each aspect configurable independently
- **Intelligent defaults** - Preset bundles sensible combinations
- **Vision flexibility** - Creative direction influences without rewriting presets
- **Checkpoint overrides** - User retains final control

#### Consequences
- Content presets need all layer settings defined
- Each layer script reads idea metadata for preset
- Vision system (when built) has clear integration point
- New content types = new preset, not new script
- `display_mode` field added to L6 assembly config

#### Implementation Steps
1. Add `display_mode`, `voice_preset`, `visual_style`, `pacing_preset` to content_presets
2. Add text overlay mode to assembly.py
3. Update audio_sync.py to read `tts_text_processing` for syntax cleaning
4. Update idea_creation.py to accept `--content-preset` flag
5. Store preset name in idea metadata for downstream layers
6. Add ImageMagick config to assembly.py for TextClip support

---

### ADR-015: L0 Mode Selection Entry Point

**Status:** Accepted
**Date:** December 2025
**Session:** D28-D30
**Impact:** Architecture
**Related:** ADR-001, ADR-014

#### Context
The pipeline had two content generation workflows (Discovery via Tavily, Generate via Perplexity) but no unified entry point. Users needed to know which script to run for each approach.

#### Options Considered
1. **Separate entry scripts** - Different scripts for different workflows
2. **L1 mode flag** - Add `--mode` flag to web_search_trend_detector.py
3. **L0 entry point** - New script above L1 that handles mode selection
4. **Config file routing** - Config determines which workflow runs

#### Decision
L0 entry point (`content_pipeline.py`) with mode selection menu:
- Discovery Mode → L1 (web_search_trend_detector.py) → L2 → L3 → L4+
- Generate Mode → L3 (idea_creation.py --content-preset) → L4+
- Future modes: Hybrid, Scheduled, Manual, Remix

L0 is the menu/mode selector, L1-L8 are the pipeline modules.

#### Key Features
- **Symmetric mode menus** - Both modes have same 1-4 menu structure
- **DiscoveryModePresetManager** - Parallel to GenerateModePresetManager
- **SourceConfig class** - Manages discovery sources (websearch, reddit_direct, action_network)
- **Tool Configuration** - `[t]` menu option accesses config/tool_config.json
- **discovery_presets section** - Added to script_presets.json

#### Rationale
- **Single entry point** - Users don't need to remember multiple scripts
- **Extensibility** - Easy to add future modes (Hybrid, Scheduled)
- **Consistency** - Both modes share same UX patterns
- **Preset system** - Both modes can save/load presets with tool selections

#### Consequences
- `content_pipeline.py` is L0, not L1
- `trend_detection.py` archived to `docs/archive/` (multi-source pattern preserved for reference)
- Source toggles moved into `web_search_trend_detector.py` as SourceConfig class *(later merged into tool_config.json in ADR-016)*
- All docs updated with L0 naming convention

---

### ADR-016: Unified Tool Configuration (data_sources)

**Status:** Accepted
**Date:** December 2025
**Session:** D41-D42
**Impact:** Architecture
**Related:** ADR-015

#### Context
After ADR-015 created the L0 mode selection entry point, Discovery Mode used a separate `SourceConfig` class (~118 lines) in `web_search_trend_detector.py` to manage data sources. This was redundant with `tool_config.json` which already had a tool configuration system with resolution order and fallback chains.

#### Options Considered
1. **Keep SourceConfig class** - Maintain separate data source management
2. **Merge into tool_config.json** - Add `data_sources` as a tool category with nested `source_configs`
3. **New config file** - Create `source_config.json` for data sources only
4. **Environment variables** - Configure sources via .env

#### Decision
Merge SourceConfig into tool_config.json as a new `data_sources` category:
- Rename `web_search` category to `data_sources`
- Add nested `source_configs` for per-source settings (domain filters, endpoints, time filters)
- Delete `SourceConfig` class entirely
- Use `tool_resolver.get_source_config()` for nested config lookup

#### New tool_config.json Structure
```json
{
  "data_sources": {
    "selected": "tavily_websearch",
    "fallback": "perplexity_search",
    "free_fallback": "manual",
    "options": ["tavily_websearch", "perplexity_search", "goatedbets_api", "reddit_api", "action_network"],
    "source_configs": {
      "tavily_websearch": {
        "focus_domains": ["reddit.com", "twitter.com"],
        "exclude_domains": ["espn.com", "nfl.com"],
        "time_filter": "since_sunday"
      },
      "goatedbets_api": {
        "endpoint": "https://api.goatedbets.com/api/bdl/matchup-analysis",
        "requires_matchup": true
      }
    }
  }
}
```

#### Tool Categories (Final)
| Category | Purpose | Used By | Options |
|----------|---------|---------|---------|
| `data_sources` | Where to find content/data | L1 | tavily_websearch, perplexity_search, goatedbets_api, reddit_api |
| `content_generation` | LLM for writing | L3 | perplexity, gemini, gpt-4o, gpt-4o-mini |
| `tts` | Voice generation | L4 | elevenlabs, openai, coqui |
| `image_gen` | Image creation | L5 | flux_fal, dalle3, pexels |
| `animation` | Video animation | L6 | kling_2.6, runway, ken_burns |

#### CLI Args Added
- L1: `--source tavily_websearch` (web_search_trend_detector.py)
- Per-layer tool view in L0 now shows L1 with `--source` CLI arg

#### Rationale
- **Consistency** - All tools configured in one place
- **Resolution order** - Data sources now use same CLI > Preset > Config > Fallback chain
- **Updatability** - Claude Desktop can update TOOLS_REFERENCE.md → oracle updates tool_config.json defaults
- **Simplicity** - ~118 lines of SourceConfig class deleted
- **Preset simplification** - Discovery presets no longer need nested `sources` structure

#### Consequences
- `SourceConfig` class deleted from `web_search_trend_detector.py`
- `tool_resolver.get_source_config(source_name)` added for nested config lookup
- Discovery presets simplified (data source config is global, not per-preset)
- Tool config UI updated: `display_config()` shows `data_sources`, `_show_all_tools_view()` option 1 is "Data Sources"
- Per-layer tool view extended to include L1

#### Implementation Steps (Task #17)
1. ✅ Update `tool_config.json`: Replace `web_search` with `data_sources`, add `source_configs`
2. ✅ Update `tool_resolver.py`: Add `get_source_config()` method
3. ✅ Delete `SourceConfig` class from `web_search_trend_detector.py`
4. ✅ Update `__init__` to use `tool_resolver.resolve_tool('data_sources')`
5. ✅ Update `content_pipeline.py`: Replace all `web_search` refs with `data_sources`
6. ✅ Add L1 to per-layer tool view with `--source` CLI arg
7. ✅ Add `--source` CLI arg to `web_search_trend_detector.py`
8. ✅ Simplify discovery presets in `script_presets.json`
9. ✅ Update tests: `web_search` → `data_sources`, add `TestGetSourceConfig`

---

### ADR-017: First Publishable Output (Infographic Preset)

**Status:** Accepted
**Date:** December 2025
**Session:** D47-D50
**Impact:** Milestone
**Related:** ADR-014, ADR-016

#### Context
After 50 dev sessions building the content automation pipeline, the first production-quality output was achieved: betting infographics generated via API data, AI image generation, and smart text processing.

#### Journey to First Output

**Key Challenges Solved:**

1. **Text Rendering (D47)**: Imagen 4 produced garbled/unreadable text
   - **Solution**: Switched to Nano Banana Pro (`gemini-3-pro-image-preview`) via multimodal chat API
   - **Lesson**: Different AI image models excel at different use cases

2. **Visual Clutter (D48)**: Single infographic was cramped with competing focal points
   - **Solution**: Split into 2 images (Best Bet + Prediction)
   - **Lesson**: Multiple focused outputs > one crowded output

3. **Text Cutoff (D48-D50)**: API insights truncated mid-sentence or lost valuable analysis
   - **Solution**: `shorten_insight()` function with smart clause breaking + key term highlighting
   - **Implementation**: 25-word cap, break at natural clauses (`, forcing`, `, causing`), bold football terms

4. **Team Colors (D49)**: Hardcoded colors didn't scale
   - **Solution**: Global `config/team_colors.py` with 256 teams across 8 leagues
   - **Lesson**: Build shared configs early

#### Technical Stack (First Output)

| Layer | Tool | Cost |
|-------|------|------|
| L3 | GoatedBets API | Free (internal) |
| L5 | Nano Banana Pro (`gemini-3-pro-image-preview`) | ~$0.13-0.15/image |
| L6 | Ken Burns animation (planned) | Free |

#### Output Artifacts

```
content/nfl/2025-2026/regular_season/week16/media/idea_001/
├── infographic_best_bet.png (740 KB)
│   └── Main prop bet + "Why This Hits" bullets + bonus props
└── infographic_prediction.png (790 KB)
    └── Team edges (25 words max, key terms bolded) + predicted winner
```

#### Key Decisions Made

1. **Use-case-based tool selection**: Same category (image_gen) uses different tools:
   - Nano Banana Pro for text-heavy infographics
   - Imagen 4 for photorealistic images
   - Pexels for stock fallback

2. **Smart text processing over truncation**: Preserve meaning, highlight key terms
   - Key terms: safety rotations, check-downs, air yards, defensive line stunts, etc.
   - Clause breaking: Natural sentence breaks, not arbitrary word limits

3. **Output Review Rule established**: Claude reads generated images directly to iterate on quality

#### Rationale
This milestone validates the preset-driven architecture (ADR-014) end-to-end. The infographic preset demonstrates:
- API data → AI processing → visual output
- Quality control via Claude's image reading capability
- Iterative refinement (4 sessions to get it right)

#### Consequences
- First publishable content type available
- Pattern established for future presets
- Team colors config reusable for all sports content
- Output review workflow proven effective
- 50 sessions = foundation built, production begins

#### Lessons for Future Presets
1. Test with multiple matchups (not just one)
2. Start with split outputs (focused) over combined (cluttered)
3. Use Claude's image viewer for rapid iteration
4. Build shared configs (colors, styles) before scaling

---

### ADR-018: Static Team Colors + Dynamic MCP Data

**Status:** Accepted
**Date:** December 2025
**Session:** O46
**Impact:** Architecture
**Related:** ADR-016, ADR-017

#### Context
With balldontlie MCP integration (configured in `~/.claude.json`), question arose: should we restructure `config/team_colors.py` to pull team data from the API instead of maintaining a hardcoded list?

#### Current Architecture

| Data Type | Source | Rationale |
|-----------|--------|-----------|
| Team Colors | `config/team_colors.py` (static) | Brand assets don't change |
| Team Names/IDs | balldontlie MCP (dynamic) | Live roster data |
| Player Info | balldontlie MCP (dynamic) | Stats, positions, injuries |
| Game Data | balldontlie MCP (dynamic) | Schedules, scores, odds |

#### Options Considered
1. **Full API migration** - Pull everything from balldontlie
2. **Hybrid with API colors** - Fetch colors if available from API
3. **Keep separate (chosen)** - Static colors + dynamic API data

#### Decision
**Keep `config/team_colors.py` as the source of truth for team colors.** balldontlie MCP provides live data (teams, players, games) but does NOT provide color data. The two systems are complementary, not redundant.

#### Rationale
- **Colors are static brand assets** - NFL team colors don't change mid-season
- **balldontlie doesn't provide colors** - API covers stats/rosters, not branding
- **Already working well** - 256 teams across 8 leagues in `team_colors.py`
- **Separation of concerns** - Visual styling (local) vs live data (API)
- **No restructuring overhead** - System works, don't fix what isn't broken

#### Consequences
- `config/team_colors.py` remains the source for `get_team_colors()` and `get_matchup_colors()`
- balldontlie MCP used for: `get_teams`, `get_players`, `get_games`, `get_stats`, etc.
- Future: If balldontlie adds color data, can revisit (unlikely for sports stats API)

#### Technical Details

**team_colors.py coverage:**
```python
TEAM_COLORS = {
    'NFL': {...},   # 32 teams
    'NBA': {...},   # 30 teams
    'MLB': {...},   # 30 teams
    'NHL': {...},   # 32 teams
    'EPL': {...},   # 20 teams
    'WNBA': {...},  # 12 teams
    'NCAAF': {...}, # ~50 teams
    'NCAAB': {...}, # ~50 teams
}
# Total: ~256 teams
```

**balldontlie MCP tools configured:**
- `nba_get_teams`, `nba_get_players`, `nba_get_games`, `nba_get_stats`
- `nfl_get_teams`, `nfl_get_players`, `nfl_get_games`, `nfl_get_stats`
- Similar patterns for MLB, NHL, EPL, WNBA, NCAAF, NCAAB, MMA

---

### ADR-019: L6 Processor Expansion (Phase 1-3 Roadmap)

**Status:** Accepted
**Date:** December 2025
**Session:** O52-O54
**Impact:** Architecture
**Related:** ADR-001 (8-Layer Pipeline), ADR-017 (First Publishable Output)

#### Context
After achieving first publishable output (ADR-017) with carousel pipeline working end-to-end (L3→L5→L6→L7), analysis revealed L6 processors (`pil_processor.py`, `ffmpeg_processor.py`) were minimal. Only basic functions existed: logo overlay, aspect conversion, Ken Burns, slideshow. To achieve production-quality content at scale, needed comprehensive post-processing capabilities.

#### Options Considered
1. **Minimal approach** - Keep current functions, add as needed
2. **External tools** - Use Canva, Adobe, or other external tools
3. **Phased expansion (chosen)** - Systematic addition of 18 functions in 3 phases
4. **All-at-once** - Implement everything immediately

#### Decision
**Phased expansion of L6 processors with 18 new functions across 3 phases:**

**Phase 1 - Quick Wins (6 functions, no new dependencies):**
| Processor | Function | Purpose |
|-----------|----------|---------|
| PIL | `add_watermark()` | Semi-transparent text for brand protection |
| PIL | `create_gradient_background()` | Programmatic gradients, reduce API calls |
| PIL | `create_text_card()` | Quote/stat cards without API |
| FFmpeg | `trim_video()` | Cut video to time range |
| FFmpeg | `concatenate_videos()` | Join multiple videos |
| FFmpeg | `add_subtitles_burn()` | Hardcode SRT subtitles |

**Phase 2 - Medium Effort (4 functions, core enhancements):**
| Processor | Function | Purpose |
|-----------|----------|---------|
| FFmpeg | `parallax_effect()` | 2.5D depth for static images |
| FFmpeg | `split_screen()` | Matchup comparisons |
| PIL | `create_collage()` | Multi-player grid layouts |
| PIL | `apply_color_filter()` | Brand mood consistency |

**Phase 3 - Advanced (new modules, optional dependencies):**
- `audio_processor.py` - Audio manipulation module (pydub)
- Coqui/Piper TTS integration in L4 - Free local voice generation
- Local Whisper integration - Free transcription
- Real-ESRGAN upscaling - Image/video quality enhancement (GPU required)

#### Rationale
- **Cost reduction**: Gradient/text card generation reduces API calls
- **Production quality**: Watermarks, subtitles, effects improve output polish
- **No new dependencies for Phase 1**: Uses existing PIL/FFmpeg capabilities
- **Modular growth**: Each phase is independently valuable
- **Free tools first**: Maximizes Tier 1 (zero-cost) capabilities before paid APIs

#### Free Tools Integration (Tier System)

| Tier | Cost | Examples | Status |
|------|------|----------|--------|
| **Tier 1** | Zero | PIL, FFmpeg, MoviePy, Pexels, Pixabay | Already integrated |
| **Tier 2** | Free tier w/ API | Google TTS, Amazon Polly, Azure TTS | Available |
| **Tier 3** | Local GPU | Coqui, Whisper, Real-ESRGAN | Phase 3 |

#### Consequences
- L6 becomes comprehensive post-processing layer
- Reduced dependency on paid image generation APIs
- Consistent CLI pattern across processors (`processor.py <command> [options]`)
- Need `config/processor_presets.json` for effect presets
- Phase 1 can start immediately; Phase 3 requires GPU evaluation

#### Technical Details

**CLI Pattern (consistent across processors):**
```bash
# PIL Processor
python3 scripts/pil_processor.py watermark image.jpg --text "@GoatedBets"
python3 scripts/pil_processor.py gradient 1080 1920 --colors charcoal navy

# FFmpeg Processor
python3 scripts/ffmpeg_processor.py trim video.mp4 --start 0:05 --end 0:30
python3 scripts/ffmpeg_processor.py subtitles video.mp4 --srt captions.srt
```

**Preset Structure:**
```json
{
  "watermark_presets": {"subtle": {"opacity": 0.2}, "visible": {"opacity": 0.5}},
  "gradient_presets": {"brand_dark": {"colors": ["charcoal", "navy"]}},
  "subtitle_styles": {"default": {"fontsize": 24}, "bold": {"fontsize": 32}}
}
```

---

### ADR-020: Pipeline Orchestrator (O67 Platform Architecture)

**Status:** Accepted
**Date:** December 2025
**Session:** O67 (Design), D95-D97 (Implementation)
**Impact:** Architecture (Major)
**Related:** ADR-001 (8-Layer Pipeline), ADR-014 (Preset-Driven Workflow), ADR-015 (L0 Mode Selection)

#### Context
After achieving first full-pipeline preset (`carousel_illustrated` in D68), the system worked but had fragmented orchestration. Each mode (Discovery, Generate) called layer scripts independently. Layers were not truly unified under a single orchestrator. Presets didn't explicitly declare which layers they used, leading to implicit assumptions in code.

#### Problem Statement
1. **No unified orchestration** - Layers called individually, not as coherent pipeline
2. **No L1 platform** - Data fetching scattered across L3 imports
3. **Implicit layer assumptions** - Code assumed which layers ran; not declarative
4. **No layer skipping** - All layers touched even when not needed (e.g., L4 audio for carousels)
5. **Standalone scripts** - `meme_generator.py` bypassed pipeline entirely

#### Options Considered
1. **Keep current approach** - Explicit layer calls per mode, implicit assumptions
2. **Simple config flag** - Add `skip_l4: true` to presets
3. **Platform Architecture (chosen)** - Layers as platforms, presets declare layers + tools
4. **Event-driven pipeline** - Pub/sub between layers

#### Decision
**Platform Architecture Model with Pipeline Orchestrator**

**Core Concepts:**
- Each layer (L0-L8) is a **platform** - main script with attached tools/processors
- Presets explicitly declare `layers` array - which platforms to run
- Presets declare `L*_tool` mappings - which tool each platform uses
- New `PipelineOrchestrator` class in `content_pipeline.py` reads preset and calls layers sequentially
- New `data_source.py` as L1 platform - unified data fetching

**Implementation (D95-D97):**

1. **D95 - Structured Extraction Pipeline**
   - Created `g_api_processor.py` - GoatedBets API Processor for L3
   - Entity extraction → Bucket organization → Layout formatting
   - Pre-refactor snapshot rule added (Rule #25)

2. **D96 - Prompt Fixes**
   - Cleaned up prompt leakage and logo zone issues
   - Removed team abbreviations from edges (column header has team)

3. **D97 - Pipeline Orchestrator Core**
   - Created `scripts/data_source.py` - L1 platform
     - `DataSourcePlatform` class routes to appropriate tool
     - `DataContext` and `NormalizedMatchup` dataclasses
     - Supports: goatedbets_api, web_search, local_assets, balldontlie, odds_api
   - Created `PipelineOrchestrator` class in `content_pipeline.py`
     - `PipelineContext` dataclass holds pipeline state
     - Reads preset's `layers` array
     - Layer runners: `_run_l1()` through `_run_l8()`
     - Falls back to legacy flow for presets without `layers` array
   - Updated presets with O67 fields (`config/script_presets.json`):
     ```json
     "carousel_illustrated": {
         "layers": ["L1", "L2", "L3", "L5", "L6", "L7"],
         "L1_tool": "goatedbets_api",
         "L3_tool": "carousel_script",
         "L5_tool": "nano_banana",
         "output_type": "carousel"
     }
     ```

#### Key Design Principles

1. **All content starts at L0** - Single entry point, no standalone scripts
2. **Presets select layers** - Skip layers entirely (not no-op pass-through)
3. **Presets select tools** - Each layer uses the tool specified by preset
4. **Platforms orchestrate** - Main scripts route to appropriate tools
5. **Symmetric modes** - Both Generate and Discovery use same orchestrator pattern

**Why skip layers (not no-op)?**
- Cleaner execution - no false "L4: skipped" logs
- Explicit - preset declares exactly which layers touch content
- Easier debugging - "broke at L5" not "broke somewhere after L4 no-op"

#### Rationale
- **Declarative over imperative** - Presets define what happens, orchestrator executes
- **Single source of truth** - Preset config is complete specification
- **Easier debugging** - Know exactly which layers and tools ran
- **Tool flexibility** - Same layer, different tools (nano_banana vs flux_schnell)
- **Unified data layer** - L1 abstracts data source complexity
- **Deprecates standalone scripts** - Everything flows through L0

#### Consequences
- `content_pipeline.py` now primary orchestrator (not just menu)
- `data_source.py` is new L1 platform script
- Presets require `layers` array for O67 path (legacy fallback available)
- `meme_generator.py` should become `meme_mashup` preset (future task)
- `truth_prompt_wrapper.py` called from L3 (not L5)
- All new presets should use O67 pattern

#### Visual: Platform Flow
```
L0: content_pipeline.py
    │
    │ User selects preset: "carousel_illustrated"
    │ Preset config loaded: layers = ["L1", "L2", "L3", "L5", "L6", "L7"]
    │
    ▼
L1: data_source.py (PLATFORM)
    │ L1_tool = "goatedbets_api"
    │ → api_utils.fetch_goatedbets_matchup()
    │
    ▼
L2: calendar_config.py (PLATFORM)
    │ Week/phase context
    │
    ▼
L3: idea_creation.py (PLATFORM)
    │ L3_tool = "carousel_script"
    │ → g_api_processor.py (structured extraction)
    │ → truth_prompt_wrapper.py (style enhancement)
    │
    ▼
    [L4 SKIPPED - not in layers array]
    │
    ▼
L5: media_generation.py (PLATFORM)
    │ L5_tool = "nano_banana"
    │
    ▼
L6: assembly.py (PLATFORM)
    │ → ffmpeg_processor.py (reel conversion)
    │ → pil_processor.py (logo overlay)
    │
    ▼
L7: distribution.py (PLATFORM)
    │ Final packaging to /final/
    │
    ▼
    [L8 SKIPPED - not in layers array]
```

---

## Design Discussions

Significant technical conversations that informed decisions but don't warrant full ADRs.

### December 2025

#### Context Preservation Strategy (D11, O7)
**Topic:** How to maintain project state across Claude compactions
**Outcome:** Hybrid 30/70 approach - Oracle detects patterns (30%), Claude provides narrative (70%)
**Key Insight:** File-based communication between sessions, no direct context sharing
**Impact:** Workflow

#### Session Activity vs Compaction Risk (O8)
**Topic:** How to estimate context usage externally
**Outcome:** Replaced time-based "compaction risk" with activity-based proxy (file changes, health updates, context growth)
**Key Insight:** Time is not externally trackable; activity is
**Impact:** Tooling

#### Document Separation (O9)
**Topic:** How to differentiate PHILOSOPHY.md from technical decisions
**Outcome:** PHILOSOPHY.md for project-level "why", CODE_HISTORY.md for technical "why"
**Key Insight:** Different audiences - goals vs implementation
**Impact:** Documentation

#### CHANGELOG vs CODE_HISTORY Scope (O9)
**Topic:** What goes in CHANGELOG vs CODE_HISTORY
**Outcome:** CHANGELOG = raw facts (what happened), CODE_HISTORY = decisions and rationale (why)
**Key Insight:** CHANGELOG is append-only archive; CODE_HISTORY is curated knowledge
**Impact:** Documentation

---

## Rejected Approaches

| Approach | Session | Why Rejected | Alternative |
|----------|---------|--------------|-------------|
| Git hooks for oracle | D7 | User unfamiliar with git workflow | Session rules + health monitor |
| `__init__.py` for oracle | D7 | Overkill for single script | Standalone script pattern |
| Time-based compaction risk | O8 | Not externally trackable | Activity-based proxy |
| Fully automatic ADR creation | O9 | Loses nuance and context | Pattern detection + manual completion |
| Keeping DECISIONS.md separate | O9 | Redundancy, unclear boundaries | Merged into CODE_HISTORY.md |
| Draft system for ADRs | O9 | Added mental overhead | Defer to future (IDEAS_BACKLOG.md) |

### Details

#### Fully Automatic ADR Creation (O9)

**Proposal:** Oracle automatically creates complete ADRs from Recent Changes
**Why Rejected:**
- Loses the "why" narrative that only Claude/human can provide
- Pattern matching can't capture nuanced reasoning
- Risk of low-quality ADRs that don't help
**Alternative:** `suggest-code-history` detects candidates, Claude completes manually (70%)

#### Draft System for ADRs (O9)

**Proposal:** Auto-create drafts with 14-day stale tracking, review queue in health monitor
**Why Rejected:**
- Added mental overhead for user (another thing to review)
- User prefers to review at their own pace
- System should serve Claude's memory, not create user tasks
**Alternative:** Added to IDEAS_BACKLOG.md for future consideration. For now, `suggest-code-history` outputs candidates and Claude adds directly to CODE_HISTORY.md.

---

## Session Reference

| Session | Date | Type | Major Decisions/Changes |
|---------|------|------|-------------------------|
| D1 | Dec 7 | Dev | 8-layer pipeline, initial architecture, L6 video assembly |
| D2 | Dec 7 | Dev | L7 distribution optimization (single-copy) |
| D3 | Dec 7 | Dev | L3 preset integration, docs merge, context file as source |
| D4 | Dec 8 | Dev | Bug fixes, file cleanup, oracle integration |
| D5 | Dec 8 | Dev | Reports organization, smart doc sync |
| D6 | Dec 8 | Dev | Auto-archive, dual context sync |
| D7 | Dec 8 | Dev | Cross-session briefing, doc restructure |
| D8 | Dec 8 | Dev | Optimization awareness system |
| D9 | Dec 8 | Dev | Health monitor Phase 1-2 |
| D10 | Dec 8 | Dev | Health monitor Phase 3-4 |
| D11 | Dec 8 | Dev | Comprehensive docs update |
| D12 | Dec 8 | Dev | Session activity system, dashboard updates |
| O1 | Dec 7 | Oracle | Oracle agent created |
| O2 | Dec 7 | Oracle | Snapshot, status, archive commands |
| O3 | Dec 8 | Oracle | Autosave command, doc restructure |
| O4 | Dec 8 | Oracle | Bug fixes, planned files handling |
| O5 | Dec 8 | Oracle | Reports folder, smart doc sync |
| O6 | Dec 8 | Oracle | Auto-archive, multi-agent support |
| O7 | Dec 8 | Oracle | Health monitor implementation |
| O8 | Dec 9 | Oracle | Session activity, calibration, context preservation |
| O9 | Dec 9 | Oracle | Code history system, session numbering |
| D17-D25 | Dec 16 | Dev | End-to-end preset testing, Pexels/Kling integration |
| D26-D28 | Dec 16 | Dev | L0 entry point built (content_pipeline.py) |
| D29-D30 | Dec 17 | Dev | Discovery Mode enhancement, symmetric menus |
| D31-D33 | Dec 17 | Dev | Tool config integration across layers |
| D34-D39 | Dec 17 | Dev | CLI tool override args, single_matchup_card preset |
| D40 | Dec 17 | Dev | Tests, health fixes |
| D41-D42 | Dec 17 | Dev | Task #17 - SourceConfig merge into data_sources |
| O10-O31 | Dec 10-17 | Oracle | Health monitor phases, doc syncs, optimization |
| O32 | Dec 17 | Oracle | Task #17 ADR, doc sync |
| D43-D46 | Dec 18 | Dev | Nano Banana fixes, infographic preset L5 |
| D47-D50 | Dec 18 | Dev | **First publishable output** - split infographics, team colors, text processing |
| O33-O36 | Dec 18 | Oracle | Health monitor tasks panel, memory troubleshooting, team colors review, ADR-017 |
| O37-O46 | Dec 19 | Oracle | Error 127 diagnosis (broken venv), venv deletion, balldontlie architecture analysis, ADR-018 |
| D51-D73 | Dec 19-20 | Dev | Carousel pipeline (L3→L5→L6→L7), PIL/FFmpeg processors, real player names in mock data |
| O47-O51 | Dec 19-20 | Oracle | Brand Rules System, health score improvements, doc overhauls |
| O52-O53 | Dec 20 | Oracle | Processor expansion analysis (18 new functions), Phase 1-3 roadmap, free tools integration docs |

---

## Related Documentation

- **docs/PHILOSOPHY.md** - Project goals and principles (why the project exists)
- **docs/ARCHITECTURE.md** - Technical implementation details
- **docs/WORKFLOW.md** - Day-to-day operational processes
- **docs/CHANGELOG.md** - Raw session facts (what happened)
- **optimization/IDEAS_BACKLOG.md** - Future planning and deferred ideas

---

*Code History - Technical decisions and their rationale, preserved across sessions.*
