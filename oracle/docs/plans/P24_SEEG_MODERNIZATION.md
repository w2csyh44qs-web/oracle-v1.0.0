# P24: Stereotactic EEG Monitor Modernization

**Created:** January 8, 2026 (O98)
**Status:** ✅ COMPLETE
**Completed:** January 8, 2026 (O98)
**File:** `oracle/seeg.py` (2,144 lines)

---

## Vision

Modernize `oracle/seeg.py` to reflect the P23 Brain Cell Architecture. Keep the multi-mode terminal view (full/compact/split/min) but update display categories to show brain cell health, API connections, and cross-session state.

---

## Current vs New Display Categories

| Category | Before | After |
|----------|--------|-------|
| HEALTH | Score 0-10, visual bar | **Keep** |
| SESSION | Dev/Maintenance, activity % | **Keep** |
| CODE BLOAT | Critical, warnings, long functions, imports | **Simplify** - Just critical/warning counts |
| DOCUMENTATION | 6 file ages | **Replace with BRAIN CELLS** |
| AUTOSAVE | Last, reminder, safety trigger | **Keep** |
| FILES WATCHED | context, scripts, changes | **Keep** |
| OPTIMIZATIONS | Pending, backlog | **Replace with API STATUS** |
| PIPELINE | L1-L8 layer status | **Keep** |
| DEV TASKS / ORACLE TASKS | From context files | **Keep** |
| DEV BACKLOG / ORACLE BACKLOG | From IDEAS_BACKLOG.md | **Remove** |

---

## User Decisions

| Question | Answer |
|----------|--------|
| Daemon status | **Show** - Display running/stopped |
| API tracking | **Connection + usage** - Status plus call counts/costs |
| Code Bloat | **Keep simplified** - Just critical/warning counts |

---

## New Display Layout (Full Mode)

### Row 1: Health + Session
```
HEALTH: 8.4/10  ********..        SESSION: Development (manual)
                                  Activity: Medium (45%)
```

### Row 2: Brain Cells + API Connections
```
BRAIN CELLS                       API CONNECTIONS
|- Microglia: OK                  |- openai: OK $0.12 (5 calls)
|- Astrocytes: OK                 |- elevenlabs: OK $0.00
|- Oligodendrocytes: OK           |- fal: OK $0.00
|- Ependymal: OK                  |- pexels: OK
|- Cortex: OK                     |- gemini: WARN missing
|- Daemon: Running                |- tavily: OK
```

### Row 3: Code Health + Autosave
```
CODE HEALTH                       AUTOSAVE
|- Critical: 0                    |- Last: 12m ago
|- Warnings: 3                    |- Next reminder: 8m
|- Health Score: 84%              |- Safety trigger: 18m
```

### Row 4: Context + Files Watched
```
CONTEXT FILES                     FILES WATCHED
|- DEV_CONTEXT: 5m ago            |- context/*.md
|- ORACLE_CONTEXT: 2h ago         |- scripts/*.py
|- Session: O98 / D102            |- Changes: 12 since start
|- Cross-Session: _(none)_
```

### Row 5: Pipeline
```
PIPELINE
|- L1. L2. L3* L4. L5. L6. L7. L8.
|- Active: L3 (Ideas)
|- Cost today: $0.12 / $3.00
```

### Row 6: Session Tasks
```
DEV TASKS (D102)                  ORACLE TASKS (O98)
|- (none)                         |- (none)
```

---

## Implementation Phases

### Phase 1: Add New Data Methods (~80 lines)
```python
def _get_brain_cell_status(self) -> Dict[str, Any]:
    """Check status of each brain cell module + daemon."""
    # Try importing each module, check daemon lock file

def _get_api_status(self) -> Dict[str, Any]:
    """Get API connection + usage status."""
    # Call get_connection_health() from oligodendrocytes
    # Add usage data from api_calls.json if available

def _get_context_status(self) -> Dict[str, Any]:
    """Get context file ages and cross-session flags."""
    # DEV_CONTEXT age, ORACLE_CONTEXT age, session numbers
    # Parse cross-session flags from context files
```

### Phase 2: Update _render_full() Layout
1. **Row 2**: Replace DOCUMENTATION with BRAIN CELLS + API CONNECTIONS
2. **Row 3**: Rename CODE BLOAT -> CODE HEALTH (simplified)
3. **Row 4**: Replace complex docs with CONTEXT FILES + FILES WATCHED
4. **Row 5**: Keep PIPELINE (moved up)
5. **Row 6**: Keep SESSION TASKS (simplified)
6. **Remove**: BACKLOG sections entirely

### Phase 3: Update Other Modes
1. **Compact mode**: Add "Cells: 6/6 | APIs: 5/6" to status line
2. **Split mode**: Add brain cells to left panel, simplify right
3. **Minimized mode**: Add cell/API indicator

### Phase 4: Cleanup
1. Remove `_get_backlog_items()` entirely
2. Simplify CODE BLOAT to just critical/warning counts
3. Update module docstring for "Stereotactic EEG" naming

---

## Estimated Line Changes

| Section | Lines | Change |
|---------|-------|--------|
| New methods | +80 |
| Updated _render_full() | -100, +120 |
| Updated _render_compact() | -10, +15 |
| Updated _render_split() | -20, +30 |
| Removed methods (backlog) | -80 |
| **Net Change** | ~+15 lines |

---

## Files Modified

| File | Changes |
|------|---------|
| `oracle/seeg.py` | Main modernization |
| `oracle/docs/context/ORACLE_CONTEXT.md` | Update Recent Changes |

---

*P24 Plan - Stereotactic EEG Monitor Modernization*
