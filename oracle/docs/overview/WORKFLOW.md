# Workflow Reference

**Last Updated:** January 8, 2026 (O101 - P25 Dynamic Context System)
**Purpose:** Operational processes, environment setup, session management, and cross-session coordination.

---

## Table of Contents

1. [V2 Oracle Daemon](#1-v2-oracle-daemon)
2. [Cross-Session Handoffs](#2-cross-session-handoffs)
3. [Environment Setup](#3-environment-setup)
4. [Session Management](#4-session-management)
5. [Build Breaks](#5-build-breaks)
6. [Context Loss Prevention](#6-context-loss-prevention)
7. [VS Code Configuration](#7-vs-code-configuration)
8. [Troubleshooting](#8-troubleshooting)
9. [Quick Reference](#9-quick-reference)

---

## 1. V2 Oracle Daemon

The V2 oracle system provides cross-session coordination via `oracle/context/daemon.py` (P23 Brain Cell Architecture).

### P25 Dynamic Context System

Context definitions, handoff rules, and ports are now configured via `oracle/context/context_registry.json` instead of hardcoded values. This makes Oracle project-agnostic - the same Oracle codebase can be used for any project by simply updating the registry.

**Registry location:** `oracle/context/context_registry.json`

**Registry loader:** `oracle/context/__init__.py` provides helper functions:
```python
from oracle.context import get_context_ids, get_context, get_handoff_rules, get_ports
```

**Session counts:** Only tracked in ORACLE_CONTEXT.md (SESSION REGISTRY table). Individual context files only track their own session number.

### Daemon Commands

```bash
# Start daemon
python oracle/context/daemon.py start
python oracle/context/daemon.py start --fallback  # Pocket mode (ports 5002/5174)

# Check status
python oracle/context/daemon.py status

# Spawn sessions
python oracle/context/daemon.py spawn dev --task "Fix L3 adapter"
python oracle/context/daemon.py spawn dash --claude

# Cross-session messaging
python oracle/context/daemon.py send dev dash "New API ready"
python oracle/context/daemon.py messages --context dev

# View handoff rules
python oracle/context/daemon.py rules

# Health audit
python oracle/context/daemon.py audit --quick
python oracle/context/daemon.py audit

# Show resume prompts
python oracle/context/daemon.py prompts

# Context activity
python oracle/context/daemon.py context
```

### Fallback Mode (Pocket)

When working on M1 Air while main Mac Studio is running:
- Main machine: Backend 5001, Frontend 5173
- M1 Air: Backend 5002, Frontend 5174

```bash
# Start servers in fallback mode
export GOATED_FALLBACK=1
python oracle/daemon.py start --fallback
FLASK_PORT=5002 python3 -m app.main
cd dashboard/frontend && VITE_PORT=5174 npm run dev
```

---

## 2. Cross-Session Handoffs

### Handoff Rules

```
Dash → Dev: custom_preset_request, api_change_request, backend_bug
Dash → Crank: content_generation_request
Crank → Dev: bug_report
Crank → Dash: content_ready
Dev → Dash: new_feature_available, preset_added, api_updated
Dev → Crank: preset_fixed, new_preset
Oracle → All: health_alert, task_assignment
Pocket → Oracle: sync_complete, fallback_active
```

### Sending Messages

```bash
# Dev notifies Dash about new feature
python oracle/daemon.py send dev dash "new_feature_available: Preset cloning API ready"

# Crank reports bug to Dev
python oracle/daemon.py send crank dev "bug_report: L5 fails on incentive preset"

# Check messages for your context
python oracle/daemon.py messages --context dev
```

### Cross-Session Flags (Legacy)

Still supported in context files for backward compatibility:

| Flag | Set By | Meaning |
|------|--------|---------|
| `NEEDS_ORACLE_PASS` | Dev | Dev compacted; oracle should do maintenance pass |
| `NEEDS_DEV_ATTENTION: [reason]` | Oracle/Crank | Issues found that need dev input |
| `NEEDS_DEV_FIX: [issue]` | Crank | Generation blocked by bug |
| `PAUSED_MID_TASK: [description]` | Any | Session paused mid-task |
| `GENERATION_IN_PROGRESS: [matchup]` | Crank | Don't compact mid-generation |

---

## 3. Environment Setup

### 1.1 Project Location

```bash
cd "/Users/Vanil/Library/Mobile Documents/com~apple~CloudDocs/*VITAL SIGNS/LIFE/INVESTMENTS/Goated Bets/Marketing/*AutomationScript"
```

### 1.2 Python Environment

**Status (Dec 2025):** venv rebuilt in O54 after being deleted in O46 due to iCloud sync conflicts.

```bash
# Navigate to project
cd "/Users/Vanil/Library/Mobile Documents/com~apple~CloudDocs/*VITAL SIGNS/LIFE/INVESTMENTS/Goated Bets/Marketing/*AutomationScript"

# Activate venv (RECOMMENDED for all script execution)
source venv/bin/activate

# Verify activation (should show (venv) prefix in terminal)
which python3  # Should show path within venv/

# Deactivate when done
deactivate
```

**If venv missing or broken:**
```bash
# Recreate venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** The oracle (`project_oracle.py`) uses only standard library modules. Pipeline scripts (L1-L8) require packages from requirements.txt.

### 1.3 Required API Keys

Create `.env` file in project root with:

```bash
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
FAL_KEY=your_key_here
PEXELS_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
```

### 1.4 MCP Servers

**Config Location:** `~/.claude.json`

| Server | Purpose | Status |
|--------|---------|--------|
| elevenlabs | Interactive TTS testing, voice exploration | ✅ Configured |
| ios-simulator | UX testing on mobile (iPhone 17 Pro, iOS 26) | ✅ Configured |

### 1.5 VS Code Extensions

**Required:**
- Claude Code by Anthropic (v2.0.58+)
- Python (Microsoft)

**Recommended:**
- Python Docstring Generator
- GitLens (if using git)

---

## 2. Session Management

### 2.1 Five-Session Model

The project uses five specialized session types, each with distinct responsibilities:

| Session | Prefix | Context File | Purpose | Scope |
|---------|--------|--------------|---------|-------|
| **Development** | D# | `docs/context/DEV_CONTEXT.md` | Build pipeline, implement features, bug fixes | `scripts/`, `config/`, `content/` |
| **Oracle** | O# | `docs/context/ORACLE_CONTEXT.md` | Health checks, documentation sync, archiving | `maintenance/`, `docs/`, `reports/` |
| **Crank** | C# | `docs/context/CRANK_CONTEXT.md` | Content production, quality review, batch runs | `content/` output only |
| **Pocket** | P# | `docs/context/POCKET_CONTEXT.md` | Portable development on MacBook Air, multi-machine workflow | Full capability, efficiency-focused |
| **Dashboard** | DB# | `docs/context/DASHBOARD_CONTEXT.md` | Web UI development, API design, frontend components | `dashboard/` folder only |

**Session Tracking (P25):**
- Master session counts tracked ONLY in ORACLE_CONTEXT.md (SESSION REGISTRY table)
- Individual context files only show their own session number (e.g., `**Session:** D104`)
- This reduces manual updates when sessions advance

**Session Isolation Principle:**
- Each session reads ONLY its own context file first
- Resume prompt format: `you are [role] - read [ROLE]_CONTEXT.md`
- Role declaration FIRST prevents confusion after compaction

### 2.2 Starting a Development Session

1. Open VS Code workspace file (`.code-workspace`)
2. Open new Claude Code chat (`Cmd+Shift+P` → "Claude Code: New Chat")
3. First message: "Read context/DEV_CONTEXT.md - resuming development"
4. Claude reads context and continues where you left off

### 2.3 Starting a Maintenance Session

1. Open VS Code (same workspace, separate Claude Code chat)
2. First message: "Read context/ORACLE_CONTEXT.md - maintenance session"
3. Or run oracle directly:
   ```bash
   python3 maintenance/project_oracle.py audit --quick  # Health + baseline
   python3 maintenance/project_oracle.py status         # One-line check
   ```

### 2.4 Pre-Compaction Checklist

Before Claude Code compacts context:

1. **Save current state (Claude does this automatically):**
   ```bash
   python3 maintenance/project_oracle.py autosave
   ```

   Output: `💾 Autosaved. [health score]. Snapshot: [filename]`

2. **Or for verbose output:**
   ```bash
   python3 maintenance/project_oracle.py snapshot --task "current task description"
   ```

3. **Good compaction points:**
   - ✅ After completing a full task (script fix, feature addition)
   - ✅ After finishing documentation updates
   - ✅ After running a successful pipeline test
   - ✅ Before starting a long operation (L4-L6 generation)
   - ✅ After resolving all pending tasks in a batch

4. **Avoid compaction during:**
   - ❌ Mid-documentation merge (partial information loss)
   - ❌ Debugging (lose error context)
   - ❌ Multi-step refactoring (lose change context)
   - ❌ When background processes are running

### 2.5 Post-Compaction Resume

After compaction or new session:

1. Claude reads the context file automatically (if instructed)
2. Or paste the resume prompt from latest snapshot
3. Claude should ask clarifying questions before making changes
4. Verify understanding before proceeding with work

### 2.6 Session End Checklist

Before ending a session:

1. Update context file's "Current State" section
2. Update "Recent Changes" with today's work
3. Update "Pending Tasks" (add new, mark completed)
4. Ask: "Should I update the detailed reference docs?"
5. If major changes: update relevant docs in `docs/`
6. Consider running: `python3 maintenance/project_oracle.py sync --apply`

---

## 3. Build Breaks

### 3.1 What is a Build Break?

A scheduled pause to review code quality, update documentation, and ensure project health. Prevents technical debt accumulation.

### 3.2 Build Break Checklist

```
□ Code efficiency review (bloat scan)
□ Remove unused imports/functions
□ Update documentation (architecture, context)
□ Review layer outputs for quality
□ Test all layers still work
□ Review pending tasks (still relevant?)
□ Save workspace state
□ Git commit (if using version control)
```

### 3.3 Build Break Schedule

| Phase | Trigger | Type |
|-------|---------|------|
| After layer completion | L4, L5, L6, L7 done | Full build break |
| Before major test | Week 14 test | Full build break |
| Before launch | Week 15 | Full build break |
| Post-launch | Monthly | Maintenance build break |
| After major refactor | As needed | Quick build break |

### 3.4 Build Break with Oracle

```bash
# Quick health check (creates baseline silently)
python3 maintenance/project_oracle.py audit --quick

# Full audit with report
python3 maintenance/project_oracle.py audit

# Quick checkpoint (sync + snapshot)
python3 maintenance/project_oracle.py autosave

# Sync all documentation
python3 maintenance/project_oracle.py sync --apply --all

# Weekly: Archive old changes
python3 maintenance/project_oracle.py autosave --archive-changes
```

### 3.5 Build Break Recommendations

At each build break, review and recommend:

**Code Optimizations:**
- Unused imports and dead code
- Functions over 100 lines (refactor candidates)
- Redundant logic
- Opportunities for consolidation

**Tool Optimizations:**
- API usage and cost analysis
- Alternative tools for expensive operations
- Caching strategies to reduce API calls
- Batch operations where applicable

**Workflow Optimizations:**
- Script consolidation opportunities
- Automation of repetitive tasks
- Checkpoint flow improvements
- Error handling enhancements

**Documentation Optimizations:**
- Stale references
- Missing information
- Cross-reference validity
- Clarity improvements

---

## 4. Context Loss Prevention

### 4.1 Why Documentation Matters

- Complex project with many moving parts
- Session constraints and compaction can lose context
- Switching environments (VS Code instances) loses state
- Documentation prevents having to repeat conversations

### 4.2 Documentation Hierarchy

| Document | Captures | When to Read |
|----------|----------|--------------|
| DEV_CONTEXT.md | NOW - current state, tasks, rules | First, every dev session |
| ORACLE_CONTEXT.md | NOW - oracle state, features | First, every maintenance session |
| ARCHITECTURE.md | HOW - technical implementation | When implementing layers |
| PHILOSOPHY.md | WHY - goals, principles | When making design decisions |
| WORKFLOW.md | HOW WE WORK - processes | When process questions arise |
| TOOLS_REFERENCE.md | WHAT WITH - API costs | When evaluating tools |
| UX_RULES.md | HOW IT FEELS - UI patterns | When building checkpoints |

### 4.3 What Each Document Type Captures

**Context Documents (NOW):**
- Current project state
- What's done, what's in progress
- Session-specific rules
- Pending tasks
- Recent changes

**Reference Documents (WHY/HOW):**
- Stable information that rarely changes
- Technical specifications
- Design principles
- Tool comparisons
- UI patterns

### 4.4 Snapshot Strategy

**When to autosave (Claude handles automatically):**
- Every ~20 exchanges
- Before expected compaction
- Before long operations (L4-L6)
- After completing features

**Quick checkpoint (minimal output):**
```bash
python3 maintenance/project_oracle.py autosave
```
Output: `💾 Autosaved. [health score]. Snapshot: [filename]`

**Detailed snapshot (with resume prompt):**
```bash
python3 maintenance/project_oracle.py snapshot \
  --task "what you're working on" \
  --file "last file edited" \
  --decisions "pending decisions" \
  --blockers "current blockers"
```

**Snapshot outputs to:** `reports/snapshots/SNAPSHOT_[timestamp].md`

### 4.5 Recovery from Context Loss

If context is lost mid-session:

1. Check latest snapshot: `ls -la reports/snapshots/`
2. Read the snapshot file for resume context
3. Or read the full context document
4. Ask Claude to summarize current state before continuing

### 4.6 How Oracle Automation Works

**Oracle is a tool, not a background process. Claude is the orchestrator.**

Each command is a separate execution - runs, does its job, exits:

```bash
python3 maintenance/project_oracle.py status        # runs ~0.5s, exits
python3 maintenance/project_oracle.py audit --quick # runs ~3s, exits
python3 maintenance/project_oracle.py autosave      # runs ~2s, exits
```

There is no persistent background process. Claude calls the script at intervals defined in session rules (Rule 6 in DEV_CONTEXT.md).

**Automation Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE SESSION                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Session Start                                               │
│       │                                                      │
│       ▼                                                      │
│  Claude reads DEV_CONTEXT.md                                 │
│       │                                                      │
│       ▼                                                      │
│  Claude sees Session Rule 6 → runs `audit --quick`           │
│       │                                                      │
│       ▼                                                      │
│  [oracle runs, exits]                                        │
│       │                                                      │
│       ▼                                                      │
│  Normal work... (exchanges 1-10)                             │
│       │                                                      │
│       ▼                                                      │
│  ~10 exchanges → Claude runs `status` [runs, exits]          │
│       │                                                      │
│       ▼                                                      │
│  Normal work... (exchanges 11-25)                            │
│       │                                                      │
│       ▼                                                      │
│  ~20 exchanges → Claude runs `autosave` [runs, exits]        │
│       │                                                      │
│       ▼                                                      │
│  ... continues ...                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key point:** Claude is the orchestrator. Oracle is just a tool Claude calls. Session rules define when Claude should call each command.

### 4.7 Oracle sEEG Monitor (P24)

A persistent dashboard (stereoEEG metaphor) that runs in a dedicated VS Code terminal, providing real-time visibility into project health.

**Renamed:** `health_monitor.py` → `seeg.py` (P23/P24)

```
┌──────────────────┐     ┌──────────────────┐
│  Claude Code     │     │  oracle/seeg.py   │
│  Session         │     │ (always running)  │
│                  │     │                   │
│  Calls oracle ───┼────▶│ Reads .health_    │
│  on triggers     │     │ status.json       │
│                  │◀────┼─ Watches files    │
│                  │     │ Escalating alerts │
└──────────────────┘     └──────────────────┘
```

**Status:** ✅ P24 COMPLETE (January 2026) - Brain Cells + API Connections display

**Start the monitor:**
```bash
python3 oracle/seeg.py
```

**Display Modes:**

| Mode | Flag | Hotkey | Use Case |
|------|------|--------|----------|
| Full | `--mode full` | `f` | All panels, maximum info (default) |
| Compact | `--mode compact` | `c` | Smaller terminals |
| Split | `--mode split` | `s` | Side-by-side health + log |
| Minimized | `--mode min` | `m` | Status line only |

**Hotkeys (P24):**

| Key | Action |
|-----|--------|
| `a` | Run autosave now |
| `h` | Full health check |
| `o` | Run optimize |
| `b` | Run brain cell diagnostics |
| `g` | Toggle debug panel (shows internal state) |
| `d` | Set session type to Development |
| `t` | Set session type to Maintenance |
| `0` | Auto-detect session type |
| `f/c/s/m` | Switch display mode (persisted!) |
| `r` | Force refresh |
| `?` | Help |
| `q` | Quit (runs final autosave) |

**Mode Persistence:** When you switch modes with hotkeys, the preference is saved to `oracle/maintenance/config.json`. Next time you start the monitor, it uses your preferred mode.

**Session Compatibility:** Works for both dev AND maintenance sessions. The monitor is session-agnostic.

**P24 Display Categories:**
- HEALTH: Score 0-10, visual bar
- SESSION: Dev/Maintenance, activity %
- BRAIN CELLS: Status of all brain cell modules (Microglia, Astrocytes, etc.)
- API CONNECTIONS: External API health + usage tracking
- CODE HEALTH: Critical issues, warnings
- AUTOSAVE: Last, reminder timing
- PIPELINE: L1-L8 layer status
- SESSION TASKS: From context files

**Configuration:**
```bash
# Different modes
python3 oracle/seeg.py --mode compact
python3 oracle/seeg.py --mode split
python3 oracle/seeg.py --mode min
```

**Dependencies:**
```bash
pip install rich watchdog
```

See `oracle/ORACLE_README.md` for full documentation.

### 4.8 Tools Update Protocol

When new tools become available or tool research is updated, follow this protocol to keep the system current.

**Files Involved:**
- `docs/TOOLS_REFERENCE.md` - Tool research, pricing, capabilities (updated by Claude Desktop)
- `config/tool_config.json` - User defaults, options arrays, source_configs
- `config/script_presets.json` - Preset tool selections

**Update Flow:**

```
┌────────────────────────────────────────────────────────────────┐
│  1. Claude Desktop updates TOOLS_REFERENCE.md                   │
│     - New tools, pricing changes, capability updates            │
│     - Research findings, recommendations                        │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  2. Oracle session reviews changes                              │
│     - Compare TOOLS_REFERENCE.md updates to tool_config.json   │
│     - Update options arrays if new tools added                  │
│     - Update defaults if better options available               │
│     - Update source_configs for new data sources                │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  3. Dev session updates presets if needed                       │
│     - Update preset tool selections if defaults changed         │
│     - Add new presets for new tool combinations                 │
│     - Test new tools in pipeline                                │
└────────────────────────────────────────────────────────────────┘
```

**When to Update tool_config.json:**
- New tool added to ecosystem → add to `options` array
- Tool deprecated or removed → remove from options (but check presets first)
- Better default identified → update `selected` value
- New data source → add to `data_sources.options` and `source_configs`

**Example: Adding a New TTS Tool**
```json
// Before
"tts": {
  "selected": "elevenlabs",
  "options": ["elevenlabs", "openai", "coqui"]
}

// After adding Cartesia
"tts": {
  "selected": "elevenlabs",
  "options": ["elevenlabs", "openai", "coqui", "cartesia"]
}
```

**Principles:**
- **TOOLS_REFERENCE.md is research** - Claude Desktop keeps it current
- **tool_config.json is operational** - Oracle/dev updates based on research
- **Presets inherit from tool_config.json** - null values use defaults
- **CLI overrides everything** - Users can always override via `--tts-tool`, `--model`, etc.

See **ADR-016** in CODE_HISTORY.md for the tool configuration system design.

---

## 5. Cross-Session Protocol

### 5.1 Five-Session Roles & Scope

| Session | Prefix | Primary Scope | Can Also Touch | Avoid |
|---------|--------|--------------|----------------|-------|
| **Dev** | D# | `scripts/`, `config/`, feature work | Quick doc fixes if urgent | Batch generation, comprehensive docs |
| **Oracle** | O# | `docs/`, `maintenance/`, health fixes | Code fixes from health scans | New features, generation |
| **Crank** | C# | Content production, quality review | Update generation queue | Code changes, doc maintenance |
| **Pocket** | P# | Portable development, multi-machine sync | Full capability | Heavy compute tasks |
| **Dashboard** | DB# | `dashboard/` web UI & API development | Read `config/`, `scripts/` interfaces | Pipeline scripts, config modifications |

**Key principles:**
- **Dev sessions**: Build → Test → Iterate → Note changes briefly
- **Oracle sessions**: Sync docs → Write ADRs → Archive → Fix health issues → **Capture principles from user feedback**
- **Crank sessions**: Generate → Review quality → Track outputs → Report issues to Dev
- **Pocket sessions**: Full dev capability on MacBook Air, iCloud sync for portability
- **Dashboard sessions**: UI/UX → API endpoints → Test locally → Document

**Oracle's critical responsibility:** User comments to Dev often contain meta-principles about reasoning style, architecture decisions, and project philosophy. Oracle must capture these in reference docs (PHILOSOPHY.md, ARCHITECTURE.md) so they persist across sessions.

### 5.2 Dev ↔ Oracle Rotation Workflow

The recommended workflow for keeping docs and code health in sync:

```
DEV SESSION                          ORACLE SESSION
    │                                      │
    ▼                                      │
[Dev work - features, scripts]             │
    │                                      │
    ▼                                      │
[Natural breakpoint reached]               │
    │                                      │
    ▼                                      │
[Update DEV_CONTEXT Recent Changes]        │
[Set 🚩 NEEDS_ORACLE_PASS flag]            │
[Compact]                                  │
    │                                      │
    └─────────────────────────────────────►│
                                           ▼
                                    [Read DEV_CONTEXT]
                                    [See NEEDS_ORACLE_PASS flag]
                                           │
                                           ▼
                                    [Update all affected docs]
                                    [Run health scan + fix issues]
                                    [Clear flag]
                                           │
                                           ▼
                                    [Update ORACLE_CONTEXT]
                                    [Compact]
    ◄──────────────────────────────────────┘
    │
    ▼
[Resume dev with fresh context]
```

### 5.3 Cross-Session Flags

Located in the `🚩 Cross-Session Flags` section of each context doc:

| Flag | Set By | Meaning |
|------|--------|---------|
| `🚩 NEEDS_ORACLE_PASS` | Dev | Dev compacted; oracle should do maintenance pass |
| `🚩 NEEDS_DEV_ATTENTION: [reason]` | Oracle/Crank | Issues found that need dev input |
| `🚩 NEEDS_DEV_FIX: [issue]` | Crank | Generation blocked by bug, needs dev fix |
| `🚩 PAUSED_MID_TASK: [description]` | Any | Session paused mid-task |
| `🚩 GENERATION_IN_PROGRESS: [matchup]` | Crank | Don't compact mid-generation |

**Oracle pass checklist (when NEEDS_ORACLE_PASS seen):**
1. Read DEV_CONTEXT Recent Changes
2. **Check for meta-principles in user feedback** - Document in PHILOSOPHY.md
3. Update affected docs based on dev changes
4. Run `audit --quick`, fix code issues
5. Clear the `NEEDS_ORACLE_PASS` flag
6. Update ORACLE_CONTEXT, compact

### 5.4 Crank ↔ Dev Communication

**Crank reports issues to Dev:**
- Bugs blocking generation → Set `🚩 NEEDS_DEV_FIX: [issue]`
- Quality issues with output → Document in CRANK_CONTEXT "Issues for Dev" section
- API data quality issues → Note for GoatedBets team feedback

**Dev reports fixes to Crank:**
- Update CRANK_CONTEXT "Immediate Next Task" section with verification steps
- Note which issues are resolved in the flag status

### 5.5 Development → Maintenance Communication

**Oracle reads DEV_CONTEXT.md to:**
- Auto-configure layers, APIs, docs
- Generate health reports
- Track documentation drift
- Validate layer health
- Check cross-session flags

**After dev session, maintenance can:**
- Run audits to find issues
- Fix code health issues (unused imports, long functions)
- Generate snapshots for continuity
- Sync documentation
- Archive old changes

### 5.6 Maintenance → Development Communication

**Oracle outputs for dev session:**
- `reports/ORACLE_REPORT_*.md` - Health findings
- `reports/snapshots/SNAPSHOT_*.md` - Context snapshots
- `docs/CHANGELOG.md` - Archived changes

**Dev session reads these by:**
- "Fix critical issues in latest oracle report"
- "Review the oracle report and prioritize fixes"
- Checking CHANGELOG for historical context

### 5.7 Shared Resources

| Resource | Created By | Used By |
|----------|------------|---------|
| `reports/snapshots/` | Both sessions | Both sessions |
| `docs/CHANGELOG.md` | Oracle | Both sessions |
| `docs/*.md` | Either (with care) | Both sessions |

### 5.8 Handoff Protocol

**Dev → Maintenance handoff:**
1. Dev session ends or pauses
2. Run: `python3 maintenance/project_oracle.py audit --quick`
3. Review report for issues
4. Fix critical issues or note for next dev session

**Maintenance → Dev handoff:**
1. Maintenance creates report/snapshot
2. Dev session starts
3. Dev reads: "Check latest oracle report for issues to address"
4. Prioritize fixes based on severity

---

## 6. VS Code Configuration

### 6.1 Workspace Settings

Save in your `.code-workspace` file or via `Cmd+Shift+P` → "Preferences: Open Workspace Settings (JSON)":

```json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "workbench.editor.openSideBySideDirection": "right",
    "workbench.editor.focusRecentEditorAfterClose": false,
    "workbench.editor.enablePreviewFromQuickOpen": false,
    "workbench.editor.enablePreview": false,
    "workbench.editor.revealIfOpen": false,
    "files.autoReveal": false,
    "terminal.integrated.scrollback": 10000,
    "python.analysis.autoImportCompletions": true,
    "files.exclude": {
      "**/__pycache__": true,
      "**/.DS_Store": true,
      "*.pyc": true
    }
  }
}
```

### 6.2 Settings Explanation

| Setting | Purpose |
|---------|---------|
| `openSideBySideDirection` | New files open to the right |
| `focusRecentEditorAfterClose` | Don't auto-focus after closing tabs |
| `enablePreview` | Disable preview tabs (files stay open) |
| `revealIfOpen` | Don't auto-switch to already-open files |
| `files.autoReveal` | Don't auto-reveal files in explorer |
| `scrollback` | More terminal history (10K lines) |
| `autoImportCompletions` | Python auto-import suggestions |
| `files.exclude` | Hide clutter files from explorer |

### 6.3 Recommended Layout

```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│  Claude Code Chat   │   Code Editor       │
│                     │   (Python file)     │
│                     │                     │
├───────────────┬─────┴─────────────────────┤
│ Health Monitor│     Command Terminal      │
│ (dedicated)   │     (run scripts here)    │
└───────────────┴───────────────────────────┘
```

**Setup:**
1. Open Claude Code chat (`Cmd+Shift+P` → "Claude Code: New Chat")
2. Drag chat tab to left side
3. Open terminal (`` Ctrl+` ``)
4. Split terminal (`Cmd+\`)
5. Left terminal: `python3 oracle/seeg.py`
6. Right terminal: run pipeline commands
7. Rename terminal tabs (right-click): "Health" and "Commands"

**Alternative (without Health Monitor):**
```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│  Claude Code Chat   │   Code Editor       │
│                     │   (Python file)     │
│                     │                     │
├─────────────────────┴─────────────────────┤
│              Terminal (venv)              │
└───────────────────────────────────────────┘
```

### 6.4 Useful Keybindings

| Keybinding | Action |
|------------|--------|
| `Cmd+Shift+P` | Command palette |
| `Cmd+,` | Settings |
| `Cmd+Shift+E` | File explorer |
| `` Ctrl+` `` | Toggle terminal |
| `Ctrl+-` | Go back (after focus jump) |
| `Cmd+\` | Split editor |
| `Cmd+1/2/3` | Focus editor group 1/2/3 |
| `Cmd+Option+Left/Right` | Switch between editor groups |

### 6.5 Claude Code Extension Notes

- **Version:** 2.0.58+ (by Anthropic)
- **Chat history:** Persists per workspace, survives VS Code restart
- **Multiple chats:** Use `Cmd+Shift+P` → "Claude Code: New Chat" for separate contexts
- **Focus stealing:** Extension auto-focuses files it edits (no setting to disable)
  - Workaround: Use split view or separate windows
  - Quick return: `Ctrl+-` to go back to chat

---

## 7. Troubleshooting

### 7.1 Common Issues

#### "No trends found"
- Run `web_search_trend_detector.py` first
- Check `output/all_trends.json` exists

#### "OPENAI_API_KEY not found"
- Create `.env` file in project root
- Add your API keys

#### Audio generation fails
- Check ELEVENLABS_API_KEY in `.env`
- Verify account has credits

#### Import errors
- Activate venv: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

#### Claude Code chat closes immediately
- Check authentication: Click Claude icon, look for sign-in
- Reinstall extension if needed
- Check extension logs: `Cmd+Shift+P` → "Developer: Show Logs"

#### "claude" command not found in terminal
- You may be in a venv that doesn't have Claude CLI
- Run `deactivate` first, or use full path
- Note: Claude Code extension doesn't require CLI

#### VS Code settings not persisting
- Ensure settings are in **Workspace** tab, not User
- Or edit `.code-workspace` file directly
- Reload window after changes: `Cmd+Shift+P` → "Developer: Reload Window"

#### Focus keeps jumping to code files
- This is Claude Code extension behavior (not configurable)
- Use split view to see both chat and code
- Or use `Ctrl+-` to jump back to chat

### 7.2 Oracle-Specific Issues

#### "Could not parse layers"
- Check Pipeline Status section format in DEV_CONTEXT.md
- Run `python3 maintenance/project_oracle.py config -v` to see what was parsed

#### Missing scripts in report
- Verify scripts are in `scripts/` folder
- Check script names match context file references

#### Wrong project root
- Oracle assumes it's in `maintenance/`
- Check `PROJECT_ROOT` calculation in script

---

## 8. Project Timeline

### 8.1 Phase Overview

| Phase | Days | Focus | Status |
|-------|------|-------|--------|
| 0 | 1 | Migration to iCloud | ✅ Complete |
| 1 | 2-3 | Vision Registry + Layer 2 | ✅ Complete |
| 2 | 4-5 | Layer 4 - Audio Sync | ✅ Complete |
| 3 | 6-7 | Layer 5 - Media Generation | ✅ Complete |
| 4 | 8-9 | Layer 6 - Assembly | ✅ Complete |
| 5 | 10 | Layer 7 - Distribution | ✅ Complete |
| 6 | 11-12 | Week 14 Test | ✅ Complete |
| 7 | 13-14 | Expansion & Polish | 🔄 In Progress |
| Launch | - | Week 15 Full Launch | 📅 Scheduled |

### 8.2 Key Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Week 14 Test (1 video) | Dec 14-15, 2025 | ✅ Complete |
| Week 15 Launch | Dec 18, 2025 | 📅 Upcoming |
| Multi-segment production | Dec 18+, 2025 | 📅 Planned |
| Analytics integration | Post-launch | 📅 Planned |
| Multi-sport expansion | TBD | 📅 Future |

### 8.3 Build Break Timeline

| Phase | Deliverable | Build Break |
|-------|-------------|-------------|
| 0 | Migration | - |
| 1 | Vision + L2 | ✅ BR1 |
| 2 | Layer 4 | ✅ BR2 |
| 3 | Layer 5 | ✅ BR3 |
| 4 | Layer 6 | ✅ BR4 |
| 5 | Layer 7 | ✅ BR5 |
| 6 | Week 14 | ✅ BR6 |
| 7 | Expansion | 🔄 BR7 |
| Launch | Week 15 | 📅 BR8 |

---

## 9. Future Planning

See `optimization/IDEAS_BACKLOG.md` for consolidated future planning.

**Relevant sections:**
- YES > Architecture - Approved improvements (L8 feedback loops, multi-sport)
- YES > Automation - Approved automation features
- MAYBE > Oracle Features - Considering (context digest, automated triggers)
- MAYBE > Workflow - Considering (scheduled generation, CI/CD)
- Reference > Multi-Agent Architecture - Future agent context files
- Reference > Automation Evolution - Phased automation approach

---

## Quick Reference

### Daily Workflow
```bash
# Start dev session
1. Open workspace
2. "Read context/DEV_CONTEXT.md"
3. Claude runs: audit --quick (health + baseline)
4. Work on tasks
5. Claude runs: autosave every ~20 exchanges
6. Before compaction: Claude runs autosave
7. End: update context file

# Start maintenance session
1. Open workspace (new chat)
2. "Read context/ORACLE_CONTEXT.md"
3. Claude runs: audit --quick (health + baseline)
4. Address issues or report to dev session
```

### Key Commands
```bash
# Pipeline (V2 - scripts in app/core/pipeline/layers/)
python3 app/core/pipeline/layers/_L3/L3_ideas.py playoffs wild_card --matchup "LAC @ HOU"
python3 app/core/pipeline/layers/_L5/L5_media.py playoffs wild_card --ids idea_001

# Oracle (P23 Brain Cell Architecture)
python3 oracle/project_oracle.py audit --quick  # Session start
python3 oracle/project_oracle.py status         # Quick check
python3 oracle/project_oracle.py presets        # Show presets table
python3 oracle/project_oracle.py api-log        # API call tracking

# sEEG Monitor (run in dedicated terminal)
python3 oracle/seeg.py                          # Full dashboard (default)
python3 oracle/seeg.py --mode compact           # Compact mode
python3 oracle/seeg.py --mode min               # Minimized

# Daemon (P23 - moved to context/)
python3 oracle/context/daemon.py start          # Start daemon
python3 oracle/context/daemon.py status         # Check status
python3 oracle/context/daemon.py prompts        # Show resume prompts
```

### Key Files
```
oracle/docs/context/DEV_CONTEXT.md       # Dev session state
oracle/docs/context/ORACLE_CONTEXT.md    # Maintenance session state
oracle/docs/overview/ARCHITECTURE.md     # Technical reference
oracle/docs/overview/PHILOSOPHY.md       # Goals & principles
oracle/reports/audits/                   # Health reports
oracle/reports/snapshots/                # Context snapshots
oracle/reports/.health_status.json       # Shared health state for sEEG
```

---

*This document captures operational knowledge for the GOATED automation project. Update when processes change.*
