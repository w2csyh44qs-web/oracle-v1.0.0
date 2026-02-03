# P31: Oracle v1.0 Final Enhancements - Set & Forget Operation

**Status:** Planning
**Created:** February 2, 2026 (O105 continuing)
**Goal:** Final polish for GitHub release - background daemon, web dashboard, git integration, enhanced seeg
**Type:** Enhancement (integrates with existing Oracle functionality)

---

## Vision

Transform Oracle from "run manually when needed" to **"drop in project once and forget"** - fully automated background operation with optional monitoring dashboards (web or terminal).

**User Experience Goals:**
1. `oracle init .` - One-time setup on any project
2. Daemon starts automatically on system boot (launchd/systemd)
3. Git hooks run verification automatically on commits
4. Web dashboard at `http://localhost:7777` for monitoring/control
5. Terminal users can use enhanced seeg with command line
6. Focus stays on project work, Oracle runs invisibly in background

**This is the FINAL step before v1.0 GitHub release.**

---

## Current State Analysis

### What Already Exists (Excellent Foundation)

✅ **Background Daemon** (`oracle/context/daemon.py` ~800 lines)
- File watching across 5 contexts
- Context detection (300-second activity windows)
- Cross-session messaging queue
- Status persistence (`.oracle_status.json`)
- Runs in 30-second loop
- Graceful shutdown on Ctrl+C

✅ **Terminal Dashboard** (`oracle/seeg.py` ~3,500 lines)
- Rich terminal UI with multiple modes
- Real-time health monitoring
- Activity tracking (file changes, health updates, context growth)
- Keyboard controls (h/d/t/c/q)
- Autosave reminders
- macOS notifications
- Activity calibration

✅ **Git Hooks** (`oracle/validation/topoisomerase.py`)
- **HookManager class** (lines 694-760)
- Generates `.pre-commit-config.yaml`
- Installs/uninstalls hooks
- Pre-commit integration ready
- CI/CD templates (GitHub Actions, GitLab CI)

✅ **Verification Commands** (`oracle/validation/topoisomerase.py`)
- `verify --quick` - 5 second check (circular imports, syntax)
- `verify --standard` - 30 second check (full analysis)
- `verify --full` - Complete with mypy/pytest
- `verify --perf` - Performance regression
- `verify --fix --apply` - Auto-fix issues

✅ **Project Orchestration** (`oracle/project_oracle.py`)
- 15 commands (audit, clean, optimize, sync, verify, assess, etc.)
- Well-structured CLI
- Context management
- Health monitoring

### What Needs Enhancement

🔨 **Daemon Auto-Start**
- No system integration (launchd/systemd)
- No startup persistence
- No recovery on crash
- No scheduled periodic checks (only event-driven)

🔨 **Web Dashboard**
- Terminal-only monitoring (no web interface)
- No real-time WebSocket streaming
- No remote monitoring capability
- No command execution from UI

🔨 **Git Integration**
- Hooks implemented but not advertised
- No automatic installation during `oracle init`
- No commit-specific context validation

🔨 **Seeg Enhancement**
- No interactive command line
- No task execution from dashboard
- Cannot run Oracle commands from seeg

---

## Implementation Phases

### Phase 1: Daemon Auto-Start (Week 1)
**Goal:** Make Oracle daemon start automatically on system boot

**Files to Create:**
- `oracle/daemon/__init__.py` (~20 lines)
- `oracle/daemon/oracle_daemon.py` (~300 lines)
- `oracle/daemon/service_manager.py` (~200 lines)

**Files to Modify:**
- `oracle/cli.py` - Add `daemon` command group (~50 lines)
- `oracle/project_oracle.py` - Add daemon management (~30 lines)

**New Commands:**
```bash
oracle daemon install        # Install system service
oracle daemon start          # Start daemon
oracle daemon stop           # Stop daemon
oracle daemon status         # Check status
oracle daemon logs           # View logs
oracle daemon uninstall      # Remove service
```

**Key Features:**
- **macOS:** launchd integration (`~/Library/LaunchAgents/com.oracle.daemon.plist`)
- **Linux:** systemd integration (`~/.config/systemd/user/oracle-daemon.service`)
- **PID file:** Prevents multiple instances
- **Logging:** Writes to `oracle/data/.oracle_daemon.log`
- **Auto-restart:** Crashes trigger automatic restart
- **Periodic checks:** Health/memory checks every 5 minutes

**Success Criteria:**
- ✅ Daemon starts on system boot
- ✅ Survives crashes with auto-restart
- ✅ Runs periodic health checks
- ✅ Prevents multiple instances
- ✅ Clean shutdown on SIGTERM

### Phase 2: Web Dashboard (Week 2)
**Goal:** Create web-based monitoring/control interface

**Files to Create:**
- `oracle/dashboard/__init__.py` (~20 lines)
- `oracle/dashboard/server/app.py` (~400 lines) - Flask app
- `oracle/dashboard/server/websocket.py` (~200 lines) - Real-time updates
- `oracle/dashboard/server/api.py` (~150 lines) - REST endpoints
- `oracle/dashboard/static/index.html` (~300 lines) - Dashboard UI
- `oracle/dashboard/static/css/terminal.css` (~200 lines) - Black theme
- `oracle/dashboard/static/js/app.js` (~300 lines) - Dashboard logic
- `oracle/dashboard/static/js/websocket.js` (~150 lines) - WebSocket client

**New Commands:**
```bash
oracle dashboard start              # Start server on :7777
oracle dashboard start --port 8080  # Custom port
oracle dashboard stop               # Stop server
oracle dashboard status             # Check if running
```

**Dashboard Features:**
- **Split View:**
  - Left: Monitoring panel (health, activity, metrics)
  - Right: Terminal panel (command interface)
- **Black Terminal Aesthetic:** Simulates seeg/venv terminal experience
- **Real-Time Updates:** WebSocket for live data streaming
- **Command Execution:** Run Oracle commands directly from web UI
- **Activity Log:** Recent events with timestamps
- **Mobile-Responsive:** Works on phones/tablets

**Visual Layout:**
```
┌──────────────────────────────┬──────────────────────────────┐
│     🧠 Oracle Dashboard       │      Oracle Terminal         │
│                              │                              │
│  Health Score: 85            │ oracle> audit --quick        │
│  ████████████░░░░ 60%        │ Running health audit...      │
│                              │ ✓ Health score: 85           │
│  Active Context: Dev         │ ✓ No critical issues         │
│  File Changes: 12            │ Completed in 4.2s            │
│  Observations: 528           │                              │
│  Daemon: Running             │ oracle> █                    │
│                              │                              │
│  Recent Activity:            │                              │
│  [15:23] File: llm.py        │                              │
│  [15:22] Audit complete      │                              │
└──────────────────────────────┴──────────────────────────────┘
```

**Success Criteria:**
- ✅ Black background (#000) with green text (#0f0)
- ✅ Real-time updates via WebSocket
- ✅ Can execute Oracle commands from web UI
- ✅ Displays all key metrics
- ✅ Works on Chrome, Firefox, Safari
- ✅ Mobile-responsive design

### Phase 3: Git Hooks Auto-Install (Week 1)
**Goal:** Install git hooks automatically during `oracle init`

**Files to Modify:**
- `oracle/bootstrap/initializer.py` - Add Step 8 (hook installation) (~30 lines)
- `oracle/validation/topoisomerase.py` - Enhance error messages (~20 lines)

**Changes to Initialization Workflow:**
```python
# Step 8: Install git hooks (new)
print_step("Installing git hooks", step=8, total=8, emoji="🪝")
from oracle.validation.topoisomerase import HookManager
hook_mgr = HookManager(self.project_root)
if hook_mgr.install_hooks():
    print_success("Pre-commit hooks installed")
else:
    print_warning("Could not install hooks")
```

**Pre-Commit Checks (verify --quick):**
- Circular import detection (~2s)
- Syntax validation (~1s)
- Context file line limits (~1s)
- Missing `__init__.py` detection (~1s)
- **Total:** ~5 seconds

**Success Criteria:**
- ✅ Hooks installed automatically during `oracle init`
- ✅ Commits blocked if critical errors found
- ✅ Can bypass with `git commit --no-verify`
- ✅ Clear error messages with fix suggestions
- ✅ Fast enough for daily use (<5s)

### Phase 4: Enhanced Seeg (Week 1)
**Goal:** Add interactive command line to terminal dashboard

**Files to Modify:**
- `oracle/seeg.py` - Add CommandPalette class (~200 lines)

**New Features:**
- **Command Mode:** Press `:` to enter (Vi-style)
- **Command Execution:** Run any `oracle` command inline
- **Autocomplete:** Tab completion for commands
- **History:** ↑/↓ arrows for command history
- **Output Display:** Results shown inline
- **Exit:** Press `Esc` or type `:quit`

**Available Commands:**
```
:audit             # Run health audit
:audit --quick     # Quick audit
:verify            # Run integrity check
:status            # Show status
:clean             # Clean reports
:optimize          # Run optimizations
:memory search X   # Search memory
:help              # Show commands
:quit              # Exit command mode
```

**Visual Layout:**
```
╔════════════════════════════════════════════════════════════╗
║                    🧠 Oracle Health Monitor                ║
║                      Health Score: 85                      ║
╠════════════════════════════════════════════════════════════╣
║ Activity: ████████████░░░░░░░░░░ 60%                      ║
║ Recent Activity:                                           ║
║  [15:23:45] File modified: app/services/llm.py            ║
╠════════════════════════════════════════════════════════════╣
║ oracle> audit --quick                                      ║
║ Running health audit...                                    ║
║ ✓ Health score: 85                                         ║
║ ✓ No critical issues                                       ║
║ Completed in 4.2s                                          ║
╠════════════════════════════════════════════════════════════╣
║ oracle> █                                     [ENTER] Run  ║
╚════════════════════════════════════════════════════════════╝
```

**Success Criteria:**
- ✅ `:` key enters command mode
- ✅ Commands execute and display output
- ✅ Tab completion works
- ✅ Command history persists
- ✅ Can run all `oracle` commands

### Phase 5: Documentation & Testing (Week 1)
**Goal:** Complete documentation and end-to-end testing

**Files to Create:**
- `oracle/docs/DAEMON_GUIDE.md` (~400 lines)
- `oracle/docs/DASHBOARD_GUIDE.md` (~300 lines)
- `oracle/docs/GIT_INTEGRATION.md` (~200 lines)
- `oracle/docs/QUICK_START.md` (~150 lines)

**Files to Modify:**
- `oracle/README.md` - Add "Set and Forget" section (~100 lines)
- `oracle/bootstrap/README.md` - Document auto-install hooks (~50 lines)
- `oracle/docs/context/ORACLE_CONTEXT.md` - Update recent changes (~50 lines)

**Testing Plan:**
- ✅ Daemon: Test on macOS (launchd) and Linux (systemd)
- ✅ Dashboard: Test on Chrome, Firefox, Safari
- ✅ Git Hooks: Test on real commits (valid + invalid)
- ✅ Seeg: Test command mode with all commands
- ✅ End-to-End: Complete "set and forget" workflow
- ✅ Performance: Verify <5s commit hooks, <100ms dashboard updates

**Success Criteria:**
- ✅ All features documented
- ✅ Quick start guide works for new users
- ✅ Integration tests pass
- ✅ Performance targets met
- ✅ Works on macOS + Linux

---

## Critical Files Summary

### New Files (~2,500 lines)
```
oracle/daemon/
├── __init__.py (20)
├── oracle_daemon.py (300)
└── service_manager.py (200)

oracle/dashboard/
├── __init__.py (20)
├── server/
│   ├── app.py (400)
│   ├── websocket.py (200)
│   └── api.py (150)
└── static/
    ├── index.html (300)
    ├── css/terminal.css (200)
    └── js/
        ├── app.js (300)
        └── websocket.js (150)
```

### Modified Files (~460 lines added)
```
oracle/cli.py (+50)
oracle/project_oracle.py (+30)
oracle/bootstrap/initializer.py (+30)
oracle/seeg.py (+200)
oracle/README.md (+100)
oracle/docs/context/ORACLE_CONTEXT.md (+50)
```

---

## End-to-End Verification

### Test Scenario 1: New Project Setup
```bash
# One-time setup
cd /path/to/new/project
oracle init .

# What happens automatically:
# 1. Oracle bootstraps (detects Flask, creates configs)
# 2. Git hooks installed (.pre-commit-config.yaml created)
# 3. Daemon service installed and started
# 4. Dashboard server starts on :7777

# Result: Oracle running in background
# User can now work on project, Oracle handles everything else
```

### Test Scenario 2: Daily Development
```bash
# Developer makes changes
vim app/services/llm.py
git add .
git commit -m "Update LLM service"

# What happens automatically:
# 1. Pre-commit hook runs (verify --quick, ~5s)
# 2. Circular imports checked
# 3. Syntax validated
# 4. Commit proceeds if checks pass
# 5. Daemon captures file change
# 6. Memory records observation
# 7. Dashboard updates in real-time

# Developer never thinks about Oracle
```

### Test Scenario 3: Monitoring Options
```bash
# Option A: Web dashboard (recommended)
open http://localhost:7777

# Option B: Terminal dashboard (power users)
oracle/seeg.py

# Option C: CLI (scripting)
oracle status
oracle audit --quick

# All three show same data, different interfaces
```

---

## Success Criteria

### Must Have
1. ✅ Daemon starts on system boot (macOS + Linux)
2. ✅ Git hooks run automatically on commits (<5s)
3. ✅ Web dashboard accessible at localhost:7777
4. ✅ Black terminal aesthetic in dashboard
5. ✅ Commands executable from both web and terminal
6. ✅ Real-time updates via WebSocket
7. ✅ Enhanced seeg with command line
8. ✅ Complete documentation

### Performance Targets
- Commit hooks: <5 seconds
- Dashboard updates: <100ms latency
- Daemon CPU: <1% idle, <5% active
- Memory footprint: <50MB

### User Experience
- One command setup: `oracle init .`
- Zero configuration after init
- Invisible operation (set and forget)
- Multiple monitoring options
- Works without Oracle expertise

---

## Timeline

**Total: 4-5 weeks (part-time)**

- Week 1: Daemon auto-start + Git hooks enhancement
- Week 2: Web dashboard (backend + frontend)
- Week 3: Enhanced seeg + integration
- Week 4: Testing + documentation
- Week 5: Polish + GitHub release prep

---

## After P31: GitHub Release Checklist

- [ ] All enhancements tested on macOS + Linux
- [ ] Documentation complete
- [ ] LICENSE file added
- [ ] CONTRIBUTING.md created
- [ ] GitHub Actions CI/CD configured
- [ ] Demo video/screenshots
- [ ] Installation script tested
- [ ] Onboard 3 external users
- [ ] Create GitHub release (v1.0.0)
- [ ] Publish to PyPI (optional)

---

*P31: Final enhancements before v1.0 GitHub release - Set and Forget Operation*
