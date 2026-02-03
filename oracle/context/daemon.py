#!/usr/bin/env python3
"""
Oracle Daemon - Background service for context management and cross-session communication.

Contexts:
- Oracle: Planning, docs, health monitoring (coordinator)
- Dev: Backend development (app/, scripts/, config/)
- Dash: Frontend development (dashboard/)
- Crank: Content production (no code changes)
- Pocket: Mobile/backup on M1 Air (fallback ports)

Features:
- File watching for context detection
- Cross-session messaging with handoff rules
- Health monitoring
- Session spawning
- Fallback mode for Pocket (alternate ports 5002/5174)

Usage:
    python oracle/context/daemon.py start              # Start daemon
    python oracle/context/daemon.py start --fallback   # Start in fallback mode (Pocket)
    python oracle/context/daemon.py status             # Check status
    python oracle/context/daemon.py spawn dev          # Spawn session for context
    python oracle/context/daemon.py send dev dash "New API ready"  # Send message
    python oracle/context/daemon.py messages           # Show pending messages
    python oracle/context/daemon.py audit              # Run health audit
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Up from context/ to oracle/ to root
sys.path.insert(0, str(PROJECT_ROOT))

from oracle.context.context_manager import ContextManager, ContextType, ContextPaths
from oracle.context.session_spawner import SessionSpawner, HANDOFF_RULES
from oracle.context import get_context_ids


# P25: All valid contexts loaded from registry
def _get_all_contexts():
    """Get all context IDs from registry with fallback."""
    ids = get_context_ids()
    return ids if ids else ["oracle", "dev", "dash", "crank", "pocket"]


ALL_CONTEXTS = _get_all_contexts()


class OracleDaemon:
    """
    Oracle Daemon - Main control center for the media engine.

    Combines:
    - Context detection and file watching
    - Cross-session messaging
    - Health monitoring
    - Session spawning
    """

    def __init__(self, fallback_mode: bool = False):
        self.fallback_mode = fallback_mode
        self.context_manager = ContextManager(fallback_mode=fallback_mode)
        self.session_spawner = SessionSpawner(fallback_mode=fallback_mode)
        self.running = False

        # Status file for daemon state
        self.status_file = PROJECT_ROOT / "data" / ".oracle_status.json"
        self.status_file.parent.mkdir(parents=True, exist_ok=True)

        # Message queue file (simple file-based messaging)
        self.message_file = PROJECT_ROOT / "data" / ".oracle_messages.json"

    def start(self, background: bool = False):
        """Start the Oracle daemon."""
        mode_str = "FALLBACK (Pocket)" if self.fallback_mode else "NORMAL"
        ports = self.context_manager.ports

        print("=" * 60)
        print("ORACLE DAEMON - Media Engine V2 Control Center")
        print("=" * 60)
        print(f"Mode: {mode_str}")
        print(f"Started at: {datetime.now().isoformat()}")
        print(f"Project root: {PROJECT_ROOT}")
        print(f"Ports: backend={ports['backend']}, frontend={ports['frontend']}")
        print(f"Contexts: {', '.join(ALL_CONTEXTS)}")
        print()

        # Start file watching
        self.context_manager.start()
        self.running = True

        # Write status file
        self._write_status("running")

        if background:
            print("[Oracle] Running in background mode")
            return

        # Main loop
        try:
            while self.running:
                self._loop_iteration()
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\n[Oracle] Shutting down...")
        finally:
            self.stop()

    def stop(self):
        """Stop the Oracle daemon."""
        self.context_manager.stop()
        self.running = False
        self._write_status("stopped")
        print("[Oracle] Daemon stopped")

    def _loop_iteration(self):
        """Single iteration of the main loop."""
        # Get activity summary
        summary = self.context_manager.get_activity_summary()
        active = self.context_manager.get_active_context()

        # Update status
        status = {
            "active_context": active,
            "activity": summary,
            "last_check": datetime.now().isoformat(),
        }
        self._write_status("running", status)

        # Print status if there's activity
        active_contexts = [ctx for ctx, data in summary.items() if data["recent_files"] > 0]
        if active_contexts:
            print(f"\n[Oracle] Active contexts: {', '.join(active_contexts)}")
            for ctx in active_contexts:
                print(f"  {ctx}: {summary[ctx]['recent_files']} recent files")

    def _write_status(self, state: str, data: dict = None):
        """Write daemon status to file."""
        status = {
            "state": state,
            "pid": os.getpid(),
            "updated_at": datetime.now().isoformat(),
            "data": data or {},
        }
        self.status_file.write_text(json.dumps(status, indent=2))

    def get_status(self) -> dict:
        """Get daemon status."""
        if self.status_file.exists():
            return json.loads(self.status_file.read_text())
        return {"state": "unknown"}

    def spawn_session(self, context: str, task: str = None, use_claude: bool = False):
        """Spawn a new session for a context."""
        if use_claude:
            result = self.session_spawner.spawn_with_claude(context, task)
        else:
            result = self.session_spawner.spawn(context, task)

        if result.get("success"):
            print(f"[Oracle] Spawned {context} session: {result['session_id']}")
        else:
            print(f"[Oracle] Failed to spawn session: {result.get('error')}")

        return result

    def show_messages(self, context: str = None):
        """Show pending messages."""
        # Without database, just show context activity
        summary = self.context_manager.get_activity_summary()

        print("\n" + "=" * 60)
        print("ORACLE - Context Activity Summary")
        print("=" * 60)

        for ctx, data in summary.items():
            if context and ctx != context:
                continue

            print(f"\n{ctx.upper()}:")
            if data["last_activity"]:
                print(f"  Last activity: {data['last_activity']}")
                print(f"  Seconds ago: {data['seconds_ago']}")
                print(f"  Recent files: {data['recent_files']}")
            else:
                print("  No recent activity")

    def send_message(
        self,
        from_ctx: str,
        to_ctx: str,
        content: str,
        msg_type: str = "info",
        priority: str = "normal"
    ) -> dict:
        """
        Send a message from one context to another.

        Validates against HANDOFF_RULES to ensure proper communication paths.
        """
        # Validate contexts
        if from_ctx not in ALL_CONTEXTS or to_ctx not in ALL_CONTEXTS:
            return {"success": False, "error": f"Invalid context. Must be one of: {ALL_CONTEXTS}"}

        # Check handoff rules (oracle can send to anyone)
        if from_ctx != "oracle":
            allowed = HANDOFF_RULES.get(from_ctx, {}).get("sends_to", {})
            if to_ctx not in allowed and to_ctx != "oracle":
                return {
                    "success": False,
                    "error": f"{from_ctx} cannot send to {to_ctx}. Allowed: {list(allowed.keys()) + ['oracle']}"
                }

        # Load existing messages
        messages = self._load_messages()

        # Create message
        msg = {
            "id": len(messages) + 1,
            "from": from_ctx,
            "to": to_ctx,
            "content": content,
            "type": msg_type,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "read_at": None,
        }

        messages.append(msg)
        self._save_messages(messages)

        print(f"[Oracle] Message sent: {from_ctx} → {to_ctx}")
        return {"success": True, "message": msg}

    def _load_messages(self) -> list:
        """Load messages from file."""
        if self.message_file.exists():
            return json.loads(self.message_file.read_text())
        return []

    def _save_messages(self, messages: list):
        """Save messages to file."""
        self.message_file.write_text(json.dumps(messages, indent=2))

    def get_messages_for(self, context: str, unread_only: bool = True) -> list:
        """Get messages for a specific context."""
        messages = self._load_messages()
        filtered = [
            m for m in messages
            if (m["to"] == context or m["to"] == "all")
            and (not unread_only or m["read_at"] is None)
        ]
        return sorted(filtered, key=lambda x: (
            {"urgent": 0, "high": 1, "normal": 2, "low": 3}.get(x["priority"], 2),
            x["created_at"]
        ))

    def mark_read(self, message_id: int):
        """Mark a message as read."""
        messages = self._load_messages()
        for msg in messages:
            if msg["id"] == message_id:
                msg["read_at"] = datetime.now().isoformat()
                break
        self._save_messages(messages)

    def show_handoff_rules(self):
        """Display the handoff rules between contexts."""
        print("\n" + "=" * 60)
        print("ORACLE - Cross-Session Handoff Rules")
        print("=" * 60)

        for ctx, rules in HANDOFF_RULES.items():
            print(f"\n{ctx.upper()}:")

            sends_to = rules.get("sends_to", {})
            if sends_to:
                print("  Sends to:")
                for target, msg_types in sends_to.items():
                    print(f"    → {target}: {', '.join(msg_types)}")

            receives = rules.get("receives_from", {})
            if receives:
                print("  Receives from:")
                for source, msg_types in receives.items():
                    print(f"    ← {source}: {', '.join(msg_types)}")

        print("\n  Note: Oracle can send/receive to/from all contexts")
        print("=" * 60)

    def run_audit(self, quick: bool = False):
        """Run a health audit."""
        print("\n" + "=" * 60)
        print("ORACLE - Health Audit")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Mode: {'FALLBACK' if self.fallback_mode else 'NORMAL'}")
        print()

        # Check context files (all 5)
        print("Context Files:")
        for ctx in ALL_CONTEXTS:
            path = self.context_manager.get_context_file_path(ctx)
            if path and path.exists():
                lines = self.context_manager.get_context_line_count(ctx)
                status = "⚠️ OVER LIMIT" if lines > 500 else "✓"
                print(f"  {ctx}: {lines} lines {status}")
            else:
                print(f"  {ctx}: ❌ NOT FOUND")

        # Check key directories
        print("\nKey Directories:")
        dirs_to_check = [
            ("app/", "Backend + Frontend (V2)"),
            ("app/frontend/src/", "Frontend code"),
            ("oracle/", "Oracle code"),
            ("config/", "Configuration"),
            ("oracle/docs/context/", "Context files"),
        ]

        for dir_path, desc in dirs_to_check:
            full_path = PROJECT_ROOT / dir_path
            if full_path.exists():
                file_count = len(list(full_path.rglob("*")))
                print(f"  {dir_path}: ✓ ({file_count} items)")
            else:
                print(f"  {dir_path}: ❌ NOT FOUND")

        if not quick:
            # Check database
            print("\nDatabase:")
            db_path = PROJECT_ROOT / "data" / "oracle.db"
            if db_path.exists():
                size_mb = db_path.stat().st_size / (1024 * 1024)
                print(f"  oracle.db: ✓ ({size_mb:.2f} MB)")
            else:
                print("  oracle.db: Not found (will be created on first use)")

        print("\n" + "=" * 60)

    def show_prompts(self):
        """Show resume prompts for all contexts."""
        self.session_spawner.print_resume_prompts()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Oracle Daemon - Media Engine V2 Control Center"
    )

    # Global fallback flag
    parser.add_argument("--fallback", "-f", action="store_true",
                       help="Run in fallback mode (Pocket - alternate ports)")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # start command
    start_parser = subparsers.add_parser("start", help="Start the daemon")
    start_parser.add_argument("--background", "-b", action="store_true", help="Run in background")

    # status command
    subparsers.add_parser("status", help="Show daemon status")

    # spawn command
    spawn_parser = subparsers.add_parser("spawn", help="Spawn a session")
    spawn_parser.add_argument("context", choices=ALL_CONTEXTS)
    spawn_parser.add_argument("--task", "-t", help="Task description")
    spawn_parser.add_argument("--claude", "-c", action="store_true", help="Use Claude Code")

    # send command (cross-session messaging)
    send_parser = subparsers.add_parser("send", help="Send message to another context")
    send_parser.add_argument("from_ctx", choices=ALL_CONTEXTS, help="Sending context")
    send_parser.add_argument("to_ctx", choices=ALL_CONTEXTS, help="Receiving context")
    send_parser.add_argument("content", help="Message content")
    send_parser.add_argument("--type", "-t", default="info",
                            choices=["info", "request", "handoff", "alert"],
                            help="Message type")
    send_parser.add_argument("--priority", "-p", default="normal",
                            choices=["low", "normal", "high", "urgent"],
                            help="Message priority")

    # messages command
    msg_parser = subparsers.add_parser("messages", help="Show messages")
    msg_parser.add_argument("--context", "-c", choices=ALL_CONTEXTS, help="Filter by context")
    msg_parser.add_argument("--all", "-a", action="store_true", help="Show all messages (including read)")

    # rules command
    subparsers.add_parser("rules", help="Show handoff rules between contexts")

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Run health audit")
    audit_parser.add_argument("--quick", "-q", action="store_true", help="Quick audit")

    # prompts command
    subparsers.add_parser("prompts", help="Show resume prompts")

    # prompt command (write single prompt to file)
    prompt_parser = subparsers.add_parser("prompt", help="Write prompt to .claude_prompt file")
    prompt_parser.add_argument("context", choices=ALL_CONTEXTS)
    prompt_parser.add_argument("--task", "-t", help="Task description")

    # context command
    subparsers.add_parser("context", help="Show active context")

    args = parser.parse_args()

    # Create daemon with fallback mode
    daemon = OracleDaemon(fallback_mode=args.fallback)

    if args.command == "start":
        daemon.start(background=args.background)

    elif args.command == "status":
        status = daemon.get_status()
        print(json.dumps(status, indent=2))

    elif args.command == "spawn":
        daemon.spawn_session(args.context, args.task, args.claude)

    elif args.command == "send":
        result = daemon.send_message(
            args.from_ctx,
            args.to_ctx,
            args.content,
            msg_type=args.type,
            priority=args.priority
        )
        if not result["success"]:
            print(f"Error: {result['error']}")

    elif args.command == "messages":
        if args.context:
            # Show messages for specific context
            messages = daemon.get_messages_for(args.context, unread_only=not args.all)
            print(f"\n{'=' * 60}")
            print(f"Messages for {args.context.upper()}")
            print(f"{'=' * 60}")
            if messages:
                for msg in messages:
                    status = "📬" if msg["read_at"] is None else "✓"
                    priority_icon = {"urgent": "🔴", "high": "🟠", "normal": "🟢", "low": "⚪"}.get(msg["priority"], "")
                    print(f"\n{status} {priority_icon} [{msg['id']}] From: {msg['from']}")
                    print(f"   {msg['content']}")
                    print(f"   ({msg['type']}) - {msg['created_at'][:16]}")
            else:
                print("\nNo messages")
        else:
            daemon.show_messages()

    elif args.command == "rules":
        daemon.show_handoff_rules()

    elif args.command == "audit":
        daemon.run_audit(quick=args.quick)

    elif args.command == "prompts":
        daemon.show_prompts()

    elif args.command == "prompt":
        # Write prompt to file without spawning VS Code
        prompt_file = daemon.session_spawner.write_prompt_file(args.context, args.task)
        print(f"Prompt written to: {prompt_file}")
        print(f"Context: {args.context}")
        if args.task:
            print(f"Task: {args.task}")

    elif args.command == "context":
        # Quick check without starting daemon
        manager = ContextManager(fallback_mode=args.fallback)
        summary = manager.get_activity_summary()
        print(f"Mode: {'FALLBACK' if args.fallback else 'NORMAL'}")
        print(f"Active context: {manager.get_active_context() or 'None'}")
        print("\nActivity summary:")
        for ctx, data in summary.items():
            print(f"  {ctx}: {data['recent_files']} recent files")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
