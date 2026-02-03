# Development Context Document

> **YOU ARE DEV** - Primary development session for feature building and implementation.

**Last Updated:** [DATE]
**Session Count:** D1
**Project:** [PROJECT_NAME]
**Purpose:** Single file for development session resume - read this FIRST and FULLY

---

## CURRENT DATE & PROJECT STATE

> **Today's Date:** Check system date
> **Project Phase:** [e.g., MVP, Beta, Production]
> **Current Sprint/Focus:** [Current work focus]

---

## DEV SESSION PROTOCOL

### On Every Resume:
1. **Read this entire file FIRST** - Contains all critical context
2. **Check Current State** - Know what's implemented vs pending
3. **Check Pending Tasks** - Continue where left off
4. **Check Recent Changes** - Understand what was just done
5. **After making changes** - Update this file

### Session Rules
1. **Dev Scope**: Feature building, testing, iteration
2. **Test After Changes**: Run tests to verify
3. **Document Changes**: Update "Recent Changes" section
4. **Context Efficiency**: Be concise, batch related work
5. **Python3 Rule**: Always use `python3` for script execution

### Resume Prompt:
```
you are dev - read DEV_CONTEXT.md
```

---

## CROSS-SESSION PROTOCOL

### Related Sessions
- **Maintenance**: See `ORACLE_CONTEXT.md`
- **Portable**: See `POCKET_CONTEXT.md` (if applicable)

### Cross-Session Flags
**Status:** _(none)_

<!--
Available flags:
- NEEDS_ORACLE_PASS - Set before compact; Oracle clears after maintenance
- NEEDS_DEV_ATTENTION: [reason] - Oracle sets if issues need dev input
-->

---

## PROJECT ARCHITECTURE

### Tech Stack
| Component | Technology |
|-----------|------------|
| Language | [e.g., Python 3.11] |
| Framework | [e.g., FastAPI, Django] |
| Database | [e.g., PostgreSQL, SQLite] |
| APIs | [List external APIs] |

### Project Structure
```
[PROJECT_NAME]/
├── src/                    # Source code
│   ├── [module]/          # Feature modules
│   └── utils/             # Shared utilities
├── tests/                  # Test files
├── config/                 # Configuration files
├── docs/                   # Documentation
│   ├── context/           # Session context files
│   └── overview/          # Reference documentation
├── maintenance/           # Oracle/health tools
├── output/                # Generated output
└── templates/             # Reusable templates
```

### Key Files
| File | Purpose |
|------|---------|
| `[main_script]` | Entry point |
| `config/[config_file]` | Configuration |
| `.env` | Environment variables (not committed) |

---

## API KEYS & SERVICES

| Key | Service | Purpose | Status |
|-----|---------|---------|--------|
| `[API_KEY_NAME]` | [Service] | [What it does] | [Active/Inactive] |

---

## CURRENT STATE

### Implemented Features
- [x] [Feature 1]
- [x] [Feature 2]
- [ ] [Feature 3 - in progress]

### Pipeline/Workflow Status
| Stage | Status | Output |
|-------|--------|--------|
| [Stage 1] | [Status] | [Output location] |
| [Stage 2] | [Status] | [Output location] |

---

## PENDING TASKS

### High Priority
1. [ ] [Task description]
   - Details: [Implementation notes]
   - Blocked by: [Dependencies if any]

### Medium Priority
2. [ ] [Task description]

### Low Priority / Future
3. [ ] [Task description]

---

## RECENT CHANGES

### [DATE] - Session [N] (D[N])
- **[Feature/Fix Name]**
  - What was done
  - Files modified
  - Any notes for future reference

### [PREVIOUS DATE] - Session [N-1] (D[N-1])
- **[Feature/Fix Name]**
  - What was done

---

## TECHNICAL NOTES

### Patterns & Conventions
- [Coding pattern used in this project]
- [Naming conventions]
- [Error handling approach]

### Known Issues / Tech Debt
- [Issue 1]: [Description and workaround]
- [Issue 2]: [Description]

### Testing
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test
python3 -m pytest tests/test_[module].py -v
```

---

## SESSION END CHECKLIST

Before ending a dev session:
1. [ ] Update "Recent Changes" with today's work
2. [ ] Update "Pending Tasks" (mark completed, add new)
3. [ ] Run tests to ensure nothing broken
4. [ ] Set `NEEDS_ORACLE_PASS` flag if docs need sync
5. [ ] Run: `python3 maintenance/project_oracle.py autosave`

---

*Dev Context Document - Development session source of truth*
