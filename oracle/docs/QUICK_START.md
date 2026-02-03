# Oracle Quick Start Guide

**Get Oracle running in 5 minutes**

Oracle is a project-agnostic development intelligence system that monitors your codebase, tracks changes, and maintains development context automatically.

---

## What You Get

After setup, Oracle provides:

- **Automatic Monitoring**: Daemon watches your project 24/7
- **Git Integration**: Pre-commit hooks verify changes automatically
- **Web Dashboard**: Real-time monitoring at `localhost:7777`
- **Terminal Dashboard**: Lightweight monitoring via `seeg`
- **Zero Maintenance**: Set it and forget it

---

## Prerequisites

- **Python 3.9+**
- **Git repository** (optional but recommended)
- **5 minutes** of your time

---

## Quick Setup

### Step 1: Initialize Oracle

```bash
cd /path/to/your/project
python3 oracle/cli.py init .
```

This will:
- ✅ Detect your project structure
- ✅ Generate configuration files
- ✅ Create directory structure
- ✅ Install git hooks automatically
- ✅ Scaffold context files

**Time:** ~30 seconds

---

### Step 2: Install Daemon (Auto-start on Boot)

```bash
python3 oracle/cli.py daemon install
python3 oracle/cli.py daemon start
```

This will:
- ✅ Install system service (launchd on macOS, systemd on Linux)
- ✅ Configure auto-start on system boot
- ✅ Start background monitoring

**Time:** ~10 seconds

**Verify:**
```bash
python3 oracle/cli.py daemon status
```

---

### Step 3: Start Web Dashboard (Optional)

```bash
# Install dashboard dependencies (one-time)
pip install flask flask-socketio flask-cors python-socketio

# Start dashboard
python3 oracle/cli.py dashboard start
```

Open browser to: **http://localhost:7777**

**Time:** ~20 seconds

---

## What Happens Next?

### Automatic Operations

Once installed, Oracle automatically:

1. **Monitors File Changes**: Daemon watches for modifications
2. **Tracks Activity**: Every change is logged and analyzed
3. **Verifies Commits**: Git hooks check commits before they're made
4. **Updates Dashboard**: Real-time status visible in web UI
5. **Maintains Context**: Development context stays fresh

**You don't need to do anything else.**

---

## Daily Workflow

### Making Commits

```bash
git add .
git commit -m "Your message"
```

Oracle's pre-commit hook runs automatically:
- Validates commit structure
- Checks for issues
- Updates tracking
- **Takes <5 seconds**

### Monitoring Progress

**Option 1: Web Dashboard**
```bash
open http://localhost:7777
```

**Option 2: Terminal Dashboard**
```bash
python3 oracle/seeg.py
```

Press `:` to enter command mode and run Oracle commands interactively.

**Option 3: CLI Commands**
```bash
python3 oracle/cli.py daemon status
```

---

## Common Commands

### Daemon Management

```bash
# Check status
python3 oracle/cli.py daemon status

# View logs
python3 oracle/cli.py daemon logs

# Restart daemon
python3 oracle/cli.py daemon restart

# Stop daemon
python3 oracle/cli.py daemon stop
```

### Dashboard Management

```bash
# Start dashboard
python3 oracle/cli.py dashboard start

# Custom port
python3 oracle/cli.py dashboard start --port 8080

# Check if running
python3 oracle/cli.py dashboard status

# Stop dashboard
python3 oracle/cli.py dashboard stop
```

### Running Commands (from seeg or dashboard)

In `seeg` or web dashboard terminal:
```
oracle> audit          # Run health audit
oracle> status         # Show Oracle status
oracle> verify         # Run integrity check
oracle> clean          # Clean old reports
oracle> optimize       # Run optimizations
oracle> help           # Show available commands
```

---

## Dashboard Overview

### Full View Mode
Shows all metrics:
- Health score with color-coded bar (green/orange/red)
- Daemon status (running, PID, uptime, context)
- Issues (critical/warnings) and optimizations
- Cost tracking and autosave status
- Recent activity feed
- Daemon logs (collapsible)
- Task list (collapsible)
- Command terminal

### Compact View Mode
Shows only essentials:
- Health score
- Daemon status
- Issues and cost
- Command terminal

Switch between views using the **Full/Compact** buttons in the header.

### Responsive Design
- Automatically adjusts to window size
- Works on desktop, tablet, and mobile
- Optimized for vertical and horizontal layouts

---

## Terminal Dashboard (seeg)

The `seeg` command provides a lightweight alternative to the web dashboard:

```bash
python3 oracle/seeg.py
```

**Features:**
- Real-time file change monitoring
- Activity feed with color-coded events
- Multiple display modes (full, compact, split, min)
- Command palette (press `:` to activate)
- Keyboard shortcuts for quick actions

**Keyboard Shortcuts:**
- `:` - Enter command mode (Vi-style)
- `d` - Run diagnostics (health audit)
- `q` - Quit
- `h` - Help
- `m` - Cycle display modes
- Arrow keys - Navigate command history (in command mode)

---

## Troubleshooting

### Daemon Won't Start

```bash
# Check logs for errors
python3 oracle/cli.py daemon logs

# Try foreground mode to see errors
python3 oracle/cli.py daemon start --foreground
```

### Dashboard Shows No Data

Dashboard is **project-agnostic** and reads from Oracle status files:
- `.oracle_status.json` - Created by daemon
- `.oracle_health_status.json` - Created by health audits

**Solution:** Run a health audit to populate data:
```bash
python3 oracle/project_oracle.py audit --quick
```

### Git Hooks Not Working

```bash
# Check if hooks are installed
ls -la .git/hooks/

# Reinstall hooks
python3 oracle/cli.py init . --verbose
```

### Dashboard Dependencies Missing

```bash
pip install flask flask-socketio flask-cors python-socketio
```

---

## Next Steps

### Learn More

- [Daemon Guide](DAEMON_GUIDE.md) - Deep dive into daemon management
- [Monitoring Guide](MONITORING_GUIDE.md) - sEEG (terminal) and web dashboard options
- [Git Integration](GIT_INTEGRATION.md) - Git hooks and workflow integration

### Advanced Usage

- **Custom Port:** `python3 oracle/cli.py dashboard start --port 8080`
- **Remote Access:** `python3 oracle/cli.py dashboard start --host 0.0.0.0`
- **Dry Run Init:** `python3 oracle/cli.py init . --dry-run`

### Get Help

```bash
# CLI help
python3 oracle/cli.py --help
python3 oracle/cli.py daemon --help
python3 oracle/cli.py dashboard --help

# Version info
python3 oracle/cli.py version
```

---

## Summary

**You're all set!** Oracle is now:

1. ✅ Monitoring your project automatically
2. ✅ Starting on system boot
3. ✅ Verifying git commits
4. ✅ Providing real-time dashboard
5. ✅ Maintaining development context

**Just keep coding.** Oracle handles the rest.

---

*Oracle v1.0 - Brain Cell Architecture*
*"Set and Forget" Development Intelligence*
