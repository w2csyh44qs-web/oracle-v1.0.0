# Pocket Context Document

> **YOU ARE POCKET** - Lightweight full-function session for portable/secondary workstation.

**Last Updated:** [DATE]
**Session Count:** P1
**Project:** [PROJECT_NAME]
**Purpose:** Full workflow capability with resource-conscious execution

---

## CURRENT DATE & PROJECT STATE

> **Today's Date:** Check system date
> **Project Phase:** [e.g., MVP, Beta, Production]

---

## POCKET SESSION PROTOCOL

### On Every Resume:
1. Read this file FIRST
2. Check what main sessions (D/O) have been doing
3. Execute task with efficiency in mind
4. Update this file + set handoff flags if needed

### Session Rules
1. **Full capability, light footprint** - Can do everything, prefer efficient paths
2. **Single-task focus** - One thing at a time, complete it, move on
3. **Handoff awareness** - Flag heavy tasks for main workstation
4. **Context sync** - Keep other context files informed

### Resume Prompt:
```
you are pocket - read POCKET_CONTEXT.md
```

---

## CAPABILITY MATRIX

| Task | Pocket Approach | Notes |
|------|-----------------|-------|
| **Dev work** | Full capability | Prefer smaller edits |
| **Heavy processing** | Single items | Avoid large batches |
| **Maintenance** | Full capability | Quick audits, doc updates |
| **Research/planning** | Full capability | Ideal for pocket |
| **Git operations** | Full capability | Commits, PRs, branches |

### Efficiency Guidelines
- **Prefer**: Quick edits, targeted work, research, planning, reviews
- **Batch carefully**: Resource-intensive operations (1-3 items)
- **Handoff when**: Heavy processing needed, multi-hour tasks

---

## CROSS-SESSION SYNC

### Reading Other Sessions
- `DEV_CONTEXT.md` - Current dev state
- `ORACLE_CONTEXT.md` - Health status, maintenance

### Pocket Flags
**Status:** _(none)_

<!--
Available flags:
- POCKET_COMPLETED: [task] - Finished something main sessions should know
- NEEDS_MAIN_WORKSTATION: [task] - Too heavy for pocket
- POCKET_IN_PROGRESS: [task] - Currently working on
-->

---

## QUICK COMMANDS

```bash
# Health check (lightweight)
python3 maintenance/project_oracle.py status

# Quick audit
python3 maintenance/project_oracle.py audit --quick

# Autosave (always do before ending)
python3 maintenance/project_oracle.py autosave
```

---

## RECENT CHANGES

### [DATE] - Session [N] (P[N])
- **[Task completed]**
  - What was done
  - Handoff notes if any

---

## PENDING TASKS

_(Tasks specifically for pocket sessions)_

- [ ] [Portable-appropriate task]

---

## SESSION END CHECKLIST

1. [ ] Run `python3 maintenance/project_oracle.py autosave`
2. [ ] Update Recent Changes
3. [ ] Set handoff flags if main workstation needs to continue
4. [ ] Update session count

---

*Pocket Context - Full capability, efficient execution*
