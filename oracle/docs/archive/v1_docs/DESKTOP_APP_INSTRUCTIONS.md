# GOATED Content Automation - Project Instructions

## Project Overview

GOATED is a sports betting content automation pipeline that transforms trending sports narratives into short-form video content for social media. The system uses an 8-layer architecture orchestrated by Claude Code, with a comprehensive maintenance system (Project Oracle) for health monitoring and documentation management.

**Owner:** V, stroke neurologist with alternating work weeks, developing this during weeks off
**Primary Tools:** Claude Code (VS Code), Claude Desktop (planning/research)
**Location:** iCloud Drive (synced between Mac Mini and MacBook Air)
**Session Count:** D98 / O72 / C10 / P0 (as of December 23, 2025)

---

## Multi-Machine Workflow

> **Project files sync via iCloud Drive** - Claude Code sessions can run from any machine.

### Machines in Use
| Machine | Primary Use | Session Types |
|---------|-------------|---------------|
| **Mac Mini** | Main workstation | Dev (D#), Oracle (O#), Crank (C#) |
| **MacBook Air** | Portable sessions | Pocket (P#) - full capability, efficiency-focused |

### Switching Machines
1. **Before switching**: Run `autosave` in current Claude Code session
2. **Wait for iCloud sync**: Check Finder for cloud sync ✅ icon
3. **On new machine**: Start new Claude Code session with resume prompt

### First-Time Machine Setup
```bash
# 1. Generate SSH key (for GitHub operations)
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519 -N ""
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

### 8-Layer Content Pipeline
| Layer | Name | Function | Key Tools |
|-------|------|----------|-----------|
| L1 | Trend Detection | Find trending sports narratives | Tavily API, web search |
| L2 | Segmentation | Break trends into content segments | OpenAI GPT |
| L3 | Ideation | Generate video ideas with scripts | OpenAI GPT, presets |
| L4 | Audio | Text-to-speech generation | ElevenLabs (primary), OpenAI TTS |
| L5 | Media | Source visuals and B-roll | FAL AI, Gemini, Pexels API |
| L6 | Assembly | Compose final videos | MoviePy, FFmpeg |
| L7 | Distribution | Quality check, distribution | Manual + automated |
| L8 | Analytics | Track performance, feed back | Planned |

### Vision System (Above Layers)
Three content philosophies that inform L3 ideation:
- **Nostradamus:** Predictive takes before outcomes
- **Historian:** Post-event analysis and narratives
- **Trendsetter:** Real-time reactive content

### Preset System
Hierarchical configuration: Global → Layer → Idea-specific
Controls voice, pacing, visual style, music, transitions per content piece.

**Active presets:**
- `carousel_illustrated` - 3-slide Instagram carousels with illustrated style
- `carousel_illustrated_reels` - Carousels + 9:16 video reels
- `meme_mashup` - Athlete clip + meme template videos (planned)
- `infographic_dark` - Dark stat cards (planned)

---

## Four-Session Model

| Session | Symbol | Focus | When to Use |
|---------|--------|-------|-------------|
| **Dev** | D# | Feature building, coding, testing | Main development work |
| **Oracle** | O# | Docs, health, maintenance, ADRs | Cleanup, documentation sync |
| **Crank** | C# | Content production, batch output | Generating deliverables |
| **Pocket** | P# | Light full-function (MacBook Air) | Portable workstation |

### Session Isolation Principle
Each session type has its own context file and scope. Sessions should NOT cross into other session's territory:
- **Dev** builds features, **Oracle** documents them
- **Crank** generates content, **Dev** fixes bugs
- **Pocket** can do everything but prefers efficiency

### Resume Prompts
```
# Mac Mini - Development
you are dev - read DEV_CONTEXT.md

# Mac Mini - Maintenance
you are oracle - read ORACLE_CONTEXT.md

# Mac Mini - Content Generation
you are crank - read CRANK_CONTEXT.md

# MacBook Air - Portable (any task)
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
| `optimize` | Full optimization scan | When planning improvements |

### Session Automation
Claude automatically runs:
- `audit --quick` at session start
- `autosave` every ~20 exchanges or at natural breakpoints
- `autosave` before sensing compaction

### Health Monitor
Persistent dashboard (`python3 maintenance/health_monitor.py`) showing:
- Health score, autosave status, pipeline progress
- Documentation freshness, draft counts
- Code bloat metrics, optimization opportunities
- Display modes: full, compact, split, minimized

---

## Claude Desktop Integration

> **Claude Desktop syncs via iCloud** - Same project folder accessible from both machines.

### Use Claude Desktop For:
- Architecture discussions and planning
- Feature design conversations
- Research and exploration
- Optimization strategy
- Cross-session context review

### Use Claude Code For:
- Writing/editing code
- Running oracle commands
- File manipulation
- Testing pipeline
- Executing generation runs

### Recommended Attachments (Claude Desktop)
When starting a planning conversation, attach:
- `DEV_CONTEXT.md` - Current development state
- `ARCHITECTURE.md` - Technical reference
- `PHILOSOPHY.md` - Goals and principles
- This file (`PROJECT_INSTRUCTIONS.md`) - Overview

---

## Key Documents

### Context Files (Source of Truth)
| File | Purpose |
|------|---------|
| `docs/context/DEV_CONTEXT.md` | Development session state, recent changes, pending tasks |
| `docs/context/ORACLE_CONTEXT.md` | Maintenance session state, oracle-specific context |
| `docs/context/CRANK_CONTEXT.md` | Content production state, generation queue |
| `docs/context/POCKET_CONTEXT.md` | Portable session state, multi-machine workflow |

### Reference Documents
| File | Purpose |
|------|---------|
| `docs/ARCHITECTURE.md` | Technical specs, file structure, layer details |
| `docs/PHILOSOPHY.md` | Project goals, principles, vision concepts |
| `docs/WORKFLOW.md` | Operational processes, VS Code config, session management |
| `docs/CODE_HISTORY.md` | ADRs, design discussions, rejected approaches |
| `docs/CHANGELOG.md` | Raw session entries (what happened) |
| `docs/TOOLS_REFERENCE.md` | API configurations, tool documentation |
| `docs/UX_RULES.md` | Checkpoint patterns, user experience guidelines |

### Optimization Files
| File | Purpose |
|------|---------|
| `optimization/OPTIMIZATION_LOG.md` | Running log of recommendations by date/category |
| `optimization/IDEAS_BACKLOG.md` | Future planning (YES/MAYBE/NO/UNREVIEWED tiers) |

---

## Workflow Patterns

### Starting a Dev Session (Mac Mini)
1. Open VS Code workspace
2. Start health monitor: `python3 maintenance/health_monitor.py`
3. New Claude Code chat
4. First message: `you are dev - read DEV_CONTEXT.md`
5. Claude runs `audit --quick` automatically

### Starting a Pocket Session (MacBook Air)
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
| `NEEDS_DEV_FIX: [issue]` | Crank | Generation blocked by bug |
| `POCKET_COMPLETED: [task]` | Pocket | Finished task for main sessions |
| `NEEDS_MAIN_WORKSTATION: [task]` | Pocket | Too heavy for portable |

---

## Optimization System

### Hybrid 30/70 Approach
- **Oracle (30%):** Detects quantifiable patterns (code metrics, doc freshness, file changes)
- **Claude (70%):** Applies judgment, prioritizes, spots novel opportunities

### Categories
Code, Workflow, Tools/Skills, VS Code, UX, Architecture, Cost, Documentation, Subagents, Automation, MCP/API, Decision Strategy, Philosophy, Project Architecture, Future Planning, Meta

### Source Tracking
| Prefix | Source |
|--------|--------|
| `[O]` | Oracle detected |
| `[CD]` | Claude (dev session) |
| `[CO]` | Claude (oracle session) |
| `[U]` | User added manually |

---

## Reusable Templates

GitHub template repository for starting new projects with this workflow:
`https://github.com/w2csyh44qs-web/project-oracle-template` (private)

### Template Contents
- `templates/DEV_CONTEXT_TEMPLATE.md` - Generic dev session template
- `templates/ORACLE_CONTEXT_TEMPLATE.md` - Generic maintenance template
- `templates/CRANK_CONTEXT_TEMPLATE.md` - Generic production template
- `templates/POCKET_CONTEXT_TEMPLATE.md` - Portable session template
- `templates/project_oracle_template.py` - Core health/audit tool
- `templates/SETUP_GUIDE.md` - How to use for new projects

### Starting a New Project
1. Create repo from template on GitHub
2. Clone to iCloud Drive folder
3. Customize context files (replace placeholders)
4. Run `python3 maintenance/project_oracle.py config -v` to verify

---

## Current State

### What's Built
- L1-L6 pipeline functional
- Project Oracle with full command suite
- Health monitor dashboard (Phases 1-5)
- Optimization awareness system
- Four-session model (D/O/C/P)
- Multi-machine workflow (iCloud + GitHub templates)
- `carousel_illustrated` preset end-to-end
- Truth prompt wrapper for visual consistency

### In Progress / Planned
- L7 (Review) refinement
- L8 (Analytics) implementation
- `meme_mashup` preset
- `infographic_dark` preset
- Multi-sport expansion (NBA, Soccer)
- Full automation mode (master orchestrator)

---

## Quick Reference

### File Locations
```
*AutomationScript/
├── docs/
│   └── context/           # Session state files (D#, O#, C#, P#)
├── docs/                   # Reference documentation
├── optimization/           # Optimization logs and ideas
├── maintenance/            # Oracle scripts, health monitor
├── reports/                # Audit reports, snapshots
├── scripts/                # Pipeline scripts (L1-L8)
├── config/                 # Presets, templates
├── content/                # Generated content by sport/phase/week
└── templates/              # Reusable project templates
```

### Common Commands
```bash
# Health monitor
python3 maintenance/health_monitor.py

# Oracle commands
python3 maintenance/project_oracle.py audit --quick
python3 maintenance/project_oracle.py autosave
python3 maintenance/project_oracle.py status
python3 maintenance/project_oracle.py optimize

# Generation (Crank sessions)
python3 scripts/idea_creation.py regular_season week16 --matchup "TEAM @ TEAM" --content-preset carousel_illustrated_reels
python3 scripts/media_generation.py regular_season week16 --generate --no-checkpoint
python3 scripts/assembly.py regular_season week16 --no-checkpoint
python3 scripts/distribution.py regular_season week16 --carousels --no-checkpoint
```

### Session Start Messages
```
# Mac Mini sessions
you are dev - read DEV_CONTEXT.md
you are oracle - read ORACLE_CONTEXT.md
you are crank - read CRANK_CONTEXT.md

# MacBook Air sessions
you are pocket - read POCKET_CONTEXT.md
```

---

## Key Principles

### From PHILOSOPHY.md
1. **Pipeline over monolith** - Each layer independent, testable
2. **Presets over hardcoding** - Configuration-driven behavior
3. **Checkpoints over prayers** - Save state frequently
4. **Context over memory** - Files are source of truth, not chat history
5. **Judgment over automation** - 70% Claude reasoning, 30% pattern detection

### User Preferences
- Prioritizes learning, integrity, relationships
- ADHD-aware: benefits from structure, checkpoints, external tracking
- Alternating busy work weeks / weeks off schedule
- Values balance between work and personal life
- Prefers curiosity-led exploration over forced structure

---

*Last updated: December 23, 2025 (O72)*
*Template version 2.0 - Four-Session Model + Multi-Machine Workflow*
