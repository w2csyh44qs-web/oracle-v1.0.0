#!/usr/bin/env python3
"""
sEEG - Oracle Brain Cell: Real-Time Monitoring Dashboard
=========================================================

Brain Metaphor: Stereoelectroencephalography (sEEG) provides deep brain monitoring
through implanted electrodes. This module provides real-time visibility into the
project's neural activity - file changes, health status, and pipeline activity.

A unified health monitor dashboard that runs persistently in VS Code terminal,
providing real-time project health visibility and reducing mental load around
context management, autosaves, and workflow optimization.

Features:
- Real-time health score display
- Autosave tracking with configurable reminders
- Pipeline progress visualization
- File change monitoring
- Multiple display modes (full, compact, split, minimized)
- Hotkey controls for quick actions
- macOS notifications for alerts

Usage:
    python oracle/seeg.py                    # Start in full mode
    python oracle/seeg.py --mode compact     # Compact mode
    python oracle/seeg.py --mode split       # Split mode
    python oracle/seeg.py --mode min         # Minimized mode
    python oracle/seeg.py --help             # Show all options

Commands: monitor

Dependencies:
    pip install rich watchdog

Integration:
    - Runs independently of Claude Code session (zero context cost)
    - Reads shared state from oracle/reports/.health_status.json
    - Triggers oracle commands via hotkeys
"""

import os
import sys
import json
import time
import signal
import argparse
import subprocess
import select
import termios
import tty
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# Check for required dependencies
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.style import Style
    from rich import box
except ImportError:
    print("Error: 'rich' library required. Install with: pip install rich")
    sys.exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Warning: 'watchdog' library not found. File watching disabled.")
    print("Install with: pip install watchdog")

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent  # Up from oracle/ to root

# Add project root to path for imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
ORACLE_DIR = PROJECT_ROOT / "oracle"
DOCS_DIR = ORACLE_DIR / "docs"                        # V2: oracle/docs/
DOCS_OVERVIEW_DIR = DOCS_DIR / "overview"             # Desktop-synced docs
DOCS_CONTEXT_DIR = DOCS_DIR / "context"               # Session context files
DOCS_CODE_DIR = DOCS_DIR / "code only"                # Code-specific docs
CONTEXT_DIR = DOCS_CONTEXT_DIR                        # Alias for backward compatibility
REPORTS_DIR = ORACLE_DIR / "reports"                  # oracle/reports/ (consolidated)
SNAPSHOTS_DIR = REPORTS_DIR / "snapshots"
OUTPUT_DIR = PROJECT_ROOT / "content"                 # Merged output → content
LAYERS_DIR = PROJECT_ROOT / "app" / "core" / "pipeline" / "layers"  # V2 layers
CONFIG_DIR = PROJECT_ROOT / "config"
OPTIMIZATION_DIR = DOCS_OVERVIEW_DIR                  # IDEAS_BACKLOG now in oracle/docs/overview/

# Key files (updated paths after folder reorganization 2025-12-19)
DEV_CONTEXT = CONTEXT_DIR / "DEV_CONTEXT.md"
ORACLE_CONTEXT = CONTEXT_DIR / "ORACLE_CONTEXT.md"
HEALTH_STATUS_FILE = REPORTS_DIR / ".health_status.json"
OPTIMIZATION_LOG = OPTIMIZATION_DIR / "OPTIMIZATION_LOG.md"
IDEAS_BACKLOG = DOCS_OVERVIEW_DIR / "IDEAS_BACKLOG.md"
LOCK_FILE = Path("/tmp/oracle_health_monitor.lock")

# Default timing (minutes)
DEFAULT_REMINDER_INTERVAL = 20
DEFAULT_SAFETY_AUTOSAVE = 30
DEFAULT_HEALTH_INTERVAL = 5

# Default thresholds
DEFAULT_ALERT_THRESHOLD = 6.0
DEFAULT_DAILY_BUDGET = 3.00
DEFAULT_LOG_LINES = 10

# Default activity calibration (can be recalibrated based on user feedback)
# These map to 100% of each component's contribution
DEFAULT_FILE_CHANGES_MAX = 40      # 40 file changes → 100% file component
DEFAULT_HEALTH_UPDATES_MAX = 10    # 10 health updates → 100% health component
DEFAULT_CONTEXT_GROWTH_PCT = 20    # 20% context growth → 100% growth component

# =============================================================================
# CONSOLE AND STYLES
# =============================================================================

console = Console()

# Custom styles
STYLE_HEADER = Style(color="cyan", bold=True)
STYLE_OK = Style(color="green")
STYLE_WARNING = Style(color="yellow")
STYLE_CRITICAL = Style(color="red", bold=True)
STYLE_DIM = Style(color="bright_black")
STYLE_HIGHLIGHT = Style(color="white", bold=True)

# Watched file extensions
WATCHED_EXTENSIONS = {'.py', '.md', '.json'}

# Folders to watch
WATCHED_FOLDERS = ['context', 'scripts', 'config', 'docs', 'reports', 'optimization']


# =============================================================================
# KEYBOARD INPUT HANDLER
# =============================================================================

class KeyboardReader:
    """Non-blocking keyboard input reader for Unix terminals."""

    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None
        self.active = False

    def start(self):
        """Put terminal in raw mode for character-by-character input."""
        try:
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
            self.active = True
        except termios.error:
            # Not a TTY (e.g., running in non-interactive mode)
            self.active = False

    def stop(self):
        """Restore terminal settings."""
        if self.old_settings is not None:
            try:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            except termios.error:
                pass
        self.active = False

    def read_key(self, timeout: float = 0.1) -> Optional[str]:
        """Read a single keypress with timeout. Returns None if no key pressed."""
        if not self.active:
            return None

        try:
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                return sys.stdin.read(1)
        except Exception:
            pass
        return None


# =============================================================================
# FILE WATCHER CLASS
# =============================================================================

class HealthMonitorEventHandler(FileSystemEventHandler if WATCHDOG_AVAILABLE else object):
    """Handle file system events for the health monitor."""

    def __init__(self, monitor: 'OracleHealthMonitor'):
        if WATCHDOG_AVAILABLE:
            super().__init__()
        self.monitor = monitor
        self.last_event_time = {}
        self.debounce_seconds = 1.0  # Ignore repeated events within 1 second

    def _should_process(self, path: str) -> bool:
        """Check if we should process this file event."""
        # Check extension
        ext = Path(path).suffix.lower()
        if ext not in WATCHED_EXTENSIONS:
            return False

        # Debounce - ignore rapid repeated events for same file
        now = time.time()
        if path in self.last_event_time:
            if now - self.last_event_time[path] < self.debounce_seconds:
                return False

        self.last_event_time[path] = now
        return True

    def _get_relative_path(self, path: str) -> str:
        """Get path relative to project root."""
        try:
            return str(Path(path).relative_to(PROJECT_ROOT))
        except ValueError:
            return Path(path).name

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        path = event.src_path
        if not self._should_process(path):
            return

        rel_path = self._get_relative_path(path)
        self.monitor._on_file_changed(rel_path, "modified")

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        path = event.src_path
        if not self._should_process(path):
            return

        rel_path = self._get_relative_path(path)
        self.monitor._on_file_changed(rel_path, "created")


class FileWatcher:
    """Manage file system watching with watchdog."""

    def __init__(self, monitor: 'OracleHealthMonitor'):
        self.monitor = monitor
        self.observer: Optional[Observer] = None
        self.running = False

    def start(self):
        """Start watching folders."""
        if not WATCHDOG_AVAILABLE:
            return

        self.observer = Observer()
        handler = HealthMonitorEventHandler(self.monitor)

        # Watch each folder
        for folder in WATCHED_FOLDERS:
            folder_path = PROJECT_ROOT / folder
            if folder_path.exists():
                self.observer.schedule(handler, str(folder_path), recursive=True)

        self.observer.start()
        self.running = True

    def stop(self):
        """Stop watching folders."""
        if self.observer and self.running:
            self.observer.stop()
            self.observer.join(timeout=2)
            self.running = False


# =============================================================================
# HEALTH MONITOR CLASS
# =============================================================================

class OracleHealthMonitor:
    """Persistent health monitoring dashboard for Oracle-managed projects."""

    def __init__(
        self,
        mode: str = "full",
        safety_autosave: int = DEFAULT_SAFETY_AUTOSAVE,
        health_interval: int = DEFAULT_HEALTH_INTERVAL,
        reminder_interval: int = DEFAULT_REMINDER_INTERVAL,
        budget: float = DEFAULT_DAILY_BUDGET,
        alert_threshold: float = DEFAULT_ALERT_THRESHOLD,
        log_lines: int = DEFAULT_LOG_LINES,
        notifications: bool = True,
        color: bool = True,
    ):
        self.mode = mode
        self.safety_autosave = safety_autosave
        self.health_interval = health_interval
        self.reminder_interval = reminder_interval
        self.budget = budget
        self.alert_threshold = alert_threshold
        self.log_lines = log_lines
        self.notifications = notifications
        self.color = color

        # State
        self.running = True
        self.session_start = datetime.now()
        self.last_autosave = self._get_last_autosave_time()
        self.last_health_check = None
        self.health_data: Dict[str, Any] = {}
        self.file_changes = 0
        self.autosave_count = 0
        self.log_entries: List[str] = []
        self.recent_file_changes: List[str] = []  # Track recent file changes for display

        # Session activity tracking (for context usage estimation)
        self.health_status_updates = 0  # Proxy for oracle command runs / exchanges
        self.context_size_baseline = self._get_context_file_sizes()  # Track context growth

        # Activity calibration (loaded from config, can be recalibrated)
        self._load_calibration()

        # File watcher
        self.file_watcher: Optional[FileWatcher] = None

        # Keyboard reader
        self.keyboard: Optional[KeyboardReader] = None

        # Alert tracking
        self.last_reminder_time: Optional[datetime] = None
        self.reminder_count = 0

        # Session type override (None = auto-detect, or "Development"/"Maintenance")
        self.session_type_override: Optional[str] = None

        # Calibration input mode
        self.calibration_mode = False
        self.calibration_input = ""  # Accumulated digits during calibration

        # Command palette mode (P31 Phase 3)
        self.command_mode = False
        self.command_input = ""
        self.command_history: List[str] = []
        self.command_history_index = -1
        self.command_output: List[str] = []
        self.max_command_output = 10  # Keep last 10 lines of command output

        # Debug panel toggle (shows internal state)
        self.show_debug = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")

        # Set up signal handlers
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

        # Initial log entry
        self._log("Session started")

    # =========================================================================
    # LIFECYCLE
    # =========================================================================

    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        self.running = False

    def _check_lock_file(self) -> bool:
        """Check if another instance is running."""
        if not LOCK_FILE.exists():
            return False

        try:
            pid = int(LOCK_FILE.read_text().strip())
            # Check if process is still running
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            # Stale lock file or process not running
            LOCK_FILE.unlink(missing_ok=True)
            return False

    def _create_lock_file(self):
        """Create lock file with current PID."""
        LOCK_FILE.write_text(str(os.getpid()))

    def _remove_lock_file(self):
        """Remove lock file."""
        LOCK_FILE.unlink(missing_ok=True)

    def _log(self, message: str):
        """Add entry to log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log_entries.append(entry)
        # Keep only recent entries
        max_entries = max(self.log_lines * 2, 20)
        if len(self.log_entries) > max_entries:
            self.log_entries = self.log_entries[-max_entries:]

    def _notify(self, title: str, message: str):
        """Send macOS notification."""
        if not self.notifications:
            return
        try:
            subprocess.run(
                ['osascript', '-e', f'display notification "{message}" with title "{title}"'],
                capture_output=True,
                timeout=5
            )
        except Exception:
            pass

    def _bell(self):
        """Sound terminal bell."""
        print('\a', end='', flush=True)

    def _on_file_changed(self, path: str, event_type: str):
        """Handle file change events from watchdog."""
        self.file_changes += 1

        # Track recent changes (keep last 10)
        self.recent_file_changes.append(path)
        if len(self.recent_file_changes) > 10:
            self.recent_file_changes = self.recent_file_changes[-10:]

        # Log the change
        self._log(f"File {event_type}: {path}")

        # Special handling for health status file (proxy for oracle commands / exchanges)
        if '.health_status.json' in path:
            self.health_status_updates += 1
            self._log("Health data updated")

        # Special handling for baseline reset (new session after compaction)
        if 'SESSION_SNAPSHOT_latest.json' in path and event_type == 'modified':
            self._log("New session detected (baseline reset)")
            self._reset_activity_counters()

        # Special handling for snapshots (autosave detected)
        if 'SNAPSHOT_' in path and path.endswith('.md') and event_type == 'created':
            self.last_autosave = datetime.now()
            self.autosave_count += 1
            activity = self._get_session_activity()
            self._log(f"Autosave #{self.autosave_count} (activity: {activity['percent']}%)")
            self._log("💡 Good time to compact if context is high")
            # Note: Don't reset activity counters on autosave - only on new session
            # This allows calibration at end of session to carry over correctly

    def _reset_activity_counters(self):
        """Reset activity counters on new session detection only."""
        self.file_changes = 0
        self.health_status_updates = 0
        self.context_size_baseline = self._get_context_file_sizes()

    def _start_file_watcher(self):
        """Start the file watcher."""
        if WATCHDOG_AVAILABLE:
            self.file_watcher = FileWatcher(self)
            self.file_watcher.start()
            self._log(f"File watching started ({len(WATCHED_FOLDERS)} folders)")

    def _stop_file_watcher(self):
        """Stop the file watcher."""
        if self.file_watcher:
            self.file_watcher.stop()
            self._log("File watching stopped")

    # =========================================================================
    # DATA GATHERING
    # =========================================================================

    def _get_last_autosave_time(self) -> datetime:
        """Find most recent autosave/snapshot timestamp."""
        latest = None

        # Check snapshot files
        if SNAPSHOTS_DIR.exists():
            for snapshot in SNAPSHOTS_DIR.glob("SNAPSHOT_*.md"):
                try:
                    mtime = datetime.fromtimestamp(snapshot.stat().st_mtime)
                    if latest is None or mtime > latest:
                        latest = mtime
                except Exception:
                    pass

        # Check context file modification times as fallback
        for ctx_file in [DEV_CONTEXT, ORACLE_CONTEXT]:
            if ctx_file.exists():
                try:
                    mtime = datetime.fromtimestamp(ctx_file.stat().st_mtime)
                    if latest is None or mtime > latest:
                        latest = mtime
                except Exception:
                    pass

        return latest or self.session_start

    def _get_autosave_status(self) -> Dict[str, Any]:
        """Get autosave timing information."""
        now = datetime.now()
        age = now - self.last_autosave
        age_minutes = int(age.total_seconds() / 60)

        reminder_in = max(0, self.reminder_interval - age_minutes)
        safety_in = max(0, self.safety_autosave - age_minutes)

        if age_minutes < self.reminder_interval:
            status = "ok"
        elif age_minutes < self.safety_autosave:
            status = "reminder"
        else:
            status = "overdue"

        return {
            "last_minutes": age_minutes,
            "reminder_in": reminder_in,
            "safety_in": safety_in,
            "status": status,
        }

    def _get_context_file_sizes(self) -> Dict[str, int]:
        """Get current context file sizes in bytes."""
        sizes = {}
        for ctx_file in [DEV_CONTEXT, ORACLE_CONTEXT]:
            if ctx_file.exists():
                try:
                    sizes[str(ctx_file)] = ctx_file.stat().st_size
                except Exception:
                    sizes[str(ctx_file)] = 0
            else:
                sizes[str(ctx_file)] = 0
        return sizes

    def _get_session_activity(self) -> Dict[str, Any]:
        """Calculate composite session activity score as proxy for context usage.

        Combines multiple trackable factors:
        - File changes (high weight) - each file change likely means tool calls
        - Health status updates (medium weight) - proxy for oracle commands / exchanges
        - Context file growth (low weight) - larger context = more tokens on resume

        Uses calibrated thresholds that can be adjusted based on user feedback.

        Returns a dict with:
        - percent: 0-100 activity percentage
        - level: qualitative level (Low/Medium/High/Critical)
        - display: formatted display string
        - breakdown: individual component values for debugging
        """
        # Component 1: File changes (high weight - 50%)
        # Uses calibrated file_changes_max threshold
        file_change_score = min(100, (self.file_changes / self.file_changes_max) * 100)

        # Component 2: Health status updates (medium weight - 30%)
        # Uses calibrated health_updates_max threshold
        health_update_score = min(100, (self.health_status_updates / self.health_updates_max) * 100)

        # Component 3: Context file growth (low weight - 20%)
        # Compare current size to baseline, uses calibrated context_growth_max
        current_sizes = self._get_context_file_sizes()
        total_baseline = sum(self.context_size_baseline.values())
        total_current = sum(current_sizes.values())
        if total_baseline > 0:
            growth_ratio = (total_current - total_baseline) / total_baseline * 100  # as percentage
            # Normalize: 0-context_growth_max% growth maps to 0-100% of this component
            context_growth_score = min(100, max(0, (growth_ratio / self.context_growth_max) * 100))
        else:
            context_growth_score = 0

        # Weighted composite score
        composite = (
            file_change_score * 0.50 +
            health_update_score * 0.30 +
            context_growth_score * 0.20
        )
        percent = int(min(100, max(0, composite)))

        # Determine level based on percentage
        if percent < 33:
            level = "Low"
        elif percent < 66:
            level = "Medium"
        elif percent < 90:
            level = "High"
        else:
            level = "Critical"

        return {
            "percent": percent,
            "level": level,
            "display": f"{level} ({percent}%)",
            "breakdown": {
                "file_changes": self.file_changes,
                "health_updates": self.health_status_updates,
                "context_growth_pct": int(context_growth_score),
            }
        }

    def _read_health_status(self) -> Dict[str, Any]:
        """Read health status from shared state file."""
        if HEALTH_STATUS_FILE.exists():
            try:
                with open(HEALTH_STATUS_FILE) as f:
                    return json.load(f)
            except Exception:
                pass

        # Return defaults if file not found
        return {
            "health_score": 0.0,
            "issues": {"critical": 0, "warnings": 0},
            "optimizations_pending": 0,
            "cost_today": 0.0,
        }

    def _detect_session_type(self) -> str:
        """Detect session type.

        If user has manually set session type via hotkey (d/t), use that override.
        Otherwise, auto-detect based on context file modification times.
        """
        # Check for manual override first
        if self.session_type_override is not None:
            return self.session_type_override

        # Auto-detect using os.stat() directly to avoid potential caching issues
        try:
            import os
            dev_mtime = os.stat(str(DEV_CONTEXT)).st_mtime if DEV_CONTEXT.exists() else 0
            oracle_mtime = os.stat(str(ORACLE_CONTEXT)).st_mtime if ORACLE_CONTEXT.exists() else 0
            return "Maintenance" if oracle_mtime > dev_mtime else "Development"
        except Exception:
            return "Unknown"

    def _toggle_session_type(self):
        """Toggle session type between Development and Maintenance."""
        current = self._detect_session_type()
        if current == "Development":
            self.session_type_override = "Maintenance"
            self._log("Session type: Maintenance (manual)")
        else:
            self.session_type_override = "Development"
            self._log("Session type: Development (manual)")

    def _set_session_type(self, session_type: str):
        """Set session type manually."""
        self.session_type_override = session_type
        self._log(f"Session type: {session_type} (manual)")

    def _clear_session_override(self):
        """Clear manual session type override, return to auto-detect."""
        self.session_type_override = None
        detected = self._detect_session_type()
        self._log(f"Session type: {detected} (auto)")

    def _toggle_debug(self):
        """Toggle debug panel visibility."""
        self.show_debug = not self.show_debug
        status = "ON" if self.show_debug else "OFF"
        self._log(f"Debug panel: {status}")
        # Also set env var for consistency
        if self.show_debug:
            os.environ["ORACLE_DEBUG"] = "1"
        else:
            os.environ.pop("ORACLE_DEBUG", None)

    def _get_debug_info(self) -> Dict[str, Any]:
        """Get internal state for debug panel."""
        return {
            "mode": self.mode,
            "running": self.running,
            "session_start": self.session_start.isoformat(),
            "last_autosave": self.last_autosave.isoformat() if self.last_autosave else None,
            "file_changes": self.file_changes,
            "autosave_count": self.autosave_count,
            "log_entries_count": len(self.log_entries),
            "recent_file_changes": len(self.recent_file_changes),
            "health_status_updates": self.health_status_updates,
            "reminder_count": self.reminder_count,
            "calibration_mode": self.calibration_mode,
            "session_type_override": self.session_type_override,
            "file_changes_max": self.file_changes_max,
            "health_updates_max": self.health_updates_max,
            "context_growth_max": self.context_growth_max,
            "calibration_points": len(self.calibration_points),
            "notifications": self.notifications,
            "ORACLE_DEBUG": os.environ.get("ORACLE_DEBUG", "not set"),
        }

    def _load_calibration(self):
        """Load activity calibration from config."""
        config = load_config()
        calibration = config.get("activity_calibration", {})
        self.file_changes_max = calibration.get("file_changes_max", DEFAULT_FILE_CHANGES_MAX)
        self.health_updates_max = calibration.get("health_updates_max", DEFAULT_HEALTH_UPDATES_MAX)
        self.context_growth_max = calibration.get("context_growth_pct", DEFAULT_CONTEXT_GROWTH_PCT)
        # Track calibration data points for averaging
        self.calibration_points = calibration.get("data_points", [])

    def _save_calibration(self):
        """Save activity calibration to config."""
        config = load_config()
        config["activity_calibration"] = {
            "file_changes_max": self.file_changes_max,
            "health_updates_max": self.health_updates_max,
            "context_growth_pct": self.context_growth_max,
            "data_points": self.calibration_points[-10:],  # Keep last 10 data points
        }
        save_config(config)

    def _record_calibration_point(self, context_percent: int):
        """Record a calibration data point and recalibrate thresholds.

        Called when user reports their current Claude context percentage.
        Uses this to adjust thresholds so activity % better matches context %.
        """
        current_activity = self._get_session_activity()
        data_point = {
            "context_pct": context_percent,
            "activity_pct": current_activity["percent"],
            "file_changes": self.file_changes,
            "health_updates": self.health_status_updates,
            "timestamp": datetime.now().isoformat(),
        }
        self.calibration_points.append(data_point)
        # Keep only last 10 data points in memory
        if len(self.calibration_points) > 10:
            self.calibration_points = self.calibration_points[-10:]

        # Recalibrate based on this point
        # If context is 58% but activity shows 30%, we're underestimating
        # Adjust thresholds so current values would produce context_percent
        if current_activity["percent"] > 0 and context_percent > 0:
            # Scale factor: how much to adjust thresholds
            # If context=58, activity=30, factor=30/58=0.52 (thresholds too high)
            # New thresholds = old * factor
            factor = current_activity["percent"] / context_percent

            # Apply factor to thresholds (lower threshold = higher sensitivity)
            self.file_changes_max = max(5, int(self.file_changes_max * factor))
            self.health_updates_max = max(2, int(self.health_updates_max * factor))
            self.context_growth_max = max(5, int(self.context_growth_max * factor))

            self._save_calibration()
            self._log(f"Calibrated: fc={self.file_changes_max}, hu={self.health_updates_max}, cg={self.context_growth_max}%")
        else:
            self._log("Calibration skipped (no activity data)")

    def _start_calibration(self):
        """Start calibration mode - user types digits, Enter to confirm, Esc to cancel."""
        activity = self._get_session_activity()
        self._log("─── CALIBRATION MODE ───")
        self._log(f"Current activity: {activity['percent']}%")
        self._log(f"  Files: {self.file_changes} | Health updates: {self.health_status_updates}")
        self._log("Enter your Claude context % (1-100):")
        self.calibration_mode = True
        self.calibration_input = ""

    def _handle_calibration_input(self, key: str):
        """Handle keypress while in calibration mode."""
        if key == '\x1b':  # Escape
            self._log("Calibration cancelled")
            self.calibration_mode = False
            self.calibration_input = ""
        elif key == '\r' or key == '\n':  # Enter
            if self.calibration_input:
                try:
                    context_pct = int(self.calibration_input)
                    if 1 <= context_pct <= 100:
                        self._record_calibration_point(context_pct)
                        self._log(f"Recorded: context={context_pct}%")
                    else:
                        self._log("Invalid: must be 1-100")
                except ValueError:
                    self._log("Invalid number")
            else:
                self._log("Calibration cancelled (empty input)")
            self.calibration_mode = False
            self.calibration_input = ""
        elif key == '\x7f' or key == '\b':  # Backspace
            if self.calibration_input:
                self.calibration_input = self.calibration_input[:-1]
                # Don't log each backspace - footer shows live input
        elif key.isdigit():
            if len(self.calibration_input) < 3:  # Max 3 digits (100)
                self.calibration_input += key
                # Don't log each digit - footer shows live input

    def _handle_command_input(self, key: str):
        """
        Handle keypress while in command mode (P31 Phase 3).

        Supports:
        - Escape: Cancel command mode
        - Enter: Execute command
        - Backspace: Delete character
        - Up/Down arrows: Navigate command history
        - Any printable character: Add to command input
        """
        if key == '\x1b':  # Escape
            self._log("Command mode cancelled")
            self.command_mode = False
            self.command_input = ""
            self.command_history_index = -1

        elif key == '\r' or key == '\n':  # Enter
            if self.command_input.strip():
                command = self.command_input.strip()
                self._log(f"oracle> {command}")

                # Add to history
                self.command_history.append(command)
                self.command_history_index = len(self.command_history)

                # Execute command
                self._execute_oracle_command(command)
            else:
                self._log("Command mode cancelled (empty input)")

            self.command_mode = False
            self.command_input = ""

        elif key == '\x7f' or key == '\b':  # Backspace
            if self.command_input:
                self.command_input = self.command_input[:-1]

        elif key == '\x1b[A':  # Up arrow (ANSI escape sequence)
            # Previous command in history
            if self.command_history_index > 0:
                self.command_history_index -= 1
                self.command_input = self.command_history[self.command_history_index]

        elif key == '\x1b[B':  # Down arrow
            # Next command in history
            if self.command_history_index < len(self.command_history) - 1:
                self.command_history_index += 1
                self.command_input = self.command_history[self.command_history_index]
            else:
                self.command_history_index = len(self.command_history)
                self.command_input = ""

        elif key.isprintable() and len(self.command_input) < 100:
            # Add printable characters to input
            self.command_input += key

    def _execute_oracle_command(self, command: str):
        """
        Execute an Oracle command and display output.

        Supported commands:
        - Built-in: help, clear
        - Oracle commands: audit, status, verify, clean, optimize, sync, etc.
        """
        # Handle built-in commands
        if command == "help":
            self._show_command_help()
            return

        if command == "clear":
            self.command_output = []
            self._log("Command output cleared")
            return

        # Execute Oracle command via project_oracle.py
        try:
            # Parse command into args
            args = command.split()
            if not args:
                return

            # Build command
            oracle_cmd = [
                sys.executable,
                str(ORACLE_DIR / "project_oracle.py")
            ] + args

            self._log(f"Executing: {' '.join(args)}")

            # Execute with timeout
            result = subprocess.run(
                oracle_cmd,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Display output
            if result.stdout:
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines[:self.max_command_output]:
                    self._log(f"  {line}")
                    self.command_output.append(line)

                # Keep command output limited
                if len(self.command_output) > self.max_command_output:
                    self.command_output = self.command_output[-self.max_command_output:]

            if result.returncode == 0:
                self._log("✓ Command completed")
            else:
                self._log(f"✗ Command failed (exit code: {result.returncode})")
                if result.stderr:
                    error_lines = result.stderr.strip().split('\n')
                    for line in error_lines[:3]:  # Show first 3 error lines
                        self._log(f"  Error: {line}")

        except subprocess.TimeoutExpired:
            self._log("✗ Command timeout (>30s)")

        except FileNotFoundError:
            self._log("✗ project_oracle.py not found")

        except Exception as e:
            self._log(f"✗ Command error: {e}")

    def _show_command_help(self):
        """Show available commands in command palette."""
        self._log("━━━ COMMAND PALETTE HELP ━━━")
        self._log("Oracle Commands:")
        self._log("  audit          - Run health audit")
        self._log("  audit --quick  - Quick health check")
        self._log("  status         - Show Oracle status")
        self._log("  verify         - Run integrity check")
        self._log("  clean          - Clean reports")
        self._log("  optimize       - Run optimizations")
        self._log("  sync           - Sync contexts")
        self._log("")
        self._log("Built-in:")
        self._log("  help           - Show this help")
        self._log("  clear          - Clear command output")
        self._log("")
        self._log("Press ':' to enter command mode")
        self._log("Press Esc to cancel command")
        self._log("Use ↑/↓ arrows for history")

    def _get_brain_cell_status(self) -> Dict[str, Any]:
        """Check status of each brain cell module + daemon.

        Returns dict with status of each brain cell module and the daemon.
        """
        cells = {
            "microglia": {"status": "unknown", "path": "maintenance/microglia.py"},
            "astrocytes": {"status": "unknown", "path": "context/astrocytes.py"},
            "oligodendrocytes": {"status": "unknown", "path": "optimization/oligodendrocytes.py"},
            "ependymal": {"status": "unknown", "path": "sync/ependymal.py"},
            "cortex": {"status": "unknown", "path": "project/cortex.py"},
            "daemon": {"status": "unknown", "path": "context/daemon.py"},
        }

        # Check each module can be imported
        for cell_name, info in cells.items():
            module_path = ORACLE_DIR / info["path"]
            if module_path.exists():
                try:
                    # Try to import the module
                    if cell_name == "microglia":
                        from oracle.maintenance import microglia
                        cells[cell_name]["status"] = "ready"
                    elif cell_name == "astrocytes":
                        from oracle.context import astrocytes
                        cells[cell_name]["status"] = "ready"
                    elif cell_name == "oligodendrocytes":
                        from oracle.optimization import oligodendrocytes
                        cells[cell_name]["status"] = "ready"
                    elif cell_name == "ependymal":
                        from oracle.sync import ependymal
                        cells[cell_name]["status"] = "ready"
                    elif cell_name == "cortex":
                        from oracle.project import cortex
                        cells[cell_name]["status"] = "ready"
                    elif cell_name == "daemon":
                        from oracle.context import daemon
                        cells[cell_name]["status"] = "ready"
                except ImportError as e:
                    cells[cell_name]["status"] = "error"
                    cells[cell_name]["error"] = str(e)
            else:
                cells[cell_name]["status"] = "missing"

        # Check if daemon is actually running (lock file)
        daemon_lock = Path("/tmp/oracle_daemon.lock")
        if daemon_lock.exists():
            try:
                pid = int(daemon_lock.read_text().strip())
                os.kill(pid, 0)  # Check if process exists
                cells["daemon"]["status"] = "running"
            except (ValueError, OSError):
                # Stale lock or process not running
                pass

        # Count ready cells
        ready_count = sum(1 for c in cells.values() if c["status"] in ["ready", "running"])
        total_count = len(cells)

        return {
            "cells": cells,
            "ready": ready_count,
            "total": total_count,
            "healthy": ready_count >= total_count - 1,  # Allow one cell to be down
        }

    def _get_api_status(self) -> Dict[str, Any]:
        """Get API connection + usage status.

        Calls get_connection_health() from oligodendrocytes and adds usage data.
        """
        result = {
            "apis": {},
            "overall_status": "unknown",
            "total_cost": 0.0,
            "total_calls": 0,
        }

        try:
            from oracle.optimization.oligodendrocytes import get_connection_health
            health = get_connection_health()
            result["apis"] = health.get("apis", {})
            result["overall_status"] = health.get("overall_status", "unknown")
        except ImportError:
            # Fallback if module not available
            pass

        # Add usage data from api_calls.json
        api_calls_file = REPORTS_DIR / "api_calls.json"
        if api_calls_file.exists():
            try:
                with open(api_calls_file) as f:
                    calls = json.load(f)

                # Sum up costs and calls per provider
                provider_usage = {}
                for call in calls:
                    provider = call.get("provider", "unknown")
                    cost = call.get("cost_usd", 0)

                    if provider not in provider_usage:
                        provider_usage[provider] = {"cost": 0.0, "calls": 0}
                    provider_usage[provider]["cost"] += cost
                    provider_usage[provider]["calls"] += 1
                    result["total_cost"] += cost
                    result["total_calls"] += 1

                # Merge usage into api status
                for provider, usage in provider_usage.items():
                    if provider in result["apis"]:
                        result["apis"][provider]["cost"] = usage["cost"]
                        result["apis"][provider]["calls"] = usage["calls"]
                    else:
                        result["apis"][provider] = {
                            "status": "configured",
                            "cost": usage["cost"],
                            "calls": usage["calls"],
                        }
            except Exception:
                pass

        return result

    def _get_context_status(self) -> Dict[str, Any]:
        """Get context file ages and cross-session flags.

        Returns DEV_CONTEXT age, ORACLE_CONTEXT age, session numbers,
        and any cross-session flags.
        """
        import re

        result = {
            "dev_context": {"age_str": "?", "session": "?"},
            "oracle_context": {"age_str": "?", "session": "?"},
            "cross_session_flags": [],
        }

        now = datetime.now()

        # Check DEV_CONTEXT
        if DEV_CONTEXT.exists():
            try:
                mtime = datetime.fromtimestamp(DEV_CONTEXT.stat().st_mtime)
                age = now - mtime
                age_minutes = int(age.total_seconds() / 60)
                age_hours = int(age.total_seconds() / 3600)

                if age_hours > 0:
                    result["dev_context"]["age_str"] = f"{age_hours}h ago"
                else:
                    result["dev_context"]["age_str"] = f"{age_minutes}m ago"

                # Parse session number
                content = DEV_CONTEXT.read_text()
                session_match = re.search(r'D(\d+)', content)
                if session_match:
                    result["dev_context"]["session"] = f"D{session_match.group(1)}"
            except Exception:
                pass

        # Check ORACLE_CONTEXT
        if ORACLE_CONTEXT.exists():
            try:
                mtime = datetime.fromtimestamp(ORACLE_CONTEXT.stat().st_mtime)
                age = now - mtime
                age_minutes = int(age.total_seconds() / 60)
                age_hours = int(age.total_seconds() / 3600)

                if age_hours > 0:
                    result["oracle_context"]["age_str"] = f"{age_hours}h ago"
                else:
                    result["oracle_context"]["age_str"] = f"{age_minutes}m ago"

                # Parse session number and cross-session flags
                content = ORACLE_CONTEXT.read_text()
                session_match = re.search(r'O(\d+)', content)
                if session_match:
                    result["oracle_context"]["session"] = f"O{session_match.group(1)}"

                # Check for cross-session flags
                if "NEEDS_ORACLE_PASS" in content:
                    result["cross_session_flags"].append("NEEDS_ORACLE_PASS")
                if "NEEDS_DEV_ATTENTION" in content:
                    result["cross_session_flags"].append("NEEDS_DEV_ATTENTION")
                if "PAUSED_MID_TASK" in content:
                    result["cross_session_flags"].append("PAUSED_MID_TASK")
            except Exception:
                pass

        return result

    def _get_doc_staleness(self) -> Dict[str, Dict[str, Any]]:
        """Check documentation staleness."""
        # Updated paths after folder reorganization (2025-12-19)
        docs = {
            "DEV_CONTEXT": DEV_CONTEXT,
            "ORACLE_CONTEXT": ORACLE_CONTEXT,
            "ARCHITECTURE": DOCS_OVERVIEW_DIR / "ARCHITECTURE.md",
            "WORKFLOW": DOCS_OVERVIEW_DIR / "WORKFLOW.md",
            "CODE_HISTORY": DOCS_OVERVIEW_DIR / "CODE_HISTORY.md",
            "CHANGELOG": DOCS_CODE_DIR / "CHANGELOG.md",
        }

        now = datetime.now()
        result = {}

        for name, path in docs.items():
            if path.exists():
                try:
                    mtime = datetime.fromtimestamp(path.stat().st_mtime)
                    age = now - mtime
                    age_days = age.days
                    age_hours = int(age.total_seconds() / 3600)
                    age_minutes = int(age.total_seconds() / 60)

                    if age_days > 0:
                        age_str = f"{age_days}d ago"
                    elif age_hours > 0:
                        age_str = f"{age_hours}h ago"
                    else:
                        age_str = f"{age_minutes}m ago"

                    result[name] = {
                        "age_str": age_str,
                        "stale": age_days > 7,
                    }
                except Exception:
                    result[name] = {"age_str": "?", "stale": False}
            else:
                result[name] = {"age_str": "missing", "stale": True}

        return result

    def _get_pipeline_status(self) -> Dict[str, Any]:
        """Get pipeline layer status based on most recently modified outputs."""
        layers = {
            "L1": {"status": "not_started", "label": "Trends", "mtime": 0},
            "L2": {"status": "not_started", "label": "Calendar", "mtime": 0},
            "L3": {"status": "not_started", "label": "Ideas", "mtime": 0},
            "L4": {"status": "not_started", "label": "Audio", "mtime": 0},
            "L5": {"status": "not_started", "label": "Media", "mtime": 0},
            "L6": {"status": "not_started", "label": "Assembly", "mtime": 0},
            "L7": {"status": "not_started", "label": "Distribution", "mtime": 0},
            "L8": {"status": "not_started", "label": "Analytics", "mtime": 0},
        }

        # Check L1 in output/ (all_trends.json)
        trends_file = OUTPUT_DIR / "all_trends.json"
        if trends_file.exists():
            layers["L1"]["status"] = "complete"
            layers["L1"]["mtime"] = trends_file.stat().st_mtime

        # Find most recent content week folder (content/nfl/{season}/phase/week#/)
        content_base = None
        content_dir = PROJECT_ROOT / "content"
        if content_dir.exists():
            week_folders = list(content_dir.glob("**/week*"))
            if week_folders:
                week_folders.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                content_base = week_folders[0]

        if content_base is None:
            content_base = OUTPUT_DIR

        # Check each layer's output and track mtime
        segments_file = content_base / "segments_config.json"
        if segments_file.exists():
            layers["L2"]["status"] = "complete"
            layers["L2"]["mtime"] = segments_file.stat().st_mtime

        ideas_file = content_base / "ideas_approved.json"
        if ideas_file.exists():
            layers["L3"]["status"] = "complete"
            layers["L3"]["mtime"] = ideas_file.stat().st_mtime
            try:
                with open(ideas_file) as f:
                    ideas = json.load(f)
                    layers["L3"]["count"] = len(ideas)
            except Exception:
                pass

        audio_dir = content_base / "audio"
        if audio_dir.exists():
            audio_files = list(audio_dir.glob("*.mp3"))
            if audio_files:
                layers["L4"]["status"] = "complete"
                layers["L4"]["count"] = len(audio_files)
                layers["L4"]["mtime"] = max(f.stat().st_mtime for f in audio_files)

        media_dir = content_base / "media"
        if media_dir.exists():
            media_folders = [d for d in media_dir.iterdir() if d.is_dir()]
            if media_folders:
                layers["L5"]["status"] = "complete"
                layers["L5"]["count"] = len(media_folders)
                layers["L5"]["mtime"] = max(d.stat().st_mtime for d in media_folders)

        assembled_dir = content_base / "assembled"
        if assembled_dir.exists():
            assembled_files = list(assembled_dir.glob("*.mp4")) + list(assembled_dir.glob("*.jpg")) + list(assembled_dir.glob("*.png"))
            if assembled_files:
                layers["L6"]["status"] = "complete"
                layers["L6"]["count"] = len(assembled_files)
                layers["L6"]["mtime"] = max(f.stat().st_mtime for f in assembled_files)

        final_dir = content_base / "final"
        if final_dir.exists():
            final_files = []
            for subdir in final_dir.iterdir():
                if subdir.is_dir():
                    final_files.extend(subdir.glob("*.mp4"))
                    final_files.extend(subdir.glob("*.jpg"))
                    final_files.extend(subdir.glob("*.png"))
            if final_files:
                layers["L7"]["status"] = "complete"
                layers["L7"]["count"] = len(final_files)
                layers["L7"]["mtime"] = max(f.stat().st_mtime for f in final_files)

        # Find the most recently modified layer and mark it as "active"
        active_layer = None
        max_mtime = 0
        for layer, info in layers.items():
            if info["mtime"] > max_mtime:
                max_mtime = info["mtime"]
                active_layer = layer

        if active_layer:
            layers[active_layer]["active"] = True

        return layers

    def _get_optimization_count(self) -> Dict[str, int]:
        """Count optimization items."""
        result = {"pending": 0, "backlog": 0}

        if OPTIMIZATION_LOG.exists():
            try:
                content = OPTIMIZATION_LOG.read_text()
                result["pending"] = content.count("[UNREVIEWED]")
            except Exception:
                pass

        if IDEAS_BACKLOG.exists():
            try:
                content = IDEAS_BACKLOG.read_text()
                # Count items in YES and MAYBE sections
                result["backlog"] = content.count("- ") // 2  # Rough estimate
            except Exception:
                pass

        return result

    def _get_session_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Parse pending tasks from both context files.

        Returns dict with 'dev' and 'oracle' keys, each containing:
        - session: current session number (e.g., "D43")
        - tasks: list of task dicts with 'text' and 'status' keys
        """
        import re

        result = {
            "dev": {"session": "?", "tasks": []},
            "oracle": {"session": "?", "tasks": []}
        }

        # Parse DEV_CONTEXT.md
        if DEV_CONTEXT.exists():
            try:
                content = DEV_CONTEXT.read_text()

                # Get session number from header (format: "D43 (Dev)")
                session_match = re.search(r'D(\d+)\s*\(Dev\)', content)
                if session_match:
                    result["dev"]["session"] = f"D{session_match.group(1)}"

                # Find Pending Tasks section
                pending_section = re.search(
                    r'###?\s*Pending Tasks.*?\n(.*?)(?=\n###|\n##|\Z)',
                    content,
                    re.DOTALL | re.IGNORECASE
                )
                if pending_section:
                    section_text = pending_section.group(1)

                    # Parse checkbox format: - [ ] Task or - [x] Task
                    task_num = 0
                    for line in section_text.split('\n'):
                        line = line.strip()
                        if line.startswith('- ['):
                            task_match = re.match(r'-\s*\[(.)\]\s*(.+)', line)
                            if task_match:
                                task_num += 1
                                checkbox, task_text = task_match.groups()
                                status = "complete" if checkbox.lower() == 'x' else "pending"

                                # Clean up: remove **bold** markers
                                display_text = re.sub(r'\*\*', '', task_text).strip()
                                # Truncate at first dash for cleaner display
                                if ' - ' in display_text:
                                    display_text = display_text.split(' - ')[0].strip()

                                # Only show non-complete tasks
                                if status != "complete" and display_text and len(display_text) > 3:
                                    display_text = f"#{task_num}: {display_text}"
                                    display_text = display_text[:55] + "..." if len(display_text) > 55 else display_text
                                    result["dev"]["tasks"].append({"text": display_text, "status": status})
            except Exception:
                pass

        # Parse ORACLE_CONTEXT.md
        if ORACLE_CONTEXT.exists():
            try:
                content = ORACLE_CONTEXT.read_text()

                # Get session number from header
                session_match = re.search(r'O(\d+)\s*\(Oracle\)', content)
                if session_match:
                    result["oracle"]["session"] = f"O{session_match.group(1)}"

                # Find Pending Tasks section (unified format with DEV_CONTEXT)
                pending_section = re.search(
                    r'###\s*Pending Tasks.*?\n(.*?)(?=\n###|\n##|\Z)',
                    content,
                    re.DOTALL
                )
                if pending_section:
                    section_text = pending_section.group(1)
                    # Parse checkbox items (same format as DEV)
                    task_num = 0
                    for line in section_text.split('\n'):
                        line = line.strip()
                        if line.startswith('- ['):
                            task_match = re.match(r'-\s*\[(.)\]\s*(.+)', line)
                            if task_match:
                                task_num += 1
                                checkbox, task_text = task_match.groups()
                                status = "complete" if checkbox.lower() == 'x' else "pending"

                                # Clean up: remove **bold** markers
                                display_text = re.sub(r'\*\*', '', task_text).strip()
                                # Truncate at first dash for cleaner display
                                if ' - ' in display_text:
                                    display_text = display_text.split(' - ')[0].strip()

                                # Only show non-complete tasks
                                if status != "complete" and display_text and len(display_text) > 3:
                                    display_text = f"#{task_num}: {display_text}"
                                    display_text = display_text[:55] + "..." if len(display_text) > 55 else display_text
                                    result["oracle"]["tasks"].append({"text": display_text, "status": status})

                # Also check Recent Changes for in-progress items (most recent session)
                recent_match = re.search(
                    r'###\s*December \d+, 2025 - Session \d+ \(O\d+\).*?\n(.*?)(?=\n###|\Z)',
                    content,
                    re.DOTALL
                )
                if recent_match:
                    recent_text = recent_match.group(1)
                    if "Pending:" in recent_text:
                        pending_line = re.search(r'Pending:\s*(.+?)(?:\n|$)', recent_text)
                        if pending_line:
                            task_text = pending_line.group(1).strip()
                            display_text = task_text[:50] + "..." if len(task_text) > 50 else task_text
                            result["oracle"]["tasks"].insert(0, {"text": display_text, "status": "pending"})
            except Exception:
                pass

        return result

    # =========================================================================
    # ACTIONS
    # =========================================================================

    def _run_autosave(self):
        """Run oracle autosave command."""
        self._log("Running autosave...")
        try:
            result = subprocess.run(
                ["python3", "maintenance/project_oracle.py", "autosave", "-q"],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=120
            )
            self.last_autosave = datetime.now()
            self.autosave_count += 1

            # Extract snapshot filename from output
            output = result.stdout
            if "SNAPSHOT_" in output:
                for line in output.split('\n'):
                    if "SNAPSHOT_" in line:
                        self._log(f"Autosave completed -> {line.split()[-1]}")
                        break
            else:
                self._log("Autosave completed")

        except subprocess.TimeoutExpired:
            self._log("Autosave timed out")
        except Exception as e:
            self._log(f"Autosave failed: {e}")

    def _run_health_check(self):
        """Run oracle health check."""
        self._log("Running health check...")
        try:
            result = subprocess.run(
                ["python3", "maintenance/project_oracle.py", "audit", "--quick"],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=60
            )
            self.last_health_check = datetime.now()

            # Parse score from output
            for line in result.stdout.split('\n'):
                if 'Health Score:' in line:
                    try:
                        score = float(line.split(':')[1].strip().split('/')[0])
                        self._log(f"Health check: {score}/10")
                    except Exception:
                        self._log("Health check completed")
                    break

        except subprocess.TimeoutExpired:
            self._log("Health check timed out")
        except Exception as e:
            self._log(f"Health check failed: {e}")

    def _run_optimize(self):
        """Run oracle optimize command."""
        self._log("Running optimization scan...")
        try:
            subprocess.run(
                ["python3", "maintenance/project_oracle.py", "optimize"],
                cwd=str(PROJECT_ROOT),
                timeout=60
            )
            self._log("Optimization scan completed")
        except Exception as e:
            self._log(f"Optimization failed: {e}")

    # =========================================================================
    # DISPLAY - HEALTH BAR
    # =========================================================================

    def _render_health_bar(self, score: float) -> Text:
        """Render visual health bar."""
        filled = int(score)
        empty = 10 - filled

        bar = Text()
        bar.append("●" * filled, style=STYLE_OK if score >= 6 else STYLE_WARNING if score >= 4 else STYLE_CRITICAL)
        bar.append("○" * empty, style=STYLE_DIM)
        return bar

    # =========================================================================
    # DISPLAY - FULL MODE
    # =========================================================================

    def _render_full(self) -> Panel:
        """Render full mode dashboard (P24 modernized layout)."""
        # Gather data
        health = self._read_health_status()
        autosave = self._get_autosave_status()
        brain_cells = self._get_brain_cell_status()
        api_status = self._get_api_status()
        context_status = self._get_context_status()
        pipeline = self._get_pipeline_status()
        session_type = self._detect_session_type()
        session_activity = self._get_session_activity()

        score = health.get("health_score", 0.0)
        issues = health.get("issues", {})

        # Build layout
        layout = Layout()
        if self.show_debug:
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="debug", size=12),
                Layout(name="log", size=self.log_lines + 2),
                Layout(name="footer", size=4),
            )
        else:
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="log", size=self.log_lines + 2),
                Layout(name="footer", size=4),
            )

        # Header
        runtime = datetime.now() - self.session_start
        runtime_str = f"{int(runtime.total_seconds() // 3600)}h {int((runtime.total_seconds() % 3600) // 60)}m"

        header_text = Text()
        header_text.append("  sEEG - Stereotactic EEG Monitor", style=STYLE_HEADER)
        header_text.append(f"                    [Running {runtime_str}]", style=STYLE_DIM)

        layout["header"].update(Panel(header_text, box=box.DOUBLE))

        # Main content - build as table
        main_table = Table(show_header=False, box=None, padding=(0, 2))
        main_table.add_column(width=35)
        main_table.add_column(width=35)

        # Row 1: Health + Session
        health_text = Text()
        health_text.append("HEALTH: ", style=STYLE_HIGHLIGHT)
        health_text.append(f"{score:.1f}/10  ", style=STYLE_OK if score >= 6 else STYLE_WARNING if score >= 4 else STYLE_CRITICAL)
        health_text.append_text(self._render_health_bar(score))

        session_text = Text()
        session_text.append("SESSION: ", style=STYLE_HIGHLIGHT)
        session_text.append(f"{session_type}", style=STYLE_OK)
        # Show indicator if manually set
        if self.session_type_override is not None:
            session_text.append(" (manual)", style=STYLE_DIM)
        session_text.append("\n")
        session_text.append("Activity: ", style=STYLE_DIM)
        activity_level = session_activity["level"]
        activity_style = STYLE_OK if activity_level == "Low" else STYLE_WARNING if activity_level in ["Medium", "High"] else STYLE_CRITICAL
        session_text.append(session_activity["display"], style=activity_style)

        main_table.add_row(health_text, session_text)

        # Blank row for readability
        main_table.add_row(Text(), Text())

        # Row 2: Brain Cells + API Connections (P24 NEW)
        cells_text = Text()
        cells_text.append("BRAIN CELLS\n", style=STYLE_HIGHLIGHT)
        cell_names = ["microglia", "astrocytes", "oligodendrocytes", "ependymal", "cortex", "daemon"]
        for i, cell_name in enumerate(cell_names):
            cell_info = brain_cells["cells"].get(cell_name, {})
            status = cell_info.get("status", "unknown")
            prefix = "└─" if i == len(cell_names) - 1 else "├─"

            # Status icons
            if status == "ready":
                cells_text.append(f"{prefix} {cell_name.capitalize()}: ", style=STYLE_DIM)
                cells_text.append("OK\n", style=STYLE_OK)
            elif status == "running":
                cells_text.append(f"{prefix} {cell_name.capitalize()}: ", style=STYLE_DIM)
                cells_text.append("Running\n", style=STYLE_OK)
            elif status == "missing":
                cells_text.append(f"{prefix} {cell_name.capitalize()}: ", style=STYLE_DIM)
                cells_text.append("Missing\n", style=STYLE_WARNING)
            elif status == "error":
                cells_text.append(f"{prefix} {cell_name.capitalize()}: ", style=STYLE_DIM)
                cells_text.append("Error\n", style=STYLE_CRITICAL)
            else:
                cells_text.append(f"{prefix} {cell_name.capitalize()}: ", style=STYLE_DIM)
                cells_text.append("?\n", style=STYLE_DIM)

        api_text = Text()
        api_text.append("API CONNECTIONS\n", style=STYLE_HIGHLIGHT)
        api_names = ["openai", "elevenlabs", "fal", "pexels", "gemini", "tavily"]
        for i, api_name in enumerate(api_names):
            api_info = api_status["apis"].get(api_name, {})
            status = api_info.get("status", "missing")
            cost = api_info.get("cost", 0.0)
            calls = api_info.get("calls", 0)
            prefix = "└─" if i == len(api_names) - 1 else "├─"

            if status == "configured":
                api_text.append(f"{prefix} {api_name}: ", style=STYLE_DIM)
                api_text.append("OK", style=STYLE_OK)
                if cost > 0 or calls > 0:
                    api_text.append(f" ${cost:.2f} ({calls})", style=STYLE_DIM)
                api_text.append("\n")
            else:
                api_text.append(f"{prefix} {api_name}: ", style=STYLE_DIM)
                api_text.append("missing\n", style=STYLE_WARNING)

        main_table.add_row(cells_text, api_text)

        # Row 3: Code Health (simplified) + Autosave
        code_text = Text()
        code_text.append("CODE HEALTH\n", style=STYLE_HIGHLIGHT)
        critical = issues.get('critical', 0)
        warnings = issues.get('warnings', 0)
        code_text.append(f"├─ Critical: {critical}\n", style=STYLE_CRITICAL if critical > 0 else STYLE_DIM)
        code_text.append(f"├─ Warnings: {warnings}\n", style=STYLE_WARNING if warnings > 0 else STYLE_DIM)
        # Calculate health percentage
        health_pct = int(score * 10)
        code_text.append(f"└─ Health Score: {health_pct}%", style=STYLE_OK if health_pct >= 80 else STYLE_WARNING if health_pct >= 60 else STYLE_CRITICAL)

        autosave_text = Text()
        autosave_text.append("AUTOSAVE\n", style=STYLE_HIGHLIGHT)
        last_style = STYLE_OK if autosave["status"] == "ok" else STYLE_WARNING if autosave["status"] == "reminder" else STYLE_CRITICAL
        autosave_text.append(f"├─ Last: {autosave['last_minutes']}m ago\n", style=last_style)
        autosave_text.append(f"├─ Next reminder: {autosave['reminder_in']}m\n", style=STYLE_DIM)
        autosave_text.append(f"└─ Safety trigger: {autosave['safety_in']}m", style=STYLE_DIM)
        if autosave["status"] == "overdue":
            autosave_text.append("\nOVERDUE - run autosave!", style=STYLE_CRITICAL)

        main_table.add_row(code_text, autosave_text)

        # Blank row for readability
        main_table.add_row(Text(), Text())

        # Row 4: Context Files + Files Watched
        ctx_text = Text()
        ctx_text.append("CONTEXT FILES\n", style=STYLE_HIGHLIGHT)
        ctx_text.append(f"├─ DEV_CONTEXT: {context_status['dev_context']['age_str']}\n", style=STYLE_DIM)
        ctx_text.append(f"├─ ORACLE_CONTEXT: {context_status['oracle_context']['age_str']}\n", style=STYLE_DIM)
        ctx_text.append(f"├─ Session: {context_status['oracle_context']['session']} / {context_status['dev_context']['session']}\n", style=STYLE_DIM)
        flags = context_status.get("cross_session_flags", [])
        if flags:
            ctx_text.append(f"└─ Cross-Session: ", style=STYLE_DIM)
            ctx_text.append(", ".join(flags), style=STYLE_WARNING)
        else:
            ctx_text.append("└─ Cross-Session: _(none)_", style=STYLE_DIM)

        files_text = Text()
        files_text.append("FILES WATCHED\n", style=STYLE_HIGHLIGHT)
        files_text.append("├─ context/*.md\n", style=STYLE_DIM)
        files_text.append("├─ scripts/*.py\n", style=STYLE_DIM)
        files_text.append(f"└─ Changes: {self.file_changes} since start", style=STYLE_DIM)

        main_table.add_row(ctx_text, files_text)

        # Blank row for readability
        main_table.add_row(Text(), Text())

        # Row 5: Pipeline
        pipeline_text = Text()
        pipeline_text.append("PIPELINE\n", style=STYLE_HIGHLIGHT)
        layer_line = "├─ "
        for layer, info in pipeline.items():
            if info.get("active"):
                layer_line += f"{layer}* "  # Active/most recent layer
            else:
                layer_line += f"{layer}. "
        pipeline_text.append(layer_line + "\n", style=STYLE_DIM)

        # Find active layer (most recently modified)
        active_layer = "None"
        for layer, info in pipeline.items():
            if info.get("active"):
                active_layer = f"{layer} ({info['label']})"
                break

        pipeline_text.append(f"├─ Active: {active_layer}\n", style=STYLE_DIM)
        cost = health.get("cost_today", 0.0)
        pipeline_text.append(f"└─ Cost today: ${cost:.2f} / ${self.budget:.2f}", style=STYLE_DIM)

        # Empty right column for pipeline row
        main_table.add_row(pipeline_text, Text())

        # Blank row for readability before Session Tasks
        main_table.add_row(Text(), Text())

        # Row 6: Session Tasks (dual view)
        session_tasks = self._get_session_tasks()

        dev_tasks_text = Text()
        dev_tasks_text.append(f"DEV TASKS ({session_tasks['dev']['session']})\n", style=STYLE_HIGHLIGHT)
        if session_tasks['dev']['tasks']:
            for i, task in enumerate(session_tasks['dev']['tasks'][:6]):  # Max 6 tasks
                prefix = "└─" if i == len(session_tasks['dev']['tasks'][:6]) - 1 else "├─"
                if task['status'] == 'complete':
                    dev_tasks_text.append(f"{prefix} [x] {task['text']}\n", style=STYLE_OK)
                elif task['status'] == 'in_progress':
                    dev_tasks_text.append(f"{prefix} [>] {task['text']}\n", style=STYLE_WARNING)
                else:
                    dev_tasks_text.append(f"{prefix} [ ] {task['text']}\n", style=STYLE_DIM)
        else:
            dev_tasks_text.append("└─ (none)\n", style=STYLE_DIM)

        oracle_tasks_text = Text()
        oracle_tasks_text.append(f"ORACLE TASKS ({session_tasks['oracle']['session']})\n", style=STYLE_HIGHLIGHT)
        if session_tasks['oracle']['tasks']:
            for i, task in enumerate(session_tasks['oracle']['tasks'][:6]):  # Max 6 tasks
                prefix = "└─" if i == len(session_tasks['oracle']['tasks'][:6]) - 1 else "├─"
                if task['status'] == 'complete':
                    oracle_tasks_text.append(f"{prefix} [x] {task['text']}\n", style=STYLE_OK)
                elif task['status'] == 'in_progress':
                    oracle_tasks_text.append(f"{prefix} [>] {task['text']}\n", style=STYLE_WARNING)
                else:
                    oracle_tasks_text.append(f"{prefix} [ ] {task['text']}\n", style=STYLE_DIM)
        else:
            oracle_tasks_text.append("└─ (none)\n", style=STYLE_DIM)

        main_table.add_row(dev_tasks_text, oracle_tasks_text)

        layout["main"].update(Panel(main_table, box=box.ROUNDED))

        # Debug panel (if enabled)
        if self.show_debug:
            debug_info = self._get_debug_info()
            debug_text = Text()
            debug_text.append("DEBUG - Internal State\n", style="bold magenta")
            debug_text.append(f"mode={debug_info['mode']} | ", style=STYLE_DIM)
            debug_text.append(f"file_changes={debug_info['file_changes']} | ", style=STYLE_DIM)
            debug_text.append(f"autosave_count={debug_info['autosave_count']} | ", style=STYLE_DIM)
            debug_text.append(f"health_updates={debug_info['health_status_updates']}\n", style=STYLE_DIM)
            debug_text.append(f"session_start={debug_info['session_start'][:19]} | ", style=STYLE_DIM)
            debug_text.append(f"last_autosave={debug_info['last_autosave'][:19] if debug_info['last_autosave'] else 'None'}\n", style=STYLE_DIM)
            debug_text.append(f"log_entries={debug_info['log_entries_count']} | ", style=STYLE_DIM)
            debug_text.append(f"recent_files={debug_info['recent_file_changes']} | ", style=STYLE_DIM)
            debug_text.append(f"reminder_count={debug_info['reminder_count']}\n", style=STYLE_DIM)
            debug_text.append(f"calibration: file_max={debug_info['file_changes_max']} | ", style=STYLE_DIM)
            debug_text.append(f"health_max={debug_info['health_updates_max']} | ", style=STYLE_DIM)
            debug_text.append(f"growth_max={debug_info['context_growth_max']}% | ", style=STYLE_DIM)
            debug_text.append(f"data_points={debug_info['calibration_points']}\n", style=STYLE_DIM)
            debug_text.append(f"ORACLE_DEBUG={debug_info['ORACLE_DEBUG']} | ", style="bold cyan")
            debug_text.append(f"notifications={debug_info['notifications']} | ", style=STYLE_DIM)
            debug_text.append(f"session_override={debug_info['session_type_override']}", style=STYLE_DIM)
            layout["debug"].update(Panel(debug_text, box=box.ROUNDED))

        # Log panel
        log_text = Text()
        log_text.append("LOG\n", style=STYLE_HIGHLIGHT)
        recent_logs = self.log_entries[-self.log_lines:]
        for entry in recent_logs:
            log_text.append(f"{entry}\n", style=STYLE_DIM)

        layout["log"].update(Panel(log_text, box=box.ROUNDED))

        # Footer with hotkeys (or calibration/command prompt)
        footer_text = Text()
        if self.calibration_mode:
            footer_text.append(f"  CALIBRATING: {self.calibration_input or '_'}% ", style="bold yellow")
            footer_text.append("[Enter=confirm, Esc=cancel, Backspace=delete]", style=STYLE_DIM)
        elif self.command_mode:
            footer_text.append("  COMMAND: ", style="bold cyan")
            footer_text.append(f"oracle> {self.command_input}", style="cyan")
            footer_text.append("█", style="cyan blink")  # Cursor
            footer_text.append("\n  ", style=STYLE_DIM)
            footer_text.append("Available: ", style=STYLE_DIM)
            footer_text.append("audit, status, verify, clean, optimize, sync, help", style="cyan")
            footer_text.append("\n  [Enter=execute, Esc=cancel, ↑/↓=history]", style=STYLE_DIM)
        else:
            # Row 1: Actions
            footer_text.append("  [a]", style=STYLE_HIGHLIGHT)
            footer_text.append("utosave ", style=STYLE_DIM)
            footer_text.append("[h]", style=STYLE_HIGHLIGHT)
            footer_text.append("ealth ", style=STYLE_DIM)
            footer_text.append("[d]", style=STYLE_HIGHLIGHT)
            footer_text.append("iagnostics ", style=STYLE_DIM)
            footer_text.append("[:]", style=STYLE_HIGHLIGHT)
            footer_text.append("cmd ", style=STYLE_DIM)
            footer_text.append("[x]", style=STYLE_HIGHLIGHT)
            footer_text.append("calibrate ", style=STYLE_DIM)
            footer_text.append("[q]", style=STYLE_HIGHLIGHT)
            footer_text.append("uit\n", style=STYLE_DIM)
            # Row 2: Modes & Session
            footer_text.append("  [f]", style=STYLE_HIGHLIGHT)
            footer_text.append("ull ", style=STYLE_DIM)
            footer_text.append("[c]", style=STYLE_HIGHLIGHT)
            footer_text.append("ompact ", style=STYLE_DIM)
            footer_text.append("[s]", style=STYLE_HIGHLIGHT)
            footer_text.append("plit ", style=STYLE_DIM)
            footer_text.append("[m]", style=STYLE_HIGHLIGHT)
            footer_text.append("in ", style=STYLE_DIM)
            footer_text.append("| ", style=STYLE_DIM)
            footer_text.append("[d]", style=STYLE_HIGHLIGHT)
            footer_text.append("ev ", style=STYLE_DIM)
            footer_text.append("[t]", style=STYLE_HIGHLIGHT)
            footer_text.append("maint ", style=STYLE_DIM)
            footer_text.append("[0]", style=STYLE_HIGHLIGHT)
            footer_text.append("auto ", style=STYLE_DIM)
            footer_text.append("[r]", style=STYLE_HIGHLIGHT)
            footer_text.append("efresh ", style=STYLE_DIM)
            footer_text.append("[?]", style=STYLE_HIGHLIGHT)
            footer_text.append("help", style=STYLE_DIM)

        layout["footer"].update(Panel(footer_text, box=box.DOUBLE))

        return Panel(layout, box=box.HEAVY, title="sEEG", subtitle="Press [?] for help")

    # =========================================================================
    # DISPLAY - COMPACT MODE
    # =========================================================================

    def _render_compact(self) -> Panel:
        """Render compact mode dashboard (P24 modernized)."""
        health = self._read_health_status()
        autosave = self._get_autosave_status()
        pipeline = self._get_pipeline_status()
        brain_cells = self._get_brain_cell_status()
        api_status = self._get_api_status()

        score = health.get("health_score", 0.0)

        # Build compact display
        layout = Layout()
        layout.split_column(
            Layout(name="status", size=4),
            Layout(name="log", size=5),
            Layout(name="footer", size=3),
        )

        # Status line 1: Health + Autosave
        status = Text()
        status.append("  sEEG  ", style=STYLE_HEADER)
        status.append(f"{score:.1f}/10 ", style=STYLE_OK if score >= 6 else STYLE_WARNING)
        status.append_text(self._render_health_bar(score))
        status.append("  |  ", style=STYLE_DIM)
        status.append(f"Save: {autosave['last_minutes']}m ", style=STYLE_OK if autosave["status"] == "ok" else STYLE_WARNING)
        status.append(f"({autosave['reminder_in']}m)", style=STYLE_DIM)

        # Status line 2: Cells + APIs + Pipeline
        line2 = Text()
        line2.append("  ", style=STYLE_DIM)

        # Brain cells indicator
        cells_ok = brain_cells["ready"]
        cells_total = brain_cells["total"]
        cell_style = STYLE_OK if cells_ok == cells_total else STYLE_WARNING
        line2.append(f"Cells: {cells_ok}/{cells_total} ", style=cell_style)
        line2.append("|  ", style=STYLE_DIM)

        # API indicator
        api_configured = sum(1 for a in api_status["apis"].values() if a.get("status") == "configured")
        api_total = 6  # openai, elevenlabs, fal, pexels, gemini, tavily
        api_style = STYLE_OK if api_configured >= api_total - 1 else STYLE_WARNING
        line2.append(f"APIs: {api_configured}/{api_total} ", style=api_style)
        line2.append("|  ", style=STYLE_DIM)

        # Pipeline
        for layer, info in pipeline.items():
            if info.get("active"):
                line2.append(f"{layer}* ", style=STYLE_OK)
            else:
                line2.append(f"{layer}. ", style=STYLE_DIM)

        combined = Text()
        combined.append_text(status)
        combined.append("\n")
        combined.append_text(line2)

        layout["status"].update(Panel(combined, box=box.ROUNDED))

        # Log
        log_text = Text()
        for entry in self.log_entries[-3:]:
            log_text.append(f"  {entry}\n", style=STYLE_DIM)
        layout["log"].update(Panel(log_text, box=box.ROUNDED))

        # Footer
        footer = Text()
        if self.calibration_mode:
            footer.append(f"  CALIBRATING: {self.calibration_input or '_'}% ", style="bold yellow")
            footer.append("[Enter=confirm, Esc=cancel, Backspace=delete]", style=STYLE_DIM)
        elif self.command_mode:
            footer.append("  COMMAND: ", style="bold cyan")
            footer.append(f"oracle> {self.command_input}", style="cyan")
            footer.append("█", style="cyan blink")
            footer.append(" | ", style=STYLE_DIM)
            footer.append("audit, status, verify, clean, optimize, sync, help", style="cyan")
            footer.append("\n  [Enter=execute, Esc=cancel, ↑/↓=history]", style=STYLE_DIM)
        else:
            footer.append("  [a]utosave [h]ealth [d]iagnostics [:]cmd [x]calibrate [q]uit [f]ull [c]ompact [s]plit [m]in", style=STYLE_DIM)
        layout["footer"].update(Panel(footer, box=box.DOUBLE))

        return Panel(layout, box=box.HEAVY, title="sEEG")

    # =========================================================================
    # DISPLAY - MINIMIZED MODE
    # =========================================================================

    def _render_minimized(self) -> Text:
        """Render minimized single-line status (P24 modernized)."""
        health = self._read_health_status()
        autosave = self._get_autosave_status()
        pipeline = self._get_pipeline_status()
        brain_cells = self._get_brain_cell_status()
        api_status = self._get_api_status()

        score = health.get("health_score", 0.0)

        # Find current layer
        current = "L1."
        for layer, info in pipeline.items():
            if info.get("active"):
                current = f"{layer}*"
                break

        line = Text()

        # Alert indicator
        if score < self.alert_threshold or autosave["status"] == "overdue":
            line.append("! ", style=STYLE_WARNING)

        line.append("sEEG | ", style=STYLE_HEADER)
        line.append(f"{score:.1f}/10 | ", style=STYLE_OK if score >= 6 else STYLE_WARNING)
        line.append(f"Save: {autosave['last_minutes']}m | ", style=STYLE_OK if autosave["status"] == "ok" else STYLE_WARNING)

        # Cell/API indicator
        cells_ok = brain_cells["ready"]
        api_configured = sum(1 for a in api_status["apis"].values() if a.get("status") == "configured")
        line.append(f"C:{cells_ok}/6 A:{api_configured}/6 | ", style=STYLE_DIM)

        line.append(f"{current} | ", style=STYLE_DIM)
        line.append("[Press any key to expand]", style=STYLE_DIM)

        return line

    # =========================================================================
    # DISPLAY - SPLIT MODE
    # =========================================================================

    def _render_split(self) -> Panel:
        """Render split mode (health left, log right) - P24 modernized."""
        health = self._read_health_status()
        autosave = self._get_autosave_status()
        pipeline = self._get_pipeline_status()
        brain_cells = self._get_brain_cell_status()
        api_status = self._get_api_status()
        context_status = self._get_context_status()

        score = health.get("health_score", 0.0)
        issues = health.get("issues", {})

        layout = Layout()
        layout.split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1),
        )

        # Left panel - Health info
        left_text = Text()
        runtime = datetime.now() - self.session_start
        runtime_str = f"{int(runtime.total_seconds() // 3600)}h {int((runtime.total_seconds() % 3600) // 60)}m"

        left_text.append(f"sEEG Monitor  {runtime_str}\n\n", style=STYLE_HEADER)
        left_text.append("HEALTH: ", style=STYLE_HIGHLIGHT)
        left_text.append(f"{score:.1f}/10 ", style=STYLE_OK if score >= 6 else STYLE_WARNING)
        left_text.append_text(self._render_health_bar(score))
        activity = self._get_session_activity()
        activity_style = STYLE_OK if activity["level"] == "Low" else STYLE_WARNING if activity["level"] in ["Medium", "High"] else STYLE_CRITICAL
        left_text.append("\nActivity: ", style=STYLE_DIM)
        left_text.append(f"{activity['display']}\n\n", style=activity_style)

        left_text.append("AUTOSAVE\n", style=STYLE_HIGHLIGHT)
        left_text.append(f"├─ Last: {autosave['last_minutes']}m ago\n", style=STYLE_OK if autosave["status"] == "ok" else STYLE_WARNING)
        left_text.append(f"├─ Reminder: {autosave['reminder_in']}m\n", style=STYLE_DIM)
        left_text.append(f"└─ Safety: {autosave['safety_in']}m\n\n", style=STYLE_DIM)

        # Brain Cells summary
        left_text.append("BRAIN CELLS\n", style=STYLE_HIGHLIGHT)
        cells_ok = brain_cells["ready"]
        cells_total = brain_cells["total"]
        cell_style = STYLE_OK if cells_ok == cells_total else STYLE_WARNING
        left_text.append(f"├─ Ready: {cells_ok}/{cells_total}\n", style=cell_style)
        # API summary
        api_configured = sum(1 for a in api_status["apis"].values() if a.get("status") == "configured")
        api_style = STYLE_OK if api_configured >= 5 else STYLE_WARNING
        left_text.append(f"└─ APIs: {api_configured}/6\n\n", style=api_style)

        # Pipeline
        left_text.append("PIPELINE\n", style=STYLE_HIGHLIGHT)
        for layer, info in pipeline.items():
            if info.get("active"):
                left_text.append(f"{layer}* ", style=STYLE_OK)
            else:
                left_text.append(f"{layer}. ", style=STYLE_DIM)
        left_text.append("\n\n")

        # Code + Context
        left_text.append("CODE        | CONTEXT\n", style=STYLE_HIGHLIGHT)
        left_text.append(f"Crit: {issues.get('critical', 0)}     | DEV: {context_status['dev_context']['age_str']}\n", style=STYLE_DIM)
        left_text.append(f"Warn: {issues.get('warnings', 0)}    | ORACLE: {context_status['oracle_context']['age_str']}\n", style=STYLE_DIM)

        layout["left"].update(Panel(left_text, box=box.ROUNDED, title="Health"))

        # Right panel - Log
        right_text = Text()
        right_text.append("LOG\n\n", style=STYLE_HIGHLIGHT)
        for entry in self.log_entries[-15:]:
            right_text.append(f"{entry}\n", style=STYLE_DIM)

        layout["right"].update(Panel(right_text, box=box.ROUNDED, title="Activity"))

        # Add footer
        outer = Layout()
        outer.split_column(
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        outer["main"].update(layout)

        footer = Text()
        if self.calibration_mode:
            footer.append(f"  CALIBRATING: {self.calibration_input or '_'}% ", style="bold yellow")
            footer.append("[Enter=confirm, Esc=cancel, Backspace=delete]", style=STYLE_DIM)
        elif self.command_mode:
            footer.append("  COMMAND: ", style="bold cyan")
            footer.append(f"oracle> {self.command_input}", style="cyan")
            footer.append("█", style="cyan blink")
            footer.append(" | ", style=STYLE_DIM)
            footer.append("audit, status, verify, clean, optimize, sync, help", style="cyan")
            footer.append("\n  [Enter=execute, Esc=cancel, ↑/↓=history]", style=STYLE_DIM)
        else:
            footer.append("  [a]utosave [h]ealth [d]iagnostics [:]cmd [x]calibrate [q]uit [f]ull [c]ompact [s]plit [m]in", style=STYLE_DIM)
        outer["footer"].update(Panel(footer, box=box.DOUBLE))

        return Panel(outer, box=box.HEAVY, title="sEEG")

    # =========================================================================
    # MAIN RENDER
    # =========================================================================

    def render(self):
        """Render current mode."""
        if self.mode == "full":
            return self._render_full()
        elif self.mode == "compact":
            return self._render_compact()
        elif self.mode == "split":
            return self._render_split()
        elif self.mode == "min":
            return self._render_minimized()
        else:
            return self._render_full()

    # =========================================================================
    # INPUT HANDLING
    # =========================================================================

    def _show_help(self):
        """Display help information."""
        self._log("Help: a=autosave h=health b=brain :=command x=calibrate")
        self._log("      f/c/s/m=modes d/t/0=session r=refresh q=quit")
        self._log("      Press ':' for command palette (audit, status, verify, etc.)")

    def _set_mode(self, new_mode: str, persist: bool = True):
        """Set display mode and optionally persist to config."""
        self.mode = new_mode
        self._log(f"Switched to {new_mode} mode")

        # Persist mode preference so it starts in this mode next time
        if persist:
            config = load_config()
            config["mode"] = new_mode
            save_config(config)

    def _handle_input(self, key: str):
        """Handle keyboard input."""
        # Route to calibration handler if in calibration mode
        if self.calibration_mode:
            self._handle_calibration_input(key)
            return

        # Route to command handler if in command mode
        if self.command_mode:
            self._handle_command_input(key)
            return

        # Enter command mode with ':'
        if key == ':':
            self.command_mode = True
            self.command_input = ""
            self.command_history_index = len(self.command_history)
            self._log("━━━ COMMAND MODE ━━━")
            self._log("Available: audit, status, verify, clean, optimize, sync, help")
            self._log("Type command and press Enter (Esc to cancel)")
            return

        if key == 'q':
            self._log("Shutting down...")
            self._run_autosave()
            self.running = False
        elif key == 'a':
            self._run_autosave()
        elif key == 'h':
            self._run_health_check()
        elif key == 'd':
            # Run brain cell diagnostics (P24)
            self._run_brain_diagnostics()
        elif key == 'f':
            self._set_mode("full")
        elif key == 'c':
            self._set_mode("compact")
        elif key == 's':
            self._set_mode("split")
        elif key == 'm':
            self._set_mode("min")
        elif key == 'd':
            self._set_session_type("Development")
        elif key == 't':
            self._set_session_type("Maintenance")
        elif key == '0':
            self._clear_session_override()
        elif key == 'r':
            self._log("Refreshing health data...")
            self.last_autosave = self._get_last_autosave_time()
            self._run_health_check()
        elif key == '?':
            self._show_help()
        elif key == 'x':
            # Start calibration process - prompts for exact %
            self._start_calibration()
        elif key == 'g':
            # Toggle debug panel
            self._toggle_debug()

    def _run_brain_diagnostics(self):
        """Run brain cell diagnostics and log status."""
        self._log("--- BRAIN CELL DIAGNOSTICS ---")
        brain_cells = self._get_brain_cell_status()
        for cell_name, info in brain_cells["cells"].items():
            status = info.get("status", "unknown")
            if status in ["ready", "running"]:
                self._log(f"  {cell_name}: OK")
            elif status == "missing":
                self._log(f"  {cell_name}: MISSING")
            elif status == "error":
                self._log(f"  {cell_name}: ERROR - {info.get('error', '?')[:30]}")
            else:
                self._log(f"  {cell_name}: {status}")
        self._log(f"Ready: {brain_cells['ready']}/{brain_cells['total']}")

    # =========================================================================
    # MAIN LOOP
    # =========================================================================

    def _check_alerts(self) -> List[str]:
        """Check for alert conditions and return list of alerts."""
        alerts = []

        # Check autosave status
        autosave = self._get_autosave_status()

        # Escalating autosave reminders
        if autosave["status"] == "reminder":
            now = datetime.now()
            # First reminder or 3+ minutes since last reminder
            if self.last_reminder_time is None or (now - self.last_reminder_time).total_seconds() >= 180:
                self.reminder_count += 1
                self.last_reminder_time = now

                if self.reminder_count == 1:
                    alerts.append("autosave_gentle")  # First reminder - gentle
                elif self.reminder_count == 2:
                    alerts.append("autosave_nudge")   # Second reminder - nudge
                else:
                    alerts.append("autosave_urgent")  # Third+ reminder - urgent

        elif autosave["status"] == "overdue":
            alerts.append("autosave_critical")

        # Reset reminder count if status is OK
        if autosave["status"] == "ok":
            self.reminder_count = 0
            self.last_reminder_time = None

        # Check health score
        health = self._read_health_status()
        score = health.get("health_score", 0.0)
        if score < 4.0:
            alerts.append("health_critical")
        elif score < self.alert_threshold:
            alerts.append("health_warning")

        return alerts

    def _handle_alert(self, alert_type: str):
        """Handle a specific alert type with appropriate notification."""
        if alert_type == "autosave_gentle":
            self._log("Autosave reminder (gentle)")
            # No bell for first reminder

        elif alert_type == "autosave_nudge":
            self._bell()
            self._log("Autosave reminder - consider saving soon")

        elif alert_type == "autosave_urgent":
            self._bell()
            self._bell()
            self._notify("Oracle", "Autosave overdue! Consider saving.")
            self._log("⚠️ Autosave reminder - OVERDUE")

        elif alert_type == "autosave_critical":
            # Safety auto-trigger
            autosave = self._get_autosave_status()
            if autosave["safety_in"] <= 0:
                self._notify("Oracle", "Running safety autosave!")
                self._bell()
                self._log("🚨 Safety autosave triggered")
                self._run_autosave()

        elif alert_type == "health_critical":
            self._notify("Oracle", "Health score critical!")
            self._log("🚨 Health score critical")

        elif alert_type == "health_warning":
            self._log("Health score below threshold")

    def run(self):
        """Main monitoring loop."""
        # Check for existing instance
        if self._check_lock_file():
            console.print("[red]Error: Oracle Health Monitor is already running.[/red]")
            console.print("[dim]Kill the existing process or remove /tmp/oracle_health_monitor.lock[/dim]")
            sys.exit(1)

        self._create_lock_file()

        # Initialize keyboard reader
        self.keyboard = KeyboardReader()

        try:
            console.print("[cyan]Starting Oracle Health Monitor...[/cyan]")
            console.print(f"[dim]Mode: {self.mode} | Safety autosave: {self.safety_autosave}m | Health check: {self.health_interval}m[/dim]")
            console.print("[dim]Press 'q' to quit, '?' for help[/dim]")
            time.sleep(1)

            # Start file watcher
            self._start_file_watcher()

            # Start keyboard reader
            self.keyboard.start()

            # Run initial health check
            self._run_health_check()

            last_health_check = time.time()
            last_alert_check = time.time()

            with Live(self.render(), refresh_per_second=1, screen=True) as live:
                while self.running:
                    now = time.time()

                    # Periodic health check
                    if now - last_health_check >= self.health_interval * 60:
                        self._run_health_check()
                        last_health_check = now

                    # Check alerts every 30 seconds
                    if now - last_alert_check >= 30:
                        alerts = self._check_alerts()
                        for alert in alerts:
                            self._handle_alert(alert)
                        last_alert_check = now

                    # Check for keyboard input
                    key = self.keyboard.read_key(timeout=0.1)
                    if key:
                        self._handle_input(key)

                    # Update display
                    live.update(self.render())

                    # Small sleep to reduce CPU usage
                    time.sleep(0.1)

        except KeyboardInterrupt:
            self._log("Interrupted - saving...")
            self._run_autosave()
        finally:
            # Stop keyboard reader
            if self.keyboard:
                self.keyboard.stop()

            # Stop file watcher
            self._stop_file_watcher()

            self._remove_lock_file()
            console.print("\n[cyan]Oracle Health Monitor stopped.[/cyan]")

            # Session summary
            duration = datetime.now() - self.session_start
            console.print(f"[dim]Session: {int(duration.total_seconds() // 60)}m | Autosaves: {self.autosave_count} | File changes: {self.file_changes}[/dim]")


# =============================================================================
# CONFIGURATION FILE
# =============================================================================

CONFIG_FILE = ORACLE_DIR / "maintenance" / "config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from file if it exists."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_config(config: Dict[str, Any]):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass  # Silently fail


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Oracle Health Monitor - Persistent VS Code Terminal Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Display Modes:
  full      All panels visible (default)
  compact   Condensed for smaller terminals
  split     Side-by-side health and log
  min       Single status line

Hotkeys:
  a = autosave    h = health check    o = optimize
  d = dev session t = maint session   0 = auto-detect
  f = full mode   c = compact mode    s = split mode
  m = minimized   r = refresh         q = quit

Examples:
  python maintenance/health_monitor.py
  python maintenance/health_monitor.py --mode compact
  python maintenance/health_monitor.py --safety-autosave 20 --reminder-interval 15
        """
    )

    parser.add_argument(
        "--mode", "-m",
        choices=["full", "compact", "split", "min"],
        default="full",
        help="Display mode (default: full)"
    )
    parser.add_argument(
        "--safety-autosave",
        type=int,
        default=DEFAULT_SAFETY_AUTOSAVE,
        help=f"Minutes before auto-autosave (default: {DEFAULT_SAFETY_AUTOSAVE})"
    )
    parser.add_argument(
        "--health-interval",
        type=int,
        default=DEFAULT_HEALTH_INTERVAL,
        help=f"Minutes between health checks (default: {DEFAULT_HEALTH_INTERVAL})"
    )
    parser.add_argument(
        "--reminder-interval",
        type=int,
        default=DEFAULT_REMINDER_INTERVAL,
        help=f"Minutes before autosave reminder (default: {DEFAULT_REMINDER_INTERVAL})"
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=DEFAULT_DAILY_BUDGET,
        help=f"Daily cost budget in dollars (default: {DEFAULT_DAILY_BUDGET})"
    )
    parser.add_argument(
        "--alert-threshold",
        type=float,
        default=DEFAULT_ALERT_THRESHOLD,
        help=f"Health score alert threshold (default: {DEFAULT_ALERT_THRESHOLD})"
    )
    parser.add_argument(
        "--log-lines",
        type=int,
        default=DEFAULT_LOG_LINES,
        help=f"Number of log lines to show (default: {DEFAULT_LOG_LINES})"
    )
    parser.add_argument(
        "--no-notifications",
        action="store_true",
        help="Disable macOS notifications"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable color output"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run single check and exit (no monitoring)"
    )

    args = parser.parse_args()

    # Load config file and merge with command line args
    config = load_config()

    # Command line args override config file
    mode = args.mode or config.get("mode", "full")
    safety_autosave = args.safety_autosave if args.safety_autosave != DEFAULT_SAFETY_AUTOSAVE else config.get("safety_autosave_minutes", DEFAULT_SAFETY_AUTOSAVE)
    health_interval = args.health_interval if args.health_interval != DEFAULT_HEALTH_INTERVAL else config.get("health_check_interval_minutes", DEFAULT_HEALTH_INTERVAL)
    reminder_interval = args.reminder_interval if args.reminder_interval != DEFAULT_REMINDER_INTERVAL else config.get("reminder_interval_minutes", DEFAULT_REMINDER_INTERVAL)
    budget = args.budget if args.budget != DEFAULT_DAILY_BUDGET else config.get("daily_budget", DEFAULT_DAILY_BUDGET)
    alert_threshold = args.alert_threshold if args.alert_threshold != DEFAULT_ALERT_THRESHOLD else config.get("alert_threshold", DEFAULT_ALERT_THRESHOLD)
    log_lines = args.log_lines if args.log_lines != DEFAULT_LOG_LINES else config.get("log_lines", DEFAULT_LOG_LINES)
    notifications = not args.no_notifications and config.get("notifications_enabled", True)
    color = not args.no_color and config.get("color_enabled", True)

    # Check we're in the right directory
    if not PROJECT_ROOT.exists() or not (PROJECT_ROOT / "oracle").exists():
        console.print("[red]Error: Must run from project root directory[/red]")
        sys.exit(1)

    # Create and run monitor
    monitor = OracleHealthMonitor(
        mode=mode,
        safety_autosave=safety_autosave,
        health_interval=health_interval,
        reminder_interval=reminder_interval,
        budget=budget,
        alert_threshold=alert_threshold,
        log_lines=log_lines,
        notifications=notifications,
        color=color,
    )

    if args.once:
        # Single check mode
        console.print(monitor.render())
    else:
        # Continuous monitoring
        monitor.run()


# =============================================================================
# PUBLIC INTERFACE FUNCTION
# =============================================================================

def run_monitor(mode: str = "full", once: bool = False) -> None:
    """Start the real-time monitoring dashboard.

    Args:
        mode: Display mode (full, compact, split, min)
        once: If True, run single check and exit
    """
    config = load_config()

    monitor = OracleHealthMonitor(
        mode=mode,
        safety_autosave=config.get("safety_autosave_minutes", DEFAULT_SAFETY_AUTOSAVE),
        health_interval=config.get("health_check_interval_minutes", DEFAULT_HEALTH_INTERVAL),
        reminder_interval=config.get("reminder_interval_minutes", DEFAULT_REMINDER_INTERVAL),
        budget=config.get("daily_budget", DEFAULT_DAILY_BUDGET),
        alert_threshold=config.get("alert_threshold", DEFAULT_ALERT_THRESHOLD),
        log_lines=config.get("log_lines", DEFAULT_LOG_LINES),
        notifications=config.get("notifications_enabled", True),
        color=config.get("color_enabled", True),
    )

    if once:
        console.print(monitor.render())
    else:
        monitor.run()


if __name__ == "__main__":
    main()
