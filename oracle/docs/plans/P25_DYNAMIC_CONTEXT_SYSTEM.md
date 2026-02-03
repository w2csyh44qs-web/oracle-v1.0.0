# P25: Dynamic Context System + Folder Cleanup

## Vision
Make the Oracle context system **project-agnostic** by:
1. Centralizing session counts in Oracle only (removing duplication from other contexts)
2. Creating a dynamic context registry that auto-discovers context files
3. Cleaning up legacy folders from V2 reorganization
4. Moving visions/ module to config/ for better organization

**Status:** ✅ COMPLETE
**Created:** January 8, 2026 (O101)
**Completed:** January 8, 2026 (O102)

---

## Part 1: Oracle-Only Session Counts

### Current Problem
Session counts are duplicated across ALL 5 context files:
```
**Session Count:** D104 / O101 / C13 / P24 / DB5
```
This requires manual updates to 5 files whenever ANY session advances.

### Solution: Centralized in Oracle
Only `ORACLE_CONTEXT.md` tracks the master session count. Other contexts track only their own session number.

**ORACLE_CONTEXT.md (Master):**
```markdown
## SESSION REGISTRY
| Context | Prefix | Current | Last Active |
|---------|--------|---------|-------------|
| Oracle | O | 101 | 2026-01-08 |
| Dev | D | 104 | 2026-01-08 |
| Dashboard | DB | 5 | 2026-01-08 |
| Crank | C | 13 | 2026-01-07 |
| Pocket | P | 24 | 2026-01-06 |
```

**DEV_CONTEXT.md (Simplified):**
```markdown
**Session:** D104
**Last Updated:** January 8, 2026
```
- No more "Session Count: D104 / O101 / C13 / P24 / DB5" line
- Just tracks its own session number

### Implementation
1. Update `ORACLE_CONTEXT.md` with SESSION REGISTRY table
2. Simplify other 4 context files (remove global session count line)
3. Update `session_spawner.py` to:
   - Increment session in Oracle registry when spawning
   - Update individual context's session number only
4. Add `get_session_count()` function to read from Oracle

---

## Part 2: Dynamic Context Registry

### Current Problem
Context system is hardcoded for 5 specific contexts (Oracle, Dev, Dash, Crank, Pocket).
- `session_spawner.py` has hardcoded prefixes (D/O/DB/C/P)
- `daemon.py` has hardcoded handoff rules
- Adding a new context requires code changes

### Solution: Config-Driven Context Registry
Create `oracle/context/context_registry.json` that defines available contexts:

```json
{
  "contexts": [
    {
      "id": "oracle",
      "prefix": "O",
      "name": "Oracle",
      "file": "ORACLE_CONTEXT.md",
      "role": "System coordinator, health monitoring",
      "resume_prompt": "you are oracle - read ORACLE_CONTEXT.md",
      "scope": ["oracle/", "docs/"]
    },
    {
      "id": "dev",
      "prefix": "D",
      "name": "Dev",
      "file": "DEV_CONTEXT.md",
      "role": "Backend development",
      "resume_prompt": "you are dev - read DEV_CONTEXT.md",
      "scope": ["app/", "scripts/", "config/"]
    }
  ],
  "handoff_rules": {
    "dash": {"to": ["dev", "crank"], "types": ["custom_preset_request", "bug_report"]},
    "dev": {"to": ["dash", "crank"], "types": ["new_feature", "preset_fixed"]},
    "crank": {"to": ["dev", "dash"], "types": ["bug_report", "content_ready"]},
    "oracle": {"to": ["*"], "types": ["health_alert", "task_assignment"]}
  }
}
```

### Benefits
- Add new contexts by editing JSON (no code changes)
- Remove project-specific contexts for other projects
- Handoff rules are configurable
- Oracle becomes truly project-agnostic

### Implementation
1. Create `oracle/context/context_registry.json`
2. Update `session_spawner.py` to read from registry
3. Update `daemon.py` to read handoff rules from registry
4. Update `astrocytes.py` context parsing to use registry

---

## Part 3: Folder Cleanup

### Findings
| Folder | Status | Action |
|--------|--------|--------|
| `docs/` (root) | Legacy artifact | DELETE |
| `docs/plans/` (root) | Legacy artifact | DELETE |
| `reports/` (root) | Legacy artifact | DELETE |
| `visions/` (root) | **ACTIVE** - used by all pipeline layers | MOVE to config/ |

### visions/ Migration
The visions module is actively imported by L2-L7 layers:
```python
from visions.vision_registry import VisionRegistry
```

**Migration Steps:**
1. Move `visions/vision_registry.py` → `config/visions/vision_registry.py`
2. Move `visions/__init__.py` → `config/visions/__init__.py` (or merge)
3. Update imports in all 6 layer files (L2-L7)
4. Delete empty `visions/` folder

**New Import:**
```python
from config.visions.vision_registry import VisionRegistry
```

---

## Part 4: Context File Template

Create a minimal, project-agnostic context template:

```markdown
# {CONTEXT_NAME} Context

> **Role:** {ROLE_DESCRIPTION}

**Session:** {PREFIX}{NUMBER}
**Last Updated:** {DATE}

---

## Resume Protocol
```
{RESUME_PROMPT}
```

## Scope
{SCOPE_DESCRIPTION}

## Current Tasks
_(none)_

## Recent Changes
### {DATE} - Session {NUMBER}
- {CHANGE_DESCRIPTION}

---

## Cross-Session Flags
**Status:** _(none)_
```

---

## Implementation Phases

### Phase 1: Cleanup (Quick Wins) ✅
- [x] Delete `docs/` folder at project root
- [x] Delete `reports/` folder at project root
- [x] Verify no code references these paths

### Phase 2: visions/ Migration ✅
- [x] Create `config/visions/` folder
- [x] Move `visions/vision_registry.py` → `config/visions/vision_registry.py`
- [x] Move `visions/__init__.py` → `config/visions/__init__.py`
- [x] Update imports in L2-L7 layer files
- [x] Delete old `visions/` folder
- [x] Test pipeline still works

### Phase 3: Context Registry ✅
- [x] Create `oracle/context/context_registry.json`
- [x] Create `oracle/context/__init__.py` with registry loader functions
- [x] Update `session_spawner.py` to use registry
- [x] Update `daemon.py` to use registry handoff rules
- [x] Test spawning and messaging still work

### Phase 4: Oracle-Only Session Counts ✅
- [x] Add SESSION REGISTRY table to ORACLE_CONTEXT.md
- [x] Simplify DEV_CONTEXT.md (remove global count)
- [x] Simplify DASHBOARD_CONTEXT.md
- [x] Simplify CRANK_CONTEXT.md
- [x] Simplify POCKET_CONTEXT.md

### Phase 5: Documentation ✅
- [x] Update WORKFLOW.md with new context system
- [x] Update ARCHITECTURE.md with context registry

---

## Files to Modify

| File | Changes |
|------|---------|
| `oracle/context/context_registry.json` | CREATE - Context definitions |
| `oracle/context/session_spawner.py` | Use registry instead of hardcoded |
| `oracle/context/daemon.py` | Use registry for handoff rules |
| `oracle/context/astrocytes.py` | Update Oracle registry on session changes |
| `oracle/docs/context/*.md` | Simplify - remove global session counts |
| `config/visions/vision_registry.py` | MOVE from visions/ |
| `app/core/pipeline/layers/_L*/` | Update visions import path |

---

## Rollback Plan
If issues arise:
1. Restore context files from git
2. Revert session_spawner.py and daemon.py
3. Move visions/ back to root

---

## New Rule: Plan Documentation

**Rule #26: Plan-First Documentation**
Before implementing any plan (P#), create `oracle/docs/plans/P{N}_{NAME}.md` so the plan can be read externally during implementation. This applies to all contexts.

---

## Implementation Summary (O101-O102)

### Files Created
| File | Purpose |
|------|---------|
| `oracle/context/context_registry.json` | Config-driven context definitions, handoff rules, ports |
| `oracle/context/__init__.py` | Registry loader functions |

### Files Modified
| File | Changes |
|------|---------|
| `oracle/context/session_spawner.py` | Uses registry for context_files, session_prefixes, ports, handoff rules |
| `oracle/context/daemon.py` | Uses registry for ALL_CONTEXTS via `get_context_ids()` |
| `oracle/docs/context/ORACLE_CONTEXT.md` | Added SESSION REGISTRY table |
| `oracle/docs/context/DEV_CONTEXT.md` | Simplified to `**Session:** D104` |
| `oracle/docs/context/DASHBOARD_CONTEXT.md` | Simplified to `**Session:** DB6` |
| `oracle/docs/context/CRANK_CONTEXT.md` | Simplified to `**Session:** C13` |
| `oracle/docs/context/POCKET_CONTEXT.md` | Simplified to `**Session:** P24` |
| `oracle/docs/overview/WORKFLOW.md` | Added P25 Dynamic Context System section |
| `oracle/docs/overview/ARCHITECTURE.md` | Added P25 registry documentation |
| `config/visions/` | Moved from `visions/` at project root |
| L2-L7 layer files | Updated visions import to `from config.visions.vision_registry` |

### Folders Deleted
- `docs/` (project root - legacy)
- `reports/` (project root - legacy)
- `visions/` (moved to config/)

### Registry Loader Functions
```python
from oracle.context import (
    get_context_ids,       # List all context IDs
    get_context,           # Get single context definition
    get_session_prefix,    # Get prefix for context (D, O, DB, etc.)
    get_context_file,      # Get context file path
    get_resume_prompt,     # Get resume prompt from registry
    get_handoff_rules,     # Get handoff rules
    get_ports,             # Get ports (normal/fallback)
    get_coordinator_context,  # Get coordinator (Oracle)
)
```

### Key Benefits Achieved
1. **Project-agnostic Oracle** - Can be copied to any project by editing registry JSON
2. **Single source of truth** - Session counts only in ORACLE_CONTEXT.md
3. **Config-driven** - No code changes needed to add/modify contexts
4. **Cleaner folder structure** - Legacy folders removed, visions moved to config/
