# Oracle Context Document

> **YOU ARE ORACLE** - Maintenance session for documentation, health checks, and project hygiene.

**Last Updated:** [DATE]
**Session Count:** O1
**Project:** [PROJECT_NAME]
**Purpose:** Single file for maintenance session resume - read this FIRST and FULLY

---

## CURRENT DATE & PROJECT STATE

> **Today's Date:** Check system date
> **Project Phase:** [e.g., MVP, Beta, Production]

---

## ORACLE SESSION PROTOCOL

### On Every Resume:
1. **Read this entire file FIRST**
2. **Run health check**: `python3 maintenance/project_oracle.py audit --quick`
3. **Check Cross-Session Flags** - Handle any `NEEDS_ORACLE_PASS`
4. **After making changes** - Update this file

### Session Rules
1. **Oracle Scope**: Docs, health fixes, maintenance - NOT new features
2. **Test After Changes**: Run `config -v` to verify parsing
3. **Document Changes**: Update "Recent Changes" section
4. **Cross-Project Features**: Oracle capabilities should work across all project modules
5. **Python3 Rule**: Always use `python3` for script execution

### Automation Triggers
| Trigger | Command | Say |
|---------|---------|-----|
| Session start | `audit --quick` | "Checking project health..." |
| Every ~20 exchanges | `autosave` | "Autosaving..." |
| Before compaction | `autosave` | "Autosaved. Ready to compact." |

### Resume Prompt:
```
you are oracle - read ORACLE_CONTEXT.md
```

---

## CROSS-SESSION PROTOCOL

### Related Sessions
- **Development**: See `DEV_CONTEXT.md`
- **Portable**: See `POCKET_CONTEXT.md` (if applicable)

### Cross-Session Flags
**Status:** _(none)_

<!--
Available flags:
- NEEDS_ORACLE_PASS - Dev sets; Oracle clears after maintenance
- NEEDS_DEV_ATTENTION: [reason] - Oracle sets if issues need dev input
-->

### Oracle Responsibilities
| Document | Update When... |
|----------|----------------|
| DEV_CONTEXT.md | Sync with actual project state |
| CHANGELOG.md | Archive old Recent Changes |
| ARCHITECTURE.md | Pipeline/structure changes |
| README.md | Project overview changes |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Health Score | [Last score]/10 |
| Critical Issues | [Count] |
| Warnings | [Count] |
| Last Audit | [Date] |

### Implemented Oracle Features
- [x] Health audit system
- [x] Context file syncing
- [x] Autosave with snapshots
- [ ] [Pending feature]

### Pending Maintenance Tasks
- [ ] [Task 1]
- [ ] [Task 2]

---

## RECENT CHANGES

### [DATE] - Session [N] (O[N])
- **[Maintenance task]**
  - What was done
  - Health score before/after

---

## COMMANDS REFERENCE

### Core Commands
```bash
# Session start - health check + baseline
python3 maintenance/project_oracle.py audit --quick

# Quick status check
python3 maintenance/project_oracle.py status

# Autosave (sync + snapshot)
python3 maintenance/project_oracle.py autosave

# Full audit with report
python3 maintenance/project_oracle.py audit

# View parsed config
python3 maintenance/project_oracle.py config -v
```

### Sync Commands
```bash
# Preview changes (dry-run)
python3 maintenance/project_oracle.py sync

# Apply changes
python3 maintenance/project_oracle.py sync --apply

# Archive old Recent Changes
python3 maintenance/project_oracle.py sync --apply --archive-changes
```

---

## WHAT ORACLE CHECKS

### Code Health
- Unused imports
- Long functions (>100 lines)
- TODO/FIXME comments
- Hardcoded credentials
- Syntax errors

### Documentation Drift
- Scripts in docs that don't exist
- Broken cross-references
- Stale timestamps

### Context Health
- Required sections present
- Timestamp freshness
- Pending task accumulation

---

## SESSION END CHECKLIST

Before ending an oracle session:
1. [ ] Update "Recent Changes" with today's work
2. [ ] Update health score in "Current State"
3. [ ] Clear any cross-session flags handled
4. [ ] Run: `python3 maintenance/project_oracle.py autosave`

---

*Oracle Context Document - Maintenance session source of truth*
