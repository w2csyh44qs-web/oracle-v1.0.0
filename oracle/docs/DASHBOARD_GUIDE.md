# Oracle Dashboard Guide

**Complete guide to the Oracle web dashboard**

The Oracle Dashboard provides real-time monitoring and command execution through a black terminal-themed web interface. Access project health, daemon status, and run Oracle commands—all from your browser.

---

## Overview

### What is the Dashboard?

A lightweight web interface that provides:

- **Real-Time Monitoring**: Health score, daemon status, activity feed
- **Command Terminal**: Execute Oracle commands from browser
- **Visual Metrics**: Color-coded health bars, issue tracking, cost monitoring
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Multiple View Modes**: Full view with logs/tasks, or compact essentials-only

### Technology Stack

- **Backend**: Flask + Flask-SocketIO (Python)
- **Frontend**: Vanilla JavaScript + Socket.IO client
- **Styling**: Pure CSS with black terminal aesthetic
- **Updates**: WebSocket (real-time) + REST API (fallback)

---

## Installation

### Dependencies

```bash
pip install flask flask-socketio flask-cors python-socketio
```

**Note:** Dashboard is **optional**. Oracle core works without it.

### Verify Installation

```bash
python3 -c "from oracle.dashboard import DashboardServer; print('✅ Dashboard available')"
```

---

## Starting the Dashboard

### Basic Start

```bash
python3 oracle/cli.py dashboard start
```

Dashboard runs at: **http://localhost:7777**

### Custom Port

```bash
python3 oracle/cli.py dashboard start --port 8080
```

Dashboard runs at: **http://localhost:8080**

### Remote Access (All Interfaces)

```bash
python3 oracle/cli.py dashboard start --host 0.0.0.0 --port 7777
```

**Warning:** This exposes dashboard to your local network. Use with caution.

### Background Mode

Dashboard runs in foreground by default. To run in background:

```bash
python3 oracle/cli.py dashboard start > /dev/null 2>&1 &
```

Or use a process manager like `screen` or `tmux`.

---

## Stopping the Dashboard

### Via CLI

```bash
python3 oracle/cli.py dashboard stop
```

Stops dashboard running on default port (7777).

### For Custom Port

```bash
python3 oracle/cli.py dashboard stop --port 8080
```

### Manual Stop

```bash
# Find process
lsof -ti:7777

# Kill process
kill <PID>
```

---

## Dashboard Interface

### Header Section

**Left Side:**
- 🧠 **ORACLE DASHBOARD** - Title

**Right Side:**
- **View Switcher**: Toggle between Full/Compact modes
- **Connection Status**: Green dot = connected, Gray dot = disconnected

### Status Section (Top Panel)

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

### Terminal Section (Bottom Panel)

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

### Footer

- **Left**: Oracle version and branding
- **Right**: Last update timestamp

---

## View Modes

### Full View

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

### Compact View

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

### Switching Views

Click **Full** or **Compact** buttons in header.

---

## Real-Time Updates

### WebSocket Connection

Dashboard uses WebSocket for <100ms latency updates:

- **Status changes** (daemon start/stop, health score)
- **Activity events** (file changes, commits)
- **Command results** (live feedback)

**Connection Indicator:**
- Green pulsing dot = Connected
- Gray dot = Disconnected

### Fallback Polling

If WebSocket fails, dashboard falls back to REST API polling:
- Updates every 5 seconds
- Less real-time but still functional
- Check console for warnings

### Manual Refresh

Dashboard auto-updates, but you can force refresh:
- Reload browser page
- Dashboard reconnects and fetches latest data

---

## Running Commands

### From Dashboard Terminal

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

### Built-In Commands

**help** - Show command list
```
oracle> help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ORACLE DASHBOARD COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Oracle Commands:
  audit          - Run health audit
  audit --quick  - Quick health check
  status         - Show Oracle status
  verify         - Run integrity check
  clean          - Clean reports
  optimize       - Run optimizations
  sync           - Sync contexts

Dashboard Commands:
  help           - Show this help
  clear          - Clear terminal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**clear** - Clear terminal output
```
oracle> clear
Oracle Terminal v1.0
Type 'help' for available commands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Oracle Commands

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

**Long-running commands:**
For commands that take >30s, use CLI instead of dashboard.

---

## Dashboard Data Sources

Dashboard is **project-agnostic** and reads from:

### 1. Daemon Status File
**Path:** `oracle/data/.oracle_status.json`

**Contains:**
- Daemon running state
- Process ID
- Uptime seconds
- Last update timestamp
- Active context

**Created by:** Daemon (when running)

### 2. Health Status File
**Path:** `oracle/data/.oracle_health_status.json`

**Contains:**
- Health score (0-100)
- Issues (critical/warnings counts)
- Optimizations pending
- Cost tracking
- Autosave status

**Created by:** Health audit commands (`audit`, `audit --quick`)

### 3. Daemon Logs
**Path:** `oracle/data/.oracle_daemon.log`

**Contains:**
- Daemon activity (startup, shutdown, errors)
- File change events
- Health check results

**Created by:** Daemon (continuous)

### If Dashboard Shows No Data

**Symptom:** All metrics show `--` or `N/A`

**Cause:** Status files don't exist yet

**Solution:**
```bash
# Run health audit to populate data
python3 oracle/project_oracle.py audit --quick

# Start daemon (creates status file)
python3 oracle/cli.py daemon start
```

---

## Logs and Tasks

### Daemon Logs Section

**Location:** Full view only, above terminal

**Features:**
- Last 20 log entries
- Color-coded by level:
  - Red = Error
  - Orange = Warning
  - Blue = Info
  - Gray = Normal
- Auto-scroll to bottom
- Collapsible (click header to toggle)

**Refresh:** Click header to collapse and re-expand (fetches fresh logs)

### Task List Section

**Location:** Full view only, above terminal

**Features:**
- Project-agnostic task tracking
- Status indicators:
  - □ = Pending (blue)
  - ✓ = Completed (green)
  - □ (red) = Priority
- Collapsible (click header to toggle)

**Current Tasks (Placeholder):**
- Next health audit scheduled
- Context sync pending

**Future Enhancement:**
Task list can be extended to read from `oracle/data/.oracle_tasks.json` for dynamic task management.

---

## Responsive Design

Dashboard automatically adjusts to window size:

### Desktop (>1024px)
- Full width layout
- All metrics visible horizontally
- Large fonts and spacing

### Tablet (768-1024px)
- Slightly smaller fonts
- Metrics stay horizontal
- Reduced spacing

### Mobile (480-768px)
- Stacked layout (vertical)
- Smaller fonts
- Command buttons wrap to multiple rows
- Footer stacks vertically

### Narrow Vertical Windows (<600px)
- Optimized for tall, narrow windows
- Health bar scales to 100% width
- Metrics stack with labels on top
- Command hints wrap efficiently

**Test responsive design:**
Resize browser window to see layout adapt in real-time.

---

## Customization

### Change Dashboard Port

**Method 1: CLI flag**
```bash
python3 oracle/cli.py dashboard start --port 8080
```

**Method 2: Environment variable**
```bash
export ORACLE_DASHBOARD_PORT=8080
python3 oracle/cli.py dashboard start
```

### Change Host (Remote Access)

```bash
python3 oracle/cli.py dashboard start --host 0.0.0.0
```

**Security Warning:** This exposes dashboard to your network. Consider:
- Firewall rules
- VPN access only
- Authentication (future enhancement)

### Custom Themes

Dashboard CSS is in `oracle/dashboard/static/css/terminal.css`.

**Color scheme:**
- Background: `#000` (pure black)
- Primary text: `#e0e0e0` (light gray)
- Accent: `#0088ff` (blue)
- Success: `#00ff00` (green)
- Warning: `#ffaa00` (orange)
- Error: `#ff4444` (red)

**Modify colors:**
Edit `terminal.css` and restart dashboard.

---

## Troubleshooting

### Dashboard Won't Start

**Symptom:** `dashboard start` fails with error

**Diagnosis:**
```bash
# Check if dependencies installed
python3 -c "import flask; import flask_socketio; print('✅ OK')"

# Check if port is available
lsof -ti:7777
```

**Solutions:**
```bash
# Install dependencies
pip install flask flask-socketio flask-cors python-socketio

# Use different port
python3 oracle/cli.py dashboard start --port 8080

# Kill process using port
kill $(lsof -ti:7777)
```

### Dashboard Shows "Disconnected"

**Symptom:** Gray dot in header, no updates

**Diagnosis:**
- Check browser console for WebSocket errors
- Verify dashboard server is running: `oracle dashboard status`

**Solutions:**
```bash
# Restart dashboard
python3 oracle/cli.py dashboard stop
python3 oracle/cli.py dashboard start

# Check logs
# (Dashboard prints to stdout/stderr)
```

### Commands Timeout

**Symptom:** Command runs but never returns result

**Cause:** Command takes >30 seconds

**Solution:**
Run long commands from CLI instead:
```bash
python3 oracle/project_oracle.py <command>
```

### Dashboard Shows No Metrics

**Symptom:** All values show `--` or `N/A`

**Cause:** Status files don't exist (see "Dashboard Data Sources" section)

**Solution:**
```bash
# Create status files
python3 oracle/project_oracle.py audit --quick
python3 oracle/cli.py daemon start
```

### WebSocket Connection Fails

**Symptom:** Dashboard works but no real-time updates

**Fallback:** Dashboard automatically switches to polling (updates every 5s)

**Check:**
- Browser blocks WebSocket (firewall, VPN)
- CORS issues (check browser console)
- Port 7777 blocked

### High Memory Usage

**Normal:** 50-100MB (Flask + SocketIO)
**High:** >200MB

**Cause:**
- Memory leak (rare)
- Too many WebSocket connections

**Solution:**
```bash
# Restart dashboard
python3 oracle/cli.py dashboard restart
```

---

## Best Practices

### Development Workflow

1. Start dashboard once per session:
   ```bash
   python3 oracle/cli.py dashboard start
   ```

2. Keep browser tab open for real-time monitoring

3. Use dashboard for:
   - Quick status checks
   - Running short commands
   - Visual health monitoring

4. Use CLI for:
   - Long-running commands
   - Scripting/automation
   - Detailed logs

### Security

**Local Development:**
- Default `localhost:7777` is safe
- Only accessible from your machine

**Remote Access:**
- Use VPN for remote dashboard access
- Don't expose to public internet
- Consider SSH tunnel:
  ```bash
  ssh -L 7777:localhost:7777 user@remote-machine
  ```

**Production:**
- Don't run dashboard on production servers
- Oracle is for development environments only

### Performance

**Low Resource Usage:**
- Dashboard uses minimal CPU (<1%)
- Memory footprint: ~50-100MB
- WebSocket keeps connection alive with minimal overhead

**For Slow Machines:**
- Use Compact view (less rendering)
- Increase poll interval (modify `startStatusPolling()` in `app.js`)
- Close logs/tasks sections

---

## API Reference

Dashboard exposes REST API endpoints:

### GET /
Returns: `index.html` (dashboard UI)

### GET /api/status
Returns: Current Oracle status (JSON)
```json
{
  "timestamp": "2026-02-03T00:00:00",
  "daemon": { "running": true, "pid": 12345 },
  "health": { "score": 85, "issues": {...} },
  "activity": [...],
  "autosave": {...}
}
```

### GET /api/health
Returns: Health metrics only (JSON)

### GET /api/activity
Returns: Recent activity events (JSON)

### POST /api/command
Body: `{"command": "audit"}`
Returns: Command execution result (JSON)

### GET /api/logs
Returns: Recent daemon logs (JSON)
```json
{
  "logs": [
    "2026-02-03 00:00:00 - INFO - Daemon started",
    "..."
  ]
}
```

**Usage Example:**
```bash
curl http://localhost:7777/api/status | jq .
```

---

## Integration with Other Tools

### With Daemon

Dashboard reads daemon's status file:
- Daemon updates `oracle/data/.oracle_status.json`
- Dashboard polls file every 2 seconds
- Real-time sync via WebSocket

### With Terminal Dashboard (seeg)

Both dashboards read the same data sources:
- `oracle/data/.oracle_status.json`
- `oracle/data/.oracle_health_status.json`
- `oracle/data/.oracle_daemon.log`

You can run both simultaneously for different monitoring options.

### With Git Hooks

Git hooks don't directly interact with dashboard, but:
- Hooks update Oracle state
- Dashboard reflects changes in real-time
- Commit activity appears in activity feed

---

## FAQ

**Q: Do I need the dashboard?**
A: No, it's optional. Use `seeg` or CLI for monitoring without web UI.

**Q: Can multiple users access the dashboard?**
A: Yes, if dashboard is started with `--host 0.0.0.0`. But no authentication exists.

**Q: Does dashboard work without daemon?**
A: Yes, but daemon metrics will show `--`. Health metrics work if you run audits manually.

**Q: Can I customize the terminal theme?**
A: Yes, edit `oracle/dashboard/static/css/terminal.css`.

**Q: Why do metrics show `--`?**
A: Status files don't exist. Run `audit --quick` and start daemon.

**Q: Can I run dashboard on server and access remotely?**
A: Yes, but use VPN or SSH tunnel for security.

**Q: Does dashboard consume a lot of resources?**
A: No, <1% CPU and ~50-100MB RAM.

**Q: Can I embed dashboard in another app?**
A: Yes, dashboard is accessible via iframe or direct API calls.

---

## Keyboard Shortcuts

**Terminal Input:**
- `Enter` - Execute command
- `↑` - Previous command (history)
- `↓` - Next command (history)
- Click anywhere - Focus input

**Command Hints:**
- Click any hint button to fill input

**Collapsible Sections:**
- Click header to toggle (logs, tasks)

---

*Oracle v1.0 - Brain Cell Architecture*
*Real-Time Development Intelligence*
