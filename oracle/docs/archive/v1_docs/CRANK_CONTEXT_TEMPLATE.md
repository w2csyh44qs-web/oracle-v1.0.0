# Crank Context Document

> **YOU ARE CRANK** - Production/output session for generating deliverables and content.

**Last Updated:** [DATE]
**Session Count:** C1
**Project:** [PROJECT_NAME]
**Purpose:** Single file for production session resume - read this FIRST and FULLY

---

## CURRENT DATE & PROJECT STATE

> **Today's Date:** Check system date
> **Project Phase:** [e.g., MVP, Beta, Production]
> **Current Production Cycle:** [e.g., Week 16, Sprint 5, Q4 Batch]

---

## CRANK SESSION PROTOCOL

### On Every Resume:
1. Read this file FIRST
2. Check generation queue status
3. Execute production tasks
4. Update this file with completion status

### Session Rules
1. **Crank Scope**: Content production, batch generation, quality review
2. **Quality over speed**: Verify outputs before marking complete
3. **Document outputs**: Update queue status after each batch
4. **Flag issues**: Set flags if dev fixes needed

### Resume Prompt:
```
you are crank - read CRANK_CONTEXT.md
```

---

## PRODUCTION QUEUE

### Current Batch
| Item | Status | Output Location | Notes |
|------|--------|-----------------|-------|
| [Item 1] | [Pending/In Progress/Complete] | [path] | |
| [Item 2] | [Pending/In Progress/Complete] | [path] | |

### Completed This Cycle
- [x] [Completed item 1]
- [x] [Completed item 2]

### Queued for Next Cycle
- [ ] [Future item 1]
- [ ] [Future item 2]

---

## CROSS-SESSION SYNC

### Reading Other Sessions
- `DEV_CONTEXT.md` - Check for new features to use
- `ORACLE_CONTEXT.md` - Check health status before big batches

### Crank Flags
**Status:** _(none)_

<!--
Available flags:
- NEEDS_DEV_FIX: [issue] - Something broken, needs dev attention
- GENERATION_IN_PROGRESS: [batch] - Long-running batch, don't interrupt
- CRANK_COMPLETED: [batch] - Batch done, ready for review/distribution
-->

---

## QUICK COMMANDS

```bash
# Check project health before big batch
python3 maintenance/project_oracle.py status

# Autosave after completing batch
python3 maintenance/project_oracle.py autosave

# [Add your project-specific generation commands here]
# python3 scripts/[your_generator].py --batch [args]
```

---

## OUTPUT LOCATIONS

| Content Type | Location | Format |
|--------------|----------|--------|
| [Type 1] | `output/[folder]/` | [format] |
| [Type 2] | `output/[folder]/` | [format] |
| Final/Distribution | `output/final/` | [format] |

---

## RECENT CHANGES

### [DATE] - Session [N] (C[N])
- **[Batch/Production task]**
  - Items generated
  - Quality notes
  - Any issues encountered

---

## SESSION END CHECKLIST

1. [ ] Update production queue status
2. [ ] Run `python3 maintenance/project_oracle.py autosave`
3. [ ] Set flags if dev attention needed
4. [ ] Update session count

---

*Crank Context - Production session source of truth*
