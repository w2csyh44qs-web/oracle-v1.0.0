# P26: Codebase Integrity Verification + Assessment

**Status:** Phase 1-5 COMPLETE (Phase 6 In Progress)
**Created:** January 8, 2026 (O103)
**Implemented:** January 8, 2026 (O104)

## Vision

**Key Metaphor:** Code = DNA. No separate "DNA" module needed.
- **Helicase** (`assess`) - Opens/unwinds new codebases for assessment
- **Topoisomerase** (`verify`) - Relieves tension from continuous edits, validates integrity

**Approach:** Reconfigure existing brain cell scripts to add new capabilities, NOT wrap them.

---

## Brain Cell Metaphor Reference

| Module | Metaphor | Function |
|--------|----------|----------|
| **microglia.py** | Immune cells | Clean, audit, ensure safety |
| **astrocytes.py** | Support cells | Stabilize context, snapshots |
| **oligodendrocytes.py** | Myelin producers | Optimize, enhance API efficiency |
| **ependymal.py** | CSF producers | Document flow, keep docs fresh |
| **cortex.py** | Brain cortex | Project-specific intelligence |
| **seeg.py** | Electrodes | Real-time monitoring |
| **helicase.py** | DNA unwinder | Assess new codebases (NEW) |
| **topoisomerase.py** | Tension reliever | Verify integrity after edits (NEW) |
| **pericytes.py** | BBB security | Security filtering (FUTURE P27) |

**Unofficially:**
- Documents = Neurons (knowledge carriers)
- Pipeline = Body (what the brain controls)

---

## Implementation Summary

### Files Created
| File | Lines | Purpose |
|------|-------|---------|
| `oracle/validation/__init__.py` | ~20 | Validation module package |
| `oracle/validation/topoisomerase.py` | ~530 | Integrity verification |
| `oracle/validation/helicase.py` | ~480 | Codebase assessment |

### Files Modified
| File | Changes |
|------|---------|
| `oracle/project_oracle.py` | Added verify/assess command routing (+120 lines) |
| `oracle/docs/context/ORACLE_CONTEXT.md` | Added Brain Cell modules, commands |

---

## Commands

### `verify` Command (Topoisomerase)
```bash
python3 oracle/project_oracle.py verify --quick     # Quick check (~5s)
python3 oracle/project_oracle.py verify             # Standard check
python3 oracle/project_oracle.py verify --full      # Full check
python3 oracle/project_oracle.py verify --perf      # Performance comparison
python3 oracle/project_oracle.py verify --perf --baseline  # Save baseline
python3 oracle/project_oracle.py verify --fix       # Preview fixes
python3 oracle/project_oracle.py verify --fix --apply  # Apply fixes
python3 oracle/project_oracle.py verify --install-hooks  # Pre-commit hooks
```

### `assess` Command (Helicase)
```bash
python3 oracle/project_oracle.py assess             # Assess codebase
python3 oracle/project_oracle.py assess --graph     # Build call graph
python3 oracle/project_oracle.py assess --graph -o graph.json  # Export graph
python3 oracle/project_oracle.py assess --ci github  # GitHub Actions template
python3 oracle/project_oracle.py assess --ci gitlab  # GitLab CI template
```

---

## Features Implemented

### Topoisomerase (verify)
- **CircularImportDetector** - Finds import cycles in codebase
- **IntegrityVerifier** - Runs quick/standard/full verification
- **PerformanceTracker** - Captures and compares performance baselines
- **AutoFixer** - Fixes trailing whitespace, missing EOF newline, missing `__init__.py`
- **HookManager** - Generates and installs pre-commit hooks

### Helicase (assess)
- **CodebaseAssessor** - Profiles codebase (files, lines, framework detection)
- **CallGraphAnalyzer** - Builds function call graph with Dashboard-compatible JSON
- **CITemplateGenerator** - Generates GitHub Actions and GitLab CI templates

---

## Implementation Phases

### Phase 1-5: COMPLETE
- [x] Core modules created
- [x] Call graph analysis
- [x] Performance regression tracking
- [x] Auto-fix capabilities
- [x] Pre-commit hooks & CI/CD templates

### Phase 6: IN PROGRESS
- [x] Update ORACLE_CONTEXT.md
- [ ] Update WORKFLOW.md with verification guide
- [x] Create plan doc (this file)
- [ ] Document P27 (pericytes.py for security)

---

## Test Results (O104)

```
verify --quick:
  Health Score: 96%
  Duration: 406ms
  Issues: 2 (0 critical, 2 warnings - circular imports)

assess:
  Project: AutomationScript
  Framework: Flask
  Files: 502 | Lines: 197,194
  Tests: Yes | CI: No | Docs: No
  Oracle Ready: Yes

assess --graph:
  Functions: 1853
  Edges: 1306
  Orphans: 1198
```

---

## Future (P27 - Pericytes)

**pericytes.py** - Blood-brain barrier security cells

Planned capabilities:
- Security vulnerability scanning
- Dependency audit (known CVEs)
- Secret detection (API keys in code)
- Input validation checking
- OWASP pattern detection
