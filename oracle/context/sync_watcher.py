#!/usr/bin/env python3
"""
Oracle Sync Watcher - Monitors context docs and code directories for changes.

Brain Cell: Schwann Cells (myelinating peripheral nerves - signal transmission)
- Detects file changes across the codebase
- Logs changes to sync queue for Oracle to process
- Enables async communication between contexts

Watched Paths:
- Context docs: oracle/docs/context/*.md
- Code dirs: app/, scripts/, config/, oracle/, utils/

Usage:
    python oracle/context/sync_watcher.py start     # Start watcher
    python oracle/context/sync_watcher.py status    # Check status
    python oracle/context/sync_watcher.py log       # View sync log
    python oracle/context/sync_watcher.py clear     # Clear sync log
"""

import os
import sys
import json
import time
import hashlib
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Hippocampus for memory capture (P30 Phase 2)
try:
    from oracle.memory import Hippocampus, ObservationType
    MEMORY_ENABLED = True
except ImportError:
    MEMORY_ENABLED = False

# Sync log location
SYNC_LOG_PATH = PROJECT_ROOT / "data" / ".context_sync_log.json"
WATCHER_STATUS_PATH = PROJECT_ROOT / "data" / ".sync_watcher_status.json"
FILE_HASHES_PATH = PROJECT_ROOT / "data" / ".file_hashes.json"

# Watched paths
CONTEXT_DOCS_DIR = PROJECT_ROOT / "oracle" / "docs" / "context"
WATCHED_CODE_DIRS = [
    PROJECT_ROOT / "app",
    PROJECT_ROOT / "scripts",
    PROJECT_ROOT / "config",
    PROJECT_ROOT / "oracle",
    PROJECT_ROOT / "utils",
]

# File patterns to watch
CONTEXT_DOC_PATTERN = "*.md"
CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", ".yml"}

# Ignore patterns
IGNORE_PATTERNS = {
    "__pycache__",
    ".pyc",
    "node_modules",
    ".git",
    ".DS_Store",
    "venv",
    ".env",
    "*.log",
}


class SyncWatcher:
    """
    Watches for file changes and logs them for Oracle sync.
    """

    def __init__(self):
        self.file_hashes: Dict[str, str] = {}
        self.running = False
        self._ensure_data_dir()
        self._load_hashes()

        # Initialize Hippocampus memory capture (P30 Phase 2)
        self.memory = None
        if MEMORY_ENABLED:
            try:
                self.memory = Hippocampus()
            except Exception as e:
                print(f"Warning: Could not initialize Hippocampus: {e}")
                self.memory = None

    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        SYNC_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    def _load_hashes(self):
        """Load stored file hashes."""
        if FILE_HASHES_PATH.exists():
            try:
                self.file_hashes = json.loads(FILE_HASHES_PATH.read_text())
            except json.JSONDecodeError:
                self.file_hashes = {}

    def _save_hashes(self):
        """Save file hashes."""
        FILE_HASHES_PATH.write_text(json.dumps(self.file_hashes, indent=2))

    def _get_file_hash(self, path: Path) -> Optional[str]:
        """Get MD5 hash of file contents."""
        try:
            content = path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except (IOError, OSError):
            return None

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        path_str = str(path)
        for pattern in IGNORE_PATTERNS:
            if pattern in path_str:
                return True
        return False

    def _get_context_from_path(self, path: Path) -> Optional[str]:
        """Extract context name from file path."""
        name = path.stem.lower()

        # Context doc mapping
        context_map = {
            "oracle_context": "oracle",
            "dev_context": "dev",
            "dashboard_context": "dash",
            "crank_context": "crank",
            "pocket_context": "pocket",
        }

        if name in context_map:
            return context_map[name]

        # Code directory mapping
        path_str = str(path)
        if "/app/frontend/" in path_str:
            return "dash"
        elif "/app/" in path_str or "/scripts/" in path_str:
            return "dev"
        elif "/oracle/" in path_str:
            return "oracle"

        return None

    def _parse_context_doc(self, path: Path) -> Dict:
        """Parse context doc for session info."""
        try:
            content = path.read_text()

            # Extract session number
            session_match = re.search(r'\*\*Session:\*\*\s*(\w+\d+)', content)
            session = session_match.group(1) if session_match else None

            # Extract last updated
            updated_match = re.search(r'\*\*Last Updated:\*\*\s*([^\n]+)', content)
            updated = updated_match.group(1) if updated_match else None

            return {
                "session": session,
                "last_updated": updated,
            }
        except (IOError, OSError):
            return {}

    def _log_change(self, path: Path, change_type: str, details: Dict = None):
        """Log a file change to sync log."""
        # Load existing log
        log_entries = []
        if SYNC_LOG_PATH.exists():
            try:
                log_entries = json.loads(SYNC_LOG_PATH.read_text())
            except json.JSONDecodeError:
                log_entries = []

        # Create entry
        rel_path = str(path.relative_to(PROJECT_ROOT))
        context = self._get_context_from_path(path)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "path": rel_path,
            "change_type": change_type,
            "context": context,
            "details": details or {},
            "synced": False,
        }

        # Add context doc specific info
        if path.suffix == ".md" and "context" in rel_path.lower():
            doc_info = self._parse_context_doc(path)
            entry["details"].update(doc_info)

        log_entries.append(entry)

        # Keep last 100 entries
        if len(log_entries) > 100:
            log_entries = log_entries[-100:]

        SYNC_LOG_PATH.write_text(json.dumps(log_entries, indent=2))

        # Capture to Hippocampus memory (P30 Phase 2)
        if self.memory:
            try:
                # Build summary for Layer 1 searches
                filename = path.name
                summary = f"{change_type.capitalize()} {filename}"
                if context:
                    summary += f" ({context})"

                # Build details for Layer 3
                details_text = f"File: {rel_path}\nChange: {change_type}\n"
                if entry["details"].get("session"):
                    details_text += f"Session: {entry['details']['session']}\n"
                if entry["details"].get("last_updated"):
                    details_text += f"Last Updated: {entry['details']['last_updated']}\n"

                # Capture observation
                session_id = entry["details"].get("session") or "sync_watcher"
                self.memory.capture_file_change(
                    file_path=rel_path,
                    change_type=change_type,
                    session_id=session_id,
                    context=context or "unknown",
                    summary=summary
                )
            except Exception as e:
                # Don't fail if memory capture fails
                print(f"Warning: Could not capture to Hippocampus: {e}")

        return entry

    def _scan_directory(self, directory: Path, extensions: set = None) -> List[Path]:
        """Scan directory for files."""
        files = []

        if not directory.exists():
            return files

        for item in directory.rglob("*"):
            if item.is_file() and not self._should_ignore(item):
                if extensions is None or item.suffix in extensions:
                    files.append(item)

        return files

    def check_for_changes(self) -> List[Dict]:
        """Check all watched paths for changes."""
        changes = []
        current_hashes = {}

        # Check context docs
        context_docs = list(CONTEXT_DOCS_DIR.glob(CONTEXT_DOC_PATTERN))
        for doc in context_docs:
            if self._should_ignore(doc):
                continue

            path_key = str(doc.relative_to(PROJECT_ROOT))
            new_hash = self._get_file_hash(doc)
            current_hashes[path_key] = new_hash

            old_hash = self.file_hashes.get(path_key)

            if old_hash is None:
                # New file
                entry = self._log_change(doc, "created")
                changes.append(entry)
            elif old_hash != new_hash:
                # Modified file
                entry = self._log_change(doc, "modified")
                changes.append(entry)

        # Check code directories
        for code_dir in WATCHED_CODE_DIRS:
            code_files = self._scan_directory(code_dir, CODE_EXTENSIONS)

            for code_file in code_files:
                if self._should_ignore(code_file):
                    continue

                path_key = str(code_file.relative_to(PROJECT_ROOT))
                new_hash = self._get_file_hash(code_file)
                current_hashes[path_key] = new_hash

                old_hash = self.file_hashes.get(path_key)

                if old_hash is None:
                    entry = self._log_change(code_file, "created")
                    changes.append(entry)
                elif old_hash != new_hash:
                    entry = self._log_change(code_file, "modified")
                    changes.append(entry)

        # Check for deleted files
        for path_key in list(self.file_hashes.keys()):
            if path_key not in current_hashes:
                full_path = PROJECT_ROOT / path_key
                entry = self._log_change(full_path, "deleted")
                changes.append(entry)

        # Update stored hashes
        self.file_hashes = current_hashes
        self._save_hashes()

        return changes

    def start(self, interval: int = 30, background: bool = False):
        """Start the watcher loop."""
        print("=" * 60)
        print("ORACLE SYNC WATCHER - File Change Monitor")
        print("=" * 60)
        print(f"Started at: {datetime.now().isoformat()}")
        print(f"Check interval: {interval}s")
        print(f"Context docs: {CONTEXT_DOCS_DIR}")
        print(f"Code dirs: {[str(d.relative_to(PROJECT_ROOT)) for d in WATCHED_CODE_DIRS]}")
        print()

        self.running = True
        self._write_status("running")

        # Initial scan
        print("[Watcher] Running initial scan...")
        initial_changes = self.check_for_changes()
        print(f"[Watcher] Found {len(initial_changes)} initial items")

        if background:
            print("[Watcher] Running in background mode")
            return

        try:
            while self.running:
                time.sleep(interval)
                changes = self.check_for_changes()

                if changes:
                    print(f"\n[Watcher] {datetime.now().strftime('%H:%M:%S')} - {len(changes)} change(s) detected:")
                    for change in changes:
                        ctx = change.get("context", "unknown")
                        print(f"  [{ctx}] {change['change_type']}: {change['path']}")
                        if change.get("details", {}).get("session"):
                            print(f"       Session: {change['details']['session']}")

        except KeyboardInterrupt:
            print("\n[Watcher] Shutting down...")
        finally:
            self.stop()

    def stop(self):
        """Stop the watcher."""
        self.running = False
        self._write_status("stopped")
        print("[Watcher] Stopped")

    def _write_status(self, state: str):
        """Write watcher status."""
        status = {
            "state": state,
            "pid": os.getpid(),
            "updated_at": datetime.now().isoformat(),
        }
        WATCHER_STATUS_PATH.write_text(json.dumps(status, indent=2))

    def get_status(self) -> Dict:
        """Get watcher status."""
        if WATCHER_STATUS_PATH.exists():
            try:
                return json.loads(WATCHER_STATUS_PATH.read_text())
            except json.JSONDecodeError:
                pass
        return {"state": "unknown"}

    def get_unsynced_changes(self) -> List[Dict]:
        """Get changes that haven't been synced to Oracle."""
        if not SYNC_LOG_PATH.exists():
            return []

        try:
            entries = json.loads(SYNC_LOG_PATH.read_text())
            return [e for e in entries if not e.get("synced", False)]
        except json.JSONDecodeError:
            return []

    def mark_synced(self, before_timestamp: str = None):
        """Mark entries as synced."""
        if not SYNC_LOG_PATH.exists():
            return

        try:
            entries = json.loads(SYNC_LOG_PATH.read_text())

            for entry in entries:
                if before_timestamp is None or entry["timestamp"] <= before_timestamp:
                    entry["synced"] = True

            SYNC_LOG_PATH.write_text(json.dumps(entries, indent=2))
        except json.JSONDecodeError:
            pass

    def get_context_summary(self) -> Dict:
        """Get summary of changes by context."""
        unsynced = self.get_unsynced_changes()

        summary = {}
        for entry in unsynced:
            ctx = entry.get("context") or "other"
            if ctx not in summary:
                summary[ctx] = {
                    "count": 0,
                    "latest_session": None,
                    "files": [],
                }

            summary[ctx]["count"] += 1
            summary[ctx]["files"].append(entry["path"])

            # Track latest session for context docs
            if entry.get("details", {}).get("session"):
                summary[ctx]["latest_session"] = entry["details"]["session"]

        return summary

    def clear_log(self):
        """Clear the sync log."""
        if SYNC_LOG_PATH.exists():
            SYNC_LOG_PATH.unlink()
        if FILE_HASHES_PATH.exists():
            FILE_HASHES_PATH.unlink()
        self.file_hashes = {}
        print("[Watcher] Sync log cleared")


def show_log():
    """Display the sync log."""
    watcher = SyncWatcher()
    unsynced = watcher.get_unsynced_changes()

    print("\n" + "=" * 60)
    print("ORACLE SYNC LOG - Unsynced Changes")
    print("=" * 60)

    if not unsynced:
        print("\nNo unsynced changes.")
        return

    # Group by context
    summary = watcher.get_context_summary()

    for ctx, data in summary.items():
        print(f"\n{ctx.upper()} ({data['count']} changes):")
        if data.get("latest_session"):
            print(f"  Latest session: {data['latest_session']}")
        for f in data["files"][-5:]:  # Show last 5 files
            print(f"  - {f}")
        if len(data["files"]) > 5:
            print(f"  ... and {len(data['files']) - 5} more")


def show_status():
    """Display watcher status."""
    watcher = SyncWatcher()
    status = watcher.get_status()

    print("\n" + "=" * 60)
    print("ORACLE SYNC WATCHER STATUS")
    print("=" * 60)
    print(f"State: {status.get('state', 'unknown')}")
    print(f"PID: {status.get('pid', 'N/A')}")
    print(f"Last updated: {status.get('updated_at', 'N/A')}")

    # Show summary
    summary = watcher.get_context_summary()
    if summary:
        print(f"\nUnsynced changes by context:")
        for ctx, data in summary.items():
            session_info = f" (session: {data['latest_session']})" if data.get("latest_session") else ""
            print(f"  {ctx}: {data['count']} changes{session_info}")


def main():
    parser = argparse.ArgumentParser(description="Oracle Sync Watcher")
    parser.add_argument("command", choices=["start", "status", "log", "clear", "check"],
                        help="Command to run")
    parser.add_argument("--interval", type=int, default=30,
                        help="Check interval in seconds (default: 30)")
    parser.add_argument("--background", action="store_true",
                        help="Run in background mode")

    args = parser.parse_args()

    watcher = SyncWatcher()

    if args.command == "start":
        watcher.start(interval=args.interval, background=args.background)
    elif args.command == "status":
        show_status()
    elif args.command == "log":
        show_log()
    elif args.command == "clear":
        watcher.clear_log()
    elif args.command == "check":
        # One-time check
        print("[Watcher] Running one-time check...")
        changes = watcher.check_for_changes()
        if changes:
            print(f"[Watcher] {len(changes)} change(s) detected:")
            for change in changes:
                ctx = change.get("context", "unknown")
                print(f"  [{ctx}] {change['change_type']}: {change['path']}")
        else:
            print("[Watcher] No changes detected")


if __name__ == "__main__":
    main()
