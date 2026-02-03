"""
Context Manager - Auto-detection and dynamic context file management.

Contexts:
- Oracle: Planning, docs, health monitoring
- Dev: Backend development (app/, scripts/, config/)
- Dash: Frontend development (dashboard/)
- Crank: Content production (no code changes)
- Pocket: Mobile/backup on M1 Air

Features:
- Detects active context based on file activity
- Auto-updates context files on changes
- Enforces 500-line limit on context files
- Provides cross-session messaging interface
- Fallback mode for Pocket (alternate ports)
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Up from context/ to oracle/ to root


class ContextType:
    """Context type constants."""
    ORACLE = "oracle"
    DEV = "dev"
    DASH = "dash"
    CRANK = "crank"
    POCKET = "pocket"

    @classmethod
    def all(cls) -> List[str]:
        return [cls.ORACLE, cls.DEV, cls.DASH, cls.CRANK, cls.POCKET]


class ContextPaths:
    """Context file paths and watch directories."""

    # Context files (V2 paths under oracle/docs/)
    FILES = {
        ContextType.ORACLE: PROJECT_ROOT / "oracle" / "docs" / "context" / "ORACLE_CONTEXT.md",
        ContextType.DEV: PROJECT_ROOT / "oracle" / "docs" / "context" / "DEV_CONTEXT.md",
        ContextType.DASH: PROJECT_ROOT / "oracle" / "docs" / "context" / "DASHBOARD_CONTEXT.md",
        ContextType.CRANK: PROJECT_ROOT / "oracle" / "docs" / "context" / "CRANK_CONTEXT.md",
        ContextType.POCKET: PROJECT_ROOT / "oracle" / "docs" / "context" / "POCKET_CONTEXT.md",
    }

    # Watch directories for each context
    WATCH_DIRS = {
        ContextType.ORACLE: [
            PROJECT_ROOT / "oracle",
            PROJECT_ROOT / "maintenance",
            PROJECT_ROOT / "docs",
        ],
        ContextType.DEV: [
            PROJECT_ROOT / "app" / "core",
            PROJECT_ROOT / "app" / "services",
            PROJECT_ROOT / "app" / "models",
            PROJECT_ROOT / "scripts",
            PROJECT_ROOT / "config",
        ],
        ContextType.DASH: [
            PROJECT_ROOT / "app" / "frontend",
            PROJECT_ROOT / "app" / "api",
        ],
        ContextType.CRANK: [
            PROJECT_ROOT / "content",  # Output directory
        ],
        ContextType.POCKET: [],  # Pocket watches nothing directly - it syncs via iCloud
    }


class FileActivityTracker:
    """Tracks file activity to determine active context."""

    def __init__(self):
        self.activity: Dict[str, List[Dict]] = {ctx: [] for ctx in ContextType.all()}
        self.last_activity: Dict[str, datetime] = {}
        self.activity_window = 300  # 5 minutes

    def record_activity(self, context: str, file_path: str, event_type: str):
        """Record file activity for a context."""
        now = datetime.now()
        self.activity[context].append({
            "file": file_path,
            "event": event_type,
            "timestamp": now.isoformat(),
        })
        self.last_activity[context] = now

        # Trim old activity (keep last 100 per context)
        if len(self.activity[context]) > 100:
            self.activity[context] = self.activity[context][-100:]

    def get_active_context(self) -> Optional[str]:
        """Determine which context is currently active based on recent activity."""
        now = datetime.now()
        recent_contexts = []

        for context, last_time in self.last_activity.items():
            if last_time and (now - last_time).total_seconds() < self.activity_window:
                recent_contexts.append((context, last_time))

        if not recent_contexts:
            return None

        # Return most recently active context
        recent_contexts.sort(key=lambda x: x[1], reverse=True)
        return recent_contexts[0][0]

    def get_activity_summary(self) -> Dict[str, Any]:
        """Get summary of recent activity across all contexts."""
        now = datetime.now()
        summary = {}

        for context in ContextType.all():
            last = self.last_activity.get(context)
            if last:
                seconds_ago = (now - last).total_seconds()
                summary[context] = {
                    "last_activity": last.isoformat(),
                    "seconds_ago": int(seconds_ago),
                    "recent_files": len([
                        a for a in self.activity[context]
                        if (now - datetime.fromisoformat(a["timestamp"])).total_seconds() < self.activity_window
                    ]),
                }
            else:
                summary[context] = {"last_activity": None, "seconds_ago": None, "recent_files": 0}

        return summary


class ContextFileHandler(FileSystemEventHandler):
    """Handles file system events for context detection."""

    def __init__(self, tracker: FileActivityTracker, context: str):
        self.tracker = tracker
        self.context = context
        self.ignore_patterns = [
            "__pycache__",
            ".pyc",
            ".git",
            "node_modules",
            ".DS_Store",
            "*.log",
        ]

    def should_ignore(self, path: str) -> bool:
        """Check if path should be ignored."""
        for pattern in self.ignore_patterns:
            if pattern in path:
                return True
        return False

    def on_modified(self, event: FileSystemEvent):
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.tracker.record_activity(self.context, event.src_path, "modified")

    def on_created(self, event: FileSystemEvent):
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.tracker.record_activity(self.context, event.src_path, "created")

    def on_deleted(self, event: FileSystemEvent):
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.tracker.record_activity(self.context, event.src_path, "deleted")


class ContextManager:
    """
    Main context manager - orchestrates file watching and context updates.

    Usage:
        manager = ContextManager()
        manager.start()  # Start file watching

        # Get current active context
        context = manager.get_active_context()

        # Update context file
        manager.update_context_file(ContextType.DEV, "## Current Focus", "New content")

        manager.stop()  # Stop file watching
    """

    def __init__(self, db_session=None, fallback_mode: bool = False):
        self.tracker = FileActivityTracker()
        self.observer = Observer()
        self.db = db_session
        self.running = False
        self.max_context_lines = 500
        self.fallback_mode = fallback_mode

        # Server ports
        self.ports = {
            "backend": 5002 if fallback_mode else 5001,
            "frontend": 5174 if fallback_mode else 5173,
        }

    def start(self):
        """Start file watching for all contexts."""
        for context, dirs in ContextPaths.WATCH_DIRS.items():
            handler = ContextFileHandler(self.tracker, context)
            for dir_path in dirs:
                if dir_path.exists():
                    self.observer.schedule(handler, str(dir_path), recursive=True)

        self.observer.start()
        self.running = True

        mode_str = "FALLBACK" if self.fallback_mode else "NORMAL"
        print(f"[ContextManager] Started in {mode_str} mode")
        print(f"[ContextManager] Ports: backend={self.ports['backend']}, frontend={self.ports['frontend']}")
        print(f"[ContextManager] Watching {len(ContextPaths.WATCH_DIRS)} contexts")

    def stop(self):
        """Stop file watching."""
        self.observer.stop()
        self.observer.join()
        self.running = False
        print("[ContextManager] Stopped")

    def get_active_context(self) -> Optional[str]:
        """Get currently active context based on file activity."""
        return self.tracker.get_active_context()

    def get_activity_summary(self) -> Dict[str, Any]:
        """Get activity summary for all contexts."""
        return self.tracker.get_activity_summary()

    def get_context_file_path(self, context: str) -> Optional[Path]:
        """Get path to context file."""
        return ContextPaths.FILES.get(context)

    def read_context_file(self, context: str) -> Optional[str]:
        """Read a context file."""
        path = self.get_context_file_path(context)
        if path and path.exists():
            return path.read_text()
        return None

    def get_context_line_count(self, context: str) -> int:
        """Get line count of a context file."""
        content = self.read_context_file(context)
        if content:
            return len(content.split("\n"))
        return 0

    def update_context_file(self, context: str, section: str, content: str) -> bool:
        """
        Update a section in a context file.

        Args:
            context: Context type (oracle, dev, dash, crank, pocket)
            section: Section header to update (e.g., "## Current Focus")
            content: New content for the section

        Returns:
            True if update was successful
        """
        path = self.get_context_file_path(context)
        if not path or not path.exists():
            return False

        file_content = path.read_text()
        lines = file_content.split("\n")

        # Find section start
        section_start = None
        section_end = None
        for i, line in enumerate(lines):
            if line.strip().startswith(section):
                section_start = i
            elif section_start is not None and line.strip().startswith("## ") and i > section_start:
                section_end = i
                break

        if section_start is None:
            return False

        if section_end is None:
            section_end = len(lines)

        # Replace section
        new_lines = lines[:section_start + 1] + ["\n" + content + "\n"] + lines[section_end:]

        # Check line limit
        if len(new_lines) > self.max_context_lines:
            print(f"[ContextManager] Warning: {context} context exceeds {self.max_context_lines} lines")

        # Write back
        path.write_text("\n".join(new_lines))

        # Update timestamp
        self._update_timestamp(path)

        return True

    def _update_timestamp(self, path: Path):
        """Update the 'Last Updated' timestamp in a context file."""
        content = path.read_text()
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if line.startswith("**Last Updated:**"):
                lines[i] = f"**Last Updated:** {datetime.now().strftime('%B %d, %Y')}"
                break

        path.write_text("\n".join(lines))

    def create_snapshot(self, context: str, trigger: str = "manual") -> Dict:
        """Create a snapshot of a context's current state."""
        content = self.read_context_file(context)

        snapshot = {
            "context": context,
            "trigger": trigger,
            "timestamp": datetime.now().isoformat(),
            "line_count": len(content.split("\n")) if content else 0,
            "content_preview": content[:1000] if content else None,
        }

        if self.db:
            from app.models import Snapshot
            db_snapshot = Snapshot(
                context=context,
                data={"content": content},
                summary=f"Snapshot from {trigger}",
                trigger=trigger,
            )
            self.db.add(db_snapshot)
            self.db.commit()
            snapshot["id"] = db_snapshot.id

        return snapshot

    def get_unread_messages(self, context: str) -> List[Dict]:
        """Get unread messages for a context."""
        if not self.db:
            return []

        from app.models import Message
        messages = self.db.query(Message).filter(
            Message.to_context.in_([context, "all"]),
            Message.read_at.is_(None)
        ).order_by(Message.priority.desc(), Message.created_at.desc()).all()

        return [m.to_dict() for m in messages]

    def send_message(
        self,
        from_context: str,
        to_context: str,
        content: str,
        subject: str = None,
        priority: str = "normal",
        message_type: str = "info"
    ) -> Optional[Dict]:
        """Send a message to another context."""
        if not self.db:
            return None

        from app.models import Message
        message = Message(
            from_context=from_context,
            to_context=to_context,
            subject=subject,
            content=content,
            priority=priority,
            message_type=message_type,
        )
        self.db.add(message)
        self.db.commit()

        return message.to_dict()

    def record_session(
        self,
        session_id: str,
        context: str,
        task: str = None
    ) -> Optional[Dict]:
        """Record a new session or update existing one."""
        if not self.db:
            return None

        from app.models import Session, SessionStatus

        existing = self.db.query(Session).filter(
            Session.session_id == session_id
        ).first()

        if existing:
            existing.touch()
            existing.task = task or existing.task
            self.db.commit()
            return existing.to_dict()

        session = Session(
            session_id=session_id,
            context=context,
            task=task,
            status=SessionStatus.ACTIVE.value,
        )
        self.db.add(session)
        self.db.commit()

        return session.to_dict()

    def get_active_sessions(self) -> List[Dict]:
        """Get all active sessions across contexts."""
        if not self.db:
            return []

        from app.models import Session, SessionStatus
        sessions = self.db.query(Session).filter(
            Session.status == SessionStatus.ACTIVE.value
        ).order_by(Session.last_activity.desc()).all()

        return [s.to_dict() for s in sessions]

    def check_mini_status(self) -> bool:
        """Check if Mac Mini servers are reachable (for Pocket fallback)."""
        import socket

        try:
            # Try to connect to Mini's backend port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 5001))
            sock.close()
            return result == 0
        except Exception:
            return False


def run_context_watcher(fallback_mode: bool = False):
    """Run the context manager as a standalone watcher (for daemon mode)."""
    manager = ContextManager(fallback_mode=fallback_mode)
    manager.start()

    try:
        while True:
            time.sleep(10)
            summary = manager.get_activity_summary()
            active = manager.get_active_context()

            if active:
                print(f"[ContextWatcher] Active context: {active}")

            for ctx, data in summary.items():
                if data["recent_files"] > 0:
                    print(f"  {ctx}: {data['recent_files']} recent files")
    except KeyboardInterrupt:
        manager.stop()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fallback", action="store_true", help="Run in fallback mode (alternate ports)")
    args = parser.parse_args()

    run_context_watcher(fallback_mode=args.fallback)
