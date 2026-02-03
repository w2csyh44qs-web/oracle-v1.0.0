# P21: Enhanced CodeOptimizer with Unified Maintenance Operations

**Status:** Complete
**Priority:** High
**Created:** 2026-01-07
**Completed:** 2026-01-07 (O94)
**Context:** Originated from P20 (L5 legacy code cleanup) - need automated way to detect and clean dead code

---

## Overview

Enhance the existing `CodeOptimizer` class in `maintenance/project_oracle.py` to handle three categories of automated code maintenance:

1. **Clean** - Remove unused imports, dead references, temporary flags
2. **Prune** - Detect and flag dead code, legacy markers, duplicate functions
3. **Optimize** - Suggest refactoring for long functions, layer violations

Keep the class name `CodeOptimizer` but expand its capabilities with a unified `optimize` CLI command.

---

## Key Design Decisions

1. **Always require `--apply`** - Safe default, always preview first
2. **Aggressive dead code detection with allowlist** - Flag everything, but maintain `config/optimizer_allowlist.json` for approved exceptions. After user confirms a function is intentionally unused (planned for future use), add to allowlist so it's not flagged again. Periodic review of allowlist during full audits.
3. **Include layer violation detection** - Detect when code crosses layer boundaries (e.g., L5 building prompts instead of L3)

---

## Current State

**Existing CodeOptimizer capabilities** (lines 2867-3323 in project_oracle.py):
- `_fix_unused_imports()` - Remove unused imports
- `_cleanup_cli_flags()` - Flag temporary CLI flags
- `_check_doc_code_gaps()` - Verify docs match code
- `_add_missing_docstrings()` - Identify missing docstrings
- `_validate_presets()` - Check preset JSON files
- `_safety_scan()` - Detect security anti-patterns

**What's missing:**
- Dead code detection (functions never called)
- Legacy marker detection (`# Legacy`, `# MVP`, `# V1`, `# Fallback`, `# TODO: remove`)
- Duplicate function detection
- Layer violation detection (code doing wrong layer's job)

---

## Implementation Plan

### 1. Add New Detection Methods to CodeOptimizer

**File:** `maintenance/project_oracle.py`

#### A. Dead Code Detection (`_detect_dead_code`)
```python
def _detect_dead_code(self) -> list:
    """Find functions that are never called anywhere in the codebase.

    Aggressive detection with allowlist support:
    - Flag ALL functions with 0 callers (except magic methods, CLI entry points)
    - Check against config/optimizer_allowlist.json for approved exceptions
    - Return both flagged items and allowlisted items (for periodic review)
    """
    # 1. Load allowlist from config/optimizer_allowlist.json
    # 2. Parse all .py files to find function definitions
    # 3. For each function, search for calls across all files
    # 4. Exclude: __init__, __str__, __repr__, main(), argparse entry points
    # 5. Check if function is in allowlist - if so, mark as "allowed" not "dead"
    # 6. Return both categories for display
```

#### A2. Allowlist Management (`_add_to_allowlist`, `_review_allowlist`)
```python
def _add_to_allowlist(self, func_signature: str, reason: str):
    """Add a function to the allowlist after user approval."""
    # func_signature: "file.py:function_name"
    # reason: "Planned for L8 analytics" or "CLI entry point"
    # Appends to config/optimizer_allowlist.json

def _review_allowlist(self) -> list:
    """Return allowlisted items for periodic review (full audit mode)."""
    # Show items that have been in allowlist >30 days
    # User can remove stale entries
```

**Allowlist file format** (`config/optimizer_allowlist.json`):
```json
{
  "dead_code": {
    "L5_media.py:_generate_modular_carousel": {
      "reason": "Alternative carousel path, keeping for flexibility",
      "added": "2026-01-07",
      "added_by": "Dev"
    }
  },
  "legacy_markers": {
    "api_utils.py:245": {
      "reason": "Legacy comment kept for V1 compatibility reference",
      "added": "2026-01-07"
    }
  }
}
```

#### B. Legacy Marker Detection (`_detect_legacy_markers`)
```python
def _detect_legacy_markers(self) -> list:
    """Find code marked as legacy/deprecated that should be reviewed."""
    # Patterns to detect:
    # - "# Legacy", "# MVP", "# V1", "# Fallback"
    # - "# TODO: remove", "# DEPRECATED", "# Old approach"
    # - Function names containing "legacy", "old_", "_v1"
```

#### C. Duplicate Function Detection (`_detect_duplicates`)
```python
def _detect_duplicates(self) -> list:
    """Find functions with identical or near-identical implementations."""
    # 1. Hash function bodies (normalized - remove whitespace/comments)
    # 2. Flag exact duplicates
    # 3. Flag similar functions (>80% token similarity)
```

#### D. Layer Violation Detection (`_detect_layer_violations`)
```python
def _detect_layer_violations(self) -> list:
    """Detect code doing work outside its designated layer."""
    # Rules:
    # - L5_media.py should NOT build prompts (that's L3)
    # - L3_ideas.py should NOT fetch data (that's L1)
    # - L6_assembly.py should NOT generate images (that's L5)
    # Pattern: Check imports and function calls against layer boundaries
```

### 2. Update `run_all()` Method

Add new operations to the operations list:
```python
def run_all(self, operations: list = None) -> dict:
    if operations is None:
        operations = ['imports', 'cli', 'docs', 'docstrings', 'presets',
                      'safety', 'dead_code', 'legacy', 'duplicates', 'layers']

    # ... existing operations ...

    if 'dead_code' in operations:
        results["dead_code"] = self._detect_dead_code()
    if 'legacy' in operations:
        results["legacy_markers"] = self._detect_legacy_markers()
    if 'duplicates' in operations:
        results["duplicates"] = self._detect_duplicates()
    if 'layers' in operations:
        results["layer_violations"] = self._detect_layer_violations()
```

### 3. Update `format_results()` Method

Add display sections for new detection types:
```python
# Dead code
if results.get("dead_code"):
    lines.append("💀 DEAD CODE (never called):")
    for item in results["dead_code"]:
        lines.append(f"   {item['file']}:{item['line']} - {item['function']}()")

# Legacy markers
if results.get("legacy_markers"):
    lines.append("🏚️ LEGACY MARKERS (review for removal):")
    for item in results["legacy_markers"]:
        lines.append(f"   {item['file']}:{item['line']} - {item['marker']}")

# Duplicates
if results.get("duplicates"):
    lines.append("👯 DUPLICATE FUNCTIONS:")
    for item in results["duplicates"]:
        lines.append(f"   {item['func1']} ≈ {item['func2']} ({item['similarity']}%)")

# Layer violations
if results.get("layer_violations"):
    lines.append("🚧 LAYER VIOLATIONS:")
    for item in results["layer_violations"]:
        lines.append(f"   {item['file']}: {item['description']}")
```

### 4. Update CLI Command: `clean` → `optimize`

**Update CLI parser** (~line 6026):
```python
# Rename and expand
opt_parser = subparsers.add_parser("optimize",
    help="🔧 Code optimizer - clean, prune, and optimize code")
opt_parser.add_argument("--apply", action="store_true")
opt_parser.add_argument("--clean", action="store_true", help="Remove unused imports, dead refs")
opt_parser.add_argument("--prune", action="store_true", help="Detect dead code, legacy markers")
opt_parser.add_argument("--check", action="store_true", help="Safety scan, layer violations")
opt_parser.add_argument("--all", action="store_true", help="Run all checks")
# Granular flags for power users
opt_parser.add_argument("--imports", action="store_true")
opt_parser.add_argument("--dead-code", action="store_true")
opt_parser.add_argument("--legacy", action="store_true")
opt_parser.add_argument("--duplicates", action="store_true")
opt_parser.add_argument("--layers", action="store_true")
# Allowlist management
opt_parser.add_argument("--allow", type=str, help="Add function to allowlist")
opt_parser.add_argument("--reason", type=str, help="Reason for allowlisting")
opt_parser.add_argument("--review-allowlist", action="store_true", help="Review stale allowlist entries")
```

**Update CLI handler** (~line 6978):
```python
elif args.command == "optimize":
    # Map category flags to operations
    if args.clean:
        operations.extend(['imports', 'cli', 'docs'])
    if args.prune:
        operations.extend(['dead_code', 'legacy', 'duplicates'])
    if args.check:
        operations.extend(['safety', 'layers', 'presets'])
    # ... granular overrides ...
```

### 5. Keep `clean` as Alias (Backwards Compatibility)

```python
# Add alias that maps to optimize --clean
clean_parser = subparsers.add_parser("clean", help="(Alias for 'optimize --clean')")
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `maintenance/project_oracle.py` | Add 5 detection methods + allowlist management, update `run_all()`, update `format_results()`, update CLI |
| `config/optimizer_allowlist.json` | **NEW** - Create empty allowlist file for approved exceptions |

---

## Usage After Implementation

```bash
# Full optimization (all checks)
python3 maintenance/project_oracle.py optimize --all

# Category-based
python3 maintenance/project_oracle.py optimize --clean   # imports, cli, docs
python3 maintenance/project_oracle.py optimize --prune   # dead_code, legacy, duplicates
python3 maintenance/project_oracle.py optimize --check   # safety, layers, presets

# Granular (power user)
python3 maintenance/project_oracle.py optimize --dead-code --legacy

# Apply fixes (not just preview)
python3 maintenance/project_oracle.py optimize --clean --apply

# Allowlist management
python3 maintenance/project_oracle.py optimize --allow "L5_media.py:_generate_modular_carousel" --reason "Alt carousel path"
python3 maintenance/project_oracle.py optimize --review-allowlist  # Show items >30 days old

# Backwards compatible
python3 maintenance/project_oracle.py clean  # Same as optimize --clean
```

---

## Typical Workflow (During Development)

1. **After making changes**, run quick prune check:
   ```bash
   python3 maintenance/project_oracle.py optimize --prune
   ```

2. **If dead code flagged**, Claude asks: "Is `_some_function` intentionally unused?"
   - If YES (planned for future): Add to allowlist
   - If NO (actually dead): Remove the code

3. **Periodic full audit** (weekly/monthly):
   ```bash
   python3 maintenance/project_oracle.py optimize --all --review-allowlist
   ```
   - Reviews allowlisted items >30 days old
   - Clean up stale entries

---

## Automation Integration

Add to recommended schedule in `maintenance/ORACLE_README.md`:

| Trigger | Command | Purpose |
|---------|---------|---------|
| After significant changes | `optimize --prune` | Find newly dead code |
| Weekly | `optimize --prune` | Accumulated dead code |
| Monthly | `optimize --all --review-allowlist` | Full codebase health + allowlist review |

---

## Estimated Scope

- ~150-200 lines of new detection methods
- ~30 lines CLI updates
- ~40 lines format_results updates
- Total: ~250 new lines in project_oracle.py

---

## Related

- **P20**: L5 Data Flow Refactor (completed) - motivated this plan
- **ADR-001**: 8-Layer Pipeline - layer violations reference this
- **ORACLE_README.md**: Update automation schedule
