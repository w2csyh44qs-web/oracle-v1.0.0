# Media Engine V2 - Comprehensive Implementation Plan

**Created:** January 5, 2026
**Target:** MVP in 2 weeks, full V2 in 4 weeks
**Approach:** Clean Build First (archive v1, new structure at root)
**Project Name:** Media-Engine-V2

---

## Executive Summary

Transform the current CLI-based 8-layer pipeline into a **Dashboard-first** multi-user content generation platform with:
- **Google OAuth** authentication
- **SQLite** persistence (jobs, presets, outputs, users)
- **SSE + REST** for real-time updates
- **Custom preset builder** with integrated Vision settings
- **G Drive bidirectional sync** (outputs + asset ingestion)
- **3 dynamic auto-updating contexts** (SYSTEM, PIPELINE, DASHBOARD)
- **Oracle as background control center** with session spawning
- **All 5 sports** (NFL + NBA for MVP)

---

## Part 1: Architecture Overview

### 1.1 New Folder Structure

**Key naming decisions:**
- `scripts/` → `utils/` (more intuitive)
- Layer structure `_L*/` preserved (familiar organization)
- Main layer files can stay at pipeline root OR move into `_L*/` folders

```
Media-Engine-V2/                  # Renamed from AutomationScript
├── archive/v1/                   # Complete archive of current codebase (READ-ONLY reference)
│
├── app/                          # Main Python package
│   ├── api/                      # REST API layer
│   │   ├── routes/               # auth, jobs, presets, sports, outputs, gdrive, health
│   │   ├── sse.py                # Server-Sent Events handler
│   │   └── middleware.py         # Auth middleware
│   │
│   ├── core/                     # Business logic
│   │   ├── pipeline/             # L0-L8 layer orchestration
│   │   │   ├── orchestrator.py   # Main pipeline controller (was L0_pipeline.py)
│   │   │   ├── context.py        # PipelineContext dataclass
│   │   │   └── layers/           # **PRESERVED _L* STRUCTURE**
│   │   │       ├── _L0/          # Entry point utils
│   │   │       │   └── utils/
│   │   │       │       └── llm_config.py
│   │   │       ├── _L1/          # Data fetching
│   │   │       │   ├── inputs/   # balldontlie_mcp, odds_fetcher, web_search, etc.
│   │   │       │   └── L1_data.py
│   │   │       ├── _L2/          # Calendar/planning
│   │   │       │   ├── processors/
│   │   │       │   └── L2_calendar.py
│   │   │       ├── _L3/          # Content ideation
│   │   │       │   ├── analysis/
│   │   │       │   │   ├── extraction/
│   │   │       │   │   └── text_processing/
│   │   │       │   ├── processors/
│   │   │       │   │   ├── data_transforms.py
│   │   │       │   │   └── prompt_builders.py
│   │   │       │   ├── utils/
│   │   │       │   │   ├── api_utils.py
│   │   │       │   │   ├── player_utils.py
│   │   │       │   │   └── team_utils.py
│   │   │       │   └── L3_ideas.py
│   │   │       ├── _L4/          # Audio/TTS
│   │   │       │   └── L4_audio.py
│   │   │       ├── _L5/          # Media generation
│   │   │       │   ├── processors/
│   │   │       │   │   ├── pil_processor.py
│   │   │       │   │   └── ffmpeg_processor.py
│   │   │       │   └── L5_media.py
│   │   │       ├── _L6/          # Assembly
│   │   │       │   └── L6_assembly.py
│   │   │       ├── _L7/          # Distribution
│   │   │       │   └── L7_distribution.py
│   │   │       └── _L8/          # Analytics (placeholder)
│   │   │           └── L8_analytics.py
│   │   │
│   │   ├── presets/              # Preset management
│   │   ├── sports/               # Multi-sport providers (nfl, nba, mlb, nhl, epl)
│   │   └── tools/                # Tool integrations (llm, tts, image, video)
│   │
│   ├── services/                 # Application services
│   │   ├── auth_service.py       # Google OAuth
│   │   ├── job_service.py        # Job queue management
│   │   ├── scheduler_service.py  # **NEW: Cron/scheduled jobs**
│   │   ├── gdrive_service.py     # G Drive sync
│   │   └── context_service.py    # Dynamic context management
│   │
│   ├── models/                   # SQLAlchemy models
│   └── db/                       # Database layer + migrations
│
├── dashboard/                    # React frontend (existing, enhanced)
│   └── src/
│       ├── pages/                # Login, Dashboard, Presets, History, Gallery, Settings, **Calendar**
│       ├── components/           # Reusable components
│       ├── contexts/             # Auth, App, SSE contexts
│       └── services/             # API client, SSE client
│
├── oracle/                       # Background service (control center)
│   ├── daemon.py                 # Background service entry
│   ├── health_monitor.py         # Terminal dashboard (enhanced)
│   ├── context_manager.py        # Dynamic context file management
│   ├── scheduler.py              # **NEW: Cron job scheduler integration**
│   └── session_spawner.py        # VS Code session spawning
│
├── config/                       # Configuration files
│   ├── presets/                  # system_presets.json (migrated)
│   ├── tools.json                # Tool configuration
│   ├── brand_rules.json          # Brand enforcement
│   ├── schedules.json            # **NEW: Scheduled job definitions**
│   └── sports/                   # Per-sport config (nfl.json, nba.json, etc.)
│
├── assets/                       # Static assets (logos, fonts, templates)
├── data/                         # Runtime data (oracle.db, cache/, temp/)
├── content/                      # Generated outputs ({sport}/{season}/{phase}/{period}/)
├── docs/                         # Documentation
│   ├── context/                  # 3 dynamic context files
│   │   ├── SYSTEM_CONTEXT.md     # Oracle/maintenance state
│   │   ├── PIPELINE_CONTEXT.md   # Dev/crank merged state
│   │   └── DASHBOARD_CONTEXT.md  # Web UI state
│   └── overview/                 # Reference docs (ARCHITECTURE, PHILOSOPHY, etc.)
├── tests/
└── utils/                        # Utility scripts (was: scripts/)
    ├── migrate.py                # V1 to V2 migration
    └── start_dev.sh              # Development startup
```

### 1.2 Database Schema (SQLite)

```sql
-- Core tables
users (id, google_id, email, name, picture_url, role, gdrive_folder_id, preferences)
presets (id, preset_id, user_id, name, description, output_type, layers, tools, tone, format, visual_style, ...)
jobs (id, job_id, user_id, preset_id, sport, matchup, season, week, status, current_layer, progress, logs, ...)
outputs (id, job_id, user_id, file_type, file_path, gdrive_id, gdrive_url, sync_status, metadata, ...)

-- Automation tables (NEW)
scheduled_jobs (id, user_id, preset_id, sport, cron_expression, enabled, last_run, next_run, config)
job_calendar (id, scheduled_job_id, run_date, job_id, status)  -- For calendar view

-- Oracle tables (replaces JSON files)
sessions (session_id, context, task, status, started_at, last_activity)
messages (id, from_context, to_context, message_type, content, priority, created_at, read_at)
snapshots (id, context, session_id, data, created_at)
health_status (id, health_score, critical_count, warning_count, data, created_at)

-- API usage tracking (cost management from IDEAS_BACKLOG)
api_usage (id, user_id, job_id, provider, endpoint, cost_usd, created_at)
```

### 1.3 API Endpoints

| Category | Endpoints |
|----------|-----------|
| **Auth** | `POST /auth/google`, `POST /auth/refresh`, `POST /auth/logout`, `GET /auth/me` |
| **Jobs** | `GET /jobs`, `POST /jobs`, `GET /jobs/:id`, `DELETE /jobs/:id`, `GET /jobs/:id/stream` (SSE) |
| **Presets** | `GET /presets`, `POST /presets`, `PUT /presets/:id`, `DELETE /presets/:id`, `POST /presets/:id/clone` |
| **Sports** | `GET /sports`, `GET /sports/:sport/calendar`, `GET /sports/:sport/matchups` |
| **Outputs** | `GET /outputs`, `GET /outputs/:id/preview`, `GET /outputs/:id/download` |
| **G Drive** | `POST /gdrive/connect`, `POST /gdrive/sync/:id`, `GET /gdrive/assets`, `POST /gdrive/ingest/:id` |
| **Health** | `GET /health`, `GET /health/oracle` |
| **Schedule** | `GET /schedules`, `POST /schedules`, `PUT /schedules/:id`, `DELETE /schedules/:id`, `GET /calendar` |

---

## Part 2: Key Design Decisions

### 2.1 Decisions From User Input

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Build approach | Clean Build First | Archive v1 to `/archive/v1/`, new structure at root |
| Primary UI | Dashboard | Dashboard for all users, Oracle in background terminal |
| Authentication | Google OAuth | Integrates with G Drive, familiar to users |
| Database | SQLite | Simple, file-based, sufficient for small team |
| Real-time | SSE + REST | SSE for server→client push, REST for submissions |
| Context files | 3 dynamic | SYSTEM, PIPELINE, DASHBOARD (auto-updating) |
| Sports | All 5 | NFL + NBA for MVP, MLB/NHL/EPL enabled later |
| G Drive | Bidirectional | Outputs sync to G Drive, assets import from G Drive |
| Vision | Integrated into presets | Not separate feature; tone/aesthetic part of preset config |
| Timeline | MVP in 2 weeks | Core working, polish later |

### 2.2 Technical Decisions

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | React 18 + Vite | Already established |
| Backend | Flask | Already established |
| ORM | SQLAlchemy | Industry standard for Flask |
| Migrations | Alembic | Standard for SQLAlchemy |
| SSE fallback | Polling (2s) | If SSE fails, fall back gracefully |
| Job queue | In-memory + SQLite | Start simple, Redis later if needed |
| Context detection | File watching + mtime | Watchdog already in use |
| Cross-session | SQLite messages table | Replaces manual flags |

---

## Part 2.5: Pipeline Preservation Guarantee

**Critical:** V2 restructuring does NOT change pipeline functionality. This is a reorganization, not a rewrite.

### What Stays Exactly The Same

| Component | Preservation Status |
|-----------|---------------------|
| L1 data fetching logic | ✅ Copied unchanged (GoatedBets API, BalldontLie MCP, SportsBlaze, web search) |
| L2 calendar/segment logic | ✅ Copied unchanged |
| L3 idea creation/prompts | ✅ Copied unchanged (all extraction functions, prompt builders) |
| L4 TTS generation | ✅ Copied unchanged (ElevenLabs, OpenAI, Coqui) |
| L5 media generation | ✅ Copied unchanged (Nano Banana, Flux, DALL-E, Pexels) |
| L6 assembly logic | ✅ Copied unchanged (carousel, reels, overlays) |
| L7 distribution logic | ✅ Copied unchanged (folder organization, platform exports) |
| L8 analytics placeholder | ✅ Copied unchanged (future implementation) |
| `_L*/` folder structure | ✅ Preserved exactly (inputs/, analysis/, processors/, utils/) |
| Preset system | ✅ Migrated to SQLite but same schema/fields |
| Tool resolution | ✅ Same CLI > preset > default chain |
| PipelineContext dataclass | ✅ Same data flow between layers |
| Display mode registry | ✅ Same routing logic |
| Brand rules | ✅ Same validation |

### What Changes (Wrapper Only)

| Component | Change | Impact |
|-----------|--------|--------|
| Entry point | CLI menu → Dashboard API | Triggers same pipeline |
| Job tracking | In-memory → SQLite | Persists across restarts |
| Progress reporting | Console logs → SSE events | Same data, different transport |
| Output location | Same `content/` structure | No change |
| Config location | Same `config/` folder | No change |

### Migration Strategy

```python
# Migration is mostly file COPY, not rewrite:
archive/v1/scripts/L1_data.py → app/core/pipeline/layers/_L1/L1_data.py
archive/v1/scripts/_L1/inputs/* → app/core/pipeline/layers/_L1/inputs/*
# etc.

# Only NEW code:
app/core/pipeline/orchestrator.py  # Thin wrapper calling existing layers
app/api/routes/jobs.py             # REST endpoints triggering orchestrator
```

---

## Part 2.6: Automation & Scheduling Architecture

### Cron Job Integration

The system supports scheduled content generation via:

1. **Database-stored schedules** (`scheduled_jobs` table)
2. **Oracle scheduler daemon** (`oracle/scheduler.py`)
3. **Dashboard calendar view** (`/calendar` page)

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTOMATION FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │   Dashboard  │     │    Oracle    │     │   Pipeline   │     │
│  │   Calendar   │     │  Scheduler   │     │  Executor    │     │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘     │
│         │                    │                    │              │
│         │ Create schedule    │                    │              │
│         │ (cron: "0 9 * * 0")│                    │              │
│         ├───────────────────►│                    │              │
│         │                    │                    │              │
│         │                    │ Every minute:      │              │
│         │                    │ Check due jobs     │              │
│         │                    ├───────────────────►│              │
│         │                    │                    │              │
│         │                    │              Execute pipeline     │
│         │                    │              (same as manual)     │
│         │                    │                    │              │
│         │                    │ Log to job_calendar│              │
│         │                    │◄───────────────────┤              │
│         │                    │                    │              │
│         │ View in calendar   │                    │              │
│         │◄───────────────────┤                    │              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Scheduler Implementation

```python
# oracle/scheduler.py
class JobScheduler:
    """Cron-style job scheduler running in Oracle daemon."""

    def __init__(self, db):
        self.db = db
        self.running = False

    def start(self):
        """Start scheduler loop (runs every minute)."""
        self.running = True
        while self.running:
            self.check_and_run_due_jobs()
            time.sleep(60)

    def check_and_run_due_jobs(self):
        """Check for scheduled jobs that are due to run."""
        now = datetime.now()
        due_jobs = self.db.query("""
            SELECT * FROM scheduled_jobs
            WHERE enabled = TRUE AND next_run <= ?
        """, (now,))

        for scheduled in due_jobs:
            # Create actual job
            job_id = self.create_job_from_schedule(scheduled)

            # Log to calendar
            self.db.insert_calendar_entry(scheduled.id, now, job_id)

            # Update next_run based on cron expression
            next_run = self.calculate_next_run(scheduled.cron_expression)
            self.db.update_scheduled_job(scheduled.id, next_run=next_run, last_run=now)
```

### Dashboard Calendar View

```jsx
// dashboard/src/pages/CalendarPage.jsx
// Shows:
// - Past runs (completed jobs from job_calendar)
// - Future scheduled runs (from scheduled_jobs.next_run)
// - Click to view job details or reschedule
```

### Example Schedule Configurations

```json
// config/schedules.json (default templates)
{
  "templates": {
    "weekly_nfl": {
      "name": "Weekly NFL Carousels",
      "cron": "0 9 * * 0",  // Every Sunday at 9 AM
      "description": "Generate all NFL matchup carousels for the week"
    },
    "daily_nba": {
      "name": "Daily NBA Content",
      "cron": "0 8 * * *",  // Every day at 8 AM
      "description": "Generate NBA content for today's games"
    }
  }
}
```

---

## Part 2.7: Deferred Features (Preserved from IDEAS_BACKLOG)

All items from `docs/overview/IDEAS_BACKLOG.md` are preserved and integrated into V2 roadmap.

### YES (Approved) - Integrated into V2

| Feature | V2 Phase | Notes |
|---------|----------|-------|
| L8 feedback loops (L8→L7, L2, L1, Vision) | Phase 5+ | Architecture supports, placeholder remains |
| Multi-sport support (NBA, Soccer, Tennis) | MVP (NFL/NBA), Week 3-4 (others) | Sport providers built |
| Master orchestrator with full automation | Phase 5 | Scheduler daemon is foundation |
| Intelligent tagging system | Week 3-4 | Tags in outputs table |
| Poll generation capability | Future | Can be added as new preset type |
| Best Bets preset with multi-model | MVP | Already working |
| Gemini/Perplexity API integration | MVP | Already working |
| Midjourney/Hailuo AI research | Future | Can add as L5 tools |
| Oracle Health Monitor | ✅ DONE | Preserved in V2 |
| Package structure refactor | V2 migration | `app/` package structure |
| Vision system expansion | Week 3-4 | Integrated into presets |
| Cross-session briefing | V2 core | Dynamic contexts |
| Gap check / optimization pass | Preserved | Oracle audit commands |
| ADR draft system | Future | Can add to Oracle |
| Claude usage monitor panel | Future | Requires Admin API key |

### MAYBE (Considering) - Preserved for Future

| Feature | Status |
|---------|--------|
| Real-time trend detection | Defer to Phase 5+ |
| Vision system expansion (AI-Generated, Custom) | Week 3-4+ |
| Platform API integration (TikTok, IG, YT) | L8 implementation |
| Custom goated-pipeline MCP skill | Future |
| xlsx skill for analytics exports | Future |
| Adjustable priority weights | Future Oracle enhancement |
| Context digest generation | Auto-archive replaces this |
| Scheduled content generation | V2 core (scheduler) |
| CI/CD integration | Future |
| Agent-based optimization | Future |

### Expansion Phases (Preserved)

These remain the long-term roadmap:

| Phase | Description | V2 Status |
|-------|-------------|-----------|
| Phase 1: L8 Full Implementation | Platform APIs, auto collection | Future |
| Phase 2: Feedback Loops | L8→L7→L2→L1→Vision | Future |
| Phase 3: Vision System Expansion | AI vision generator, custom creator | Partial in V2 |
| Phase 4: Multi-Sport Support | NBA, Soccer, Tennis | Core in V2 |
| Phase 5: Automation & Agents | Master orchestrator, scheduled gen | Core in V2 |

---

## Part 3: Implementation Phases

### Phase 1: Foundation (Days 1-4)

**Goal:** Project structure, database, authentication

#### Tasks:
1. **Archive v1 and create new structure**
   - `mv AutomationScript archive/v1/`
   - Create new folder structure
   - Copy working pipeline code to `app/core/pipeline/`

2. **Set up SQLite database**
   - Create `app/db/schema.sql`
   - Initialize Alembic migrations
   - Create models: User, Preset, Job, Output

3. **Implement Google OAuth**
   - Install `google-auth-oauthlib`
   - Create `app/api/routes/auth.py`
   - Create `dashboard/src/contexts/AuthContext.jsx`
   - Add Google login button

4. **Basic API structure**
   - Create Flask app factory in `app/main.py`
   - Set up route blueprints
   - Add auth middleware

#### Files to create:
- `app/__init__.py`, `app/main.py`, `app/config.py`
- `app/db/session.py`, `app/db/schema.sql`
- `app/models/user.py`, `app/models/preset.py`, `app/models/job.py`, `app/models/output.py`
- `app/api/routes/auth.py`, `app/api/middleware.py`
- `dashboard/src/contexts/AuthContext.jsx`
- `dashboard/src/components/auth/GoogleLoginButton.jsx`

---

### Phase 2: Pipeline Integration (Days 5-8)

**Goal:** Connect dashboard to pipeline execution with real-time updates

#### Tasks:
1. **Port pipeline orchestrator**
   - Copy L0-L8 layer logic to `app/core/pipeline/`
   - Create `PipelineOrchestrator` class
   - Maintain `PipelineContext` dataclass

2. **Job service with SQLite**
   - Create `app/services/job_service.py`
   - Implement job queue (start with threading)
   - Progress tracking with layer detection

3. **SSE implementation**
   - Create `app/api/sse.py`
   - Events: `layer_start`, `progress`, `log`, `complete`, `error`
   - Add `dashboard/src/contexts/SSEContext.jsx`
   - Fallback polling in `dashboard/src/services/sse.js`

4. **Job API endpoints**
   - `POST /jobs` - Create and queue job
   - `GET /jobs/:id/stream` - SSE endpoint
   - `GET /jobs` - List with pagination

#### Files to create/modify:
- `app/core/pipeline/orchestrator.py`
- `app/core/pipeline/layers/*.py` (port from scripts/)
- `app/services/job_service.py`
- `app/api/sse.py`
- `app/api/routes/jobs.py`
- `dashboard/src/contexts/SSEContext.jsx`
- `dashboard/src/hooks/useSSE.js`

---

### Phase 3: Preset System (Days 9-11)

**Goal:** Custom preset creation with Vision integration

#### Tasks:
1. **Migrate system presets to database**
   - Parse `script_presets.json`
   - Insert as `is_system=True` rows
   - Keep JSON as backup/reference

2. **Preset CRUD API**
   - `GET /presets` - List all (system + user)
   - `POST /presets` - Create custom preset
   - `POST /presets/:id/clone` - Clone and customize
   - Validation endpoint

3. **Preset Builder UI**
   - `PresetBuilderPage.jsx` - Full editor
   - `VisionSettings.jsx` - Visual style, colors, player style
   - `LayerSelector.jsx` - Choose L1-L8
   - `ToolSelector.jsx` - Choose tools per layer
   - `PromptEditor.jsx` - Edit prompt template
   - Live preview component

4. **Vision integrated into presets**
   - Tone, aesthetic, brand rules as preset fields
   - Color scheme picker
   - Visual style dropdown (illustrated, dark, minimal, etc.)

#### Files to create:
- `app/api/routes/presets.py`
- `app/core/presets/manager.py`, `app/core/presets/schema.py`
- `dashboard/src/pages/PresetBuilderPage.jsx`
- `dashboard/src/components/presets/*.jsx`

---

### Phase 4: Multi-Sport & Gallery (Days 12-14)

**Goal:** All 5 sports functional, output gallery

#### Tasks:
1. **Sport providers**
   - Abstract `SportProvider` base class
   - `NFLProvider`, `NBAProvider` (MVP)
   - `MLBProvider`, `NHLProvider`, `EPLProvider` (stubs)
   - Season/calendar awareness

2. **Gallery and history pages**
   - `HistoryPage.jsx` - Job queue + completed jobs
   - `GalleryPage.jsx` - Output grid with filters
   - Preview modal, download buttons
   - Pagination and search

3. **Output management API**
   - `GET /outputs` with filters
   - `GET /outputs/:id/preview`
   - `GET /outputs/:id/download`

#### Files to create:
- `app/core/sports/base.py`, `app/core/sports/nfl.py`, `app/core/sports/nba.py`, etc.
- `config/sports/nfl.json`, `config/sports/nba.json`
- `dashboard/src/pages/HistoryPage.jsx`, `dashboard/src/pages/GalleryPage.jsx`
- `dashboard/src/components/outputs/*.jsx`

---

### Phase 5: G Drive & Oracle V2 (Days 15-21)

**Goal:** G Drive sync, Oracle as control center

#### Tasks:
1. **G Drive OAuth and sync**
   - Add Drive scopes to Google OAuth
   - Create `GDriveSyncService`
   - Folder picker UI
   - Sync-on-complete hook
   - Asset ingestion from G Drive

2. **Oracle V2: Control center**
   - SQLite tables for sessions, messages, snapshots
   - `ContextManager` - auto-detect active context
   - `SessionSpawner` - spawn VS Code sessions
   - `CrossSessionMessenger` - replace manual flags

3. **Dynamic context system**
   - Merge DEV+CRANK+POCKET → PIPELINE_CONTEXT.md
   - Merge ORACLE → SYSTEM_CONTEXT.md
   - Auto-update on file changes
   - 500-line limit enforcement

4. **Enhanced health monitor**
   - Read from SQLite instead of JSON
   - Context indicator panel
   - Messages panel
   - Spawn session hotkeys

#### Files to create:
- `app/services/gdrive_service.py`
- `app/api/routes/gdrive.py`
- `dashboard/src/components/gdrive/*.jsx`
- `oracle/daemon.py`, `oracle/context_manager.py`, `oracle/session_spawner.py`
- `docs/context/SYSTEM_CONTEXT.md`, `docs/context/PIPELINE_CONTEXT.md`

---

### Phase 6: Polish & Testing (Days 22-28)

**Goal:** Production-ready MVP

#### Tasks:
1. **UI polish**
   - Loading states, error handling
   - Responsive design
   - Toast notifications
   - Dark mode (optional)

2. **Testing**
   - Unit tests for core services
   - Integration tests for API
   - E2E test: Login → Select → Generate → Download

3. **Documentation**
   - Update ARCHITECTURE.md, WORKFLOW.md
   - Create user guide
   - API documentation

4. **Migration script**
   - `scripts/migrate.py` - Move v1 data to v2
   - Preset migration
   - Content folder linking

---

## Part 4: Critical File Mappings

### From V1 to V2

| V1 Location | V2 Location | Notes |
|-------------|-------------|-------|
| `scripts/L0_pipeline.py` | `app/core/pipeline/orchestrator.py` | Refactor to class |
| `scripts/L1_data.py` - `L8_analytics.py` | `app/core/pipeline/layers/*.py` | Individual modules |
| `scripts/_L*/` | `app/core/pipeline/layers/` | Merge into layer modules |
| `config/script_presets.json` | Database + `config/presets/system_presets.json` | Migrate to SQLite |
| `config/tool_config.json` | `config/tools.json` | Keep as file |
| `config/brand_rules.json` | `config/brand_rules.json` | Keep as file |
| `maintenance/project_oracle.py` | `oracle/daemon.py` + services | Split into modules |
| `maintenance/health_monitor.py` | `oracle/health_monitor.py` | Enhance with SQLite |
| `docs/context/DEV_CONTEXT.md` | `docs/context/PIPELINE_CONTEXT.md` | Merge with CRANK/POCKET |
| `docs/context/ORACLE_CONTEXT.md` | `docs/context/SYSTEM_CONTEXT.md` | Rename/consolidate |
| `dashboard/backend/` | `app/api/` | Restructure |
| `dashboard/frontend/` | `dashboard/` | Enhance |

---

## Part 5: MVP Checklist (2 Weeks)

### Day 1 Must Have (Critical Path)
- [x] Google OAuth login working ✅ (Jan 6, 2026)
- [ ] Core flow: Select sport → Pick matchup → Choose preset → Generate → Download
- [ ] Preset cloning/modification capability
- [x] SQLite persistence for jobs ✅ (Jan 6, 2026)

### Week 1-2 Must Have (MVP)
- [ ] SSE progress tracking (real-time)
- [ ] All current presets working
- [ ] NFL + NBA matchup selection
- [ ] Output preview and download
- [ ] Job history view
- [ ] Basic error handling

### Nice to Have (Week 3-4)
- [ ] Custom preset builder UI
- [ ] G Drive sync
- [ ] Oracle session spawning
- [ ] Dynamic context auto-updates
- [ ] Gallery with filters
- [ ] MLB/NHL/EPL sports

### Deferred
- [ ] Redis job queue
- [ ] Multi-machine sync
- [ ] Analytics dashboard (L8)
- [ ] Scheduled jobs
- [ ] Collaborative editing

---

## Part 6: Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Google OAuth complexity | Use established libraries, test early |
| SSE browser issues | Implement polling fallback |
| Pipeline migration breaks | Keep v1 archived, test each layer |
| iCloud path handling | Use absolute paths, handle spaces (already working) |
| Context file sync | SQLite as source of truth, files are views |
| Scope creep | Strict MVP checklist, defer nice-to-haves |

---

## Part 7: Daily Workflow During Build

1. **Start of day:**
   - Oracle: `python3 oracle/daemon.py audit --quick`
   - Review pending messages in SQLite

2. **During dev:**
   - Dashboard running: `npm run dev` (port 5173)
   - Backend running: `python3 -m app.main` (port 5001)
   - Oracle health monitor in background terminal

3. **Every ~20 exchanges:**
   - Autosave: `python3 oracle/daemon.py autosave`

4. **End of day:**
   - Commit changes
   - Update PIPELINE_CONTEXT.md (auto or manual)
   - Note blockers for next session

---

## Part 8: Success Criteria

### MVP Success (2 weeks)
1. User can log in with Google
2. User can select NFL game, pick preset, generate content
3. User can see real-time progress
4. User can download generated content
5. Jobs persist across sessions (SQLite)
6. Oracle health monitor works with new structure

### Full V2 Success (4 weeks)
1. All 5 sports selectable (NFL/NBA full, others basic)
2. Custom preset builder functional
3. G Drive sync working
4. 3 dynamic contexts auto-updating
5. Oracle can spawn sessions
6. Cross-session messages replace manual flags
7. Gallery with search/filter

---

## Appendix A: Preset Schema (V2)

```json
{
  "preset_id": "my_custom_carousel",
  "name": "My Custom Carousel",
  "description": "Custom illustrated style with enhanced colors",
  "output_type": "carousel",
  "user_id": 1,
  "is_system": false,

  "layers": ["L1", "L2", "L3", "L5", "L6", "L7"],
  "tools": {
    "L1_tool": "goatedbets_api",
    "L3_tool": "carousel_script",
    "L5_tool": "nano_banana",
    "L6_tool": "carousel_assembly"
  },

  "tone": "analytical_confident",
  "format": "hook_body_cta",
  "length": "medium",
  "prompt_template": "Create betting analysis for {matchup}...",

  "vision": {
    "visual_style": "illustrated",
    "display_mode": "carousel",
    "infographic_style": "illustrated",
    "color_scheme": {
      "background": "#F5F2EB",
      "accent": "#D4822C",
      "text": "#000000"
    },
    "player_style": "watercolor/sketch",
    "text_style": "editorial magazine"
  },

  "aspect_ratio": "1:1",
  "final_aspect_ratio": "9:16",
  "slide_count": 3,

  "tags": ["betting", "carousel", "illustrated"]
}
```

---

## Appendix B: Context File Templates

### SYSTEM_CONTEXT.md (auto-updated)
```markdown
# SYSTEM_CONTEXT.md - Oracle Media Engine V2

**Last Updated:** {auto_timestamp}
**Active Context:** {detected_context}
**Health Score:** {health_score}/10

## Core Protocols
[Session rules, automation rules - static]

## Tool Configuration
[From tools.json - auto-synced]

## Sports Status
[From config/sports/ - auto-synced]

## Pending Messages
[From SQLite messages table - auto-synced]

## Recent System Events
[Last 10 events - auto-populated]
```

### PIPELINE_CONTEXT.md (auto-updated)
```markdown
# PIPELINE_CONTEXT.md - Active Development

**Last Updated:** {auto_timestamp}
**Session:** P{n}
**Active Jobs:** {count}

## Current Focus
[Detected from file activity]

## Active Job
[From SQLite jobs table if running]

## Recent Changes
[Auto-generated from git/file changes]

## Pending Tasks
[From todo tracking]
```

---

## Appendix C: Commands Reference

```bash
# Development
npm run dev                              # Frontend (port 5173)
python3 -m app.main                      # Backend (port 5001)

# Oracle
python3 oracle/daemon.py audit --quick   # Health check
python3 oracle/daemon.py autosave        # Sync + snapshot
python3 oracle/daemon.py status          # One-line health
python3 oracle/daemon.py context         # Show active context
python3 oracle/daemon.py spawn pipeline  # Spawn VS Code session
python3 oracle/daemon.py messages        # View cross-session messages

# Database
python3 -m alembic upgrade head          # Run migrations
python3 scripts/migrate.py               # Migrate v1 data
```

---

## Appendix D: Claude Code Tips for This Project

Based on the Advent of Claude 2025 article, these patterns will be especially useful:

### Session Management
- **`claude --continue`** - Resume last session instantly (use when returning to work)
- **`claude --resume`** - Pick from past conversations (when switching between Pipeline/Dashboard work)
- **`/rename V2-Pipeline-Day3`** - Name sessions for easy identification

### Context Efficiency
- **`/context`** - Visualize token usage (important for this large project)
- **`@app/core/pipeline/`** - Fast file references with fuzzy matching
- **`! git status`** - Bypass model processing for quick shell commands

### Plan Mode (Use for V2 work)
- **`Shift+Tab` twice** - Enter Plan mode before major changes
- Creates approval checkpoints
- Perfect for Phase 1-6 milestone work

### Automation Patterns
- **Headless mode**: `claude -p "Run tests for app/core/"` - Good for CI/CD later
- **Lifecycle hooks**: `/hooks` - Automate approvals, block dangerous commands
- **Reusable commands**: Save frequent prompts as `.md` files in commands directory

### Extended Thinking (Use for complex decisions)
- Include "ultrathink" in prompts for architecture decisions
- Up to 32k tokens for internal reasoning
- Use when: designing database schema, planning migrations, debugging complex issues

### Multi-Agent Workflows
- **Subagents**: Each gets own 200k context window
- **Run parallel**: When researching + implementing simultaneously
- **Agent Skills**: Encapsulate expertise (deployment, testing, docs)

### For This Project Specifically

```bash
# Quick commands to save as slash commands:

# /v2-status - Check V2 health
claude -p "Check health of Media-Engine-V2: run tests, check migrations, verify OAuth"

# /v2-migrate - Continue migration work
claude --continue  # Resume migration session

# /v2-dashboard - Focus on dashboard work
claude -p "Working on dashboard. Read DASHBOARD_CONTEXT.md and continue from last task."
```

### Permission Boundaries
```bash
# Set up sandbox for V2 development
/sandbox
# Allow: app/**, dashboard/**, oracle/**, config/**
# Block: archive/v1/** (don't modify archived code)
```

### Export for Documentation
```bash
# After completing a phase, export conversation for records
/export phase1-foundation.md
```

### Tips for Context Files
- Keep each context under 500 lines
- Use `@docs/context/PIPELINE_CONTEXT.md` for fast reference
- Auto-update via Oracle daemon (no manual edits)

---

## Appendix E: Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEDIA ENGINE V2 QUICK REF                     │
├─────────────────────────────────────────────────────────────────┤
│ FOLDER             │ PURPOSE                                     │
│ app/               │ Python backend (API, core, services)        │
│ app/core/pipeline/ │ L0-L8 layers (PRESERVED _L* structure)      │
│ dashboard/         │ React frontend + calendar view              │
│ oracle/            │ Control center + scheduler daemon           │
│ config/            │ Presets, tools, schedules, sports           │
│ content/           │ Generated outputs                           │
│ utils/             │ Utility scripts (was: scripts/)             │
│ archive/v1/        │ Old codebase (read-only reference)          │
├─────────────────────────────────────────────────────────────────┤
│ PIPELINE           │ PRESERVED (COPY, NOT REWRITE)               │
│ L1 data fetching   │ ✅ GoatedBets, MCP, SportsBlaze, web search │
│ L3 idea creation   │ ✅ All extraction, prompts, transforms      │
│ L5 media gen       │ ✅ Nano Banana, Flux, DALL-E, Pexels        │
│ L6 assembly        │ ✅ Carousels, reels, overlays               │
│ _L*/ structure     │ ✅ inputs/, analysis/, processors/, utils/  │
├─────────────────────────────────────────────────────────────────┤
│ AUTOMATION         │                                             │
│ Scheduler          │ oracle/scheduler.py (cron jobs)             │
│ Calendar           │ dashboard/src/pages/CalendarPage.jsx        │
│ scheduled_jobs     │ SQLite table for recurring jobs             │
├─────────────────────────────────────────────────────────────────┤
│ COMMANDS           │                                             │
│ npm run dev        │ Start frontend (5173)                       │
│ python -m app      │ Start backend (5001)                        │
│ oracle audit       │ Health check                                │
│ oracle autosave    │ Sync + snapshot                             │
│ oracle spawn       │ Spawn VS Code session                       │
│ oracle schedule    │ Manage scheduled jobs                       │
├─────────────────────────────────────────────────────────────────┤
│ MVP TIMELINE       │                                             │
│ Day 1              │ OAuth + Core flow + Preset cloning          │
│ Week 1             │ SSE + All presets + NFL/NBA                 │
│ Week 2             │ History + Gallery + Polish                  │
│ Week 3-4           │ G Drive + Custom builder + Scheduler + All sports │
└─────────────────────────────────────────────────────────────────┘
```

---

*Plan created by Oracle (O89) on January 5, 2026*
*Ready for implementation. Run `/v2-start` to begin.*
