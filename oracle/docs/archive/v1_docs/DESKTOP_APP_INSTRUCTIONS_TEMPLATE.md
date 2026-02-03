# [PROJECT_NAME] - Desktop App Instructions

> **Claude Desktop companion document** - Attach this file when starting planning/research conversations in Claude Desktop.

## Project Overview

[Brief 2-3 sentence description of what this project does]

**Owner:** [Your name/role]
**Primary Tools:** Claude Code (VS Code), Claude Desktop (planning/research)
**Location:** iCloud Drive (synced between [list machines])
**Session Count:** D0 / O0 / C0 / P0 (as of [DATE])

---

## Multi-Machine Workflow

> **Project files sync via iCloud Drive** - Claude Code sessions can run from any machine.

### Machines in Use
| Machine | Primary Use | Session Types |
|---------|-------------|---------------|
| **[Main Machine]** | Main workstation | Dev (D#), Oracle (O#), Crank (C#) |
| **[Portable Machine]** | Portable sessions | Pocket (P#) - full capability, efficiency-focused |

### Switching Machines
1. **Before switching**: Run `autosave` in current Claude Code session
2. **Wait for iCloud sync**: Check Finder for cloud sync ✅ icon
3. **On new machine**: Start new Claude Code session with resume prompt

### First-Time Machine Setup
```bash
# 1. Generate SSH key (for GitHub operations)
ssh-keygen -t ed25519 -C "YOUR_EMAIL" -f ~/.ssh/id_ed25519 -N ""
ssh-keyscan github.com >> ~/.ssh/known_hosts
cat ~/.ssh/id_ed25519.pub | pbcopy
# Add to GitHub Settings > SSH Keys

# 2. Configure git
git config --global user.name "YOUR_USERNAME"
git config --global user.email "YOUR_EMAIL"

# 3. iCloud syncs project folder automatically - no git clone needed
```

---

## Architecture Summary

[Describe your project's architecture here]

### Key Components
| Component | Purpose | Key Files |
|-----------|---------|-----------|
| [Component 1] | [What it does] | `path/to/files` |
| [Component 2] | [What it does] | `path/to/files` |

### Tech Stack
- [Language/Framework 1]
- [Language/Framework 2]
- [APIs/Services used]

---

## Four-Session Model

| Session | Symbol | Focus | When to Use |
|---------|--------|-------|-------------|
| **Dev** | D# | Feature building, coding, testing | Main development work |
| **Oracle** | O# | Docs, health, maintenance, ADRs | Cleanup, documentation sync |
| **Crank** | C# | Content/output production, batch runs | Generating deliverables |
| **Pocket** | P# | Light full-function (portable machine) | Portable workstation |

### Session Isolation Principle
Each session type has its own context file and scope. Sessions should NOT cross into other session's territory:
- **Dev** builds features, **Oracle** documents them
- **Crank** generates output, **Dev** fixes bugs
- **Pocket** can do everything but prefers efficiency

### Resume Prompts
```
# Main Machine - Development
you are dev - read DEV_CONTEXT.md

# Main Machine - Maintenance
you are oracle - read ORACLE_CONTEXT.md

# Main Machine - Production/Output
you are crank - read CRANK_CONTEXT.md

# Portable Machine - Any task
you are pocket - read POCKET_CONTEXT.md
```

---

## Project Oracle (Maintenance System)

Automated health monitoring and documentation management.

### Core Commands
| Command | Purpose | When to Use |
|---------|---------|-------------|
| `audit --quick` | Fast health check + silent baseline | **Session start** |
| `audit` | Full project audit with report | After major features |
| `status` | Quick one-line status | When requested |
| `autosave` | Sync context + snapshot | **Every ~20 exchanges / breakpoints** |
| `autosave --archive-changes` | Archive old Recent Changes | Weekly |

### Session Automation
Claude automatically runs:
- `audit --quick` at session start
- `autosave` every ~20 exchanges or at natural breakpoints
- `autosave` before sensing compaction

---

## Claude Desktop Integration

> **Claude Desktop syncs via iCloud** - Same project folder accessible from both machines.

### Use Claude Desktop For:
- Architecture discussions and planning
- Feature design conversations
- Research and exploration
- Strategy decisions
- Cross-session context review

### Use Claude Code For:
- Writing/editing code
- Running oracle commands
- File manipulation
- Testing
- Executing production runs

### Recommended Attachments (Claude Desktop)
When starting a planning conversation, attach:
- This file (`DESKTOP_APP_INSTRUCTIONS.md`) - Overview
- `DEV_CONTEXT.md` - Current development state
- [Other key reference docs for your project]

---

## Key Documents

### Context Files (Source of Truth)
| File | Purpose |
|------|---------|
| `docs/context/DEV_CONTEXT.md` | Development session state, recent changes, pending tasks |
| `docs/context/ORACLE_CONTEXT.md` | Maintenance session state, oracle-specific context |
| `docs/context/CRANK_CONTEXT.md` | Production state, output queue |
| `docs/context/POCKET_CONTEXT.md` | Portable session state, multi-machine workflow |

### Reference Documents
| File | Purpose |
|------|---------|
| [Add your project's reference docs here] | |

---

## Workflow Patterns

### Starting a Dev Session (Main Machine)
1. Open VS Code workspace
2. New Claude Code chat
3. First message: `you are dev - read DEV_CONTEXT.md`
4. Claude runs `audit --quick` automatically

### Starting a Pocket Session (Portable Machine)
1. Verify iCloud synced (files show ✅ not downloading)
2. Open VS Code workspace
3. New Claude Code chat
4. First message: `you are pocket - read POCKET_CONTEXT.md`
5. Claude runs `audit --quick` automatically

### During Sessions
- Claude runs `autosave` every ~20 exchanges or at breakpoints
- Claude suggests compaction at natural stopping points
- User can say "continue" or "compact now"

### Ending Sessions
1. Claude runs `autosave` automatically
2. Context files updated, snapshot created
3. Wait for iCloud sync before switching machines

### Cross-Session Handoffs
| Flag | Set By | Means |
|------|--------|-------|
| `NEEDS_ORACLE_PASS` | Dev | Docs need sync after dev work |
| `NEEDS_DEV_ATTENTION: [reason]` | Oracle | Code issue needs dev input |
| `NEEDS_DEV_FIX: [issue]` | Crank | Production blocked by bug |
| `POCKET_COMPLETED: [task]` | Pocket | Finished task for main sessions |
| `NEEDS_MAIN_WORKSTATION: [task]` | Pocket | Too heavy for portable |

---

## Current State

### What's Built
- [List completed features]

### In Progress / Planned
- [List planned features]

---

## Quick Reference

### File Locations
```
[PROJECT_FOLDER]/
├── docs/
│   └── context/           # Session state files (D#, O#, C#, P#)
├── maintenance/           # Oracle scripts
├── reports/               # Audit reports, snapshots
├── [your source folders]
└── templates/             # Reusable templates
```

### Common Commands
```bash
# Oracle commands
python3 maintenance/project_oracle.py audit --quick
python3 maintenance/project_oracle.py autosave
python3 maintenance/project_oracle.py status

# [Add your project-specific commands here]
```

### Session Start Messages
```
# Main Machine sessions
you are dev - read DEV_CONTEXT.md
you are oracle - read ORACLE_CONTEXT.md
you are crank - read CRANK_CONTEXT.md

# Portable Machine sessions
you are pocket - read POCKET_CONTEXT.md
```

---

## Key Principles

[Add your project's guiding principles here]

1. **[Principle 1]** - [Description]
2. **[Principle 2]** - [Description]
3. **Context over memory** - Files are source of truth, not chat history
4. **Checkpoints over prayers** - Save state frequently

### User Preferences
- [Add relevant personal workflow preferences]
- ADHD-aware: benefits from structure, checkpoints, external tracking
- Values balance between work and personal life

---

*Last updated: [DATE]*
*From Project Oracle Template System*
