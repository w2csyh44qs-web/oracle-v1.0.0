# P23: Oracle Brain Cell Architecture Plan

**Created:** January 8, 2026 (O97)
**Status:** ✅ COMPLETE
**Completed:** January 8, 2026 (O97)
**Objective:** Transform monolithic `project_oracle.py` (7,748 lines) into modular brain-inspired maintenance system

---

## Vision

Transform the monolithic `project_oracle.py` (7,748 lines) into a modular brain-inspired maintenance system where each script has a clear neurological metaphor and focused responsibility. **Oracle should be project-agnostic** - able to be copied to any project.

---

## Brain Cell Mapping

| Brain Cell | Script Name | Responsibility | Current Source |
|------------|-------------|----------------|----------------|
| **Microglia** | `microglia.py` | Error detection, code pruning, cleanup, debugging | CodeHealthAuditor, CodeOptimizer, LayerHealthAuditor, ScriptDebugger |
| **Astrocytes** | `astrocytes.py` | Context management, environment support, snapshots | ContextHealthAuditor, ContextAutoUpdater, ContextParser, SessionDiffTracker |
| **Oligodendrocytes** | `oligodendrocytes.py` | Performance optimization, API cost tracking, efficiency | APICostAuditor, APICallLogger, OptimizationDetector |
| **Ependymal/Neurons** | `ependymal.py` | Documentation sync, reports, knowledge flow | DocDriftAuditor, DocOptimizer, DocSyncEngine, ReportGenerator, desktop_sync.py |
| **sEEG** | `seeg.py` | Real-time monitoring dashboard (stereoEEG metaphor) | health_monitor.py (renamed) |
| **Cortex** | `cortex.py` | Project-specific tools (presets, pipeline, content types) | PresetAnalyzer, project-specific configs |

> Note: "Neurons" is an unofficial alias for ependymal (docs/knowledge flow). Folder names remain neutral (not brain-themed).

---

## Current Oracle Folder Structure

```
oracle/                           # CURRENT STATE
├── __init__.py
├── daemon.py                     # Cross-session daemon
├── context_manager.py            # Context file management
├── session_spawner.py            # Session spawning
├── maintenance/
│   ├── project_oracle.py         # 7,748 lines (MONOLITHIC)
│   ├── health_monitor.py         # 2,106 lines
│   ├── desktop_sync.py           # 291 lines
│   ├── health_monitor_config.json
│   ├── ORACLE_README.md
│   └── reports/                  # Output directory
├── debugger/
│   └── __init__.py               # Empty
├── docs/
│   ├── context/                  # 5 context files
│   ├── overview/                 # Reference docs
│   ├── plans/                    # Implementation plans
│   ├── templates/                # Context templates
│   └── archive/                  # Old versions
└── reports/                      # Duplicate reports folder
```

---

## Proposed File Structure

```
oracle/
├── __init__.py
├── project_oracle.py             # MOVED: Main CLI orchestrator (~400 lines)
├── seeg.py                       # MOVED+RENAMED: Real-time monitoring (~600 lines)
├── session_spawner.py            # Session spawning (keep at root - general utility)
│
├── maintenance/                  # Audit, cleanup, debugging
│   ├── __init__.py
│   ├── microglia.py              # Error detection, cleanup, debugging (~900 lines)
│   └── config.json               # Health monitor config (renamed)
│
├── context/                      # Context & session management
│   ├── __init__.py
│   ├── astrocytes.py             # Context, snapshots, environment (~600 lines)
│   ├── context_manager.py        # MOVED: Context file management
│   └── daemon.py                 # MOVED: Cross-session daemon
│
├── optimization/                 # Performance & efficiency
│   ├── __init__.py
│   └── oligodendrocytes.py       # Performance & cost optimization (~500 lines)
│
├── sync/                         # Documentation & knowledge flow
│   ├── __init__.py
│   └── ependymal.py              # Doc sync, reports, desktop sync (~800 lines)
│
├── project/                      # Project-specific tools
│   ├── __init__.py
│   └── cortex.py                 # Presets, pipeline info (~300 lines)
│
├── reports/                      # Consolidated reports (remove duplicates)
│   ├── audits/
│   ├── snapshots/
│   ├── .health_status.json
│   └── api_calls.json
│
└── docs/                         # Keep as-is
    ├── context/
    ├── overview/
    ├── plans/
    ├── templates/
    └── archive/

# DELETED:
# - debugger/                     # Empty folder
# - maintenance/health_monitor.py # Moved to seeg.py at root
# - maintenance/desktop_sync.py   # Merged into sync/ependymal.py
# - maintenance/project_oracle.py # Moved to root
```

---

## Folder Changes Summary

| Folder | Contents | Purpose |
|--------|----------|---------|
| `oracle/` (root) | project_oracle.py, seeg.py, session_spawner.py | Main orchestration & utilities |
| `maintenance/` | microglia.py | Audit, cleanup, debugging |
| `context/` | astrocytes.py, context_manager.py, daemon.py | Context & session management |
| `optimization/` | oligodendrocytes.py | Performance & API costs |
| `sync/` | ependymal.py | Documentation sync & reports |
| `project/` | cortex.py | Project-specific tools |
| `reports/` | audits/, snapshots/ | Output files |
| `docs/` | context/, overview/, plans/ | Documentation |

---

## Class Distribution

### microglia.py - "Immune System" (~900 lines)
**Purpose**: Detect damage, prune dead code, clean up, debug scripts
```python
# From project_oracle.py:
- CodeHealthAuditor (line 2102) - code health analysis
- CodeOptimizer (line 2869) - code quality suggestions
- LayerHealthAuditor (line 2556) - layer structure validation
- ScriptDebugger (line 1146) - script execution tracing
- cleanup_old_files() - report cleanup
- _prune_completed_tasks() - task pruning
- ACCEPTED_LONG_FUNCTIONS dict - trim to ~20 essential entries
- HISTORICAL_SCRIPTS dict - trim to ~10 essential entries
```
**Commands**: `audit`, `clean`, `debug-script`

### astrocytes.py - "Support System" (~600 lines)
**Purpose**: Maintain environment, manage context, snapshots
```python
# From project_oracle.py:
- ContextHealthAuditor (line 2730) - context file monitoring
- ContextAutoUpdater (line 4834) - auto-update context files
- ContextParser (line 1614) - parse DEV_CONTEXT.md
- SessionDiffTracker (line 4342) - session change tracking / snapshots
- CrossSessionBriefing (line 580) - cross-session info
```
**Commands**: `status`, `context`, `snapshot`

### seeg.py - "Real-Time Monitoring" (~600 lines)
**Purpose**: Stereo-EEG metaphor - real-time project activity monitoring dashboard
```python
# From health_monitor.py (RENAME, keep mostly intact):
- KeyboardReader - non-blocking keyboard input
- HealthMonitorEventHandler - file system events
- FileWatcher - file change monitoring
- OracleHealthMonitor - main dashboard class
- Real-time dashboard display modes
- Hotkey integration
- Configuration via health_monitor_config.json
```
**Commands**: `monitor`

### oligodendrocytes.py - "Speed & Efficiency" (~500 lines)
**Purpose**: Optimize performance, track costs, improve efficiency
```python
# From project_oracle.py:
- APICostAuditor (line 2632) - API cost tracking
- APICallLogger (line 1356) - API call logging
- OptimizationDetector (line 892) - find optimization opportunities
- OptimizationEngine (line 4210) - orchestrate optimizations
```
**Commands**: `optimize`, `api-log`, `costs`

### ependymal.py - "Flow & Circulation" aka "Neurons" (~800 lines)
**Purpose**: Sync documentation, reports, circulate knowledge, maintain flow
```python
# From project_oracle.py:
- DocDriftAuditor (line 2350) - detect doc staleness
- DocOptimizer (line 3750) - documentation optimization
- DocSyncEngine (line 5112) - sync docs with code
- DocChangeDetector (line 406) - track doc changes
- ReportGenerator (line 5886) - audit report generation
- Issue/Suggestion/AuditReport dataclasses

# From desktop_sync.py:
- Merge functionality into this module
```
**Commands**: `sync`, `docs`, `report`

### cortex.py - "Project-Specific Intelligence" (~300 lines)
**Purpose**: Project-specific tools that shouldn't be in generic Oracle
```python
# From project_oracle.py:
- PresetAnalyzer (line 7562) - preset reference and validation
- Any pipeline-specific configuration parsing
- Content type analysis
- Layer-specific tooling
```
**Commands**: `presets`, `layers`, `pipeline-info`

### project_oracle.py - "Central Orchestrator" (~400 lines)
**Purpose**: Main CLI, imports modules, routes commands
```python
# Keep:
- Main CLI argument parsing
- Command routing to appropriate module
- Shared utilities (debug_log, cleanup_old_files, load_config)
- Configuration loading (PROJECT_ROOT, paths)
- `config` command for debugging

# Remove:
- All 23+ classes (moved to cell modules)
- All audit/optimize/sync logic (delegated)
- PresetAnalyzer (moved to cortex.py)
```
**Commands**: Routes all commands to appropriate cell module

---

## Commands Consolidation

### Final Command List (13 commands)

| Command | Module | Purpose |
|---------|--------|---------|
| `audit` | microglia | Health audits (--quick, --deep, --code) |
| `clean` | microglia | Unified cleanup (--reports, --tasks, --dead-code) |
| `debug-script` | microglia | Script debugging/tracing |
| `status` | astrocytes | One-line health summary |
| `context` | astrocytes | Context file management |
| `snapshot` | astrocytes | Context snapshot (--sync flag for autosave) |
| `monitor` | seeg | Real-time dashboard |
| `optimize` | oligodendrocytes | Performance optimization |
| `api-log` | oligodendrocytes | API cost tracking |
| `sync` | ependymal | Documentation sync (--desktop flag) |
| `docs` | ependymal | Doc optimization |
| `report` | ependymal | Full report generation |
| `config` | project_oracle | Show parsed configuration (debugging) |
| `presets` | cortex | Preset reference and validation |

### Removed Commands

| Command | Reason |
|---------|--------|
| `prune` | Merged into `clean --dead-code` |
| `suggest-docs` | Rarely used, low value |
| `suggest-code-history` | Rarely used, low value |
| `briefing` | daemon.py handles cross-session now |
| `autosave` | Merged into `snapshot --sync` |
| `desktop-sync` | Merged into `sync --desktop` |
| `diff --baseline` | Merged into `snapshot` |

---

## Implementation Phases

### Phase 0: Folder Setup
1. **Create new folders**
   ```bash
   mkdir -p oracle/context oracle/optimization oracle/sync oracle/project
   touch oracle/context/__init__.py oracle/optimization/__init__.py
   touch oracle/sync/__init__.py oracle/project/__init__.py
   ```

2. **Consolidate reports folders**
   - Keep `oracle/reports/` as the single reports location
   - Move contents from `oracle/maintenance/reports/` and `oracle/docs/oracle reports/`
   - Update all path references in code

3. **Remove empty `oracle/debugger/` folder**

### Phase 1: Create Brain Cell Modules
1. **Create `oracle/maintenance/microglia.py`** (~900 lines)
2. **Create `oracle/context/astrocytes.py`** (~600 lines)
3. **Move+rename to `oracle/seeg.py`** (~600 lines)
4. **Create `oracle/optimization/oligodendrocytes.py`** (~500 lines)
5. **Create `oracle/sync/ependymal.py`** (~800 lines)
6. **Create `oracle/project/cortex.py`** (~300 lines)

### Phase 2: Slim project_oracle.py (~400 lines)
1. Move `oracle/maintenance/project_oracle.py` → `oracle/project_oracle.py`
2. Remove all extracted classes (23+)
3. Add imports from submodules
4. Update CLI to route commands to modules

### Phase 3: Move Existing Files
1. Move `oracle/context_manager.py` → `oracle/context/context_manager.py`
2. Move `oracle/daemon.py` → `oracle/context/daemon.py`
3. Rename `oracle/maintenance/health_monitor_config.json` → `oracle/maintenance/config.json`

### Phase 4: Delete Merged Files + Cleanup
1. Delete `oracle/maintenance/desktop_sync.py` (merged into sync/ependymal.py)
2. Delete `oracle/debugger/` folder (empty)
3. Consolidate report folders to `oracle/reports/`

### Phase 5: Update Imports & References
1. Update ORACLE_CONTEXT.md with new commands and folder structure
2. Update all imports for new locations
3. Update seeg.py config path

### Phase 6: Test All Commands
```bash
python3 oracle/project_oracle.py audit --quick
python3 oracle/project_oracle.py status
python3 oracle/project_oracle.py monitor
python3 oracle/project_oracle.py sync --dry-run
python3 oracle/project_oracle.py presets
python3 oracle/project_oracle.py config
python3 oracle/project_oracle.py clean --reports
python3 oracle/project_oracle.py snapshot
python3 oracle/project_oracle.py report
```

---

## Estimated Line Counts (Post-Refactor)

| File | Location | Lines | Change |
|------|----------|-------|--------|
| project_oracle.py | `oracle/` | ~400 | -7,348 (moved+slimmed) |
| microglia.py | `oracle/maintenance/` | ~900 | new |
| astrocytes.py | `oracle/context/` | ~600 | new |
| seeg.py | `oracle/` | ~600 | moved+renamed |
| oligodendrocytes.py | `oracle/optimization/` | ~500 | new |
| ependymal.py | `oracle/sync/` | ~800 | new |
| cortex.py | `oracle/project/` | ~300 | new |
| health_monitor.py | - | 0 | deleted (moved) |
| desktop_sync.py | - | 0 | deleted (merged) |
| **Total** | | ~4,100 | **-5,850 lines** |

---

## Module Interface Pattern

Each cell module exports functions that project_oracle.py routes to:

```python
# oracle/maintenance/microglia.py
def run_audit(quick=False, deep=False, code_only=False) -> AuditReport
def run_clean(reports=False, tasks=False, dead_code=False) -> CleanupResult
def run_debug_script(script_path) -> DebugResult

# oracle/context/astrocytes.py
def get_status() -> str
def manage_context() -> None
def create_snapshot(sync=False) -> SnapshotResult

# oracle/seeg.py
def run_monitor() -> None  # blocking real-time dashboard

# oracle/optimization/oligodendrocytes.py
def run_optimize() -> OptimizeResult
def get_api_log() -> list

# oracle/sync/ependymal.py
def run_sync(dry_run=True, desktop=False) -> SyncResult
def run_docs() -> DocsResult
def generate_report() -> str

# oracle/project/cortex.py
def analyze_presets() -> PresetAnalysis
```

---

## Import Structure in project_oracle.py

```python
from oracle.maintenance.microglia import run_audit, run_clean, run_debug_script
from oracle.context.astrocytes import get_status, manage_context, create_snapshot
from oracle.optimization.oligodendrocytes import run_optimize, get_api_log
from oracle.sync.ependymal import run_sync, run_docs, generate_report
from oracle.project.cortex import analyze_presets
from oracle import seeg

# Route commands
if args.command == "audit":
    run_audit(quick=args.quick)
elif args.command == "monitor":
    seeg.run_monitor()
# etc.
```

---

*P23 - Oracle Brain Cell Architecture Plan*
