# GOATED Content Automation - System Architecture V2

**Last Updated:** January 8, 2026
**Version:** 2.0 (V2 Media Engine)
**Purpose:** Technical architecture for the V2 dashboard-first content pipeline.

---

## Table of Contents

1. [Overview](#overview)
2. [V2 Architecture](#v2-architecture)
3. [Layer System (L0-L8)](#layer-system-l0-l8)
4. [Oracle System](#oracle-system)
5. [Sports Provider System](#sports-provider-system)
6. [API Endpoints](#api-endpoints)
7. [File Structure](#file-structure)
8. [Preset System](#preset-system)
9. [Tool Configuration](#tool-configuration)
10. [Dashboard Integration](#dashboard-integration)
11. [Testing](#testing)
12. [Reference Documents](#reference-documents)

---

## Overview

The GOATED Media Engine V2 is a **dashboard-first content automation pipeline** for multi-sport betting content. V2 wraps the proven V1 layer scripts with a modern Flask/React architecture.

**Key V2 Principles:**
- **Dashboard-First**: Web UI is primary interface, CLI for automation/scripting
- **Adapter Pattern**: V2 adapters wrap V1 scripts without modifying them
- **Multi-Sport**: SportProvider abstraction (NFL weekly, NBA daily calendars)
- **Cross-Session**: Oracle daemon coordinates Dev/Dash/Crank/Pocket contexts
- **SSE Progress**: Real-time layer progress via Server-Sent Events

For philosophy and design principles, see **PHILOSOPHY.md**.

---

## V2 Architecture

### High-Level Flow

```
User (Browser)
    |
Dashboard Frontend (React + Vite)
    | HTTP/SSE
Dashboard Backend (Flask)
    |
PipelineOrchestrator
    |
[L1 -> L2 -> L3 -> L4 -> L5 -> L6 -> L7 -> L8] Adapters
    |
V1 Scripts (scripts/*.py)
```

### Backend Structure (`app/`)

```
app/
├── __init__.py              # Package init
├── config.py                # Flask configuration
├── main.py                  # Flask entry point (port 5001)
├── api/
│   ├── sse.py               # SSE utilities
│   └── routes/              # API route modules
│       ├── auth.py          # Google OAuth
│       ├── jobs.py          # Job CRUD + streaming
│       ├── presets.py       # Preset management
│       ├── sports.py        # Sport/matchup queries
│       ├── outputs.py       # Output file serving
│       ├── health.py        # Oracle health endpoints
│       ├── sync.py          # Google Drive sync
│       └── scheduler.py     # Cron job scheduling
├── core/
│   ├── pipeline/
│   │   ├── orchestrator.py  # Pipeline controller
│   │   └── adapters/        # Layer adapters (L1-L8)
│   │       ├── base.py      # BaseAdapter class
│   │       ├── l1_adapter.py  # Data Source
│   │       ├── l2_adapter.py  # Calendar
│   │       ├── l3_adapter.py  # Ideas
│   │       ├── l4_adapter.py  # Audio
│   │       ├── l5_adapter.py  # Media
│   │       ├── l6_adapter.py  # Assembly
│   │       ├── l7_adapter.py  # Distribution
│   │       └── l8_adapter.py  # Analytics
│   └── sports/
│       ├── base.py          # SportProvider, CalendarType
│       ├── registry.py      # Provider lookup
│       └── providers/
│           ├── nfl.py       # NFL: 32 teams, weekly
│           └── nba.py       # NBA: 30 teams, daily
├── models/
│   ├── user.py              # User model (OAuth)
│   ├── preset.py            # Preset model
│   ├── job.py               # Job model
│   ├── output.py            # Output model
│   ├── scheduled_job.py     # ScheduledJob model
│   ├── api_usage.py         # APIUsage tracking
│   └── oracle.py            # Session, Message, Snapshot, HealthStatus
├── services/
│   ├── auth_service.py      # Google OAuth + Drive scope
│   ├── job_service.py       # Job execution + SSE
│   ├── preset_service.py    # DB + JSON fallback
│   ├── gdrive_service.py    # Google Drive sync
│   ├── oracle_service.py    # Health monitoring
│   └── scheduler_service.py # Cron scheduling
└── db/
    ├── __init__.py          # Central db instance
    └── session.py           # Session utilities
```

### Oracle System (`oracle/`) - P23 Brain Cell Architecture + P25 Dynamic Context

```
oracle/
├── __init__.py              # Package exports
├── project_oracle.py        # Central CLI orchestrator (~370 lines)
├── seeg.py                  # Real-time monitoring dashboard (stereoEEG metaphor)
├── ORACLE_README.md         # Oracle documentation
├── context_registry.json    # P25: Dynamic context definitions (contexts, handoff rules, ports)
│
├── context/                 # Context & session management
│   ├── __init__.py          # P25: Registry loader functions (get_context_ids, get_handoff_rules, etc.)
│   ├── astrocytes.py        # Context health, snapshots, parsing (~911 lines)
│   ├── context_manager.py   # File watching, activity tracking (~473 lines)
│   ├── daemon.py            # Cross-session orchestration (~483 lines)
│   └── session_spawner.py   # VS Code/Claude Code spawning - P25: uses registry (~594 lines)
│
├── maintenance/             # Audit, cleanup, debugging
│   ├── __init__.py
│   ├── microglia.py         # Error detection, cleanup + Glial utilities (~1,000 lines)
│   └── config.json          # Health monitor configuration
│
├── optimization/            # Performance & efficiency
│   ├── __init__.py
│   └── oligodendrocytes.py  # API costs + Synapses connection functions (~850 lines)
│
├── sync/                    # Documentation & knowledge flow
│   ├── __init__.py
│   └── ependymal.py         # Doc sync, reports (~800 lines)
│
├── project/                 # Project-specific tools
│   ├── __init__.py
│   └── cortex.py            # Presets, layers (~340 lines)
│
├── reports/                 # Output files
│   ├── audits/
│   ├── snapshots/
│   └── .health_status.json  # Shared health state for sEEG
│
└── docs/                    # Documentation
    ├── context/             # Session context files
    ├── overview/            # Reference docs
    ├── plans/               # Implementation plans
    └── archive/             # Old versions
```

### Brain Cell Modules

| Module | Location | Responsibility |
|--------|----------|----------------|
| Microglia | `maintenance/microglia.py` | Audit, clean, debug + Glial support utilities |
| Astrocytes | `context/astrocytes.py` | Status, context, snapshot |
| Oligodendrocytes | `optimization/oligodendrocytes.py` | Optimize, api-log + Synapses connections |
| Ependymal | `sync/ependymal.py` | Sync, docs, report |
| Cortex | `project/cortex.py` | Presets, layers |
| sEEG | `seeg.py` | Real-time monitoring |

### Frontend Structure (`dashboard/frontend/`)

```
dashboard/frontend/
├── src/
│   ├── App.jsx              # Main app with routing
│   ├── components/
│   │   ├── SportSelection.jsx
│   │   ├── MatchupSelection.jsx
│   │   ├── PresetSelection.jsx
│   │   ├── PresetBuilder.jsx
│   │   ├── PresetEditor.jsx
│   │   ├── PresetPreview.jsx
│   │   ├── GenerationFlow.jsx
│   │   ├── ProgressTracker.jsx
│   │   ├── SchedulerPage.jsx
│   │   ├── ScheduleEditor.jsx
│   │   ├── LoginPage.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── UserProfile.jsx
│   ├── contexts/
│   │   ├── AuthContext.jsx
│   │   ├── AppContext.jsx
│   │   └── JobContext.jsx
│   ├── hooks/               # Custom React hooks
│   └── services/
│       └── api.js           # Axios instance + endpoints
├── public/
│   └── assets/branding/     # Logo, brand assets
└── package.json
```

---

## Layer System (L0-L8)

### Adapter Pattern

V2 adapters wrap V1 scripts without modifying them:

```python
# Example: L1Adapter
class L1Adapter(BaseAdapter):
    def fetch(self, context: PipelineContext) -> AdapterResult:
        # 1. Setup sys.path for V1 imports
        # 2. Import V1 script functions
        # 3. Call V1 functions with context
        # 4. Emit SSE progress events
        # 5. Return AdapterResult
```

### Layer Reference

| Layer | Purpose | Adapter Method | V1 Script |
|-------|---------|----------------|-----------|
| L1 | Data fetching (APIs, web search) | `fetch()` | L1_data.py |
| L2 | Calendar & segment config | `configure()` | L2_calendar.py |
| L3 | Content idea generation | `generate()` | L3_ideas.py |
| L4 | TTS audio generation | `generate()` | L4_audio.py |
| L5 | Image/video generation | `generate()` | L5_media.py |
| L6 | Content assembly | `assemble()` | L6_assembly.py |
| L7 | Platform distribution | `distribute()` | L7_distribution.py |
| L8 | Analytics & feedback | `analyze()` | L8_analytics.py |

### Pipeline Execution

```python
from app.core.pipeline.orchestrator import run_pipeline, run_pipeline_to_layer

# Full pipeline (all 8 layers)
context = run_pipeline(job_id, preset_config, progress_callback)

# Partial execution - stop after L5
context = run_pipeline_to_layer(job_id, preset_config, "L5", progress_callback)
```

### Default Layer Configurations

```python
# Typical carousel preset
layers = ["L1", "L3", "L5", "L6", "L7"]

# Full pipeline with audio
layers = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]

# Quick test (data only)
layers = ["L1"]
```

---

## Oracle System

The Oracle daemon provides cross-session coordination for the 5-context system.

### P25 Dynamic Context Registry

Context definitions, handoff rules, and ports are now config-driven via `oracle/context_registry.json`. This makes Oracle project-agnostic.

**Registry Structure:**
```json
{
  "contexts": [
    {"id": "oracle", "prefix": "O", "name": "Oracle", "file": "ORACLE_CONTEXT.md", ...},
    {"id": "dev", "prefix": "D", ...}
  ],
  "handoff_rules": {"dash": {"to": ["dev", "crank"], "types": [...]}},
  "ports": {"normal": {"backend": 5001, "frontend": 5173}, "fallback": {...}},
  "context_path": "oracle/docs/context/"
}
```

**Registry Loader:** `oracle/context/__init__.py`
```python
from oracle.context import get_context_ids, get_context, get_handoff_rules, get_ports
```

**Session Tracking:** Only ORACLE_CONTEXT.md tracks all session counts (SESSION REGISTRY table).

### Contexts

| Context | Role | Scope |
|---------|------|-------|
| **Oracle** | System coordinator | Health, docs, cross-session orchestration |
| **Dev** | Backend development | `app/`, `scripts/`, `config/` |
| **Dash** | Frontend development | `app/frontend/` |
| **Crank** | Content production | Generation queue, quality review |
| **Pocket** | M1 Air portable | Fallback ports (5002/5174) |

### Daemon Commands

```bash
# Start daemon (P23: moved to oracle/context/)
python oracle/context/daemon.py start
python oracle/context/daemon.py start --fallback  # Pocket mode

# Check status
python oracle/context/daemon.py status

# Spawn sessions
python oracle/context/daemon.py spawn dev --task "Fix L3 adapter"
python oracle/context/daemon.py spawn dash --claude

# Cross-session messaging
python oracle/context/daemon.py send dev dash "New API ready"
python oracle/context/daemon.py messages --context dev

# View handoff rules
python oracle/context/daemon.py rules

# Health audit
python oracle/context/daemon.py audit --quick
python oracle/context/daemon.py audit

# Show resume prompts
python oracle/context/daemon.py prompts
```

### Cross-Session Handoff Rules

```
Dash → Dev: custom_preset_request, api_change_request, backend_bug
Dash → Crank: content_generation_request
Crank → Dev: bug_report
Crank → Dash: content_ready
Dev → Dash: new_feature_available, preset_added, api_updated
Dev → Crank: preset_fixed, new_preset
Oracle → All: health_alert, task_assignment
Pocket → Oracle: sync_complete, fallback_active
```

### Context Manager Features

| Feature | Description |
|---------|-------------|
| File watching | Monitors `app/`, `dashboard/`, `oracle/` for activity |
| Context detection | Determines active context from recent file changes |
| Activity tracking | Records file modifications per context |
| Snapshot creation | Creates context snapshots on demand |
| Message interface | Send/receive messages between contexts |

### Session Spawner Features

| Feature | Description |
|---------|-------------|
| VS Code spawn | Opens project with correct context file |
| Claude Code spawn | Starts Claude session with context prompt |
| Session tracking | Records sessions in database |
| Resume prompts | Generates context-specific resume prompts |

---

## Sports Provider System

SportProvider abstraction handles different sports with their unique calendar types.

### Calendar Types

| Sport | CalendarType | Period Format | Example |
|-------|--------------|---------------|---------|
| NFL | WEEKLY | phase + week | `week18` |
| NBA | DAILY | YYYY-MM-DD | `2026-01-06` |
| MLB | DAILY | YYYY-MM-DD | `2026-04-15` |
| NHL | DAILY | YYYY-MM-DD | `2026-01-06` |
| EPL | WEEKLY | matchday | `matchday20` |

### Usage

```python
from app.core.sports import get_provider, SportRegistry

# Get provider for a sport
nfl = get_provider("nfl")
nba = get_provider("nba")

# Provider interface
nfl.get_current_period()  # {"phase": "regular_season", "week": "week18"}
nba.get_current_period()  # {"date": "2026-01-06", "season": "2025-26"}

nfl.get_teams()           # Dict[str, TeamData] - 32 teams
nba.get_teams()           # Dict[str, TeamData] - 30 teams

nfl.get_matchups("week18")     # List[MatchupData]
nba.get_matchups("2026-01-06") # List[MatchupData]
```

### Data Source Priority

1. **balldontlie** (PRIMARY) - Most reliable, well-documented API
2. **SportsBlaze** (SECONDARY) - NFL stats enrichment
3. **GoatedBets** (TERTIARY) - Betting analysis content

---

## API Endpoints

### Jobs API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/jobs` | POST | Create job, queue for execution |
| `/jobs` | GET | List jobs with pagination |
| `/jobs/:id` | GET | Job details + logs |
| `/jobs/:id/stream` | GET | SSE progress (real layer events) |
| `/jobs/:id` | DELETE | Cancel job |

### Presets API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/presets` | GET | List all presets (DB + JSON fallback) |
| `/presets/:id` | GET | Get preset details |
| `/presets` | POST | Create custom preset (auth required) |
| `/presets/:id` | PUT | Update custom preset |
| `/presets/:id` | DELETE | Delete custom preset |
| `/presets/:id/clone` | POST | Clone preset for customization |
| `/presets/seed` | POST | Seed system presets to database |
| `/presets/layers/:layer` | GET | Get layer-specific presets |
| `/presets/tools` | GET | Get tool configuration |

### Sports API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sports` | GET | List all supported sports |
| `/sports/:sport` | GET | Sport details with current period |
| `/sports/:sport/teams` | GET | Teams with filtering |
| `/sports/:sport/calendar` | GET | Sport-aware calendar structure |
| `/sports/:sport/matchups` | GET | Matchups for period |
| `/sports/:sport/playoffs` | GET | Playoff matchups with round filter |

### Health API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check with score |
| `/health/oracle` | GET | Detailed health breakdown |
| `/health/pipeline` | GET | All 8 layer statuses |
| `/health/costs` | GET | API cost summary |
| `/health/jobs` | GET | Job statistics |
| `/health/db` | GET | Database connectivity |
| `/health/full` | GET | Complete status in one call |

### Scheduler API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scheduler` | GET | List user's schedules |
| `/scheduler` | POST | Create a new schedule |
| `/scheduler/:id` | GET | Get schedule details |
| `/scheduler/:id` | PUT | Update a schedule |
| `/scheduler/:id` | DELETE | Delete a schedule |
| `/scheduler/:id/trigger` | POST | Manually trigger schedule |
| `/scheduler/presets` | GET | Get common schedule presets |
| `/scheduler/validate` | POST | Validate cron expression |
| `/scheduler/due` | GET | Get schedules due to run |

### Sync API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sync/status` | GET | Check Drive sync configuration |
| `/sync/folder` | POST | Sync local folder to Drive |
| `/sync/job/:job_id` | POST | Sync job outputs to Drive |
| `/sync/files` | GET | List files in Drive folder |
| `/sync/upload` | POST | Upload single file to Drive |

### Auth API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | GET | Get Google OAuth URL |
| `/auth/callback` | GET | OAuth callback handler |
| `/auth/me` | GET | Current user info |
| `/auth/logout` | POST | Logout and revoke token |

---

## File Structure

### Project Root

```
AutomationScript/
├── app/                        # V2 Flask backend
├── oracle/                     # Cross-session daemon
├── dashboard/                  # React frontend
│   ├── backend/                # Dashboard backend (legacy, merged to app/)
│   └── frontend/               # React + Vite
├── app/core/pipeline/          # V2 layer scripts (moved from scripts/)
│   ├── orchestrator.py         # Pipeline controller
│   ├── adapters/               # Layer adapters (L1-L8)
│   └── layers/                 # Layer scripts & tools
│       ├── _L1/                # L1: Data sourcing
│       │   ├── L1_data.py
│       │   └── inputs/         # AI models, odds fetcher, trend detector
│       ├── _L2/                # L2: Calendar config
│       │   ├── L2_calendar.py
│       │   └── processors/     # Segment organizers
│       ├── _L3/                # L3: Idea generation
│       │   ├── L3_ideas.py
│       │   └── utils/          # API utils modules (29 files)
│       ├── _L4/                # L4: Audio generation
│       │   ├── L4_audio.py
│       │   └── processors/     # audio_processor.py (transcription, subtitles)
│       ├── _L5/                # L5: Media generation
│       │   ├── L5_media.py
│       │   └── processors/     # Image, Nano Banana
│       ├── _L6/                # L6: Assembly
│       │   ├── L6_assembly.py
│       │   └── processors/     # video_effects.py (parallax, split screen)
│       ├── _L7/                # L7: Distribution
│       │   └── L7_distribution.py
│       └── _L8/                # L8: Analytics
│           └── L8_analytics.py
├── archive/v1/                 # Archived V1 scripts
│   └── scripts_active_2026-01-07/
├── config/
│   ├── script_presets.json     # Preset definitions
│   ├── tool_config.json        # Tool selections (V2 tool keys)
│   ├── tool_resolver.py        # Tool resolution logic + aliases
│   ├── platforms.py            # Platform definitions
│   └── nfl_calendar.py         # NFL season structure
├── oracle/docs/                # All documentation (V2)
│   ├── context/                # Session context files
│   │   ├── ORACLE_CONTEXT.md
│   │   ├── DEV_CONTEXT.md
│   │   ├── DASHBOARD_CONTEXT.md
│   │   ├── CRANK_CONTEXT.md
│   │   └── POCKET_CONTEXT.md
│   ├── overview/               # Reference docs
│   │   ├── ARCHITECTURE.md     # This file
│   │   ├── PHILOSOPHY.md
│   │   ├── WORKFLOW.md
│   │   ├── TOOLS_REFERENCE.md
│   │   ├── CODE_HISTORY.md
│   │   └── CHANGELOG.md
│   ├── archive/                # Archived docs and contexts
│   └── plans/                  # Implementation plans
├── content/                    # Generated content
│   └── nfl/2025-2026/
│       └── regular_season/
│           └── week18/
│               ├── media/      # L5 output
│               ├── assembled/  # L6 output
│               └── final/      # L7 output
├── data/                       # Oracle daemon data
│   ├── oracle.db               # SQLite database
│   ├── .oracle_status.json     # Daemon status
│   └── .oracle_messages.json   # Message queue
├── reports/                    # Health reports
├── assets/                     # Static assets
├── venv/                       # Python virtual environment
├── .env                        # API keys (git-ignored)
└── README.md
```

---

## Preset System

### Preset Structure

```json
{
  "name": "carousel_illustrated",
  "output_type": "carousel",
  "layers": ["L1", "L3", "L5", "L6", "L7"],
  "L1_tool": "goatedbets_api",
  "L3_tool": "carousel_script",
  "L5_tool": "nano_banana",
  "L6_tool": "reel_converter",
  "sports": ["nfl", "nba"],
  "aspect_ratio": {
    "working": "1:1",
    "final": "9:16"
  },
  "slides": 6,
  "description": "6-slide prop carousel with insights"
}
```

### Preset Resolution Order

```
1. CLI override (--preset, --source, etc.)
   ↓
2. Preset tool selections (preset config)
   ↓
3. User tool_config.json defaults
   ↓
4. System defaults / fallbacks
```

### Database + JSON Fallback

PresetService loads presets with priority:
1. **Database presets** (user-created, cloned)
2. **JSON presets** (`config/script_presets.json`)
3. Auto-seeds 20 system presets on startup

---

## Tool Configuration

### Configuration File

**Location:** `config/tool_config.json`

```json
{
  "data_sources": {
    "selected": "tavily_websearch",
    "fallback": "perplexity_search",
    "options": ["tavily_websearch", "perplexity_search", "goatedbets_api"]
  },
  "content_generation": {
    "selected": "perplexity",
    "fallback": "gpt-4o-mini",
    "options": ["perplexity", "gemini", "gpt-4o", "gpt-4o-mini"]
  },
  "tts": {
    "selected": "elevenlabs",
    "fallback": "openai",
    "options": ["elevenlabs", "openai", "coqui"]
  },
  "image_gen": {
    "selected": "flux_fal",
    "fallback": "pexels",
    "options": ["flux_fal", "dalle3", "pexels", "pixabay"]
  }
}
```

### ToolResolver

```python
from config.tool_resolver import tool_resolver

# Basic resolution
model = tool_resolver.resolve_tool('content_generation')

# With CLI override
model = tool_resolver.resolve_tool('content_generation', vision_override=args.model)

# Get source config
source_cfg = tool_resolver.get_source_config('tavily_websearch')
```

---

## Dashboard Integration

### User Flow

1. **Sport Selection** - Choose NFL, NBA, etc.
2. **Matchup Selection** - Pick game/matchup for content
3. **Preset Selection** - Choose preset or build custom
4. **Generation** - Real-time progress via SSE
5. **Output Gallery** - Browse, preview, download outputs

### Brand Color System

```css
:root {
  --goat-gold: #f59e0b;       /* Primary CTAs, logo glow */
  --goat-gold-light: #fbbf24;
  --goat-purple: #8b5cf6;     /* UI elements, indicators */
  --goat-purple-text: #c4b5fd; /* Readable purple on dark */
  --success: #22c55e;         /* Selection states */
  --bg-primary: #0f1419;
  --bg-secondary: #1a1f2e;
}
```

### Ports

| Service | Normal Mode | Fallback (Pocket) |
|---------|-------------|-------------------|
| Backend | 5001 | 5002 |
| Frontend | 5173 | 5174 |

---

## Testing

### Start V2 Backend

```bash
cd "AutomationScript" && source venv/bin/activate
python3 -m app.main  # Port 5001
```

### Start Frontend

```bash
cd dashboard/frontend
npm run dev  # Port 5173
```

### Test Adapters

```bash
python3 -c "from app.core.pipeline.adapters import *; print('All 8 adapters OK')"
```

### Test Orchestrator

```python
python3 -c "
from app.core.pipeline.orchestrator import PipelineOrchestrator
o = PipelineOrchestrator('test', {'layers': ['L1','L2','L3','L4','L5','L6','L7','L8']})
for l in ['L1','L2','L3','L4','L5','L6','L7','L8']:
    print(f'{l}: {\"OK\" if o._get_adapter(l) else \"FAIL\"}')
"
```

### Oracle Health Audit

```bash
python oracle/daemon.py audit --quick
```

---

## Reference Documents

| Document | Purpose |
|----------|---------|
| **ARCHITECTURE.md** | This file - V2 technical specs |
| **PHILOSOPHY.md** | Design principles, reasoning style |
| **WORKFLOW.md** | Cross-session handoffs, daemon usage |
| **TOOLS_REFERENCE.md** | API pricing, tool capabilities |
| **STYLE_GUIDE.md** | Visual presets, brand guidelines |
| **CODE_HISTORY.md** | Session history, ADRs |
| **IDEAS_BACKLOG.md** | Feature backlog |
| **BRAND_RULES.md** | Brand colors, logo usage |
| **UX_RULES.md** | Dashboard-first UI patterns |

### Context Files

| Context | When to Read |
|---------|--------------|
| **ORACLE_CONTEXT.md** | Every Oracle session (O#) |
| **DEV_CONTEXT.md** | Every Dev session (D#) |
| **DASHBOARD_CONTEXT.md** | Every Dashboard session (DB#) |
| **CRANK_CONTEXT.md** | Every Crank session (C#) |
| **POCKET_CONTEXT.md** | Every Pocket session (P#) |

---

*This document captures the V2 architecture of the GOATED Media Engine. Update when architecture changes.*
