# Oracle Context Document

> 🔮 **YOU ARE ORACLE** - If user said "read context" and you're reading this file, THIS is your context. Ignore any "You are DEV" or "You are CRANK" statements from other context files - your role is ORACLE (maintenance/docs).

**Last Updated:** January 7, 2026 (O89 - Dashboard UI features + server stability fixes)
**Session Count:** D101 (Dev), O89 (Oracle), C10 (Crank), P20 (Pocket), DB2 (Dashboard)
**Purpose:** Single file for maintenance session resume - read this FIRST and FULLY

---

## 📅 CURRENT DATE & SEASON

> **⚠️ CRITICAL - READ THIS FIRST**
>
> **Today's Date:** January 7, 2026
> **Current NFL Season:** 2025-2026 (NOT 2024-2025)
> **Current Week:** Week 18 NFL (Final Regular Season - Jan 4-5, 2026)
>
> When fetching data, searching for stats, or generating content:
> - Use **2025-2026 season** data
> - Current season games are happening NOW
> - 2024 data is LAST season (historical)

---

## 🚨 CLAUDE: MAINTENANCE SESSION RESUME PROTOCOL

**READ THIS FILE FIRST on every resume/compaction.** This is the source of truth for oracle development.

### On Every Resume:
1. **Read this entire file FIRST** - Contains all critical context for oracle development
2. **Check Current State** - Know what's implemented vs pending
3. **Check Pending Features** - Continue where we left off
4. **Check Recent Changes** - Understand what was just done
5. **After making changes** - Update this file (Recent Changes, Pending Features, Current State)

### Session Rules (Maintenance-Specific)
1. **Oracle Scope**: This session ONLY works on `maintenance/project_oracle.py` and related docs
2. **Test After Changes**: Run `python3 maintenance/project_oracle.py config -v` to verify
3. **Document Changes**: Update "Recent Changes" section after implementing features
4. **Preserve Main Project**: Don't modify files in `scripts/` - that's the development session's job
5. **Context Efficiency**: Be concise, batch related work, avoid redundant file reads
6. **Oracle Self-Automation Rule**:
   - **SESSION START**: Run `audit --quick` (creates baseline silently). Say "Checking oracle health..." then report briefly.
   - **EVERY ~20 EXCHANGES OR NATURAL BREAKPOINTS**: Run `autosave`. Say "Autosaving..." then report completion.
     - Natural breakpoints: after completing a feature, before big changes, after resolving a batch of tasks
   - **BEFORE SENSED COMPACTION**: Run `autosave`. Say "Autosaved. Ready to compact whenever, or continue working."
   - **ON FAILURE**: If oracle script errors, run `config -v` to verify parsing still works
   - **WEEKLY** (manual trigger): Run `autosave --archive-changes`
   - **ON RESUME**: Check for incomplete actions (review Recent Changes, Pending Features). If last action was incomplete, complete it FIRST.
   - **STATUS**: Only run `status` when user explicitly requests it (not periodic)
7. **Compaction Context Preservation Rule**:
   - Before compaction, capture ALL ongoing context in your final message:
     - Current task in progress (if any)
     - Pending decisions or questions
     - Files being modified
     - Any temporary state not in Recent Changes
   - Use the todo list to track in-progress work
   - If mid-task when compaction happens, the compaction summary must include enough detail to resume seamlessly

   **Friendly language** (feel like a video game checkpoint):
   - "Autosaving..." (not "running snapshot")
   - "Quick health check..." (not "running status")
   - "Checking oracle health..." (not "running audit")

8. **Context Doc Auto-Management Rule**:
   - **Context docs are Claude's memory** - they should always be up-to-date
   - **Autosave auto-updates**: Oracle's autosave now auto-appends file changes to Recent Changes
   - **Claude enriches context**: Add the "why" and "how" to Recent Changes entries, not just file lists
   - **Before significant work**: Ensure Recent Changes has context for what you're about to do
   - **After significant work**: Update Recent Changes with meaningful descriptions (what was done + why)
   - **Pending Features**: Keep in sync with todo list - mark completed, add new items
   - **No manual user edits**: User relies on Claude for ALL context doc edits

9. **Python3 Rule**:
   - **Always use `python3`** for all script execution commands
   - All shebangs in scripts use `#!/usr/bin/env python3`
   - Documentation examples must use `python3 maintenance/...` not `python maintenance/...`
   - When editing docs, verify python commands use `python3`

10. **Optimization Principle (Trim to Preserve)**:
    - **Remove redundant code/data** - Eliminate duplication, unused fields, unnecessary abstractions
    - **Preserve all functionality** - Direct features AND indirect capabilities must remain intact
    - **Verify after trimming** - Test that affected features still work as expected
    - **Example**: Removed `recent_changes`/`pending_tasks` from JSON baseline (redundant - context files are source of truth), but verified diff detection still works via file timestamps

11. **Incremental Implementation Rule**:
    - **One action at a time** - Complete one task, pause for user confirmation, then proceed to next
    - **Pause after each step** - Allows user to compact if needed without losing work
    - **Minimize context loss** - Each completed step is saved; incomplete multi-step work gets lost on compaction
    - **Checkpoint after each action** - User can say "continue" or "compact now"

12. **Temporary Implementation Plan Rule**:
    - **Check IMPLEMENTATION PLANS section** - Before starting feature work, check if there's a plan
    - **Follow the plan** - Use the detailed spec in the plan, don't redesign from scratch
    - **Save important info before delete** - Preserve implementation details, command specs, design decisions to CODE_HISTORY.md
    - **Remove plan when complete** - After all steps done, delete the temporary plan section

13. **Cross-Project Feature Rule**:
    - **Oracle features serve all projects** - New oracle capabilities should work for both `maintenance/` AND `scripts/` (dev project)
    - **Consider both scopes** - When adding audits, debug features, or tooling, ensure they scan/apply to dev scripts too
    - **Environment variables for cross-project** - Use `ORACLE_DEBUG` env var pattern for features that span projects
    - **Example**: Memory leak detection scans both `scripts/` and `maintenance/`; `--debug` sets `ORACLE_DEBUG=1` for any script to check

14. **Dev ↔ Oracle Rotation Rule**:
    - **On session start**: Check DEV_CONTEXT for `🚩 NEEDS_ORACLE_PASS` flag
    - **When flag present**: (1) Read DEV_CONTEXT Recent Changes, (2) Update affected docs, (3) Run health scan + fix issues, (4) Clear flag, (5) Compact
    - **Set NEEDS_DEV_ATTENTION**: If code issues require dev input (not auto-fixable)
    - **Oracle scope**: Docs, health fixes, code maintenance - expanded to include `scripts/` for health issues

15. **Session Role Clarity Rule**:
    | Role | Primary Focus | Can Touch | Avoid |
    |------|---------------|-----------|-------|
    | **Dev (D#)** | Feature building, pipeline scripts, testing, iteration | Quick notes in Recent Changes | Comprehensive doc updates, ADRs, batch generation |
    | **Oracle (O#)** | Doc maintenance, health fixes, ADRs, archiving | Code fixes from health scans | New features, major refactors, generation |
    | **Crank (C#)** | Content production, quality review, batch runs | Update generation queue | Code changes, doc maintenance |
    | **Dashboard (DB#)** | Web UI development, API design, frontend components | Dashboard folder only | Pipeline scripts, config files |

    - **Dev sessions**: Build → Test → Iterate → Note changes briefly
    - **Oracle sessions**: Sync docs → Write ADRs → Archive → Fix health issues
    - **Dashboard sessions**: UI/UX → API endpoints → Test locally → Document
    - **Handoff**: Dev sets `NEEDS_ORACLE_PASS`, oracle does comprehensive update
    - **⚠️ ORACLE OWNS ALL REFERENCE DOC SYNC** - Oracle syncs changes from ALL sessions (Dev, Oracle, Crank, Dashboard) to reference docs. No permission needed. See "Detailed Docs Update Protocol" below for triggers.

16. **Output Review Rule**:
    - **Claude views images directly**: Use Read tool to view generated images (PNG, JPG) for quality feedback
    - **Iterate based on visual inspection**: Claude can see text rendering, layout, colors - use this for rapid iteration
    - **iOS Simulator for mobile preview**: Use when testing 9:16 vertical format or mobile-specific UX
    - **Default to direct viewing**: Most cases don't need simulator - Claude's built-in image viewer is faster
    - **Document visual issues**: When images have problems, describe what's wrong for context preservation

17. **Cross-Session Communication Rule**:
    - **Complete context in handoffs**: When passing tasks between dev ↔ oracle, include ALL details needed to execute
    - **No translation loss**: Assume the other session has NO memory of discussions - write everything explicitly
    - **Include**: Exact file paths, function names, parameter values, design decisions, rationale
    - **For presets/config**: Include the actual JSON structure or code snippet, not just descriptions
    - **For bugs/fixes**: Include error messages, root cause, and solution details
    - **Example bad**: "Fix monitor display" → **Example good**: "In `health_monitor.py:1220-1250`, task list shows only 4 items and text gets cut off. Increase `main_table` column width or add text wrapping."

18. **Task Documentation Comprehensiveness Rule**:
    - **Never lose information**: When documenting tasks, include ALL implementation details
    - **Archive before delete**: Move completed task details to CHANGELOG.md or CODE_HISTORY.md, don't just remove
    - **Task specs include**: Goal, current state, implementation location, logic needed, files to modify, code examples
    - **Dependency tracking**: Note blockers and what each task unblocks
    - **Rationale**: Future sessions can pick up exactly where we left off without re-discovery

19. **Modular Architecture Rule (Layer Pathways)**:
    - **Every pathway follows the layer model**: Content, presets, vision data, analytics - ALL flow through L1→L8
    - **Route by `display_mode`**: Each layer checks content type and routes to appropriate handler
    - **No bypassing layers**: Don't create shortcuts that skip layers - maintain the L3→L5→L6→L7 flow
    - **New content types**: When adding (infographics, videos), implement handlers in EACH layer

20. **Prompt Engineering Rule** *(P5 - See STYLE_GUIDE.md for full details)*:
    - **Structured prompts**: Use `[LOCKED]`, `[LAYOUT]`, `[CONTENT]`, `[ACCENTS]` sections
    - **Never paraphrase locked sections**: Copy exact wording that produced good results
    - **Use overrides, not inline edits**: Pass `overrides={'key': 'value'}` instead of editing prompt text
    - **Post-generation tweaks via Gemini edit**: Don't regenerate to fix minor issues - use image editing
    - **Scan verbose output**: Review generated images for drift before finalizing

21. **Automation with Granular Control Rule** *(P6 - See PHILOSOPHY.md §2.6 for full details)*:
    - **Three modes**: Full Automation (default), Guided Control, Granular Manual
    - **Defaults enable automation**: Running with no args should "just work"
    - **Parameters enable control**: Every auto-behavior can be overridden via CLI/function args
    - **Layer architecture**: L0=Entry Point, L1=Data Source, L2=Planning, L3=Script/Prompt, L4=Audio, L5=Media, L6=Assembly, L7=Distribution, L8=Analytics
    - **New data sources go in L1**: Asset ingestion, new APIs, web scraping = L1 tools

22. **Cost Tracking Integration Rule (APICallLogger)**:
    - **Every NEW API tool must log costs**: When implementing any new API integration, add cost logging
    - **Oracle verifies on new tools**: During health scans, check new API calls have logging
    - **Pattern**: `api_logger.log_call()` + `api_logger._save_to_file()`
    - **Import**: `from maintenance.project_oracle import api_logger`
    - **Metadata**: Include context (`slide_type`, `content_type`, etc.)
    - **Health monitor reads**: `cost_today` pulls from `reports/api_calls.json`
    - **Already implemented**: `media_generation.py` logs all Gemini calls (O50)
    - **Checklist for new tools**: (1) Import api_logger, (2) Add log_call() after API response, (3) Include provider/model/cost/metadata
    - **Rationale**: Cost visibility enables budget management and identifies expensive operations

21. **Context File Size Guard**:
    - **Target size**: Context files should stay under ~800 lines
    - **Recent Changes**: Keep only last 3-5 sessions with full detail
    - **Archive trigger**: When Recent Changes exceeds ~50 sessions or file exceeds 1500 lines
    - **Archive process**: Move old sessions to CHANGELOG.md with milestone summaries
    - **What to keep**: Session Rules, Current State, Pending Tasks, recent 3-5 sessions
    - **Rationale**: Bloated context files lose usefulness - key info gets buried

22. **Naming Convention Rule**:
    - **Script/config/file names**: Intuitive and symmetric wherever possible
    - **Output file naming**: `{visual_style}_{slide_type}.{ext}`
      - `visual_style`: The aesthetic preset (illustrated, dark, minimal)
      - `slide_type`: The content type (cover, matchup, bonus)
      - Examples: `illustrated_cover.mp4`, `illustrated_matchup.jpg`, `dark_bonus.mp4`
    - **Preset naming**: `{content_type}_{visual_style}` → `carousel_illustrated`, `infographic_dark`
    - **Matchup folders**: `{away}_at_{home}` lowercase → `patriots_at_ravens/`
    - **Intermediate folders** (can be deleted after distribution):
      - `week16/media/` - L5 raw generated images
      - `week16/assembled/` - L6 assembled content (rename from `reels/`)
    - **Final folders** (distribution-ready, keep):
      - `final/carousels/` - Slides + reels together (P13)
      - `final/animations/` - Ken_burns + effects animations (P13)
      - `final/infographics/` - Dark stat cards
      - Platform folders for platform-optimized exports
    - **Avoid redundancy**: Don't repeat info in nested paths
    - **Rationale**: Visual style prefix enables quick identification of source preset

### Oracle-Specific: Detailed Docs Update Protocol

**Oracle is responsible for syncing ALL sessions' changes to reference docs.**

| Document | Update When... | Source |
|----------|----------------|--------|
| **CHANGELOG.md** | Any session makes code changes | Archive from context Recent Changes |
| **CODE_HISTORY.md** | Major architectural decisions, milestones | Add ADRs for significant changes |
| **ARCHITECTURE.md** | Pipeline changes, layer/tool changes, file structure | Dev changes to scripts/ or dashboard changes |
| **PHILOSOPHY.md** | New principles, reasoning patterns, vision changes | User feedback to any session |
| **WORKFLOW.md** | Process changes, session protocol, commands | Any workflow improvements |
| **TOOLS_REFERENCE.md** | New tools, pricing changes, capabilities | Tool evaluations |

**Process:**
1. Read other sessions' Recent Changes (DEV_CONTEXT, CRANK_CONTEXT)
2. Identify which reference docs are affected
3. Read affected docs, make targeted updates
4. Update timestamps
5. Capture meta-principles from user feedback → PHILOSOPHY.md

### Context Efficiency Rules:
- Reference from memory unless file was edited externally
- Summarize changes, don't show full code blocks
- Use todo tracking for multi-step tasks
- Keep this file updated as source of truth

### Before Making Changes:
- Verify understanding with user if unclear
- Test commands work before documenting them
- Backup strategy: oracle creates `.backup` files automatically

### Handling User Rejection Feedback
**When user rejects a proposed change with additional context/instructions:**
1. **PARSE BOTH PARTS:**
   - Part A: The rejection/modification to the proposed change
   - Part B: Any NEW tasks or context added in the feedback
2. **CREATE EXPLICIT TODO LIST** - Write out ALL tasks from the rejection feedback
3. **EXECUTE SEQUENTIALLY** - Don't skip Part B after handling Part A
4. **CONFIRM COMPLETION** - "I've completed: [list]. Anything I missed?"

### Resume Prompt (copy this after compaction):
```
you are oracle - read ORACLE_CONTEXT.md
```

**Why this format?** After compaction, Claude may see stale role identity from the previous session's context. Declaring "you are oracle" FIRST overrides any confusion before reading the file.

---

## 🔗 CROSS-SESSION PROTOCOL

### Related Sessions
- **Development**: See `context/DEV_CONTEXT.md`
- **Crank**: See `context/CRANK_CONTEXT.md`
- **Pocket**: See `context/POCKET_CONTEXT.md`
- **Dashboard**: See `context/DASHBOARD_CONTEXT.md`

### Maintenance → Development Communication
Oracle outputs for dev session:
- `reports/audits/ORACLE_REPORT_*.md` - Health findings
- `reports/diffs/SESSION_DIFF_*.md` - Session diffs
- `reports/snapshots/SNAPSHOT_*.md` - Context snapshots
- `docs/CHANGELOG.md` - Archived changes

Dev session reads these by:
- "Fix critical issues in latest oracle report"
- "Review the oracle report and prioritize fixes"

### Development → Maintenance Communication
Oracle reads `context/DEV_CONTEXT.md` to:
- Auto-detect layers, APIs, scripts
- Check documentation drift
- Validate layer health
- Check cross-session flags (`🚩 NEEDS_ORACLE_PASS`)

### Session Scope

| Session | Primary Scope | Can Also Touch |
|---------|--------------|----------------|
| **Dev** | `scripts/`, `config/`, `output/`, feature work | Quick doc fixes if urgent |
| **Oracle** | `docs/`, `maintenance/`, `context/`, health fixes | Code fixes from health scans |

**Oracle expanded scope**: Oracle can fix code issues (unused imports, long functions, etc.) discovered during health scans, even in `scripts/`.

### 🚩 Cross-Session Flags
<!-- Flags for dev ↔ oracle rotation workflow -->

**Status:** _(none)_

<!--
Available flags (set by replacing "_(none)_" above):
- 🚩 NEEDS_ORACLE_PASS - Dev sets before compact; Oracle clears after maintenance pass
- 🚩 NEEDS_DEV_ATTENTION: [reason] - Oracle sets if issues need dev input
- 🚩 PAUSED_MID_TASK: [description] - Dev sets if pausing mid-task for urgent maintenance

When oracle sees NEEDS_ORACLE_PASS:
1. Read DEV_CONTEXT Recent Changes
2. Update all affected docs
3. Run health scan, fix issues
4. Clear the flag
5. Update ORACLE_CONTEXT, compact
-->

---

## 🎯 OPTIMIZATION AWARENESS

### System Overview
Hybrid 30/70 system: Oracle detects quantifiable patterns (30%), Claude adds judgment (70%).

Recommendations are tracked in:
- `optimization/OPTIMIZATION_LOG.md` - Running log by date/category
- `optimization/IDEAS_BACKLOG.md` - Future ideas (YES/MAYBE/NO/UNREVIEWED)
- `optimization/reports/OPT_REPORT_*.md` - Detailed reports

### Categories (Same as DEV_CONTEXT.md)
Code, Workflow, Tools/Skills, VS Code, UX, Architecture, Cost, Documentation, Subagents, Automation, MCP/API, Decision Strategy, Philosophy, Project Architecture, Future Planning, Meta

### Source Tracking
- `[O]` - Oracle detected (automated 30%)
- `[CD]` - Claude (dev session - 70% judgment)
- `[CO]` - Claude (oracle/maintenance session)
- `[U]` - User added

**Note:** In maintenance/oracle sessions, use `[CO]` prefix for Claude-judged recommendations.

### Maintenance-Specific Opportunities
In oracle/maintenance sessions, particularly watch for:
- Documentation drift and staleness
- Oracle system improvements (meta)
- Automation opportunities for health checks
- Architecture patterns across codebase
- Cross-session protocol improvements

### Commands
```bash
python3 maintenance/project_oracle.py optimize           # Full scan, console output
python3 maintenance/project_oracle.py optimize --report  # Save to optimization/reports/
python3 maintenance/project_oracle.py optimize --log     # Append to OPTIMIZATION_LOG.md
```

### Auto-Updates During Autosave
- Optimization summary shown in autosave output
- Manual logging via `optimize --log` when needed

---

## 📊 CURRENT STATE

| Metric | Value |
|--------|-------|
| Capabilities | Audit, Sync (--fix), Report, Config, Snapshot, Status, Diff, Optimize |
| Docs Synced | DEV_CONTEXT.md (auto), 6 reference docs (warnings + --fix) |
| Test Coverage | 66 pytest tests (`tests/test_*.py`) |
| Cost Tracking | `APICallLogger` in `project_oracle.py`, used by `media_generation.py` |
| Status | Functional, expanding |

### Running Tests
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_tool_resolver.py -v

# Run with coverage (if pytest-cov installed)
python3 -m pytest tests/ --cov=scripts
```

### Implemented Features
- [x] ContextParser - reads DEV_CONTEXT.md as config source
- [x] 5 Auditors - Code, Docs, Layers, API, Context health
- [x] DocSyncEngine - writes updates to DEV_CONTEXT.md
- [x] Reference doc checking - warnings for all 6 docs
- [x] `--fix` mode - safe targeted fixes for reference docs
- [x] Backup system - creates .backup before writes
- [x] Dry-run default - preview before applying
- [x] `diff` command - session diff tracking with snapshots
- [x] `--prune-tasks` flag - remove completed tasks from Pending Tasks
- [x] `snapshot` command - unified context snapshot (state + changes + resume prompt)
- [x] `status` command - one-line health dashboard (quiet mode)
- [x] `--archive-changes` flag - move old Recent Changes to docs/CHANGELOG.md
- [x] `autosave` command - sync + snapshot with minimal output (video game checkpoint feel)
- [x] `audit --quick` silent baseline - creates baseline automatically on session start
- [x] New documentation structure - context/ folder, DEV_CONTEXT.md, ORACLE_CONTEXT.md
- [x] File cleanup - keeps only last 5 reports/snapshots/diffs
- [x] Reports folder organization - `reports/audits/`, `reports/diffs/`, `reports/snapshots/`
- [x] Smart doc sync - `suggest-docs` command and `autosave --suggest-docs`
- [x] Auto-archive Recent Changes - autosave keeps 5 most recent sessions, archives older to CHANGELOG
- [x] Dual context file syncing - autosave archives both DEV_CONTEXT.md and ORACLE_CONTEXT.md
- [x] Dynamic multi-agent support - CONTEXT_FILES list for easy addition of new agents
- [x] Cross-session briefing - surfaces relevant info from other session type at session start
- [x] **Optimization Awareness System** - 30/70 hybrid detection with IDEAS_BACKLOG.md consolidation
- [x] **Oracle Health Monitor** - Full implementation (Phases 1-4 complete)
  - Phase 1: Core dashboard with `rich` library
  - Phase 2: File watching with `watchdog` library
  - Phase 3: Alerts & automation (keyboard input, escalating reminders)
  - Phase 4: Oracle integration (`reports/.health_status.json`)
  - Phase 5: Session Activity system (context usage proxy with calibration)

### Pending Tasks
- [x] **L1 Data Sources Deep Dive** - ✅ O74 - Completed, documented in ARCHITECTURE.md
  - Tested all 3 data sources: GoatedBets, SportsBlaze, BalldontLie
  - Created Data Source Comparison Matrix (10 data types across 3 sources)
  - Documented SportsBlaze endpoints: standings, boxscores (142 stats), rosters, schedules
  - Confirmed BalldontLie free tier limitations (standings/stats/injuries/odds require paid)
  - Added "Recommended Data Source Combinations" table for content types
- [x] **Triage Dev pending tasks** - ✅ O61 - Consolidated from 46 to 11 tasks, removed completed, reorganized
- [x] **L6 text overlay research** - ✅ O62 - Researched, documented in DEV_CONTEXT Task #2
- [x] **Archive regen_slide.py** - ✅ O66 - Script moved to `scripts/archive/` (main pipeline handles regeneration)

### Deferred Features
- [ ] Automated triggers (VS Code open, git commit) - *Current session rules sufficient*
- [ ] Context digest generation - *Auto-archive keeps context files manageable*

### Future Tasks
- [ ] **P20 L5 Data Flow Refactor** - L5 should receive pre-extracted data from L3
  - Currently L5_media.py calls L3 extraction functions as fallbacks (lines 2015-2017, 2066)
  - Pattern: `insight_1 = best_bet.get('insight_1') or extract_cover_insight(...)`
  - Fix: Ensure L3 always provides these fields so L5 never calls extraction
  - Scope: Modify L3_ideas.py to extract insights before passing to L5
- [x] **P19 api_utils.py Migration** - ✅ O86 - COMPLETE (proper layer location)
  - Moved api_utils.py (2,839 lines) to `_L3/utils/api_utils.py`
  - Extracted L0 toggle to `_L0/utils/llm_config.py` (set_llm_extraction, is_llm_extraction_enabled)
  - Updated 8 imports across 5 files (L0_pipeline, L3_ideas, L5_media, data_transforms, g_api_processor)
  - `scripts/` root now has 9 files: 9 `L*_*.py` mains only
- [x] **P18 Main Script Rename** - ✅ O85 - COMPLETE (simplified layer names)
  - Renamed 9 main scripts with `L*_` prefix and simplified names
  - `content_pipeline.py` → `L0_pipeline.py`, `data_source.py` → `L1_data.py`
  - `calendar_config.py` → `L2_calendar.py`, `idea_creation.py` → `L3_ideas.py`
  - `audio_sync.py` → `L4_audio.py`, `media_generation.py` → `L5_media.py`
  - `assembly.py` → `L6_assembly.py`, `distribution.py` → `L7_distribution.py`
  - `analytics.py` → `L8_analytics.py`
  - Updated 4 imports in 3 files (api_utils.py, data_transforms.py, test file)
  - `scripts/` root now has 10 files: 9 `L*_*.py` mains + api_utils.py
- [x] **P17 Shim Removal** - ✅ O84 - COMPLETE (clean architecture)
  - Removed 11 backward-compatible shims from `scripts/` root
  - Updated all imports to use direct `_L*/` paths
  - Backups stored in `scripts/archive/emergency_shims/`
- [x] **P16 Scripts Reorganization** - ✅ O83 - COMPLETE (remaining layer tools)
  - Unmigrated `calendar_config.py` back to `scripts/` root as L2 main
  - Migrated 4 tools to `_L*/` folders with backward-compatible shims
  - L1: odds_fetcher, web_search_trend_detector, refine_search → `_L1/inputs/`
  - L2: organize_segments → `_L2/processors/`
- [x] **P15 Scripts Reorganization** - ✅ O81 - COMPLETE (all phases + cleanup)
  - Phase 1-2: 8 helper files migrated to `_L*` folders
  - Phase 3: api_utils.py decomposition (extraction, text_processing, processors, utils modules)
  - Phase 4: api_utils.py cleanup (4,819 → 2,839 lines, 41% reduction)
  - Phase 5 (Cleanup): Removed 8 backup files + rollback script (~257KB)

---

## 📝 RECENT CHANGES

### January 7, 2026 - Session 89 (O89) ✅ COMPLETE
- **Dashboard UI Improvements (DB2)** ✅
  - **PresetPreview Component**: Created live mockup preview for PresetBuilder
    - Shows carousel slides, single images, videos, infographics based on form settings
    - Sport-specific colors, pipeline flow display, audio indicators
    - Updates in real-time as user changes output_type, aspect_ratio, slides_count
    - Files: [PresetPreview.jsx](dashboard/frontend/src/components/PresetPreview.jsx), [PresetPreview.css](dashboard/frontend/src/components/PresetPreview.css)
  - **PresetBuilder Layout**: Side-by-side form + preview with responsive grid
    - Updated [PresetBuilder.jsx](dashboard/frontend/src/components/PresetBuilder.jsx) with preview panel
    - Updated [PresetBuilder.css](dashboard/frontend/src/components/PresetBuilder.css) with `.builder-layout` grid
  - **Green Color Scheme**: Changed pipeline layer selections to green (#10b981)
    - Layer card hover, selected states, checkboxes all use consistent green
    - Pipeline flow text in preview also green
- **Server Stability Fixes** ✅
  - **Multiple frontend server issue**: Fixed by adding `pkill` + `--strictPort` to npm dev script
    - [package.json](dashboard/frontend/package.json): `"dev": "pkill -f 'vite.*5173' 2>/dev/null; vite --port 5173 --strictPort"`
    - Prevents accumulation of zombie Vite servers on different ports
  - **OAuth redirect fix**: Changed default FRONTEND_URL from 5174 to 5173
    - [auth.py:20](app/api/routes/auth.py#L20): `FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")`
  - **CORS config expanded**: Added ports 5173, 5174, 5175 to allowed origins
    - [config.py:59](app/config.py#L59): Updated CORS_ORIGINS
  - **Debug logging added**: Console logs in MatchupSelection.jsx for troubleshooting
- **Servers Running**:
  - Frontend: http://localhost:5173/ (Vite)
  - Backend: http://localhost:5001/ (Flask Media Engine V2)

### January 5, 2026 - Session 88 (O88) ✅ COMPLETE
- **Context Files Synced for Dashboard Session** ✅
  - Updated [DASHBOARD_CONTEXT.md](docs/context/DASHBOARD_CONTEXT.md) with implementation plan details
    - Added link to full plan: `/Users/Vanil/.claude/plans/curious-questing-summit.md`
    - Added Phase 2-5 roadmap (Core Functionality, Config Sync, Multi-User, Output Editing)
    - Added Architecture Decisions section (Preset-Based Tool Customization, Config Sync, Multi-User Tracking, Output Editing)
  - Synced session counts across ALL context files to D101/O88/C10/P20/DB1
    - [DEV_CONTEXT.md](docs/context/DEV_CONTEXT.md) - Added DB1
    - [CRANK_CONTEXT.md](docs/context/CRANK_CONTEXT.md) - Fixed to O87→O88, kept C10
    - [POCKET_CONTEXT.md](docs/context/POCKET_CONTEXT.md) - Updated O85→O88, added DB1
    - [DASHBOARD_CONTEXT.md](docs/context/DASHBOARD_CONTEXT.md) - Updated O86→O88
  - Updated [DEV_CONTEXT.md](docs/context/DEV_CONTEXT.md) with Dashboard integration info
    - Added Dashboard to Related Sessions list
    - Added Development ↔ Dashboard communication sections
    - Dashboard reads presets, pipeline interface, tool categories
    - Dashboard wraps pipeline via subprocess (no code modifications)
  - Dashboard session now has complete context to begin Phase 2 implementation
- Health score: 7.0/10, 0 critical, 155 warnings

### January 5, 2026 - Session 87 (O87) ✅ COMPLETE
- **Dashboard Integration - Five-Session Model** ✅
  - Created `docs/context/DASHBOARD_CONTEXT.md` for dashboard development sessions (DB#)
  - Updated ORACLE_CONTEXT.md session count to include DB1 (Dashboard)
  - Added Dashboard to Related Sessions list and session roles table
  - Updated `maintenance/project_oracle.py` CONTEXT_FILES list (added CRANK, POCKET, DASHBOARD)
  - Updated ARCHITECTURE.md with comprehensive Dashboard section (file structure, APIs, integration points)
  - Updated WORKFLOW.md from three-session to five-session model
  - Updated dashboard.md status: "Plan Approved, Ready for Implementation"
  - Implementation plan: `/Users/Vanil/.claude/plans/curious-questing-summit.md`
  - Five-session model now active: D# (Dev), O# (Oracle), C# (Crank), P# (Pocket), DB# (Dashboard)
  - Health score: 7.0/10, 0 critical, 139 warnings

### January 3, 2026 - Session 86 (O86) ✅ COMPLETE
- **P19 api_utils.py Migration - COMPLETE** ✅
  - Moved `api_utils.py` (2,839 lines) from `scripts/` root to `_L3/utils/api_utils.py`
  - Extracted L0 toggle to new file `_L0/utils/llm_config.py`:
    - `set_llm_extraction()` - toggle LLM vs regex extraction
    - `is_llm_extraction_enabled()` - check current mode
  - **Updated imports** in 5 files:
    - `L0_pipeline.py:42` - now imports from `scripts._L0.utils.llm_config`
    - `L3_ideas.py:967,998,1111` - now imports from `scripts._L3.utils.api_utils`
    - `L5_media.py:47` - now imports from `scripts._L3.utils.api_utils`
    - `_L3/processors/data_transforms.py:92` - updated import path
    - `_L3/analysis/g_api_processor.py:46,54` - updated import path
  - **Re-exports** for backward compatibility: api_utils.py re-exports llm_config functions
  - `scripts/` root now has exactly 9 files (L0-L8 mains only)
  - **Created P20** for L5 data flow refactor (runtime layer violation, not import issue)

### January 3, 2026 - Session 85 (O85) ✅ COMPLETE
- **P18 Main Script Rename - COMPLETE** ✅
  - Renamed 9 main pipeline scripts with `L*_` prefix + simplified names
  - | Old Name | New Name |
    |----------|----------|
    | `content_pipeline.py` | `L0_pipeline.py` |
    | `data_source.py` | `L1_data.py` |
    | `calendar_config.py` | `L2_calendar.py` |
    | `idea_creation.py` | `L3_ideas.py` |
    | `audio_sync.py` | `L4_audio.py` |
    | `media_generation.py` | `L5_media.py` |
    | `assembly.py` | `L6_assembly.py` |
    | `distribution.py` | `L7_distribution.py` |
    | `analytics.py` | `L8_analytics.py` |
  - **Updated imports** in 3 files:
    - `api_utils.py:200` - `from scripts.L3_ideas import`
    - `_L3/processors/data_transforms.py:66,577` - `from scripts.L3_ideas import`
    - `tests/interactive_test_layer2.py:123` - `from scripts.L3_ideas import`
  - **Verified** all 9 scripts import correctly
  - Layer architecture now visible in file listing: `ls scripts/L*.py`

### January 3, 2026 - Session 84 (O84) ✅ COMPLETE
- **P17 Shim Removal - COMPLETE** ✅
  - User asked "do we need the shims?" - confirmed shims ARE needed (main scripts import from root paths)
  - Decided to remove shims and update imports instead
  - **Backed up** 11 shims to `scripts/archive/emergency_shims/`
  - **Updated imports** in 8 files:
    - `idea_creation.py` - 2 places (ai_models, balldontlie_mcp)
    - `assembly.py` - 1 place (pil_processor)
    - `api_utils.py` - 2 places (balldontlie_mcp, g_api_processor)
    - `_L3/processors/data_transforms.py` - 2 places (balldontlie_mcp, g_api_processor)
    - `_L1/inputs/balldontlie_mcp.py`, `_L1/inputs/odds_fetcher.py` - docstring examples
    - `_L5/processors/pil_processor.py`, `_L5/processors/ffmpeg_processor.py` - docstring examples
  - **Deleted** 11 shim files from `scripts/` root
  - **Verified** all imports work correctly
  - **ARCHITECTURE.md updated** - P17 status, removed shim references from all tables

### January 3, 2026 - Session 83 (O83) ✅ COMPLETE
- **Layer Architecture Clarification** - User noticed scripts still in `scripts/` root, triggered review
  - **P15 Status**: Complete for 8 helper files (shims in place)
  - **Main pipeline scripts** (L0-L8): Correctly stay in `scripts/` root
  - **L2 correction**: `calendar_config.py` should be L2 main (not `organize_segments.py`)
- **P16 Scripts Reorganization - COMPLETE** ✅
  - **Unmigrated** `calendar_config.py` back to `scripts/` root as L2 main (replaced shim with 955-line implementation)
  - **Deleted** `scripts/_L2/utils/calendar_config.py` (wrongly migrated location)
  - **Migrated L1 tools** with backward-compatible shims:
    - `odds_fetcher.py` → `_L1/inputs/odds_fetcher.py`
    - `web_search_trend_detector.py` → `_L1/inputs/web_search_trend_detector.py`
    - `refine_search.py` → `_L1/inputs/refine_search.py`
  - **Migrated L2 tool** with backward-compatible shim:
    - `organize_segments.py` → `_L2/processors/organize_segments.py`
  - **ARCHITECTURE.md updated** - P16 table marked complete, layer references updated

### January 2, 2026 - Session 82 (O82) ✅ COMPLETE
- **Player Database Expansion** - Dev was blocked by "prompt is too long" when trying to update all players at once
  - Root cause: Dev tried to add entire NFL rosters in single prompt (too many players)
  - Solution: Batched updates by division/conference to avoid context overflow
  - **Before**: 135 PLAYER_TEAMS, 130 PLAYER_POSITIONS
  - **After**: 208 PLAYER_TEAMS, 208 PLAYER_POSITIONS (54% increase)
  - All 32 teams now have 4-9 players each (previously some had only 2-3)
  - Updated [player_utils.py](scripts/_L3/utils/player_utils.py) with Week 18 rosters
- **Health check**: 7.0/10, 0 critical, 90 warnings

### January 2, 2026 - Session 81 (O81) ✅ COMPLETE
- **P15 Reorganization Review & Cleanup**
  - Confirmed P15 scope: helper files + api_utils.py decomposition (NOT main pipeline scripts)
  - Main scripts (content_pipeline, media_generation, assembly, distribution, idea_creation) stay in `scripts/` root
  - **Cleanup executed**: Removed 8 backup files + rollback script (~257KB)
  - All imports verified working post-cleanup

### January 2, 2026 - Session 80 (O80) ✅ COMPLETE
- **P15 Phase 4: api_utils.py cleanup - FULL EXECUTION**
  - **Pass 1**: Replaced prompt builders (3 functions) → `_L3/processors/prompt_builders.py`
  - **Pass 2**: Replaced data transforms (6 functions) → `_L3/processors/data_transforms.py`
  - **Pass 3**: Replaced player utils (6 dicts + 5 functions) → `_L3/utils/player_utils.py`
  - **Pass 4**: Replaced extraction (determine_predicted_winner) → `_L3/analysis/extraction/`
  - **Total lines removed**: 1,980 (41% reduction)
  - **api_utils.py**: 4,819 → 2,839 lines
  - All imports verified working, all 4 migration flags = True
- **Health check**: 7.0/10, 0 critical, 100 warnings

### December 31, 2025 - Session 79 (O79) ✅ COMPLETE
- **P15 Phase 4 scoped** - api_utils.py cleanup marked as future task
  - Identified ~1,800 lines removable (prompt_builders + data_transforms originals)
  - Shim already functional, originals can be replaced with thin wrappers
  - Added to "Future Tasks" section for dedicated session
- **Health check**: 7.0/10, 0 critical, 100 warnings

### December 31, 2025 - Session 78 (O78) ✅ COMPLETE
- **P15 Scripts Reorganization - Phase 3** - api_utils.py decomposition with enhanced architecture
  - **api_utils.py is 4,766 lines** - being decomposed into modular structure
  - **Strategy Change**: Instead of simple code relocation, we're restructuring by **capability** with new features added

  - **Completed Modules:**
    | Location | Module | Lines | Contents |
    |----------|--------|-------|----------|
    | `_L3/utils/` | `team_utils.py` | ~60 | TEAM_NAMES, TEAM_ABBREVS, get_team_name, get_team_abbrev, clean_insight |
    | `_L3/utils/` | `bucket_definitions.py` | ~100 | BETTING_PROP_BUCKETS, GAME_PREVIEW_BUCKETS, PLAYER_ANALYSIS_BUCKETS, INCENTIVE_BUCKETS |
    | `_L3/utils/` | `player_utils.py` | ~450 | PLAYER_POSITIONS, PLAYER_TEAMS, TEAM_QBS/RBS/WRS, get_thesis_aligned_player, get_position_pose |
    | `_L3/analysis/` | `text_analysis.py` | ~500 | analyze_for_highlights, analyze_for_buckets, analyze_for_sentiment, extract_entities |

  - **NEW: `_L3/analysis/extraction/` subfolder** - 9 modules, unified extraction by capability:
    | Module | Purpose | Key Exports |
    |--------|---------|-------------|
    | `config.py` | Toggle + LLM utils + caching | set_llm_extraction, call_llm, cache_key |
    | `thesis.py` | Betting thesis (pass/run/situational) | extract_betting_thesis, get_thesis_description |
    | `insights.py` | Cover insights (setup/conflict/resolution) | extract_cover_insight, extract_all_insights |
    | `winner.py` | Winner prediction | extract_predicted_winner, get_winner_confidence, is_upset_pick |
    | `props.py` | **NEW** - Player prop extraction | PlayerProp, extract_player_props, format_prop_for_display |
    | `injuries.py` | **NEW** - Injury impact extraction | InjuredPlayer, InjuryStatus, position impact weights |
    | `spreads.py` | **NEW** - Spread/line analysis | SpreadInfo, NFL_KEY_NUMBERS, assess_spread_value |
    | `trends.py` | **NEW** - Momentum & historical trends | MomentumLevel, TrendType, extract_trends, get_momentum_score |
    | `confidence.py` | **NEW** - Betting confidence scoring | ConfidenceTier, extract_confidence, should_bet, get_unit_recommendation |

  - **Design Benefits:**
    - Single import: `from _L3.analysis import extract_trends, ConfidenceTier, should_bet`
    - Built-in caching for repeated extractions
    - 5 NEW capabilities (props, injuries, spreads, trends, confidence) for future content types
    - Backward-compatible `smart_*` wrappers

  - **Import Tests Passing:**
    - ✅ All 9 extraction modules import correctly
    - ✅ Parent `_L3/analysis/__init__.py` re-exports all extraction functions
    - ✅ Full import chain works: `from _L3.analysis import extract_confidence`

  - **NEW: `_L3/analysis/text_processing/` subfolder** - 8 modules, unified text processing:
    | Module | Purpose | Key Exports |
    |--------|---------|-------------|
    | `config.py` | LLM utils + text cleaning + caching | call_llm, clean_text, truncate_text |
    | `highlights.py` | Visual emphasis extraction | extract_highlights, HighlightPhrase |
    | `headlines.py` | **NEW** - Social headlines | generate_headline, HeadlineStyle, Platform |
    | `hooks.py` | **NEW** - Scroll-stopping hooks | generate_hook, HookStyle, HOOK_TEMPLATES |
    | `summarization.py` | Text condensing | summarize_to_length, create_tldr, extract_key_points |
    | `sentiment.py` | Tone analysis | analyze_sentiment, Sentiment, Tone |
    | `entities.py` | Entity extraction | extract_entities, extract_players, extract_stats |
    | `formatting.py` | **NEW** - Text formatting | format_for_carousel, format_spread, format_record |

  - **Total NEW Capabilities Added:**
    - **extraction/**: props, injuries, spreads, trends, confidence (5 new)
    - **text_processing/**: headlines, hooks, formatting (3 new)

  - **Import Tests All Passing:**
    - ✅ All 9 extraction modules import correctly
    - ✅ All 8 text_processing modules import correctly
    - ✅ Full chain: `from _L3.analysis.text_processing import generate_hook, HookStyle`

  - **NEW: `_L3/processors/` subfolder** - 2 modules, data transforms & prompt generation:
    | Module | Lines | Key Exports |
    |--------|-------|-------------|
    | `data_transforms.py` | ~400 | transform_matchup_for_carousel, transform_matchup_for_infographic, fetch_and_transform_matchup, get_mock_data, TEAM_STAR_PLAYERS |
    | `prompt_builders.py` | ~1300 | build_carousel_prompts, build_insights_carousel_prompts, build_dark_incentives_prompt, analyze_for_highlights |

  - **api_utils.py Shim Created:**
    - Added P15 migration re-exports at top of api_utils.py
    - `_PROMPT_BUILDERS_MIGRATED` and `_DATA_TRANSFORMS_MIGRATED` flags = True
    - Existing code continues to work (original implementations still present)
    - New code can import from modular locations directly

  - **Import Tests All Passing:**
    - ✅ `_L3/processors` imports work
    - ✅ `api_utils` backward compatibility imports work
    - ✅ Core pipeline scripts (content_pipeline, idea_creation, assembly, media_generation, distribution) all load successfully

  - **Phase 3 Complete** - All migrations done:
    - ✅ `data_transforms.py` (~500 lines) → `_L3/processors/data_transforms.py`
    - ✅ `prompt_builders.py` (~1500 lines) → `_L3/processors/prompt_builders.py`
    - ✅ api_utils.py shim tested and backward compatible

### December 29, 2025 - Session 77 (O77) ✅ COMPLETE
- **P15 Scripts Reorganization - Phase 1 & 2** - 8 files migrated successfully
  - Created `_L0` through `_L8` folder structure with 5-folder pattern (inputs/, analysis/, processors/, outputs/, utils/)
  - **8 files migrated successfully:**
    | Original | New Location | Status |
    |----------|--------------|--------|
    | `pil_processor.py` | `_L5/processors/pil_processor.py` | ✅ Working |
    | `ffmpeg_processor.py` | `_L5/processors/ffmpeg_processor.py` | ✅ Working |
    | `balldontlie_mcp.py` | `_L1/inputs/balldontlie_mcp.py` | ✅ Working |
    | `ai_models.py` | `_L1/inputs/ai_models.py` | ✅ Working |
    | `g_api_processor.py` | `_L3/analysis/g_api_processor.py` | ✅ Working |
    | `approve_ideas.py` | `_L3/utils/approve_ideas.py` | ✅ Working |
    | `calendar_config.py` | `_L2/utils/calendar_config.py` | ✅ Working |
    | `asset_ingestion.py` | `_L1/inputs/asset_ingestion.py` | ✅ Working |
  - **Shim pattern**: Original files now re-export from new locations for backward compatibility
  - **Rollback script**: `python3 scripts/_migration_rollback.py` (or `status` to check)
  - **All tests pass**: Core scripts (assembly, idea_creation, media_generation, distribution, content_pipeline) load correctly
  - **Path fixes applied**: Files with PROJECT_ROOT/ASSETS_DIR paths updated to navigate from new depth
  - **Next batch**: api_utils.py decomposition (4,763 lines → ~10 files)

### December 29, 2025 - Session 76 (O76) ✅ COMPLETE
- **Pocket Sessions P1-P20 Sync** - Comprehensive sync of all Pocket session work to main contexts
  - **Display Mode Registry (P9-P12)** - Created `config/display_modes.py` for centralized routing
    - Replaced scattered if/elif checks across L0-L7 with registry functions
    - New helpers: `is_carousel()`, `has_reels()`, `skip_logo()`, `get_slide_count()`
    - Future-proofed routing: new presets work automatically via registry
  - **dark_incentives Pipeline (P10)** - Full L0-L7 integration for incentive content
    - Manual input preset with `_collect_manual_incentive_data()` + `_run_l3_manual()`
  - **LLM-Powered Extraction (P9)** - Replaced regex with LLM functions
    - `extract_betting_thesis_llm()`, `extract_cover_insight_llm()`, `determine_predicted_winner_llm()`
    - Smart wrappers with global toggle (L0 menu: Tool Configuration → Toggle LLM Extraction)
  - **Week 17 Sunday Slate (P20)** - Generated all 11 Sunday insights carousels (66 slides + 66 reels)
    - Ink splatter intensity reduced from 30-100% to 15-40% permanently
    - Total cost: ~$0.132
  - **Meme Creation (P16-P17)** - Chargers wheelchair meme with FFmpeg vs OpenCV comparison
  - **Vision System Design (P18)** - Documented Vision vs Display Mode separation
- **Context Files Updated** - All session counts synced to P20
- **CRANK_CONTEXT Updated** - Week 17 generation queue marked complete
- **Health score**: 7.0/10, 0 critical, 71 warnings

### December 24, 2025 - Session 75 (O75) ✅ COMPLETE
- **D100 Carousel Architecture Cleanup** - Completed all cleanup tasks from D100 simplification
  - **Verified assemble_carousel() NOT deprecated** - Still needed as internal helper for logo overlay
    - Called by `assemble_carousel_reels()` at [assembly.py:1888](scripts/assembly.py#L1888)
    - Provides logo overlay step before reel conversion
  - **Updated documentation** - Fixed docstring in [assembly.py:1875](scripts/assembly.py#L1875)
    - Changed `reels_config` → `carousel_config` in Args section
  - **Verified carousel_illustrated_reels removed** - No code references found
    - Only historical references in context docs (appropriate to keep)
  - **Verified distribution.py carousel handling** - Working correctly
    - P13: Slides + reels now go together in `final/carousels/` folder
    - P13: `--animations` flag for ken_burns content (replaces `--static-videos`)
  - **Updated ARCHITECTURE.md** - Simplified carousel preset examples
    - Removed deprecated `carousel_illustrated_reels` preset
    - Added `illustrated_insights_carousel` preset
    - Added descriptions explaining D100 output format (1:1 slides + 9:16 MP4s)
  - **Cleared 🚩 NEEDS_ORACLE_PASS flag** in DEV_CONTEXT.md
- **Health Check Improvements** - Health score: 5.7 → 8.4/10 (+2.7 improvement)
  - Fixed 1 critical issue (CHANGELOG.md path corrected)
  - Resolved 7 warnings (unused imports, long functions accepted)
  - **CHANGELOG.md path fix**: Updated DEV_CONTEXT to reference correct location
  - **Accepted unused imports**: Path, Any in data_source.py; Any in content_pipeline.py
  - **Accepted 6 long functions**: Complex business logic in api_utils.py, distribution.py, assembly.py
  - **Cleaned stale script references**: Updated naming convention examples in DEV_CONTEXT
- **Session count**: D100 / O75 / C10 / P0

### December 23, 2025 - Session 74 (O74) ✅ COMPLETE
- **L1 Data Sources Deep Dive** - Comprehensive analysis of all L1 data sources
  - **SportsBlaze API** - Tested 4 endpoints:
    - Standings: 32 teams with records (regular season, home/away/division splits, win%)
    - Boxscores: 142 team stats per game (passing, rushing, receiving, defensive, special teams)
    - Rosters: 53-man rosters (name, position, height/weight, age, headshot URL)
    - Schedules: Season/weekly game lists
    - Note: No individual player game stats, only team aggregates
  - **BalldontLie MCP** - Free tier limitations confirmed:
    - ✅ Works: Teams, Games (with AP-style summaries), Players (basic info)
    - ❌ 401 Unauthorized: Standings, Season Stats, Injuries, Betting Odds
  - **GoatedBets API** - Remains primary for betting analysis/picks
- **ARCHITECTURE.md Updated** - Added comprehensive L1 documentation:
  - Data Source Comparison Matrix (10 data types × 3 sources)
  - Detailed endpoint documentation for each source
  - Sample data structures (standings JSON, boxscore stats list)
  - "Recommended Data Source Combinations" table for content types
  - Updated code snippet to reflect current data_source.py implementation
- **Critical Issue Fixed** - Moved hardcoded SportsBlaze API key to `.env`
  - Added `SPORTSBLAZE_API_KEY` to `.env` with expiration comment
  - Updated `data_source.py` to use `os.getenv()` + `load_dotenv()`
  - Health score improved: 5.8 → 7.8/10, critical issues: 1 → 0
- **Session count**: D98 / O74 / C10 / P0

### December 23, 2025 - Session 72 (O72) ✅ COMPLETE
- **PROJECT_INSTRUCTIONS.md Overhaul** - Complete rewrite for Claude Desktop integration
  - Added Four-Session Model documentation (D#/O#/C#/P#)
  - Added Multi-Machine Workflow section (iCloud sync, machine switching)
  - Added Claude Desktop Integration section (when to use Desktop vs Code)
  - Added Reusable Templates section (GitHub template repo)
  - Updated session counts: D98 / O72 / C10 / P0
  - Updated current state and available presets
  - Version 2.0 - Four-Session Model + Multi-Machine Workflow
- **File location**: `PROJECT_INSTRUCTIONS.md` in project root

### December 23, 2025 - Session 71 (O71) ✅ COMPLETE
- **Pocket Context Created** (`docs/context/POCKET_CONTEXT.md`)
  - New session type (P#) for portable MacBook Air usage
  - Full capability with efficiency-focused guidelines
  - Multi-machine workflow instructions (iCloud sync)
  - MacBook Air first-time setup commands included
- **GitHub Setup Complete**
  - SSH key generated and added to GitHub
  - Git configured with user credentials
  - Repository created: `w2csyh44qs-web/project-oracle-template` (private)
  - Marked as template repository for reuse
- **Reusable Templates Created** (`templates/`)
  - `DEV_CONTEXT_TEMPLATE.md` - Generic dev session template
  - `ORACLE_CONTEXT_TEMPLATE.md` - Generic maintenance template
  - `POCKET_CONTEXT_TEMPLATE.md` - Portable session template
  - `project_oracle_template.py` - Core health/audit tool (17KB)
  - `SETUP_GUIDE.md` - How to use templates for new projects
- **Four-Session Model Now Active**: D# / O# / C# / P#
- **Session count**: D98 / O71 / C10 / P0

### December 22, 2025 - Session 70 (O70) ✅ COMPLETE
- **Health Audit & Doc Sync Pass**
  - Fixed 3 doc references to archived scripts in ARCHITECTURE.md
    - `text_extraction.py` → `g_api_processor.py` (3 places)
    - `best_bets_workflow.py` → removed from file structure (archived)
  - Updated DEV_CONTEXT.md implementation plan to show COMPLETE
  - Health score improved: 8.2 → 8.5
- **D97 Documentation Sync**
  - Added `PipelineOrchestrator` and `PipelineContext` to ARCHITECTURE.md
  - Updated "Current Implementation (D97)" section with code examples
- **Optimization False Positive Fixes** (`project_oracle.py`)
  - Fixed test detection: Now checks `PROJECT_ROOT/tests/test_*.py`
  - Fixed cost tracking detection: Now checks for `APICallLogger` class
  - Optimization opportunities reduced: 51 → 10 (removed false positives)
- **Documentation Updates**
  - Added test running instructions to CURRENT STATE section
  - Updated Rule #20 with checklist for new API tools
- **Session count**: D98 / O70 / C10

### December 22, 2025 - Session 69 (O69) ✅ COMPLETE
- **Context Consolidation** - Major cleanup of ORACLE_CONTEXT.md
  - Reduced from 2015 lines to ~790 lines (61% reduction)
  - Archived O11-O65 session entries to CHANGELOG.md (Oracle Sessions Archive section)
  - Kept only O66-O68 recent sessions with full detail
  - Added milestone summary in place of detailed entries
- **New Rule #21: Context File Size Guard** - Prevents future bloat
  - Target: ~800 lines max, 3-5 recent sessions
  - Archive trigger: >50 sessions or >1500 lines
  - Session count updated: D97 / O69 / C9

### December 22, 2025 - Session 68 (O68) ✅ COMPLETE
- **Oracle Doc Ownership Clarified** - Enhanced Rule #15 and Detailed Docs Update Protocol
  - Added "⚠️ ORACLE OWNS ALL REFERENCE DOC SYNC" to Rule #15
  - Expanded protocol section with trigger table: which doc to update, when, from what source
  - Oracle syncs changes from ALL sessions (Dev, Oracle, Crank) to reference docs
  - No permission needed - Oracle has full authority
- **Context Consolidation Discussion** - User noted context files may be getting too long; merged approach preferred over new rules

### December 22, 2025 - Session 67 (O67) ✅ COMPLETE
- **Platform Architecture Model** - Major design documented in ARCHITECTURE.md
  - Each layer (L0-L8) is a "platform" with attached tools/processors
  - Presets define which layers are activated AND which tools each layer uses
  - Presets skip layers entirely (not no-op pass-through) for cleaner execution
  - New L1 `data_source.py` platform to unify all data fetching (GoatedBets, web search, local assets, etc.)
  - `truth_prompt_wrapper.py` moves from L5 to L3 (content processing belongs at ideation)
  - ✅ `meme_generator.py` converted to `meme_mashup` preset in L6 assembly.py (P6 - archived to `archive/deprecated/`)
- **Script Layer Map** - Complete mapping of all 21 scripts to their layers
  - Platform scripts (L0-L8 main orchestrators)
  - L1 tools (data fetchers)
  - L3 tools (content processing)
  - Shared processors (multi-layer utilities)
- **Implementation Tasks Defined** for Dev session (D96+):
  1. Create `data_source.py` (L1 platform)
  2. Update preset configs with `layers` array and `L*_tool` mappings
  3. Update `content_pipeline.py` to read preset layers
  4. Move `truth_prompt_wrapper.py` to L3
  5. ✅ Integrate `meme_generator.py` as `meme_mashup` preset (P6 complete)
- **Date/Season Confusion Fix** - Added "📅 CURRENT DATE & SEASON" section to all 3 context files
  - Prominent warning that 2025-2026 is current NFL season, NOT 2024-2025
  - Added to DEV_CONTEXT.md, ORACLE_CONTEXT.md, CRANK_CONTEXT.md
- **Crank Task List Cleared** - Week 16 marked complete in CRANK_CONTEXT.md
  - All illustrated carousel matchups generated (C9)
  - Week 17 template prepared for next schedule
- **Dev Context Updated** - Added O67 Platform Architecture Implementation as D96 priority task
  - 5 subtasks listed in Pending Tasks section
  - Week 16 carousels marked complete

### December 21, 2025 - Session 66 (O66)
- **Documentation sync** - Verified ARCHITECTURE.md already uses `assembled/` folder naming
- **regen_slide.py archived** - Script moved to `scripts/archive/`
  - Imports from deprecated `carousel_generator.py` (already archived)
  - Main pipeline handles regeneration, no need for separate tool
  - Updated pending task in both DEV_CONTEXT and ORACLE_CONTEXT

### December 21, 2025 - Session 65 (O65)
- **Naming Convention Rule Added** (Rule #21 in Session Rules)
  - Output file naming: `{visual_style}_{slide_type}.{ext}` → `illustrated_cover.mp4`, `dark_bonus.jpg`
  - Preset naming: `{content_type}_{visual_style}` → `carousel_illustrated`, `infographic_dark`
  - Matchup folders: `{away}_at_{home}` lowercase → `patriots_at_ravens/`
  - Intermediate folder: `week16/assembled/` (replaces `reels/`)
  - Final folders: `carousels/`, `animations/`, `infographics/` (P13 update)
- **Folder Structure Cleanup**
  - P13: Carousel slides + reels now go to SAME folder in `final/carousels/`
  - P13: Added `animations/` folder for ken_burns + effects (replaces `static_videos/`)
  - Created `final/infographics/` folder for future dark preset
  - Removed intermediate `week16/reels/` folder (superseded by `assembled/`)
  - Cleaned up duplicate folders (double underscores in matchup names)
- **Code Updates for New Structure**
  - **assembly.py**: Changed output from `reels/` to `assembled/` (line 1921-1923)
  - **distribution.py**:
    - P13: `find_animations()` / `distribute_animations()` (replaces static_videos methods)
    - Fixed matchup slug to use single underscore: `replace(' @ ', '_at_')`
    - P13: `--animations` flag for animation category content
- **Pipeline Verified**: Assembly → Distribution tested end-to-end
  - Assembly outputs to `week16/assembled/idea_001/`
  - P13: Carousel with reels goes to `final/carousels/{timestamp}_{matchup}/` (slides + reels together)
- **Session count**: D94 / O65 / C8

### December 21, 2025 - Session 64 (O64)
- **Three-Session Model Documentation Complete** - Updated ARCHITECTURE.md and WORKFLOW.md
  - **ARCHITECTURE.md**: Updated file structure to show `docs/context/` with all 3 context files (D#, O#, C#)
  - **ARCHITECTURE.md**: Updated Reference Documents table with all 3 context files and added reasoning style note to PHILOSOPHY.md
  - **WORKFLOW.md**: Rewrote section 2.1 as "Three-Session Model" with session table, count format, isolation principle
  - **WORKFLOW.md**: Rewrote section 5.1 as "Three-Session Roles & Scope" with all 3 sessions
  - **WORKFLOW.md**: Added Oracle's critical responsibility to capture meta-principles from user feedback
  - **WORKFLOW.md**: Added section 5.4 "Crank ↔ Dev Communication"
  - **WORKFLOW.md**: Updated cross-session flags to include Crank-specific flags (`NEEDS_DEV_FIX`, `GENERATION_IN_PROGRESS`)
  - **WORKFLOW.md**: Added step 2 to Oracle pass checklist: "Check for meta-principles in user feedback"
- **User Feedback Issue Addressed**: User noted that comments like "changes should be universal" and "limiting hardcoded things" were being ignored during Dev sessions. This session ensures these principles are now documented in:
  - PHILOSOPHY.md 2.3 (Reasoning & Thinking Style) - already done in O63
  - WORKFLOW.md 5.1 (Oracle's critical responsibility to capture principles)
- **Logo Reels Investigation** - User asked why logo isn't showing on carousel_reels
  - Traced code path: `assemble_carousel_reels()` → `assemble_carousel()` → `ImageOverlay.add_logo()`
  - D94 fix IS in place: lines 361-362 and 2031-2032 include `carousel_reels` in display_mode check
  - **Resolution**: Logo IS present in both 1:1 slides and 9:16 reels - user was looking at intermediate `week16/reels/` folder instead of `week16/final/reels/`
  - Verified by extracting logo area from both source slide and reel frame - both show GOATED BETS logo clearly
- **Distribution Fix for carousel_reels** - Fixed TypeError when distributing carousel_reels content
  - **Root cause**: `distribution.py` didn't handle `carousel_reels` type - `output_path` is a list of paths, not single path
  - **Fix in distribution.py**:
    - Added `self.reels_dir = f"{self.final_dir}/reels"` directory definition
    - Added `os.makedirs(self.reels_dir, exist_ok=True)` in directory creation
    - Added explicit `carousel_reels` type handler in `process_videos()` method
    - Now distributes BOTH slides to `final/carousels/` AND reels to `final/reels/{matchup}/`
  - Successfully ran distribution: Patriots @ Ravens content now in final folder
- **Session count**: D94 / O64 / C7

### Earlier Sessions (O11-O65) - Archived to CHANGELOG.md
**See `docs/CHANGELOG.md` > "Oracle Sessions Archive (O49-O68)" for details.**

Key milestones:
- O63-O65: PHILOSOPHY.md reasoning style, three-session docs, naming conventions
- O55-O62: Health monitor Phase 5, image meme research, script archival
- O33-O54: Health monitor Phases 1-4, optimization awareness, brand rules
- O11-O32: Core oracle capabilities (audit, sync, snapshot, status, diff)

## 🔧 SESSION WORKFLOW

| Trigger | Command | Claude Says |
|---------|---------|-------------|
| Session start | `audit --quick` (+ silent baseline) | "Checking project health... [result]" |
| Every ~10 exchanges | `status` | Nothing unless issues found |
| Every ~20 exchanges / breakpoints | `autosave` | "Autosaving... Done. [health score]" |
| Before sensed compaction | `autosave` | "Autosaving... Ready to compact or continue." |
| Weekly (manual) | `autosave --archive-changes` | "Autosaving with archive... Done." |

**Commands:**
```
SESSION START:    python3 maintenance/project_oracle.py audit --quick
                  (checks health + creates baseline silently)

DURING SESSION:   python3 maintenance/project_oracle.py status
                  (quick one-line health check)

EVERY ~20 EXCH:   python3 maintenance/project_oracle.py autosave
                  (sync + snapshot, minimal output)

BEFORE COMPACT:   python3 maintenance/project_oracle.py autosave
                  (ensures context is saved)
```

**Output locations:**
- Snapshots: `reports/snapshots/SNAPSHOT_[timestamp].md`
- Baselines: `reports/snapshots/SESSION_SNAPSHOT_latest.json`
- Audit reports: `reports/audits/ORACLE_REPORT_[timestamp].md`
- Session diffs: `reports/diffs/SESSION_DIFF_[timestamp].md`

---

## 📋 COMMANDS REFERENCE

### Core Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| **`autosave`** | 💾 Sync + snapshot + auto doc suggestions | **EVERY ~20 EXCHANGES / BREAKPOINTS** |
| `autosave -q` | Autosave without doc suggestions | When you want minimal output |
| `autosave --archive-changes` | Autosave + archive old changes | **WEEKLY** |
| `audit --quick` | Fast health check (+ silent baseline) | **SESSION START** |
| `audit` | Full health checks | After major features |
| `status` | ⚡ One-line health summary | Quick check anytime |
| `suggest-docs` | 📝 Suggest which docs need updating | After changes |
| `suggest-docs --staleness` | Show doc freshness times | Doc maintenance |
| `snapshot` | 📸 Full context snapshot with resume prompt | When you need verbose output |
| `snapshot -t "task"` | Snapshot with explicit task description | When task isn't clear |
| `report` | Generate full report | For review/archival |
| `config -v` | Show parsed configuration | Debug/verify parsing |
| `optimize` | Get optimization suggestions | When planning improvements |
| `diff --baseline` | Create baseline only (legacy) | Rarely needed now |

### Sync Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `sync` | Preview changes (dry-run) | Before applying |
| `sync --apply` | Update DEV_CONTEXT.md | Session start, before compaction |
| `sync --apply --all` | Check all reference docs (warnings) | After refactors |
| `sync --apply --all --fix` | Fix stale dates in reference docs | Weekly maintenance |
| `sync --apply --add-tasks` | Sync + add audit issues to Pending Tasks | Session end |
| `sync --apply --prune-tasks` | Remove completed tasks | After task completion |
| `sync --apply --archive-changes` | Move old Recent Changes to CHANGELOG | Periodically |

### Command Options

**Snapshot Options:**
- `--task, -t` - What you're currently working on
- `--file, -f` - Last file being edited
- `--decisions, -d` - Pending decisions that need resolution
- `--blockers, -b` - Current blockers

**Diff Options:**
- `--baseline` - Create lightweight baseline at SESSION START (fast, no audit)
- `--no-save` - Generate diff report but don't update the baseline

**Sync Options:**
- `--apply` - Actually write changes (default is dry-run preview)
- `--all` - Also check reference docs (ARCHITECTURE, README, etc.)
- `--fix` - Make safe targeted fixes (stale dates, add warning comments)
- `--add-tasks` - Add critical audit issues to Pending Tasks
- `--prune-tasks` - Remove completed tasks (✅, [x], COMPLETE, DONE)
- `--archive-changes` - Move old Recent Changes to docs/CHANGELOG.md
- `--context-only` - Only sync DEV_CONTEXT.md

### What --fix Mode Does (Safe Fixes Only)

| Doc | Fix Action | What It Won't Touch |
|-----|------------|---------------------|
| PROJECT_OVERVIEW.md | Updates stale date (>7 days) | Layer descriptions, prose |
| TOOLS_REFERENCE.md | Updates stale date (>30 days) | Pricing info, comparisons |
| ARCHITECTURE.md | Adds HTML warning comment | Any content |
| ORACLE_README.md | Updates timestamp | Session progress, features |

---

## 🖥️ TECHNICAL DETAILS

### File Locations

| File | Purpose |
|------|---------|
| `maintenance/project_oracle.py` | Main oracle script |
| `maintenance/ORACLE_README.md` | User-facing oracle documentation |
| `context/ORACLE_CONTEXT.md` | This file - maintenance session state |
| `context/DEV_CONTEXT.md` | Development session state (oracle reads for config) |
| `reports/audits/ORACLE_REPORT_*.md` | Audit reports |
| `reports/diffs/SESSION_DIFF_*.md` | Session diffs |
| `reports/snapshots/` | Context snapshots |

### Configuration Auto-Detection

Oracle reads `context/DEV_CONTEXT.md` to automatically detect:
- **Layers** - From "Pipeline Status" section
- **API Services** - From "API KEYS & MCPs" table
- **Scripts** - From "Current Workflow" section
- **Doc Files** - From "Document Purposes" table
- **MCPs** - From "MCP Servers" table
- **Pending Tasks** - From "PENDING TASKS" section

**No manual config needed** - keep DEV_CONTEXT.md updated and Oracle stays in sync.

### What Gets Parsed

```markdown
## Pipeline Status
✅ Layer 1: Trend Detection → output/all_trends.json
✅ Layer 2: Calendar & Segments → segments_config.json
...

## API KEYS & MCPs
| Key | Service | Layer | Status |
| OPENAI_API_KEY | GPT-4o-mini | L1, L3, L4 | ✅ Active |
...
```

Oracle extracts layer numbers, names, outputs, API keys, and which layers use which APIs.

### What Gets Checked

**Code Health:**
- Unused imports
- Functions over 100 lines
- TODO/FIXME comments
- Hardcoded credentials
- Syntax errors

**Documentation Drift:**
- Scripts mentioned in docs that don't exist
- Broken cross-references between docs
- Stale timestamps
- Missing required sections in DEV_CONTEXT.md

**Layer Health:**
- Missing layer scripts
- Import/syntax errors
- Output directories exist

**API Usage:**
- Missing API keys in .env
- API calls in code vs configured keys
- Cost tracking presence

**Context Health:**
- Required sections present
- Timestamp freshness
- Pending task accumulation
- Placeholder markers (TODO, TBD, etc.)

---

## ⏸️ GOOD COMPACTION POINTS

**Suggest compaction AFTER:**
- ✅ Completing a full feature (new command, new auditor)
- ✅ Finishing documentation updates
- ✅ Running a successful audit
- ✅ After resolving all pending tasks in a batch

**AVOID compaction during:**
- ❌ Mid-feature implementation
- ❌ Debugging issues
- ❌ Multi-step refactoring

**Compaction Prompt Template:**
"This is a good compaction point - [feature] is complete and tested. Ready to compact?"

---

## 🚨 CRITICAL REMINDERS

- **Oracle reads DEV_CONTEXT.md** to auto-configure - keep it updated
- **Don't modify scripts/** - that's the development session's job
- **Test commands** before documenting them
- **Backup files** are created automatically before writes
- **This file is truth** for maintenance sessions

---

## 🖥️ HEALTH MONITOR INTEGRATION

The health monitor (`maintenance/health_monitor.py`) runs persistently and reads oracle output.

### Shared State File

Oracle writes `reports/.health_status.json` after each command:

```json
{
  "timestamp": "...",
  "health_score": 7.6,
  "last_autosave": "...",
  "last_audit": "...",
  "issues": {
    "critical": 0,
    "warnings": 24,
    "long_functions": 10,
    "long_functions_ok": 10,
    "long_functions_new": 0,
    "unused_imports_ok": 0,
    "unused_imports_new": 0,
    "stale_refs": 0
  },
  "optimizations_pending": 17,
  "cost_today": 0.0
}
```

**Note:** `_ok` counts are items in acceptance lists (visible but don't lower score). `_new` counts are items flagged as warnings.

### Commands That Update Shared State

| Command | Updates |
|---------|---------|
| `status` | health_score |
| `audit` / `audit --quick` | health_score, issues |
| `autosave` | last_autosave, triggers monitor refresh |
| `optimize` | optimizations_pending |

### Starting Health Monitor

```bash
# Full dashboard (recommended)
python3 maintenance/health_monitor.py

# Minimized (single status line)
python3 maintenance/health_monitor.py --mode min

# Single check (no monitoring)
python3 maintenance/health_monitor.py --once
```

See `maintenance/ORACLE_README.md` for full documentation.

---

## 🔮 FUTURE PLANNING

See `optimization/IDEAS_BACKLOG.md` for consolidated future planning.

### Quick Reference

**Relevant sections in IDEAS_BACKLOG.md:**
- ~~YES > Automation > Oracle Health Monitor~~ ✅ IMPLEMENTED
- YES > Package Structure > `__init__.py` refactor
- MAYBE > Oracle Features > Context digest, automated triggers
- Reference > Multi-Agent Architecture

### Multi-Agent Support (Active)

Oracle supports dynamic multi-agent context management. To add a new agent:
1. Create `context/[AGENT]_CONTEXT.md`
2. Add path to `CONTEXT_FILES` list in `project_oracle.py`
3. Autosave will automatically manage all context files

See `maintenance/ORACLE_README.md` for details.

---

## ✅ SESSION END CHECKLIST

Before ending a maintenance session:
1. Update "Current State" section if capabilities changed
2. Update "Recent Changes" with today's work
3. Update "Pending Features" (add new, mark completed)
4. Run: `python3 maintenance/project_oracle.py snapshot`
5. Verify snapshot was created in `reports/snapshots/`

---

*Oracle Context Document - Maintenance session source of truth*
