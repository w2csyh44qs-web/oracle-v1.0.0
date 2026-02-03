# Oracle Monitoring Guide

**Complete guide to monitoring Oracle with sEEG (terminal) or web dashboard**

Oracle provides two powerful monitoring interfaces—choose the one that fits your workflow. Both provide real-time monitoring, command execution, and project health insights.

---

## Monitoring Options

Oracle offers **two monitoring interfaces**—both are optional and provide similar functionality:

### Option 1: sEEG (Terminal Dashboard)
**Best for:** Developers who prefer terminal-based workflows, IDE integration, Claude Code extension users

- Pure terminal interface
- Minimal resource usage
- Vi-style command palette (`:` key)
- Multiple view modes (Full/Compact/Split)
- Works in any terminal
- Perfect for CLI-first workflows

### Option 2: Web Dashboard
**Best for:** Visual monitoring, remote access, multi-device monitoring

- Browser-based interface
- Real-time WebSocket updates
- Black terminal aesthetic
- Mobile-responsive design
- Multiple view modes (Full/Compact)
- Remote access capability

**Choose one based on your preference.** Both read from the same data sources and provide equivalent functionality.

---

## Option 1: sEEG (Terminal Dashboard)

### What is sEEG?

sEEG (Stereo-Electro-Encephalo-Graphy) is Oracle's terminal-based monitoring dashboard. It provides a real-time view of Oracle's state directly in your terminal.

**Etymology:** Named after the medical brain monitoring technique, reflecting Oracle's brain cell architecture.

### Features

- **Real-Time Monitoring**: Health score, daemon status, file changes
- **Command Palette**: Execute Oracle commands inline (Vi-style `:` key)
- **Multiple Views**: Full, Compact, Split modes
- **Diagnostics**: Quick health checks with `[d]` key
- **Activity Feed**: Recent daemon activity and file changes
- **Lightweight**: <1% CPU, minimal memory usage

### Installation

sEEG is included with Oracle core—no additional dependencies.

**Verify:**
```bash
python3 oracle/seeg.py
```

### Starting sEEG

**Basic Start:**
```bash
python3 oracle/seeg.py
```

**From Oracle CLI:**
```bash
python3 oracle/cli.py monitor
```

**Exit:** Press `q` to quit

### Interface Layout

sEEG displays three main sections:

#### Header
```
╔══════════════════════════════════════════════════════════════╗
║  🧠 ORACLE MONITORING                    [●] Connected      ║
║  Health: 85 ████████░░  Daemon: ✓ Running  Files: 12       ║
╚══════════════════════════════════════════════════════════════╝
```

**Metrics:**
- **Health Score**: 0-100 with color-coded bar
  - Green (≥80): Healthy
  - Yellow (60-79): Warning
  - Red (<60): Critical
- **Daemon Status**: Running/Stopped with PID
- **File Changes**: Recent modifications count

#### Activity Panel
```
┌─ RECENT ACTIVITY ────────────────────────────────────────────┐
│ 14:32:15  Modified: app.py (+45 -12)                         │
│ 14:30:22  Health check: 85 (stable)                          │
│ 14:28:10  Daemon started (PID: 12345)                        │
└──────────────────────────────────────────────────────────────┘
```

Shows last 10 events from daemon.

#### Footer (Command Bar)
```
[q]uit  [d]iagnostics  [r]efresh  [v]iew  [:]cmd
```

**View Modes:**
- Press `v` to cycle: Full → Compact → Split

**Command Mode:**
- Press `:` to activate command palette
- Type command and press Enter
- Use `↑`/`↓` for history

### Command Palette

Press `:` to enter command mode (Vi-style):

```
Command: audit --quick█
```

**Available Commands:**
- `audit` - Run full health audit
- `audit --quick` - Quick health check
- `status` - Show Oracle status
- `verify` - Run integrity check
- `clean` - Clean old reports
- `optimize` - Run optimizations
- `sync` - Sync contexts
- `help` - Show available commands

**Features:**
- Command history (↑/↓ arrows)
- 30-second timeout for long commands
- Inline result display
- Subprocess execution

**Exit command mode:** Press `Esc` or execute command

### View Modes

#### Full View
**What's visible:**
- All metrics (health, daemon, files)
- Recent activity (last 10 events)
- Current context
- Command bar with all options

**Best for:** Comprehensive monitoring during active development

#### Compact View
**What's visible:**
- Essential metrics only (health, daemon status)
- Minimal activity (last 3 events)
- Simplified command bar

**Best for:** Quick status checks, small terminal windows

#### Split View
**What's visible:**
- Metrics on top half
- Activity feed on bottom half
- Dual-panel layout

**Best for:** Monitoring activity while keeping metrics visible

**Switch views:** Press `v` to cycle through modes

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit sEEG |
| `d` | Run diagnostics (quick health check) |
| `r` | Refresh data manually |
| `v` | Cycle view modes (Full/Compact/Split) |
| `:` | Enter command palette |
| `↑` | Previous command (in command mode) |
| `↓` | Next command (in command mode) |
| `Esc` | Exit command mode |
| `Enter` | Execute command (in command mode) |

### Data Sources

sEEG reads from:

1. **`oracle/data/.oracle_status.json`** - Daemon status
2. **`oracle/data/.oracle_health_status.json`** - Health metrics
3. **`oracle/data/.oracle_daemon.log`** - Activity events

**If metrics show `--`:**
```bash
# Create status files
python3 oracle/project_oracle.py audit --quick
python3 oracle/cli.py daemon start
```

### sEEG Best Practices

**Development Workflow:**
1. Start sEEG in dedicated terminal tab/pane
2. Keep it running throughout development session
3. Glance at metrics periodically
4. Use command palette for quick checks
5. Run diagnostics with `d` key when needed

**Terminal Multiplexer Integration:**
```bash
# tmux
tmux new-session -s oracle 'python3 oracle/seeg.py'
tmux attach -t oracle

# screen
screen -S oracle -dm python3 oracle/seeg.py
screen -r oracle
```

**IDE Integration:**
- Many IDEs support embedded terminals
- Run sEEG in IDE terminal for unified workspace
- Works perfectly with Claude Code extension

**Performance:**
- CPU: <0.5% (updates every 2s)
- Memory: ~10-20MB
- No network overhead (local file reads)

### Troubleshooting sEEG

**Terminal rendering issues:**
- Ensure terminal supports Unicode
- Minimum terminal size: 80x24
- Use Full HD terminal for best experience

**No data displayed:**
- Run `python3 oracle/project_oracle.py audit --quick`
- Start daemon: `python3 oracle/cli.py daemon start`
- Check that status files exist in `oracle/data/`

**Command palette not responding:**
- Press `Esc` to exit command mode
- Restart sEEG if frozen

---

## Option 2: Web Dashboard

### What is the Web Dashboard?

A lightweight browser-based interface that provides real-time monitoring and command execution through a black terminal-themed web UI.

### Features

- **Real-Time Monitoring**: Health score, daemon status, activity feed
- **Command Terminal**: Execute Oracle commands from browser
- **Visual Metrics**: Color-coded health bars, issue tracking, cost monitoring
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Multiple View Modes**: Full view with logs/tasks, or compact essentials-only
- **Remote Access**: Access from any device on your network

### Technology Stack

- **Backend**: Flask + Flask-SocketIO (Python)
- **Frontend**: Vanilla JavaScript + Socket.IO client
- **Styling**: Pure CSS with black terminal aesthetic
- **Updates**: WebSocket (real-time) + REST API (fallback)

### Installation

**Dependencies:**
```bash
pip install flask flask-socketio flask-cors python-socketio
```

**Note:** Dashboard is **optional**. Oracle core works without it.

**Verify Installation:**
```bash
python3 -c "from oracle.dashboard import DashboardServer; print('✅ Dashboard available')"
```

### Starting the Dashboard

**Basic Start:**
```bash
python3 oracle/cli.py dashboard start
```

Dashboard runs at: **http://localhost:7777**

**Custom Port:**
```bash
python3 oracle/cli.py dashboard start --port 8080
```

**Remote Access (All Interfaces):**
```bash
python3 oracle/cli.py dashboard start --host 0.0.0.0 --port 7777
```

**Warning:** This exposes dashboard to your local network. Use with caution.

**Background Mode:**
```bash
python3 oracle/cli.py dashboard start > /dev/null 2>&1 &
```

Or use a process manager like `screen` or `tmux`.

### Stopping the Dashboard

**Via CLI:**
```bash
python3 oracle/cli.py dashboard stop
```

**For Custom Port:**
```bash
python3 oracle/cli.py dashboard stop --port 8080
```

**Manual Stop:**
```bash
# Find process
lsof -ti:7777

# Kill process
kill <PID>
```

### Dashboard Interface

#### Header Section

**Left Side:**
- 🧠 **ORACLE DASHBOARD** - Title

**Right Side:**
- **View Switcher**: Toggle between Full/Compact modes
- **Connection Status**: Green dot = connected, Gray dot = disconnected

#### Status Section (Top Panel)

Displays project-agnostic metrics:

1. **HEALTH**: Score (0-100) with color-coded bar
   - Green (≥80): Healthy
   - Orange (60-79): Warning
   - Red (<60): Critical

2. **DAEMON**: Running status, PID, uptime, active context
   - ✓ YES (green) = Running
   - ✗ NO (red) = Stopped

3. **ISSUES**: Critical count, warnings, optimizations pending

4. **COST TODAY**: Daily API cost tracking

5. **ACTIVITY**: Recent daemon activity (inline feed)

6. **DAEMON LOGS**: Collapsible section showing last 20 log entries (Full view only)

7. **TASKS**: Collapsible task list (Full view only)

#### Terminal Section (Bottom Panel)

**Terminal Output:**
- Command history
- Command results
- Connection messages

**Available Commands (Clickable):**
- `audit` - Run health audit
- `status` - Show Oracle status
- `verify` - Run integrity check
- `clean` - Clean old reports
- `optimize` - Run optimizations
- `help` - Show available commands

**Command Input:**
- Type command and press Enter
- Use ↑/↓ arrows for history navigation

#### Footer

- **Left**: Oracle version and branding
- **Right**: Last update timestamp

### View Modes

#### Full View

**What's Visible:**
- All metrics (health, daemon, issues, cost, autosave)
- Activity feed
- Daemon logs (collapsible)
- Task list (collapsible)
- Terminal with full command history

**Best For:**
- Detailed monitoring
- Debugging issues
- Comprehensive project oversight

#### Compact View

**What's Visible:**
- Essential metrics only (health, daemon, issues, cost)
- Terminal with command input

**What's Hidden:**
- Activity feed
- Daemon logs
- Task list
- Metric details (PID, uptime, etc.)

**Best For:**
- Quick status checks
- Small screens
- Minimal distraction

**Switch Views:** Click **Full** or **Compact** buttons in header

### Real-Time Updates

**WebSocket Connection:**
Dashboard uses WebSocket for <100ms latency updates:
- Status changes (daemon start/stop, health score)
- Activity events (file changes, commits)
- Command results (live feedback)

**Connection Indicator:**
- Green pulsing dot = Connected
- Gray dot = Disconnected

**Fallback Polling:**
If WebSocket fails, dashboard falls back to REST API polling:
- Updates every 5 seconds
- Less real-time but still functional
- Check console for warnings

**Manual Refresh:**
Dashboard auto-updates, but you can force refresh by reloading the browser page.

### Running Commands

**From Dashboard Terminal:**
1. Click command hint (e.g., `audit`) to fill input, OR
2. Type command manually (e.g., `status`)
3. Press Enter to execute

**Example:**
```
oracle> audit
Executing...
✓ Health Score: 85
✓ No critical issues
✓ Command completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Built-In Commands:**
- `help` - Show command list
- `clear` - Clear terminal output

**Oracle Commands:**
All `oracle/project_oracle.py` commands work from dashboard:
```
oracle> audit              # Full health audit
oracle> audit --quick      # Quick check
oracle> status             # Current status
oracle> verify             # Integrity check
oracle> clean              # Clean old reports
oracle> optimize           # Run optimizations
oracle> sync               # Sync contexts
```

**Command timeout:** 30 seconds

**Long-running commands:** For commands that take >30s, use CLI instead.

### Dashboard Data Sources

Dashboard is **project-agnostic** and reads from:

1. **Daemon Status File** - `oracle/data/.oracle_status.json`
   - Daemon running state, PID, uptime, active context
   - Created by: Daemon (when running)

2. **Health Status File** - `oracle/data/.oracle_health_status.json`
   - Health score, issues counts, cost tracking, autosave status
   - Created by: Health audit commands (`audit`, `audit --quick`)

3. **Daemon Logs** - `oracle/data/.oracle_daemon.log`
   - Daemon activity, file changes, health check results
   - Created by: Daemon (continuous)

**If Dashboard Shows No Data:**
```bash
# Run health audit to populate data
python3 oracle/project_oracle.py audit --quick

# Start daemon (creates status file)
python3 oracle/cli.py daemon start
```

### Responsive Design

Dashboard automatically adjusts to window size:

- **Desktop (>1024px)**: Full width, all metrics horizontal, large fonts
- **Tablet (768-1024px)**: Slightly smaller fonts, reduced spacing
- **Mobile (480-768px)**: Stacked vertical layout, smaller fonts
- **Narrow Vertical (<600px)**: Optimized for tall narrow windows

**Test responsive design:** Resize browser window to see layout adapt in real-time.

### Customization

**Change Dashboard Port:**
```bash
python3 oracle/cli.py dashboard start --port 8080
```

**Change Host (Remote Access):**
```bash
python3 oracle/cli.py dashboard start --host 0.0.0.0
```

**Security Warning:** This exposes dashboard to your network. Consider firewall rules, VPN access only.

**Custom Themes:**
Dashboard CSS is in `oracle/dashboard/static/css/terminal.css`.

**Color scheme:**
- Background: `#000` (pure black)
- Primary text: `#e0e0e0` (light gray)
- Accent: `#0088ff` (blue)
- Success: `#00ff00` (green)
- Warning: `#ffaa00` (orange)
- Error: `#ff4444` (red)

Modify `terminal.css` and restart dashboard to apply changes.

### Web Dashboard Best Practices

**Development Workflow:**
1. Start dashboard once per session
2. Keep browser tab open for real-time monitoring
3. Use dashboard for quick status checks and short commands
4. Use CLI for long-running commands and scripting

**Security:**
- **Local Development**: Default `localhost:7777` is safe (only accessible from your machine)
- **Remote Access**: Use VPN or SSH tunnel:
  ```bash
  ssh -L 7777:localhost:7777 user@remote-machine
  ```
- **Production**: Don't run dashboard on production servers

**Performance:**
- CPU: <1%
- Memory: ~50-100MB
- WebSocket: Minimal overhead

**For Slow Machines:**
- Use Compact view (less rendering)
- Close logs/tasks sections
- Increase poll interval (modify `app.js`)

### Troubleshooting Web Dashboard

**Dashboard Won't Start:**
```bash
# Check dependencies
python3 -c "import flask; import flask_socketio; print('✅ OK')"

# Check if port is available
lsof -ti:7777

# Solutions:
pip install flask flask-socketio flask-cors python-socketio
python3 oracle/cli.py dashboard start --port 8080
kill $(lsof -ti:7777)
```

**Dashboard Shows "Disconnected":**
- Check browser console for WebSocket errors
- Restart dashboard: `oracle dashboard stop && oracle dashboard start`

**Commands Timeout:**
- Run long commands from CLI instead
- Dashboard has 30-second timeout

**WebSocket Connection Fails:**
- Dashboard automatically falls back to polling (5s updates)
- Check firewall, VPN, or CORS issues in browser console

### API Reference

Dashboard exposes REST API endpoints:

- `GET /` - Returns dashboard UI
- `GET /api/status` - Current Oracle status (JSON)
- `GET /api/health` - Health metrics only
- `GET /api/activity` - Recent activity events
- `POST /api/command` - Execute command
- `GET /api/logs` - Recent daemon logs

**Usage Example:**
```bash
curl http://localhost:7777/api/status | jq .
```

---

## Comparison: sEEG vs Web Dashboard

### When to Use sEEG (Terminal)

**Best for:**
- Terminal-first workflows
- CLI power users
- IDE integration (VSCode, Neovim, Emacs)
- Claude Code extension users
- Minimal resource usage
- No external dependencies

**Advantages:**
- Faster startup (<1s)
- Lower resource usage (10-20MB vs 50-100MB)
- Works in any terminal
- No browser required
- Vi-style command palette
- Perfect for SSH sessions

**User Preference Example:**
> "Personally I prefer the terminal dashboard with IDE client and Claude Code extension."

### When to Use Web Dashboard

**Best for:**
- Visual monitoring preference
- Remote access needs
- Multi-device monitoring
- Teams (shared dashboard URL)
- Mobile/tablet access
- Graphical metrics preference

**Advantages:**
- Browser-based (accessible from any device)
- WebSocket real-time updates
- Collapsible logs/tasks sections
- Click-to-execute commands
- Better for presentations/demos
- Mobile-responsive design

### Feature Comparison

| Feature | sEEG (Terminal) | Web Dashboard |
|---------|----------------|---------------|
| **Health Monitoring** | ✅ | ✅ |
| **Command Execution** | ✅ (`:` palette) | ✅ (terminal input) |
| **Real-Time Updates** | ✅ (2s poll) | ✅ (<100ms WebSocket) |
| **View Modes** | 3 (Full/Compact/Split) | 2 (Full/Compact) |
| **Resource Usage** | 10-20MB, <0.5% CPU | 50-100MB, <1% CPU |
| **Remote Access** | SSH only | HTTP (any device) |
| **Dependencies** | None | Flask, Flask-SocketIO |
| **Startup Time** | <1s | ~3s |
| **Mobile Support** | Terminal apps | Native browser |
| **Logs Display** | Activity feed | Collapsible panel |
| **Task Management** | Via commands | Visual list |

### Using Both Together

**You can run both simultaneously:**
- Both read from the same data sources
- No conflicts or synchronization issues
- Choose based on current task

**Example workflow:**
```bash
# Terminal 1: Start daemon
python3 oracle/cli.py daemon start

# Terminal 2: Run sEEG for active monitoring
python3 oracle/seeg.py

# Browser: Open web dashboard for visual overview
open http://localhost:7777
```

**When to use both:**
- sEEG in IDE terminal for immediate feedback
- Web dashboard on second monitor for visual overview
- Team collaboration (share web dashboard URL)

---

## Integration with Oracle Components

### With Daemon

Both monitoring options integrate with Oracle daemon:
- Daemon updates `oracle/data/.oracle_status.json`
- Both sEEG and web dashboard poll this file
- Real-time sync of daemon state

**If daemon is stopped:**
- Metrics show `--` or `N/A`
- Commands still work (executed directly)
- Activity feed shows no events

### With Git Hooks

Git hooks don't directly interact with monitoring, but:
- Hooks update Oracle state during commits
- Changes appear in activity feeds
- Health score updates after pre-commit checks

### With Memory System (Hippocampus)

Monitoring displays memory-captured observations:
- Recent observations in activity feed
- Observation counts in metrics
- Context updates trigger visual refresh

---

## FAQ

**Q: Do I need to use a monitoring interface?**
A: No, both are optional. You can use Oracle via CLI only.

**Q: Which monitoring option is better?**
A: Personal preference. sEEG for terminal workflows, web dashboard for visual monitoring.

**Q: Can I use both sEEG and web dashboard simultaneously?**
A: Yes, they work independently and read from the same data sources.

**Q: Does monitoring work without daemon?**
A: Yes, but daemon metrics will show `--`. Health metrics work if you run audits manually.

**Q: Why do metrics show `--` or `N/A`?**
A: Status files don't exist. Run `oracle audit --quick` and start daemon.

**Q: Can I access the web dashboard remotely?**
A: Yes, use `--host 0.0.0.0`, but consider security (VPN, SSH tunnel).

**Q: Which monitoring option uses less resources?**
A: sEEG uses ~10-20MB, web dashboard uses ~50-100MB.

**Q: Can I customize the monitoring interface?**
A: sEEG has limited customization. Web dashboard CSS can be fully customized.

**Q: Do monitoring tools work on Windows?**
A: sEEG requires terminal with Unicode support. Web dashboard works in any browser.

**Q: Can monitoring tools be embedded in other applications?**
A: Web dashboard can be embedded via iframe or API. sEEG is standalone terminal app.

---

## Quick Reference

### sEEG Commands

```bash
# Start sEEG
python3 oracle/seeg.py

# Keyboard shortcuts
q         # Quit
d         # Diagnostics
r         # Refresh
v         # Cycle views
:         # Command palette
↑/↓       # Command history
Esc       # Exit command mode
```

### Web Dashboard Commands

```bash
# Start dashboard
python3 oracle/cli.py dashboard start

# Custom port
python3 oracle/cli.py dashboard start --port 8080

# Remote access
python3 oracle/cli.py dashboard start --host 0.0.0.0

# Stop dashboard
python3 oracle/cli.py dashboard stop

# Access
open http://localhost:7777
```

### Data Sources (Both)

Both monitoring options read from:
- `oracle/data/.oracle_status.json` - Daemon status
- `oracle/data/.oracle_health_status.json` - Health metrics
- `oracle/data/.oracle_daemon.log` - Activity logs

**Initialize data:**
```bash
python3 oracle/project_oracle.py audit --quick
python3 oracle/cli.py daemon start
```

---

*Oracle v1.0 - Brain Cell Architecture*
*Choose Your Monitoring Interface*
