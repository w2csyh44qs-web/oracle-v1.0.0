# Project Oracle

**Automated Project Health and Optimization Agent**

Project Oracle maintains project health across Claude Code context compactions by auditing code, documentation, and workflow - all auto-configured from your DEV_CONTEXT.md.

---

## Quick Start

```bash
# Quick health check (also creates baseline silently)
python3 maintenance/project_oracle.py audit --quick

# One-line status
python3 maintenance/project_oracle.py status

# Autosave (sync + snapshot, minimal output) - like a video game checkpoint
python3 maintenance/project_oracle.py autosave

# Health Monitor (persistent dashboard - runs in separate terminal)
python3 maintenance/health_monitor.py
```

---

## Health Monitor

A persistent dashboard that runs in VS Code terminal, providing real-time visibility into project health.

### Features

- Real-time health score display (reads from `.health_status.json`)
- Autosave tracking with escalating reminders
- Session Activity indicator (proxy for context usage) with calibration
- Code bloat tracking with ok/new format (e.g., "Long functions: 10 ok, 0 new")
- Pipeline progress visualization
- File change monitoring (watchdog)
- Multiple display modes (full, compact, split, minimized)
- Hotkey controls for quick actions
- macOS notifications for critical alerts

### Dashboard Panels

| Panel | Information |
|-------|-------------|
| **HEALTH** | Score (0-10), visual bar |
| **SESSION** | Type (Dev/Maintenance), Activity level + % (proxy for context usage) |
| **CODE BLOAT** | Critical, Warnings, Long functions (ok/new), Unused imports (ok/new), Stale refs |
| **DOCUMENTATION** | Staleness of key docs |
| **AUTOSAVE** | Last autosave, reminder timing, safety trigger |
| **PIPELINE** | L1-L8 status, current layer, cost |
| **OPTIMIZATIONS** | Pending count, backlog ideas |
| **FILES WATCHED** | Monitored folders, change count |

### Acceptance Lists

The dashboard tracks "accepted" vs "new" for certain warning types:

- **Long functions**: Functions >100 lines that are intentionally long (checkpoint UIs, core processing)
- **Unused imports**: Imports that appear unused but are needed (type hints, re-exports)

Accepted items don't lower the health score but remain visible for awareness. See `ACCEPTED_LONG_FUNCTIONS` and `ACCEPTED_UNUSED_IMPORTS` in `project_oracle.py`.

### Usage

```bash
# Start in full mode (default)
python3 maintenance/health_monitor.py

# Start in compact mode
python3 maintenance/health_monitor.py --mode compact

# Start in split mode (health left, log right)
python3 maintenance/health_monitor.py --mode split

# Start in minimized mode (single status line)
python3 maintenance/health_monitor.py --mode min

# Single check (no monitoring)
python3 maintenance/health_monitor.py --once
```

### Hotkeys

| Key | Action |
|-----|--------|
| `a` | Run autosave |
| `h` | Run health check |
| `o` | Run optimize |
| `y` | Run suggest-code-history (find ADR candidates) |
| `g` | Toggle debug panel (shows internal state) |
| `x` | Start calibration (prompts for exact context %) |
| `d` | Set session type to Development |
| `t` | Set session type to Maintenance |
| `0` | Auto-detect session type |
| `f` | Full mode (saved) |
| `c` | Compact mode (saved) |
| `s` | Split mode (saved) |
| `m` | Minimized mode (saved) |
| `r` | Refresh |
| `?` | Help |
| `q` | Quit (runs autosave first) |

**Mode Persistence:** When you switch modes with hotkeys (f/c/s/m), the preference is saved to `health_monitor_config.json`. Next time you start the monitor, it uses your preferred mode.

**Session Compatibility:** Works for both dev AND maintenance sessions. The monitor is session-agnostic - just run it in a dedicated terminal and forget about it.

### Session Activity (Context Usage Proxy)

Since we can't directly measure Claude's context window usage externally, the monitor tracks a **Session Activity** composite score as a proxy:

| Component | Weight | What It Tracks |
|-----------|--------|----------------|
| File changes | 50% | Number of file modifications (more edits = more tool calls) |
| Health updates | 30% | Oracle command runs / exchanges |
| Context growth | 20% | Growth of context files since last autosave |

**Calibration:** The thresholds can be tuned based on actual Claude context % feedback:
1. Press `[x]` to start calibration - shows current activity breakdown in LOG
2. Check Claude's reported context % (visible in Claude Code UI)
3. Enter the exact percentage (e.g., `73`) when prompted
4. Thresholds auto-adjust so activity % better matches context %

Calibration persists in `health_monitor_config.json`. After each autosave, activity counters reset and you'll see "💡 Good time to compact if context is high".

**New Session Detection:** When you compact and start a new session, the monitor automatically detects `SESSION_SNAPSHOT_latest.json` updates (created by `audit --quick`) and resets activity counters. No manual intervention needed.

### Configuration

```bash
# Custom timing
python3 maintenance/health_monitor.py --safety-autosave 25 --reminder-interval 15

# Disable notifications
python3 maintenance/health_monitor.py --no-notifications
```

### Dependencies

```bash
pip install rich watchdog
```

---

## Commands

### Primary Commands (Use These)

| Command | Description | When |
|---------|-------------|------|
| **`autosave`** | 💾 Sync + snapshot + auto doc suggestions | Every ~20 exchanges / breakpoints |
| `autosave -q` | Autosave without doc suggestions | When you want minimal output |
| `autosave --archive-changes` | Autosave + archive old changes | Weekly |
| `audit --quick` | Fast health check (+ silent baseline) | Session start |
| `status` | ⚡ One-line health summary | Quick check anytime |

### Additional Commands

| Command | Description |
|---------|-------------|
| `audit` | Full health audit with report |
| `snapshot` | Full context snapshot with resume prompt |
| `snapshot -t "task"` | Snapshot with explicit task description |
| `report` | Generate detailed report |
| `optimize` | 🔍 Get optimization suggestions (30% automated detection) |
| `optimize --report` | Save optimization report to `optimization/reports/` |
| `optimize --log` | Append findings to `optimization/OPTIMIZATION_LOG.md` |
| `config -v` | Show parsed configuration |
| `suggest-docs` | 📝 Suggest which docs need updating |
| `suggest-docs --staleness` | Show doc staleness (last modified times) |
| `briefing` | 📋 Show cross-session briefing |
| `briefing --session dev` | Force dev session perspective |
| `suggest-code-history` | 📜 Find decision candidates for CODE_HISTORY.md |
| `diff --baseline` | Create baseline only (legacy, rarely needed) |

### Debugging & API Tracking

| Command | Description |
|---------|-------------|
| `debug-script SCRIPT [ARGS]` | 🔍 Run script with execution tracing |
| `debug-script SCRIPT --trace-calls` | Trace function entry/exit with args |
| `debug-script SCRIPT --trace-lines` | Trace every line (verbose) |
| `debug-script SCRIPT --watch-vars "x,self.y"` | Watch variable changes |
| `debug-script SCRIPT -o trace.log` | Save trace to file |
| `api-log` | 📡 View logged API calls |
| `api-log --summary` | Show cost/call summary only |
| `api-log --last 50` | Show last 50 calls |
| `api-log --provider openai` | Filter by provider |
| `api-log --clear` | Clear the log file |

### Documentation Sync

| Command | Description |
|---------|-------------|
| `sync` | Preview changes (dry-run) |
| `sync --apply` | Apply changes to context file |
| `sync --apply --all` | Check all reference docs |
| `sync --apply --fix` | Fix stale dates in docs |
| `sync --apply --prune-tasks` | Remove completed tasks |
| `sync --apply --archive-changes` | Move old changes to CHANGELOG |

---

## Recommended Workflow

### Automated (Claude handles this)

| Trigger | Command | Claude Says |
|---------|---------|-------------|
| Session start | `audit --quick` | "Checking project health..." |
| Every ~10 exchanges | `status` | (silent unless issues) |
| Every ~20 exchanges | `autosave` | "Autosaving... Done." |
| Before compaction | `autosave` | "Autosaved. Ready to compact." |
| Weekly | `autosave --archive-changes` | "Autosaving with archive..." |

### Manual (if needed)

```bash
# Session Start - health check with baseline
python3 maintenance/project_oracle.py audit --quick

# Quick checkpoint
python3 maintenance/project_oracle.py autosave

# Full snapshot with resume prompt
python3 maintenance/project_oracle.py snapshot
```

---

## What Gets Checked

### Code Health
- Unused imports
- Functions over 100 lines
- TODO/FIXME comments
- Hardcoded credentials
- Syntax errors

### Documentation Drift
- Scripts mentioned in docs that do not exist
- Broken cross-references between docs
- Stale timestamps
- Missing required sections

### Layer Health
- Missing layer scripts
- Import/syntax errors
- Output directories exist

### API Usage
- Missing API keys in .env
- API calls in code vs configured keys
- Cost tracking presence

---

## Auto-Configuration

Oracle reads DEV_CONTEXT.md to automatically detect:

- **Layers** - From Pipeline Status section
- **API Services** - From API KEYS and MCPs table
- **Scripts** - From Current Workflow section
- **Doc Files** - From Document Purposes table
- **Pending Tasks** - From PENDING TASKS section

No manual config needed - keep DEV_CONTEXT.md updated and Oracle stays in sync.

---

## Multi-Agent Support

Oracle supports multiple agent context files. To add a new agent:

1. Create `context/[AGENT]_CONTEXT.md`
2. Add path to `CONTEXT_FILES` list in `project_oracle.py`:
   ```python
   CONTEXT_FILES = [
       CONTEXT_DIR / "DEV_CONTEXT.md",
       CONTEXT_DIR / "ORACLE_CONTEXT.md",
       CONTEXT_DIR / "YOUR_AGENT_CONTEXT.md",  # Add here
   ]
   ```
3. Autosave will automatically manage all context files (auto-archive, etc.)

See `context/ORACLE_CONTEXT.md` Future Planning section for more details.

---

## Cross-Session Briefing

Oracle automatically surfaces relevant information from the other session type when you start a session.

### How It Works

At session start (during `audit --quick`), Oracle:
1. Auto-detects which session type you're in (dev or maintenance)
2. Reads the other session's context file and reports
3. Surfaces relevant findings

### What Each Session Sees

**Dev Session** sees from maintenance:
- Health score if below 7.0 (warning) or 5.0 (critical)
- Critical issues found in last audit
- Recent maintenance session changes

**Maintenance Session** sees from dev:
- Layer modifications mentioned in Recent Changes
- Script file changes
- Task backlog warnings (if >10 pending tasks)
- Recent snapshots available

### Manual Briefing

```bash
# Auto-detect session and show briefing
python3 maintenance/project_oracle.py briefing

# Force specific session perspective
python3 maintenance/project_oracle.py briefing --session dev
python3 maintenance/project_oracle.py briefing --session maintenance
```

---

## Optimization System

Oracle includes a hybrid 30/70 optimization system:
- **30% Automated**: Oracle detects quantifiable patterns (long functions, stale docs, placeholders)
- **70% Judgment**: Claude adds context and prioritization

### Files

| File | Purpose |
|------|---------|
| `optimization/OPTIMIZATION_LOG.md` | Running log of recommendations by date/category |
| `optimization/IDEAS_BACKLOG.md` | Consolidated future planning (YES/MAYBE/NO/UNREVIEWED) |
| `optimization/reports/OPT_REPORT_*.md` | Detailed optimization reports |

### Commands

```bash
# Full scan with console output
python3 maintenance/project_oracle.py optimize

# Save detailed report
python3 maintenance/project_oracle.py optimize --report

# Append findings to log
python3 maintenance/project_oracle.py optimize --log
```

### What Gets Detected

- **Code**: Functions >100 lines, potential duplication
- **Documentation**: Files not updated recently
- **Architecture**: Placeholder markers, future markers
- **Cost**: Missing cost tracking

### Integration with Other Commands

- `audit --quick` shows optimization summary
- `autosave` shows optimization count in output
- Both point to `optimize` for full details

---

## Output

### Reports
- Location: `reports/audits/ORACLE_REPORT_[timestamp].md`
- Contains: Health score, issues, suggestions, layer status

### Session Diffs
- Location: `reports/diffs/SESSION_DIFF_[timestamp].md`
- Contains: Changes since session start, files modified

### Snapshots
- Location: `reports/snapshots/SNAPSHOT_[timestamp].md`
- Contains: Current state, changes since baseline, resume prompt

---

## Command Options

### Snapshot Options
- `--task, -t` - What you are currently working on
- `--file, -f` - Last file being edited
- `--decisions, -d` - Pending decisions
- `--blockers, -b` - Current blockers

### Sync Options
- `--apply` - Actually write changes (default is dry-run)
- `--all` - Also check reference docs
- `--fix` - Make safe targeted fixes
- `--add-tasks` - Add audit issues to Pending Tasks
- `--prune-tasks` - Remove completed tasks
- `--archive-changes` - Move old changes to CHANGELOG
- `--context-only` - Only sync DEV_CONTEXT.md

### What --fix Mode Does

| Doc | Fix Action |
|-----|------------|
| PHILOSOPHY.md | Updates stale date |
| TOOLS_REFERENCE.md | Updates stale date |
| ARCHITECTURE.md | Adds warning comment |
| ORACLE_README.md | Updates timestamp |

---

## Customization

### Add New Layer

Just update DEV_CONTEXT.md:
```markdown
## Pipeline Status
...
Layer 9: New Layer -> output/new_output/
```

Oracle will detect it on next run.

### Add New API

Add to the API table in DEV_CONTEXT.md:
```markdown
| NEW_API_KEY | New Service | L9 | Active |
```

### Change Thresholds

Edit project_oracle.py:
```python
# Function length threshold
max_lines: int = 100

# Health score weights
score -= critical_count * 1.5
```

---

## Troubleshooting

### Could not parse layers
- Check Pipeline Status section format in DEV_CONTEXT.md
- Run `python3 maintenance/project_oracle.py config -v` to see what was parsed

### Missing scripts in report
- Verify scripts are in scripts folder
- Check script names match context file references

### Wrong project root
- Oracle assumes it is in maintenance folder
- Check PROJECT_ROOT calculation in script

---

## Files

```
maintenance/
  project_oracle.py      # Main script
  ORACLE_README.md       # This file

context/
  ORACLE_CONTEXT.md      # Maintenance session state

reports/
  snapshots/             # Context snapshots
  ORACLE_REPORT_*.md     # Audit reports
```

---

## Glossary

| Term | Definition |
|------|------------|
| **Audit** | Health check that finds issues in code and documentation |
| **Snapshot** | Point-in-time capture of project state for session continuity |
| **Baseline** | Starting point for tracking changes within a session |
| **Sync** | Update documentation to match code reality |
| **Health Score** | 0-10 rating of overall project health |
| **Context File** | DEV_CONTEXT.md or ORACLE_CONTEXT.md - session state documents |

---

## How Oracle Works

**Oracle is a tool, not a background process. Claude is the orchestrator.**

### Execution Model

Each command is a separate execution - runs, does its job, exits:

```bash
python3 maintenance/project_oracle.py status        # runs ~0.5s, exits
python3 maintenance/project_oracle.py audit --quick # runs ~3s, exits
python3 maintenance/project_oracle.py autosave      # runs ~2s, exits
```

There is no persistent background process. Claude calls the script at intervals defined in session rules.

### Automation Flow

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

### Key Point

Claude is the orchestrator. Oracle is just a tool Claude calls. Session rules in DEV_CONTEXT.md define when Claude should call each command.

### If "Always Running" Is Needed (Future)

That's the Background Health Monitor - a separate persistent process. See `context/ORACLE_CONTEXT.md` Future Planning section.

---

## Related Documentation

- **context/ORACLE_CONTEXT.md** - Maintenance session state (Claude reads first)
- **context/DEV_CONTEXT.md** - Development session state
- **docs/WORKFLOW.md** - Operational processes including oracle usage

---

*Project Oracle - Keeping your project healthy across context compactions.*
