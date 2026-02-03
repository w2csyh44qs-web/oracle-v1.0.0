# P22: Phase 2 V2 Consolidation

**Created:** January 7, 2026 (O95)
**Objective:** Complete V2 consolidation - unified backend, frontend integration, import cleanup
**Status:** COMPLETE

---

## Executive Summary

**Phase 1 (COMPLETE):** Archived V1 folders, moved docs/maintenance to oracle/, cleaned root.

**Phase 2 (THIS PLAN):** Final consolidation:
1. Delete obsolete `dashboard/backend/` - use `app/` as single backend
2. Move `dashboard/frontend/` → `app/frontend/` - unified app structure
3. Full import refactor - eliminate all `scripts._L*` references
4. Fix dashboard performance lag
5. Update maintenance tools for new paths

---

## Why Two Backends Exist (Context)

| Aspect | app/ (V2 Backend) | dashboard/backend/ (MVP) |
|--------|-------------------|--------------------------|
| **Framework** | Flask + SQLAlchemy | Flask (minimal) |
| **Auth** | Google OAuth, sessions | None |
| **Database** | SQLite ORM | File system only |
| **Endpoints** | 40+ (auth, jobs, presets, sports, outputs, health, sync, scheduler) | 12 basic (/api/*) |
| **Job Tracking** | DB persistence, SSE streaming | In-memory only |
| **Status** | Production-ready | Obsolete MVP |

**Frontend expects V2 endpoints** (`/auth/login`, `/jobs`, `/presets`, etc.) - dashboard/backend/ uses incompatible `/api/*` routes and lacks required features.

**Decision:** Delete dashboard/backend/, consolidate everything into app/.

---

## Execution Plan

### Step 1: Delete Obsolete Dashboard Backend

```bash
# Archive first (reference only)
mv dashboard/backend/ archive/v1/dashboard_backend_obsolete/
```

### Step 2: Move Frontend into App

```bash
# Move frontend to unified structure
mv dashboard/frontend/ app/frontend/

# Move OAuth files to app/
mv dashboard/client_secret_*.json app/
mv dashboard/"Create OAuth credentials..." app/

# Remove empty dashboard/ folder
rm -rf dashboard/
```

### Step 3: Full Import Refactor

Update `app/core/pipeline/adapters/base.py` line 77:
```python
# Before:
scripts_dir = str(PROJECT_ROOT / "scripts")

# After:
layers_dir = str(PROJECT_ROOT / "app" / "core" / "pipeline" / "layers")
```

Fix hardcoded `scripts._L*` imports in 12 layer files.

### Step 4: Update Maintenance Tools

- Update health_monitor.py UX_RULES.md path
- Verify project_oracle.py V2 structure detection

### Step 5: Fix Dashboard Performance

Profile and optimize React re-renders, API payloads, SSE connections.

### Step 6: Verify

Test imports, frontend build, backend startup, health audit.

---

## Final V2 Structure

```
AutomationScript/
├── app/                          # UNIFIED V2 APPLICATION
│   ├── main.py
│   ├── frontend/                 # React + Vite (moved)
│   ├── api/routes/
│   ├── core/pipeline/
│   │   ├── adapters/
│   │   └── layers/
│   ├── models/
│   └── services/
│
├── oracle/                       # V2 Control center
│   ├── daemon.py
│   ├── maintenance/
│   ├── debugger/
│   └── docs/
│
├── config/
├── assets/
├── content/
├── data/
├── tests/
├── utils/
├── venv/
│
└── archive/v1/
    ├── dashboard_backend_obsolete/
    └── ...
```

---

## Checklist

### Documentation
- [x] Save plan to oracle/docs/plans/P22_PHASE2_V2_CONSOLIDATION.md

### Backend Consolidation
- [x] Archive dashboard/backend/ → archive/v1/dashboard_backend_obsolete/
- [x] Move dashboard/frontend/ to app/frontend/
- [x] Move OAuth files to app/
- [x] Remove empty dashboard/

### Import Refactor
- [x] Update base.py to use layers/ path
- [x] Fix all scripts._L* imports (12 files)
- [x] Restore visions/ (still needed by layers)

### Maintenance Updates
- [x] Update health_monitor.py paths (PROJECT_ROOT, ORACLE_DIR, DOCS_DIR, REPORTS_DIR)
- [x] Verify project_oracle.py (SCRIPTS_DIR → LAYERS_DIR, all paths updated)

### Performance
- [x] Profile dashboard (identified MatchupSelection re-fetching on tab switch)
- [x] Implement fixes (added matchupCache + useCallback/useMemo)
- [x] Added Vite build optimizations (chunking, dep pre-bundling)

### Verification
- [x] Test imports (L1, L3, L5, L6 adapters verified)
- [x] Test frontend build (vite build passes)
- [x] Run health audit (audit --quick passes, report generated)
