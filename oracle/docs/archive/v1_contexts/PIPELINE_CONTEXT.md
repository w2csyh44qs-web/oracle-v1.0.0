# PIPELINE_CONTEXT.md - Active Development

**Last Updated:** January 7, 2026
**Session:** V2 Migration - Phase 5.7 Dynamic Context System
**Active Jobs:** 0

---

## Current Focus

**Phase 5.7: Dynamic Context System** - ✅ COMPLETE

Session O90 additions:
- Oracle models: Session, Message, Snapshot, HealthStatus
- Context manager with file watching
- Session spawner for VS Code/Claude Code
- Oracle daemon for background monitoring

**Phase 7: Output Gallery + PresetPreview** - IN PROGRESS

Session DB3 additions:
- UI Polish: Sport selection colors, matchup card layout, purple text readability

Session DB2 additions:
- PresetPreview component for live preset mockups
- Server stability fixes (pkill + strictPort, OAuth redirect, CORS)

**Phase 6.2: Scheduler UI** - ✅ COMPLETE

Schedule management UI with create/edit/delete, cron presets, and manual trigger.

**Phase 6.1: Auth UI** - ✅ COMPLETE

Google OAuth login flow with protected routes, user profile display, and logout functionality.

**Phase 5.6: UI Branding** - ✅ COMPLETE

Goated Bets logo integration and brand color system. Gold CTAs, purple UI elements, green selection states.

**Phase 5.5: Live Data Integration** - ✅ COMPLETE

balldontlie API integration for live matchups/season data. Playoff support added.

**Phase 5.4: Frontend UI** - ✅ COMPLETE

Preset Builder and Clone/Customize flow for React frontend.

**Phase 5.3: Scheduler** - ✅ COMPLETE

Job scheduling service with cron-style automation and built-in NFL/NBA presets.

**Phase 5.2: Oracle Service** - ✅ COMPLETE

Backend health monitoring service with API endpoints for pipeline status, costs, and job stats.

**Phase 5.1: G Drive Sync** - ✅ COMPLETE

Google Drive sync service for automatic output backup and sharing.

**Phase 4: Multi-Sport Providers** - ✅ COMPLETE

SportProvider abstraction layer fully wired through orchestrator and API.

**Phase 3: Preset System** - ✅ BACKEND COMPLETE

PresetService implemented with database-first loading and JSON fallback. Auto-seeds 20 system presets on startup.

**Phase 2: Pipeline Integration** - ✅ COMPLETE

Option C (Direct Import with Adapters) fully implemented for all 8 layers.

---

## Completed This Session (O90 - Dynamic Context System)

### Oracle Models Created (`app/models/oracle.py`)

| Model | Purpose |
|-------|---------|
| `Session` | Track sessions across contexts (oracle, pipeline, dashboard) |
| `Message` | Cross-session messaging with priority and acknowledgment |
| `Snapshot` | Context state snapshots for recovery |
| `HealthStatus` | Health metrics persistence |

### Context Manager (`oracle/context_manager.py`)

| Feature | Description |
|---------|-------------|
| File watching | Monitors `app/`, `dashboard/`, `oracle/` for activity |
| Context detection | Determines active context from recent file changes |
| Activity tracking | Records file modifications per context |
| Snapshot creation | Creates context snapshots on demand |
| Message interface | Send/receive messages between contexts |

### Session Spawner (`oracle/session_spawner.py`)

| Feature | Description |
|---------|-------------|
| VS Code spawn | Opens project with correct context file |
| Claude Code spawn | Starts Claude session with context prompt |
| Session tracking | Records sessions in database |
| Resume prompts | Generates context-specific resume prompts |

### Oracle Daemon (`oracle/daemon.py`)

| Command | Description |
|---------|-------------|
| `start` | Start daemon with file watching |
| `status` | Show daemon status |
| `spawn <ctx>` | Spawn session for oracle/pipeline/dashboard |
| `messages` | Show context activity summary |
| `audit` | Run health audit on project |
| `prompts` | Show resume prompts for all contexts |

### Usage

```bash
# Start Oracle daemon
python oracle/daemon.py start

# Spawn a new pipeline session
python oracle/daemon.py spawn pipeline --task "Fix L3 adapter"

# Run quick health audit
python oracle/daemon.py audit --quick

# Show resume prompts
python oracle/daemon.py prompts
```

---

## Completed Previously (DB3 - UI Polish)

### Sport Selection Color Scheme

Three-line info display with consistent font sizes (1rem):
- **Line 1** (season-display): Gold `var(--goat-gold)` - e.g., "2025-26 Season"
- **Line 2** (phase-display): Purple `var(--goat-purple-text)` - e.g., "Regular Season"
- **Line 3** (period-display): Green `var(--success)` - e.g., "Week 18"

### Matchup Card Improvements

| Change | Before | After |
|--------|--------|-------|
| Score position | Corner status badge (overlapping) | Centered below team names |
| Score styling | Small badge text | Gold 1.1rem `.final-score` class |
| Duplicate info | `matchup_display` showed full team names | Removed (abbrevs already shown) |
| Status badge | Showed for all non-scheduled games | Only shows for 'final' or 'in_progress' |
| Status text | Raw status value | "Final" or "Live" |

### Purple Text Readability

Added new CSS variable for text on dark backgrounds:
```css
--goat-purple-text: #c4b5fd;  /* Brighter than #8b5cf6 for readability */
```

Updated files to use `--goat-purple-text`:
- `SportSelection.css` - phase-display
- `MatchupSelection.css` - game-time
- `PresetBuilder.css` - use-existing-btn
- `GenerationFlow.css` - file-group h4

### Files Modified

| File | Changes |
|------|---------|
| `global.css` | Added `--goat-purple-text: #c4b5fd` |
| `SportSelection.css` | Three-line color scheme (gold/purple/green) |
| `MatchupSelection.jsx` | Score moved to center, removed matchup_display, status badge logic |
| `MatchupSelection.css` | Added `.final-score`, updated game-time color |
| `PresetBuilder.css` | use-existing-btn purple text |
| `GenerationFlow.css` | file-group h4 purple text |

---

## Completed Previously (DB2 - PresetPreview + Server Fixes)

### PresetPreview Component Created

| File | Purpose |
|------|---------|
| `dashboard/frontend/src/components/PresetPreview.jsx` | Live mockup preview based on preset form settings |
| `dashboard/frontend/src/components/PresetPreview.css` | Preview panel styling |

### PresetPreview Features

- **Output Type Previews**: Shows carousel slides, single images, videos, infographics
- **Sport-Specific Colors**: NFL blue, NBA red, etc.
- **Pipeline Flow Display**: Shows active layers (e.g., "L1 → L3 → L5 → L6")
- **Audio Indicators**: Shows audio icon for video content with L4
- **Real-Time Updates**: Preview updates as user changes form fields
- **Aspect Ratio Visualization**: Device frame shows configured aspect ratio

### PresetBuilder Layout Update

- Side-by-side layout: form on left, preview panel on right
- Updated `PresetBuilder.jsx` with `.builder-layout` wrapper
- Updated `PresetBuilder.css` with CSS grid layout
- Green color scheme (#10b981) for layer selection cards
- Layer cards: hover, selected states, checkboxes use consistent green

### Server Stability Fixes

| Issue | Fix | File |
|-------|-----|------|
| Multiple frontend servers | `pkill` + `--strictPort` in npm dev script | `package.json` |
| OAuth redirect to wrong port | Changed default FRONTEND_URL from 5174 → 5173 | `auth.py:20` |
| CORS blocking requests | Added ports 5173, 5174, 5175 to allowed origins | `config.py:59` |
| Debugging matchup loading | Added console logs to MatchupSelection.jsx | `MatchupSelection.jsx` |

### Current Server State

- **Frontend**: http://localhost:5173/ (Vite with `--strictPort`)
- **Backend**: http://localhost:5001/ (Flask Media Engine V2)

---

## Completed Previously (Phase 6.2 Scheduler UI)

### Scheduler Components Created

| File | Purpose |
|------|---------|
| `dashboard/frontend/src/components/SchedulerPage.jsx` | Schedule list with filters, CRUD actions, trigger button |
| `dashboard/frontend/src/components/SchedulerPage.css` | Scheduler page styles |
| `dashboard/frontend/src/components/ScheduleEditor.jsx` | Create/edit modal with cron presets and validation |
| `dashboard/frontend/src/components/ScheduleEditor.css` | Editor modal styles |

### Scheduler Features

- **Schedule List**: Displays all user schedules with sport badge, preset name, cron expression, next/last run
- **Filters**: Filter by sport and enabled status
- **CRUD Operations**: Create, edit, delete schedules via modal
- **Cron Presets**: Quick-select buttons for NFL Sunday/Thursday/Monday, NBA Daily, Weekly
- **Live Validation**: Validates cron expression and shows next run time
- **Manual Trigger**: Run any schedule immediately with "▶ Run" button
- **Navigation**: "📅 Schedules" button in header to switch between generator and scheduler

### API Endpoints Added (`api.js`)

```javascript
export const getSchedules = (filters = {}) => api.get('/scheduler', { params: filters });
export const getSchedule = (scheduleId) => api.get(`/scheduler/${scheduleId}`);
export const createSchedule = (data) => api.post('/scheduler', data);
export const updateSchedule = (scheduleId, data) => api.put(`/scheduler/${scheduleId}`, data);
export const deleteSchedule = (scheduleId) => api.delete(`/scheduler/${scheduleId}`);
export const triggerSchedule = (scheduleId) => api.post(`/scheduler/${scheduleId}/trigger`);
export const getSchedulePresets = () => api.get('/scheduler/presets');
export const validateCron = (cronExpression) => api.post('/scheduler/validate', { cron_expression: cronExpression });
```

### App.jsx Updates

- Added page state (`currentPage`: 'generator' | 'scheduler')
- Conditional rendering for generator flow vs scheduler page
- Header subtitle changes based on current page
- `UserProfile` receives `onScheduler` prop for navigation

### CSS Updates (`App.css`)

- Added `.nav-btn` and `.scheduler-nav-btn` styles
- Purple border for scheduler button, hover fills purple background

---

## Completed Previously (Phase 6.1 Auth UI)

### Auth Components Created

| File | Purpose |
|------|---------|
| `dashboard/frontend/src/contexts/AuthContext.jsx` | Auth state management (user, login, logout, loading) |
| `dashboard/frontend/src/components/LoginPage.jsx` | Google OAuth login page with branding |
| `dashboard/frontend/src/components/LoginPage.css` | Login page styles |
| `dashboard/frontend/src/components/ProtectedRoute.jsx` | Route guard for authenticated pages |

### Auth Flow

1. User visits dashboard → `ProtectedRoute` checks authentication
2. If no token → Shows `LoginPage` with Google OAuth button
3. User clicks "Sign in with Google" → Redirects to backend `/auth/login`
4. Backend returns OAuth URL → User authenticates with Google
5. Google callback → Backend creates session, returns token via URL param
6. Frontend stores token in localStorage → `AuthContext` fetches user info
7. User is authenticated → Dashboard loads

### API Updates (`api.js`)

- Added axios interceptors for auth token injection
- Added 401 response handler (clears invalid tokens)
- New endpoints: `getLoginUrl()`, `getCurrentUser()`, `verifyToken()`, `logout()`

### App.jsx Updates

- Wrapped app with `AuthProvider` → `AppProvider` → `ProtectedRoute`
- New `UserProfile` component in header (avatar, name, admin badge, logout)
- Header restructured with `header-main` and `header-title` divs

### CSS Updates (`App.css`)

- Header changed from centered column to row with space-between
- User profile styles: `.user-profile`, `.user-avatar`, `.user-name`, `.admin-badge`, `.logout-btn`
- Responsive: stacks vertically on mobile (max-width: 768px)

---

## Completed Previously (Phase 5.6 UI Branding)

### Brand Color System

CSS variables defined in `global.css`:

```css
:root {
  --goat-gold: #f59e0b;       /* Primary CTAs, logo glow */
  --goat-gold-light: #fbbf24;
  --goat-gold-dark: #d97706;
  --goat-purple: #8b5cf6;     /* UI elements, indicators */
  --goat-purple-light: #a78bfa;
  --success: #22c55e;         /* Selection states, confirmations */
  --bg-primary: #0f1419;
  --bg-secondary: #1a1f2e;
  --bg-tertiary: #2d3748;
}
```

### Color Distribution

| Color | Usage |
|-------|-------|
| **Gold** (`#f59e0b`) | Primary CTA buttons (Generate, Build New, Submit), logo glow, header border |
| **Purple** (`#8b5cf6`) | Step indicators, filter tabs, toggle buttons, badges, form focus, progress bars |
| **Green** (`#22c55e`) | Card hover/selection, download buttons, success states |

### Logo Integration

- Logo path: `dashboard/frontend/public/assets/branding/logos/welcome_logo.png`
- Displayed in header with glow effect via `filter: drop-shadow(0 0 20px rgba(245, 158, 11, 0.4))`
- 60px height, centered with header title

### Header Styling

```css
.dashboard-header h1 {
  text-transform: uppercase;
  font-style: italic;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
```

### Files Modified

| File | Changes |
|------|---------|
| `dashboard/frontend/src/styles/global.css` | CSS variables for brand colors |
| `dashboard/frontend/src/styles/App.css` | Header with logo, purple step indicators |
| `dashboard/frontend/src/App.jsx` | Logo import and display |
| `dashboard/frontend/src/components/SportSelection.css` | Green hover, purple season display, hidden playoff badge |
| `dashboard/frontend/src/components/MatchupSelection.css` | Purple toggle/badges, green card hover |
| `dashboard/frontend/src/components/PresetSelection.css` | Purple tabs/customize, green card hover |
| `dashboard/frontend/src/components/PresetBuilder.css` | Purple form elements |
| `dashboard/frontend/src/components/GenerationFlow.css` | Purple progress bar, green download buttons |

### Removed Elements

- "Playoffs Available" badge: Hidden with `display: none` in SportSelection.css

---

## Completed Previously (Phase 5.5 Live Data Integration)

### API Priority System

Data sources for sports/matchups (in priority order):
1. **balldontlie** (PRIMARY) - Most reliable, well-documented API
2. **SportsBlaze** (SECONDARY) - May not be renewed, less reliable
3. **GoatedBets** (TERTIARY) - Fallback, sometimes not current

### Environment Variables Updated

```bash
# .env additions
BALLDONTLIE_API_KEY=c4a4d71d-0d38-4593-8f81-a76fbf54b762  # NFL/NBA games, teams, players
GOATEDBETS_API_URL=https://api.goatedbets.com
GOATEDBETS_API_KEY=your_goatedbets_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### balldontlie API Endpoints

| Sport | Base URL | Games Endpoint | Params |
|-------|----------|----------------|--------|
| NFL | `https://api.balldontlie.io/nfl/v1` | `/games` | `seasons[]`, `weeks[]`, `postseason` |
| NBA | `https://api.balldontlie.io/v1` | `/games` | `dates[]`, `postseason` |

### SportProvider Methods Added

| Method | Purpose |
|--------|---------|
| `get_season_info()` | Season year, display name, key periods, current phase |
| `get_playoff_matchups(round)` | Playoff games with optional round filter |
| `get_current_period()` | Dynamic calculation based on current date |

### NFL Provider Updates (`app/core/sports/providers/nfl.py`)

- Fixed balldontlie URL (was double-nested `/v1/nfl/v1/games`)
- Fixed SportsBlaze filter ("Regular Season" not "Regular")
- Dynamic week calculation based on dates:
  - Season start: September 4, 2025
  - Wild Card: January 10, 2026
  - Divisional: January 17, 2026
  - Conference: January 25, 2026
  - Super Bowl: February 8, 2026
- Season info with key periods and phase detection

### NBA Provider Updates (`app/core/sports/providers/nba.py`)

- Added `get_season_info()` with key periods
- Added `get_playoff_matchups()` method
- Season display: "2025-26 Season"

### Sports API Updates (`app/api/routes/sports.py`)

List endpoint now returns:
```json
{
  "id": "nfl",
  "name": "NFL",
  "season": "2025-26",
  "season_display": "2025-26 Season",
  "current_phase": "regular_season",
  "current_period": {"week": "week18", "week_num": 18, "phase": "regular_season"},
  "has_playoffs": true,
  "key_periods": [...]
}
```

New endpoint:
- `GET /sports/:sport/playoffs?round=wild_card` - Playoff matchups with round filter

### Frontend Updates

**SportSelection.jsx:**
- Season display badge (e.g., "2025-26 Season")
- Current phase label (e.g., "Regular Season", "Playoffs")
- Current period display (e.g., "Week 18" or "Today")
- Playoff badge for sports with playoffs

**MatchupSelection.jsx:**
- Period type toggle (Regular Season / Playoffs)
- Week selector with "(Current)" marker for NFL
- Date selector with "Today" button for NBA
- Playoff round selector (Wild Card, Divisional, Conference, Super Bowl/Finals)
- Game status badges (Final, In Progress)
- Round labels for playoff games

**api.js:**
- Added `getPlayoffs(sport, round)` function

### CSS Updates

| File | New Styles |
|------|------------|
| `SportSelection.css` | `.season-display`, `.phase-display`, `.period-display`, `.playoff-badge` |
| `MatchupSelection.css` | `.period-toggle`, `.toggle-btn`, `.date-selector`, `.playoff-selector`, `.round-badge`, `.status-badge` |

---

## Completed Previously (Phase 5.4 Frontend UI)

### Frontend Components Created

| File | Purpose |
|------|---------|
| `dashboard/frontend/src/components/PresetBuilder.jsx` | Full preset creation form with layer selection |
| `dashboard/frontend/src/components/PresetEditor.jsx` | Modal for quick clone + customize flow |
| `dashboard/frontend/src/components/PresetBuilder.css` | Styles for builder component |
| `dashboard/frontend/src/components/PresetEditor.css` | Styles for editor modal |

### PresetBuilder Features
- Output type selection (carousel, single_image, infographic, video)
- Layer selection with L1-L8 checkboxes (L1 required)
- Aspect ratio configuration (working + final)
- API source selection
- Slides count for carousels
- Audio toggle (auto-adds L4)
- "Apply Recommended" layers by output type
- Form validation with error messages

### Clone/Customize Flow
- Clone button on every preset card in PresetSelection
- PresetEditor modal opens with preset data pre-filled
- Quick edit: name, layers, aspect ratios, slides
- Three actions: Cancel, Use Original, Clone & Use
- Cloned preset saved to database and used immediately

### Updated Files

| File | Changes |
|------|---------|
| `dashboard/frontend/src/services/api.js` | Added createPreset, updatePreset, deletePreset, clonePreset, getPresetsByLayer |
| `dashboard/frontend/src/components/PresetSelection.jsx` | Added clone button, editor modal integration, "Build Custom" button |
| `dashboard/frontend/src/components/PresetSelection.css` | Styles for new card layout, customize button, build button |
| `dashboard/frontend/src/App.jsx` | Added PresetBuilder import, step 2.5 routing |

### User Flow
1. Sport → Matchup → PresetSelection (step 3)
2. From PresetSelection:
   - Click preset card → Use directly → Generate (step 4)
   - Click "Clone & Customize" → Editor modal → Clone & Use → Generate
   - Click "+ Build Custom" → PresetBuilder (step 2.5) → Create & Use → Generate

---

## Completed Previously (Phase 5.3 Scheduler)

### SchedulerService Created

| File | Purpose |
|------|---------|
| `app/services/scheduler_service.py` | SchedulerService class with cron scheduling |

Features:
- CRUD operations for scheduled jobs
- Cron expression validation and parsing
- Next run time calculation
- Human-readable schedule descriptions
- Built-in presets for NFL/NBA schedules
- Manual trigger support

### Schedule Presets

| Preset | Cron | Description |
|--------|------|-------------|
| `nfl_sunday` | `0 8 * * 0` | Sunday 8am before games |
| `nfl_thursday` | `0 16 * * 4` | Thursday 4pm before TNF |
| `nfl_monday` | `0 16 * * 1` | Monday 4pm before MNF |
| `nba_daily` | `0 10 * * *` | Daily 10am for games |
| `weekly` | `0 9 * * 1` | Monday 9am weekly |

### Scheduler API Endpoints

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

### Future Expansion (when needed)
- Background worker process to poll `/scheduler/due`
- APScheduler integration for in-process scheduling
- Email/webhook notifications

---

## Completed Previously (Phase 5.2 Oracle Service)

### OracleService Created

| File | Purpose |
|------|---------|
| `app/services/oracle_service.py` | OracleService class with health monitoring |

Features:
- Health score calculation (0-10) with status (healthy/degraded/critical)
- Pipeline layer status for all 8 adapters
- API cost tracking by time period, provider, and layer
- Job statistics from database
- 30-second cache for performance
- Writes `.health_status.json` for external tools

### Health API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check with score |
| `/health/oracle` | GET | Detailed health breakdown |
| `/health/pipeline` | GET | All 8 layer statuses |
| `/health/costs` | GET | API cost summary |
| `/health/jobs` | GET | Job statistics |
| `/health/db` | GET | Database connectivity |
| `/health/full` | GET | Complete status in one call |

### Future Expansion (when needed)
- File watching daemon for real-time monitoring
- SSE alerts for critical issues
- Auto-remediation for common problems

---

## Completed Previously (Phase 5.1 G Drive Sync)

### GDriveService Created

| File | Purpose |
|------|---------|
| `app/services/gdrive_service.py` | GDriveService class with upload, sync, folder management |

Features:
- Single file upload with resumable support for large files (>5MB)
- Folder sync with recursive subdirectory support
- Job output sync with organized folder structure (SPORT/week/matchup/)
- Folder creation and caching
- File pattern filtering

### OAuth Updated

- Added `https://www.googleapis.com/auth/drive.file` scope to auth_service.py
- Users will need to re-authenticate to grant Drive permissions

### Sync API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sync/status` | GET | Check Drive sync configuration status |
| `/sync/folder` | POST | Sync a local folder to Drive |
| `/sync/job/:job_id` | POST | Sync job outputs to Drive |
| `/sync/files` | GET | List files in Drive folder |
| `/sync/upload` | POST | Upload single file to Drive |

### L7 Adapter Integration

- Added `sync_to_drive()` method to L7Adapter
- Syncs distributed content with organized folder structure
- Categories: carousels, animations, videos

---

## Completed Previously (Phase 4 Multi-Sport)

### SportProvider System Created

| File | Purpose |
|------|---------|
| `app/core/sports/base.py` | SportProvider abstract class, CalendarType enum, TeamData/MatchupData dataclasses |
| `app/core/sports/registry.py` | SportRegistry for provider lookup, auto-registration |
| `app/core/sports/providers/nfl.py` | NFLProvider - 32 teams, weekly calendar, NFL-specific logic |
| `app/core/sports/providers/nba.py` | NBAProvider - 30 teams, daily calendar, NBA-specific logic |

### Adapters Updated for Sport-Awareness

| Adapter | Changes |
|---------|---------|
| L1Adapter | Sport detection from preset, `get_teams()`, `get_preferred_tools()`, `get_current_period()` |
| L2Adapter | Calendar type detection (weekly vs daily), sport-aware period defaults |

### Orchestrator Updated

- Sport extracted from preset's "sports" array or "sport" field
- CalendarType detection (weekly vs daily)
- Auto-detects current period from provider
- Passes sport, week, game_date to layer execution

### Sports API Updated

- `GET /sports` - Uses SportRegistry, shows calendar type
- `GET /sports/:sport` - Sport details with current period
- `GET /sports/:sport/teams` - Teams with filtering
- `GET /sports/:sport/calendar` - Sport-aware calendar structure
- `GET /sports/:sport/matchups` - Uses SportProvider

### Test Results

```
✅ NFL: 32 teams, weekly calendar, tools: goatedbets_api, sportsblaze, balldontlie
✅ NBA: 30 teams, daily calendar, tools: balldontlie, goatedbets_api
✅ L1Adapter correctly routes by sport from preset config
✅ L2Adapter correctly detects calendar type (weekly vs daily)
✅ Provider auto-registration on import
✅ Orchestrator NFL: week=week1, phase=regular_season, calendar=weekly
✅ Orchestrator NBA: game_date=2026-01-06, calendar=daily
✅ Job API passes sport to orchestrator via sports array
```

---

## V2 Structure (Complete)

```
app/
├── __init__.py, config.py, main.py
├── api/
│   ├── sse.py           # SSE utilities
│   └── routes/          # auth, jobs, presets, sports, outputs, health, sync
├── core/
│   ├── pipeline/
│   │   ├── orchestrator.py  # Pipeline controller (uses all adapters)
│   │   └── adapters/        # ✅ COMPLETE - All 8 layer adapters
│   │       ├── __init__.py  # Exports all adapters
│   │       ├── base.py      # BaseAdapter class
│   │       ├── l1_adapter.py  # Data Source (sport-aware)
│   │       ├── l2_adapter.py  # Calendar (sport-aware)
│   │       ├── l3_adapter.py  # Ideas
│   │       ├── l4_adapter.py  # Audio
│   │       ├── l5_adapter.py  # Media
│   │       ├── l6_adapter.py  # Assembly
│   │       ├── l7_adapter.py  # Distribution
│   │       └── l8_adapter.py  # Analytics
│   └── sports/          # ✅ NEW - Multi-sport provider system
│       ├── __init__.py  # SportRegistry, get_provider()
│       ├── base.py      # SportProvider, CalendarType, TeamData, MatchupData
│       ├── registry.py  # Provider registration and lookup
│       └── providers/
│           ├── nfl.py   # NFL: weekly calendar, 32 teams
│           └── nba.py   # NBA: daily calendar, 30 teams
├── models/              # User, Preset, Job, Output, ScheduledJob, APIUsage
├── services/
│   ├── auth_service.py  # Google OAuth (with Drive scope)
│   ├── job_service.py   # Job execution + SSE
│   ├── preset_service.py # Unified preset access (DB + JSON fallback)
│   ├── gdrive_service.py # ✅ Phase 5.1 - Google Drive sync
│   ├── oracle_service.py # ✅ Phase 5.2 - Backend health monitoring
│   └── scheduler_service.py # ✅ Phase 5.3 - Job scheduling
└── db/
    ├── __init__.py      # Central db instance
    └── session.py       # Session utilities
```

---

## Layer Reference

| Layer | Purpose | Adapter Method | v1 Script |
|-------|---------|----------------|-----------|
| L1 | Data fetching (APIs, web search) | `fetch()` | L1_data.py |
| L2 | Calendar & segment config | `configure()` | L2_calendar.py |
| L3 | Content idea generation | `generate()` | L3_ideas.py |
| L4 | TTS audio generation | `generate()` | L4_audio.py |
| L5 | Image/video generation | `generate()` | L5_media.py |
| L6 | Content assembly | `assemble()` | L6_assembly.py |
| L7 | Platform distribution | `distribute()` | L7_distribution.py |
| L8 | Analytics & feedback | `analyze()` | L8_analytics.py |

---

## API Endpoints

| Endpoint | Status | Notes |
|----------|--------|-------|
| POST /jobs | Working | Creates job, queues for execution |
| GET /jobs | Working | Lists jobs with pagination |
| GET /jobs/:id | Working | Job details + logs |
| GET /jobs/:id/stream | Working | SSE progress (real layer events) |
| DELETE /jobs/:id | Working | Cancel job |

### New Functions (Ready to Use)

```python
from app.core.pipeline.orchestrator import run_pipeline, run_pipeline_to_layer

# Full pipeline (all 8 layers)
context = run_pipeline(job_id, preset_config, progress_callback)

# Partial execution - stop after L5
context = run_pipeline_to_layer(job_id, preset_config, "L5", progress_callback)
```

### Preset Endpoints (Phase 3) ✅ NEW

| Endpoint | Status | Notes |
|----------|--------|-------|
| GET /presets | Working | List all presets (DB + JSON fallback) |
| GET /presets/:id | Working | Get preset details |
| POST /presets | Working | Create custom preset (requires auth) |
| PUT /presets/:id | Working | Update custom preset |
| DELETE /presets/:id | Working | Delete custom preset |
| POST /presets/:id/clone | Working | Clone preset for customization |
| POST /presets/seed | Working | Seed system presets to database |
| GET /presets/layers/:layer | Working | Get layer-specific presets (L3-L7) |
| GET /presets/tools | Working | Get tool configuration |

### Future Endpoints (Ready to Implement)

| Endpoint | Purpose |
|----------|---------|
| POST /jobs/{id}/run-to-layer/{layer} | Execute up to specific layer, stop |
| POST /jobs/{id}/resume-from/{layer} | Resume from checkpoint |
| GET /jobs/{id}/layers/{layer}/output | Get intermediate layer output |

---

## Pending Tasks

### Phase 3: Preset System - ✅ BACKEND COMPLETE
- [x] Create PresetService for unified preset access
- [x] Update API routes to use database instead of JSON
- [x] Create preset seeder to populate database from JSON
- [x] Auto-seed presets on app startup (20 presets seeded)
- [ ] Preset builder UI (frontend - Phase 5)
- [ ] Clone/customize flow (frontend - Phase 5)

### Phase 4: Multi-Sport Providers - ✅ COMPLETE
- [x] Create SportProvider base class and interface
- [x] Create SportRegistry for provider lookup
- [x] Implement NFLProvider (32 teams, weekly calendar)
- [x] Implement NBAProvider (30 teams, daily calendar)
- [x] Update L1Adapter with sport-aware data fetching
- [x] Update L2Adapter with sport-aware calendar types
- [x] Wire sport selection through orchestrator
- [x] Update sports API to use SportRegistry
- [x] Job API passes sport to orchestrator
- [ ] Enable MLB/NHL/EPL providers (when needed - just add provider file)

### Phase 5.1: G Drive Sync - ✅ COMPLETE
- [x] Create GDriveService for upload/sync operations
- [x] Add Drive scope to OAuth flow
- [x] Create sync API endpoints (/sync/*)
- [x] Integrate with L7 adapter (sync_to_drive method)
- [x] Folder organization: SPORT/week/matchup/

### Phase 5.2: Oracle Service - ✅ COMPLETE
- [x] Create OracleService for health monitoring
- [x] Health score calculation with issue tracking
- [x] Pipeline layer status for all adapters
- [x] API cost tracking (today/week/month, by provider/layer)
- [x] Job statistics from database
- [x] Health API endpoints (/health/*)
- [ ] File watching daemon (future expansion)
- [ ] SSE alerts (future expansion)

### Phase 5.3: Scheduler - ✅ COMPLETE
- [x] Create SchedulerService with cron support
- [x] Cron expression validation and parsing
- [x] Next run time calculation
- [x] Built-in NFL/NBA schedule presets
- [x] Scheduler API endpoints (/scheduler/*)
- [x] Manual trigger support
- [ ] Background worker daemon (future expansion)
- [ ] APScheduler integration (future expansion)

### Phase 5.4: Frontend UI - ✅ COMPLETE
- [x] PresetBuilder component for full preset creation
- [x] PresetEditor modal for clone/customize flow
- [x] Clone button on preset cards
- [x] Updated api.js with CRUD endpoints
- [x] Updated App.jsx with step 2.5 routing
- [x] CSS styles for new components

### Phase 5.5: Live Data Integration - ✅ COMPLETE
- [x] balldontlie API as primary data source
- [x] Fixed NFL balldontlie URL (was double-nested)
- [x] Fixed SportsBlaze filter ("Regular Season")
- [x] Season info methods on SportProviders
- [x] Playoff matchup support with round filtering
- [x] Dynamic NFL week calculation based on dates
- [x] New `/sports/:sport/playoffs` endpoint
- [x] Frontend period toggle (Regular/Playoffs)
- [x] Week/Date selectors on MatchupSelection
- [x] Updated .env with API keys

### Phase 5.6: UI Branding - ✅ COMPLETE
- [x] Goated Bets logo integration in header
- [x] CSS variables for brand colors (gold, purple, green)
- [x] Gold for primary CTAs (Generate, Build, Submit)
- [x] Purple for UI elements (steps, tabs, toggles, progress)
- [x] Green for selection states (card hover, downloads)
- [x] Header font: uppercase, italic, letter-spacing
- [x] Hidden "Playoffs Available" badges
- [x] Updated all component CSS files

### Phase 6.1: Auth UI - ✅ COMPLETE
- [x] AuthContext for user state management
- [x] LoginPage with Google OAuth button
- [x] ProtectedRoute component for route guards
- [x] api.js auth interceptors and endpoints
- [x] UserProfile component in header
- [x] Login/logout flow with localStorage token
- [x] Responsive header layout

### Phase 6.2: Scheduler UI - ✅ COMPLETE
- [x] SchedulerPage component with schedule list
- [x] ScheduleEditor modal with CRUD operations
- [x] CronBuilder/PresetSelector with live validation
- [x] Schedule trigger button (manual run)
- [x] Navigation button in header ("📅 Schedules")
- [x] Scheduler API endpoints in api.js
- [x] CSS styling matching brand colors

### Phase 7: Output Gallery - PENDING
- [ ] OutputsPage component
- [ ] Gallery grid with thumbnails
- [ ] Preview modal (images/videos)
- [ ] Download individual/batch files
- [ ] Filter by job, preset, sport, date
- [ ] Delete outputs

---

## Commands

```bash
# Start V2 backend
cd "AutomationScript" && source venv/bin/activate
python3 -m app.main  # Port 5001

# Test all 8 adapters
python3 -c "from app.core.pipeline.adapters import *; print('All 8 adapters OK')"

# Test orchestrator with all layers
python3 -c "
from app.core.pipeline.orchestrator import PipelineOrchestrator
o = PipelineOrchestrator('test', {'layers': ['L1','L2','L3','L4','L5','L6','L7','L8']})
for l in ['L1','L2','L3','L4','L5','L6','L7','L8']:
    print(f'{l}: {\"OK\" if o._get_adapter(l) else \"FAIL\"}')
"
```

---

## Architecture Notes

### Adapter Pattern (Option C)

Each adapter:
1. **Import Path Setup** - Adds `scripts/` to sys.path via BaseAdapter
2. **Progress Callbacks** - Emits SSE events during execution
3. **Clean Interface** - Single main method per adapter
4. **Result Serialization** - Returns `AdapterResult` dataclass

### Default Layer Configurations

```python
# Typical carousel preset
layers = ["L1", "L3", "L5", "L6", "L7"]

# Full pipeline with audio
layers = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]

# Quick test (data only)
layers = ["L1"]
```

### Partial Execution

```python
# Stop after L5 (before L6 assembly)
orchestrator.run_to_layer("L5")

# Result:
# - L1: completed
# - L3: completed
# - L5: completed
# - L6: not executed (not in layer_status)
```

---

## Sports Provider Architecture

### SportProvider Base Class

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

nfl.get_matchups("week18")  # List[MatchupData]
nba.get_matchups("2026-01-06")  # List[MatchupData]
```

### Calendar Types

| Sport | CalendarType | Period Format | Example |
|-------|--------------|---------------|---------|
| NFL | WEEKLY | phase + week | `week18` |
| NBA | DAILY | YYYY-MM-DD | `2026-01-06` |
| MLB | DAILY | YYYY-MM-DD | `2026-04-15` |
| NHL | DAILY | YYYY-MM-DD | `2026-01-06` |
| EPL | WEEKLY | matchday | `matchday20` |

### Sport-Aware Adapters

```python
# L1 and L2 adapters now detect sport from preset config
from app.core.pipeline.adapters import L1Adapter, L2Adapter

# NFL preset
nfl_adapter = L1Adapter({"sports": ["nfl"]})
nfl_adapter.get_preferred_tools()  # ["goatedbets_api", "sportsblaze", "balldontlie"]
nfl_adapter.get_teams()            # 32 NFL teams

# NBA preset
nba_adapter = L1Adapter({"sports": ["nba"]})
nba_adapter.get_preferred_tools()  # ["balldontlie", "goatedbets_api"]
nba_adapter.get_teams()            # 30 NBA teams
```

---

## Resume Prompt

```
You are Oracle. Read @docs/context/PIPELINE_CONTEXT.md - O90 session complete.

V2 Dashboard Status:
- Phase 2 ✅ All 8 adapters (L1-L8) wrapping v1 scripts
- Phase 3 ✅ PresetService with DB + JSON fallback, 20 presets seeded
- Phase 4 ✅ Multi-sport: NFL (weekly) + NBA (daily) providers
- Phase 5.1 ✅ G Drive Sync service
- Phase 5.2 ✅ Oracle Service (backend health monitoring)
- Phase 5.3 ✅ Scheduler Service (cron-style job scheduling)
- Phase 5.4 ✅ Frontend UI (Preset builder, Clone/customize)
- Phase 5.5 ✅ Live Data Integration (balldontlie API, playoffs)
- Phase 5.6 ✅ UI Branding (Goated Bets logo, color system)
- Phase 5.7 ✅ Dynamic Context System (NEW)
- Phase 6.1 ✅ Auth UI (Google OAuth, protected routes, user profile)
- Phase 6.2 ✅ Scheduler UI (schedule list, create/edit modal, cron presets)
- Phase 7 🔄 Output Gallery + PresetPreview (IN PROGRESS)

O90 Session Additions (Dynamic Context System):
- Oracle models: Session, Message, Snapshot, HealthStatus (app/models/oracle.py)
- Context manager with file watching (oracle/context_manager.py)
- Session spawner for VS Code/Claude (oracle/session_spawner.py)
- Oracle daemon for background ops (oracle/daemon.py)

Oracle Daemon Commands:
- python oracle/daemon.py start          # Start file watching
- python oracle/daemon.py spawn pipeline # Spawn pipeline session
- python oracle/daemon.py audit --quick  # Health check
- python oracle/daemon.py prompts        # Show resume prompts

Servers:
- Frontend: http://localhost:5173/ (Vite --strictPort)
- Backend: http://localhost:5001/ (Flask Media Engine V2)

Next: Continue Phase 7 Output Gallery or spawn separate sessions for Pipeline/Dashboard work
```
