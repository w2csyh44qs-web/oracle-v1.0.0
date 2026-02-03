# Oracle Daemon Guide

**Complete guide to Oracle's background daemon system**

The Oracle daemon provides 24/7 automatic monitoring of your project, running health checks, tracking file changes, and maintaining development context without any manual intervention.

---

## Overview

### What is the Daemon?

The Oracle daemon is a background process that:

- **Monitors file changes** in your project
- **Runs scheduled health checks** every 5 minutes
- **Tracks activity** and maintains logs
- **Auto-restarts** on crash
- **Starts automatically** on system boot (when installed as service)

### Architecture

```
System Boot
     ↓
Launch Service (launchd/systemd)
     ↓
Oracle Daemon Process
     ↓
├─ File Watcher (monitors changes)
├─ Health Scheduler (runs audits)
├─ Activity Logger (tracks events)
└─ Status Manager (updates state)
```

---

## Installation

### Install as System Service

**macOS:**
```bash
python3 oracle/cli.py daemon install
```

Creates: `~/Library/LaunchAgents/com.oracle.daemon.plist`

**Linux:**
```bash
python3 oracle/cli.py daemon install
```

Creates: `~/.config/systemd/user/oracle-daemon.service`

### What Installation Does

1. Generates platform-specific service file
2. Configures auto-start on boot
3. Sets up logging to `oracle/data/.oracle_daemon.log`
4. Creates PID file at `oracle/data/.oracle_daemon.pid`

**Verification:**
```bash
python3 oracle/cli.py daemon status
```

Expected output:
```json
{
  "running": false,
  "message": "Daemon is installed but not running",
  "service_installed": true
}
```

---

## Basic Operations

### Start Daemon

**Background mode (recommended):**
```bash
python3 oracle/cli.py daemon start
```

**Foreground mode (for debugging):**
```bash
python3 oracle/cli.py daemon start --foreground
```

### Stop Daemon

```bash
python3 oracle/cli.py daemon stop
```

Sends `SIGTERM` to daemon process, allowing graceful shutdown.

### Restart Daemon

```bash
python3 oracle/cli.py daemon restart
```

Equivalent to: `stop` + `start`

### Check Status

```bash
python3 oracle/cli.py daemon status
```

Returns:
- `running`: Boolean indicating if daemon is active
- `pid`: Process ID (if running)
- `uptime`: Seconds since daemon started
- `last_update`: Timestamp of last status update
- `active_context`: Current development context

---

## Service Management

### Enable Auto-Start

```bash
python3 oracle/cli.py daemon enable
```

**macOS:** Loads service with `launchctl load`
**Linux:** Enables service with `systemctl --user enable`

### Disable Auto-Start

```bash
python3 oracle/cli.py daemon disable
```

**macOS:** Unloads service with `launchctl unload`
**Linux:** Disables service with `systemctl --user disable`

### Uninstall Service

```bash
python3 oracle/cli.py daemon uninstall
```

Removes service files and configurations. **Daemon data is preserved.**

---

## Logs and Monitoring

### View Logs

**Last 50 lines:**
```bash
python3 oracle/cli.py daemon logs
```

**Live tail (real-time):**
```bash
tail -f oracle/data/.oracle_daemon.log
```

**Search logs:**
```bash
grep "ERROR" oracle/data/.oracle_daemon.log
grep "health" oracle/data/.oracle_daemon.log
```

### Log Levels

Logs include:
- `INFO` - Normal operations (startup, health checks, file changes)
- `WARNING` - Non-critical issues (missing files, skipped checks)
- `ERROR` - Critical failures (crashes, permission errors)

### Log Rotation

Logs are automatically rotated when they exceed 10MB:
- Current log: `.oracle_daemon.log`
- Rotated logs: `.oracle_daemon.log.1`, `.oracle_daemon.log.2`, etc.

---

## Configuration

### Daemon Settings

Located in `oracle/config/oracle_config.json`:

```json
{
  "daemon": {
    "health_check_interval": 300,
    "file_watch_enabled": true,
    "auto_restart": true,
    "log_level": "INFO"
  }
}
```

**Options:**
- `health_check_interval`: Seconds between health audits (default: 300 = 5 minutes)
- `file_watch_enabled`: Enable/disable file monitoring (default: true)
- `auto_restart`: Auto-restart on crash (default: true)
- `log_level`: Logging verbosity (INFO, WARNING, ERROR)

**Apply changes:** Restart daemon after editing config.

### PID File Location

`oracle/data/.oracle_daemon.pid`

Contains the process ID of the running daemon. Used to:
- Prevent multiple daemon instances
- Send signals to daemon (stop, restart)
- Check daemon status

**Never manually edit or delete this file while daemon is running.**

---

## Advanced Usage

### Run Multiple Projects

Each project can have its own daemon instance:

```bash
# Project 1
cd /path/to/project1
python3 oracle/cli.py daemon start

# Project 2
cd /path/to/project2
python3 oracle/cli.py daemon start
```

Each daemon:
- Has its own PID file
- Writes to its own log
- Operates independently

### Custom Health Check Interval

Edit `oracle_config.json`:
```json
{
  "daemon": {
    "health_check_interval": 600
  }
}
```

Then restart:
```bash
python3 oracle/cli.py daemon restart
```

### Disable File Watching

For projects with large file counts or network drives:

```json
{
  "daemon": {
    "file_watch_enabled": false
  }
}
```

### Debug Mode

Run daemon in foreground with verbose logging:

```bash
python3 oracle/cli.py daemon start --foreground --verbose
```

Press `Ctrl+C` to stop.

---

## Troubleshooting

### Daemon Won't Start

**Symptom:** `daemon start` fails immediately

**Diagnosis:**
```bash
# Check logs for errors
python3 oracle/cli.py daemon logs

# Try foreground mode
python3 oracle/cli.py daemon start --foreground
```

**Common causes:**
- Port already in use
- Permissions issue
- Missing dependencies
- Corrupted PID file

**Solutions:**
```bash
# Check for existing daemon
python3 oracle/cli.py daemon status

# Remove stale PID file
rm oracle/data/.oracle_daemon.pid

# Check permissions
ls -la oracle/data/
```

### Daemon Crashes Repeatedly

**Symptom:** Daemon starts but stops within seconds

**Diagnosis:**
```bash
# Check recent logs
tail -50 oracle/data/.oracle_daemon.log | grep ERROR
```

**Common causes:**
- Invalid configuration
- Missing files
- Disk space full
- Memory limit reached

**Solutions:**
```bash
# Validate config
python3 oracle/cli.py init . --dry-run

# Check disk space
df -h

# Check memory
free -h  # Linux
vm_stat  # macOS
```

### Service Won't Auto-Start on Boot

**macOS:**
```bash
# Check if service is loaded
launchctl list | grep oracle

# Manually load service
launchctl load ~/Library/LaunchAgents/com.oracle.daemon.plist

# Check service file
cat ~/Library/LaunchAgents/com.oracle.daemon.plist
```

**Linux:**
```bash
# Check service status
systemctl --user status oracle-daemon

# Enable service
systemctl --user enable oracle-daemon

# Check service file
cat ~/.config/systemd/user/oracle-daemon.service
```

### High CPU Usage

**Normal:** 1-5% during health checks
**High:** >10% continuously

**Diagnosis:**
```bash
# Monitor CPU
top -pid $(cat oracle/data/.oracle_daemon.pid)
```

**Common causes:**
- Large project (>10k files)
- File watcher on network drive
- Frequent file changes

**Solutions:**
```bash
# Disable file watcher
# Edit oracle_config.json: "file_watch_enabled": false

# Increase health check interval
# Edit oracle_config.json: "health_check_interval": 900

# Restart daemon
python3 oracle/cli.py daemon restart
```

### Daemon Stops Unexpectedly

**Check logs:**
```bash
tail -100 oracle/data/.oracle_daemon.log | grep -A 5 "Stopping"
```

**Common reasons:**
- Manual stop command
- System shutdown
- Out of memory
- Unhandled exception

**If crashes persist:**
1. Enable debug logging
2. Run in foreground mode
3. Check system logs (`/var/log/system.log` on macOS, `journalctl` on Linux)

---

## Performance Optimization

### For Large Projects (>10k files)

```json
{
  "daemon": {
    "health_check_interval": 900,
    "file_watch_enabled": false
  }
}
```

### For Small Projects (<1k files)

```json
{
  "daemon": {
    "health_check_interval": 180,
    "file_watch_enabled": true
  }
}
```

### For Remote/Network Drives

```json
{
  "daemon": {
    "file_watch_enabled": false,
    "health_check_interval": 600
  }
}
```

---

## Security Considerations

### User-Level Service

Oracle daemon runs as the current user:
- **macOS:** LaunchAgent (not LaunchDaemon)
- **Linux:** systemd user service (not system service)

**Implications:**
- No root/sudo required
- Same permissions as your user account
- Stops when you log out (unless configured otherwise)

### File Permissions

Daemon writes to:
- `oracle/data/.oracle_daemon.pid` (read/write)
- `oracle/data/.oracle_daemon.log` (append)
- `oracle/data/.oracle_status.json` (read/write)

Ensure these are not world-readable if project contains sensitive info.

### Network Exposure

Daemon itself does **not** expose any network ports. It's purely local.

Web dashboard (separate process) exposes port 7777 by default. See [Dashboard Guide](DASHBOARD_GUIDE.md) for security best practices.

---

## Best Practices

### Development Workflow

1. Start daemon once per project: `oracle daemon start`
2. Let it run continuously (24/7)
3. Check status occasionally: `oracle daemon status`
4. View logs if issues occur: `oracle daemon logs`
5. Restart after config changes: `oracle daemon restart`

### Production Use

Oracle is designed for **development environments**, not production deployment:
- Don't install on production servers
- Don't expose dashboard publicly
- Keep daemon running only on dev machines

### Backup and Recovery

Daemon state is stored in:
- `oracle/data/.oracle_status.json`
- `oracle/data/.oracle_daemon.log`

**Backup strategy:**
```bash
# Include in project backups
tar -czf oracle-backup.tar.gz oracle/data/
```

**Recovery:**
```bash
# Restore data
tar -xzf oracle-backup.tar.gz

# Restart daemon
python3 oracle/cli.py daemon restart
```

---

## Command Reference

### Installation
```bash
oracle daemon install          # Install system service
oracle daemon uninstall        # Remove system service
```

### Control
```bash
oracle daemon start            # Start in background
oracle daemon start --foreground  # Start in foreground (debug)
oracle daemon stop             # Graceful shutdown
oracle daemon restart          # Stop + start
```

### Status
```bash
oracle daemon status           # Check if running
oracle daemon logs             # View recent logs
```

### Auto-Start
```bash
oracle daemon enable           # Enable auto-start on boot
oracle daemon disable          # Disable auto-start
```

---

## Integration with Other Components

### With Web Dashboard

Daemon provides data to dashboard via:
- `oracle/data/.oracle_status.json` - Daemon status
- `oracle/data/.oracle_health_status.json` - Health metrics
- `oracle/data/.oracle_daemon.log` - Activity logs

Dashboard polls these files every 2 seconds.

### With Git Hooks

Git hooks trigger daemon updates:
- Pre-commit hook → Daemon logs commit activity
- Post-commit hook → Daemon updates context

### With Terminal Dashboard (seeg)

Seeg reads the same status files as web dashboard:
- Real-time updates from daemon
- Command execution triggers daemon operations

---

## FAQ

**Q: Can I run daemon on multiple projects simultaneously?**
A: Yes, each project has its own daemon instance with separate PID/logs.

**Q: Does daemon affect git performance?**
A: No, daemon monitors via file watching, not git hooks.

**Q: What happens if I delete the PID file while daemon is running?**
A: Daemon continues running but status commands will fail. Restart daemon to fix.

**Q: Can daemon run without git?**
A: Yes, daemon works independently of git.

**Q: How much RAM does daemon use?**
A: Typically 20-50MB depending on project size.

**Q: Can I run daemon as a system service (requires root)?**
A: Not recommended. User-level service is safer and easier.

---

*Oracle v1.0 - Brain Cell Architecture*
*Autonomous Development Intelligence*
