"""
Session Spawner - Spawn VS Code/Claude Code sessions with correct context.

P25: Now uses dynamic context registry (oracle/context/context_registry.json) for
project-agnostic configuration. Contexts, handoff rules, and ports are
all configurable via JSON.

P30: Enhanced with Hippocampus memory integration. Resume prompts can optionally
include relevant recent observations for cross-session intelligence.

Cross-Session Handoffs:
- Configured in context_registry.json handoff_rules
- Dash → Dev: Custom preset requests, API changes
- Dash → Crank: Content generation requests
- Crank → Dev: Bug reports (no fixes in Crank)
- Dev → Dash: New features to expose in UI
- Oracle → All: Coordination, health alerts
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# P30: Import Hippocampus for memory integration
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from oracle.memory import Hippocampus
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Up from context/ to oracle/ to root


# P25: Registry helper functions (imported from __init__.py)
def _load_registry() -> Dict:
    """Load context registry from JSON."""
    registry_path = PROJECT_ROOT / "oracle" / "context" / "context_registry.json"
    if registry_path.exists():
        return json.loads(registry_path.read_text())
    return {"contexts": [], "handoff_rules": {}, "ports": {}}


def _get_context_ids() -> List[str]:
    """Get all context IDs from registry."""
    return [ctx.get("id") for ctx in _load_registry().get("contexts", [])]


class ContextType:
    """Context type constants - loaded from registry with fallbacks."""
    ORACLE = "oracle"
    DEV = "dev"
    DASH = "dash"
    CRANK = "crank"
    POCKET = "pocket"

    @classmethod
    def all(cls) -> List[str]:
        """Get all context IDs from registry."""
        ids = _get_context_ids()
        return ids if ids else [cls.ORACLE, cls.DEV, cls.DASH, cls.CRANK, cls.POCKET]


# P25: Load handoff rules from registry (with fallback to hardcoded)
def _get_handoff_rules() -> Dict:
    """Load handoff rules from registry, converting to sends_to/receives_from format."""
    registry = _load_registry()
    registry_rules = registry.get("handoff_rules", {})

    if not registry_rules:
        # Fallback to hardcoded rules if registry is empty
        return {
            ContextType.DASH: {
                "sends_to": {
                    ContextType.DEV: ["custom_preset_request", "api_change_request", "backend_bug"],
                    ContextType.CRANK: ["content_generation_request"],
                },
            },
            ContextType.CRANK: {
                "sends_to": {
                    ContextType.DEV: ["bug_report"],
                    ContextType.DASH: ["content_ready"],
                },
            },
            ContextType.DEV: {
                "sends_to": {
                    ContextType.DASH: ["new_feature_available", "preset_added", "api_updated"],
                    ContextType.CRANK: ["preset_fixed", "new_preset"],
                },
            },
            ContextType.ORACLE: {
                "sends_to": {
                    ContextType.DEV: ["health_alert", "task_assignment"],
                    ContextType.DASH: ["health_alert", "task_assignment"],
                    ContextType.CRANK: ["health_alert", "task_assignment"],
                    ContextType.POCKET: ["sync_request"],
                },
            },
            ContextType.POCKET: {
                "sends_to": {
                    ContextType.ORACLE: ["sync_complete", "fallback_active"],
                },
            },
        }

    # Convert registry format to internal format
    # Registry: {"dash": {"to": ["dev", "crank"], "types": [...]}}
    # Internal: {"dash": {"sends_to": {"dev": [...], "crank": [...]}}}
    rules = {}
    for ctx_id, rule_def in registry_rules.items():
        targets = rule_def.get("to", [])
        types = rule_def.get("types", [])

        # Handle "*" as all contexts
        if "*" in targets:
            targets = [c for c in _get_context_ids() if c != ctx_id]

        rules[ctx_id] = {
            "sends_to": {target: types for target in targets}
        }

    return rules


# Lazy-loaded handoff rules
HANDOFF_RULES = _get_handoff_rules()


class SessionSpawner:
    """
    Spawn and manage VS Code/Claude Code sessions.

    Usage:
        spawner = SessionSpawner()

        # Spawn a new dev session
        spawner.spawn(ContextType.DEV, task="Fix L3 adapter bug")

        # Get resume prompt for a context
        prompt = spawner.get_resume_prompt(ContextType.DASH)

        # Send cross-session message
        spawner.send_handoff(ContextType.DASH, ContextType.DEV, "custom_preset_request", {...})
    """

    def __init__(self, db_session=None, fallback_mode: bool = False):
        self.db = db_session
        self.project_root = PROJECT_ROOT
        self.fallback_mode = fallback_mode

        # P25: Load configuration from registry
        registry = _load_registry()
        context_path = registry.get("context_path", "oracle/docs/context/")

        # Context file paths - built from registry
        self.context_files = {}
        self.session_prefixes = {}
        for ctx in registry.get("contexts", []):
            ctx_id = ctx.get("id")
            if ctx_id:
                self.context_files[ctx_id] = self.project_root / context_path / ctx.get("file", f"{ctx_id.upper()}_CONTEXT.md")
                self.session_prefixes[ctx_id] = ctx.get("prefix", ctx_id[0].upper())

        # Server ports from registry (normal vs fallback)
        self.server_ports = registry.get("ports", {
            "normal": {"backend": 5001, "frontend": 5173},
            "fallback": {"backend": 5002, "frontend": 5174},
        })

        # Active ports based on mode
        self.ports = self.server_ports.get("fallback" if fallback_mode else "normal", {"backend": 5001, "frontend": 5173})

    def get_next_session_id(self, context: str) -> str:
        """Generate next session ID for a context."""
        prefix = self.session_prefixes.get(context, "S")

        if self.db:
            from app.models import Session
            sessions = self.db.query(Session).filter(
                Session.context == context
            ).all()

            max_num = 0
            for s in sessions:
                try:
                    num = int(s.session_id.replace(prefix, ""))
                    max_num = max(max_num, num)
                except ValueError:
                    pass

            return f"{prefix}{max_num + 1}"

        return f"{prefix}{datetime.now().strftime('%H%M')}"

    def _get_memory_context(self, context: str, days_back: int = 3, limit: int = 5) -> str:
        """
        Get relevant memory context for resume prompt (P30).

        Searches Hippocampus for recent decisions, features, and important changes
        relevant to this context.

        Args:
            context: Context name (oracle, dev, dash, etc.)
            days_back: Days to search back (default: 3)
            limit: Max observations to include (default: 5)

        Returns:
            Formatted memory section for resume prompt, or empty string if unavailable
        """
        if not MEMORY_AVAILABLE:
            return ""

        try:
            hippo = Hippocampus()

            # Normalize context name (capitalize for consistency with observations)
            context_normalized = context.capitalize()

            # Get recent high-value observations
            # Priority: decisions > session events > file changes
            memory_lines = []

            # 1. Recent decisions for this context
            decisions = hippo.search(
                query="",
                context=context_normalized,
                observation_type="decision",
                days_back=days_back,
                limit=3
            )
            if decisions:
                memory_lines.append("Recent Decisions:")
                for obs in decisions[:2]:  # Top 2
                    memory_lines.append(f"  • {obs.get('summary')}")

            # 2. Session events (completions, milestones)
            sessions = hippo.search(
                query="",
                context=context_normalized,
                observation_type="session_event",
                days_back=days_back,
                limit=3
            )
            if sessions:
                if memory_lines:
                    memory_lines.append("")
                memory_lines.append("Recent Sessions:")
                for obs in sessions[:2]:  # Top 2
                    memory_lines.append(f"  • {obs.get('summary')}")

            # 3. File changes (most active files)
            patterns = hippo.detect_patterns(days_back=days_back)
            file_patterns = [p for p in patterns if p.pattern_type == "repeated_file"]
            if file_patterns:
                if memory_lines:
                    memory_lines.append("")
                memory_lines.append("Active Files:")
                for pattern in file_patterns[:3]:  # Top 3
                    file_path = pattern.description.split(": ")[1] if ": " in pattern.description else "unknown"
                    memory_lines.append(f"  • {file_path} ({pattern.occurrence_count}x)")

            if memory_lines:
                return "\n\n---\n🧠 Memory Context (last " + str(days_back) + " days):\n" + "\n".join(memory_lines) + "\n---"

            return ""

        except Exception as e:
            # Silently fail if memory system not available
            return ""

    def get_resume_prompt(self, context: str, task: str = None, include_memory: bool = True) -> str:
        """Generate a resume prompt for a context.

        P25: First checks registry for resume_prompt, falls back to detailed prompts.
        P30: Optionally includes memory context from Hippocampus.

        Args:
            context: Context name
            task: Optional specific task description
            include_memory: Include relevant observations from Hippocampus (default: True)
        """
        context_file = self.context_files.get(context)
        if not context_file:
            return f"Unknown context: {context}"

        # P25: Check registry for resume_prompt first
        registry = _load_registry()
        for ctx in registry.get("contexts", []):
            if ctx.get("id") == context:
                resume_prompt = ctx.get("resume_prompt")
                if resume_prompt:
                    prompt = resume_prompt
                    if task:
                        prompt += f"\n\nCurrent task: {task}"
                    # P30: Add memory context if available
                    if include_memory:
                        memory = self._get_memory_context(context)
                        if memory:
                            prompt += memory
                    return prompt

        # Fallback: detailed prompts (project-specific, kept for backward compatibility)
        base_prompts = {
            ContextType.ORACLE: """You are Oracle. Read @oracle/docs/context/ORACLE_CONTEXT.md first.

Role: Planning, documentation, health monitoring, cross-session coordination.

Responsibilities:
- Coordinate Dev, Dash, Crank, Pocket sessions
- Maintain context files and documentation
- Run health audits (python oracle/daemon.py audit)
- Spawn sessions (python oracle/daemon.py spawn <ctx>)
- Monitor cross-session messages""",

            ContextType.DEV: """You are Dev. Read @oracle/docs/context/DEV_CONTEXT.md first.

Role: Backend development - adapters, services, pipeline, presets.

Scope: app/, scripts/, config/ (NO dashboard/ changes)

Servers: Backend http://localhost:5001/""",

            ContextType.DASH: """You are Dash. Read @oracle/docs/context/DASHBOARD_CONTEXT.md first.

Role: Frontend React development - UI components, API integration.

Scope: dashboard/ only (NO app/ or scripts/ changes)

Servers: Frontend http://localhost:5173/""",

            ContextType.CRANK: """You are Crank. Read @oracle/docs/context/CRANK_CONTEXT.md first.

Role: Content production - generate content using pipeline. NO CODE CHANGES.

Scope: Run pipeline commands, check quality, note bugs for Dev.""",

            ContextType.POCKET: """You are Pocket. Read @oracle/docs/context/POCKET_CONTEXT.md first.

Role: Mobile/backup on M1 MacBook Air. Fallback if Mac Mini crashes.

Normal Mode: Read-only access, light tasks, mobile work
Fallback Mode: Full server operation if Mini is down""",
        }

        prompt = base_prompts.get(context, f"Read @oracle/docs/context/{context.upper()}_CONTEXT.md")

        if task:
            prompt += f"\n\nCurrent task: {task}"

        # P30: Add memory context if available
        if include_memory:
            memory = self._get_memory_context(context)
            if memory:
                prompt += memory

        return prompt

    def write_prompt_file(self, context: str, task: str = None, include_memory: bool = True) -> Path:
        """
        Write resume prompt to .claude_prompt file for VS Code task integration.

        P30: Optionally includes memory context from Hippocampus.
        """
        prompt = self.get_resume_prompt(context, task, include_memory=include_memory)
        prompt_file = self.project_root / ".claude_prompt"
        prompt_file.write_text(prompt)
        return prompt_file

    def spawn(
        self,
        context: str,
        task: str = None,
        new_window: bool = True,
        wait: bool = False
    ) -> Dict:
        """Spawn a new VS Code session with the correct context."""
        session_id = self.get_next_session_id(context)
        context_file = self.context_files.get(context)

        if not context_file or not context_file.exists():
            return {
                "success": False,
                "error": f"Context file not found: {context_file}",
            }

        # Write prompt file for VS Code task integration
        prompt_file = self.write_prompt_file(context, task)

        cmd = ["code"]
        if new_window:
            cmd.append("-n")
        if wait:
            cmd.append("-w")

        cmd.extend([str(self.project_root), str(context_file)])

        result = {
            "session_id": session_id,
            "context": context,
            "task": task,
            "context_file": str(context_file),
            "prompt_file": str(prompt_file),
            "command": " ".join(cmd),
            "spawned_at": datetime.now().isoformat(),
        }

        try:
            subprocess.Popen(cmd, start_new_session=True)
            result["success"] = True
            print(f"[SessionSpawner] Prompt written to .claude_prompt")

            if self.db:
                from app.models import Session, SessionStatus
                session = Session(
                    session_id=session_id,
                    context=context,
                    task=task,
                    status=SessionStatus.ACTIVE.value,
                )
                self.db.add(session)
                self.db.commit()
                result["db_id"] = session.id

            print(f"[SessionSpawner] Spawned {context} session: {session_id}")

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)

        return result

    def spawn_with_claude(
        self,
        context: str,
        task: str = None,
        model: str = "opus"
    ) -> Dict:
        """Spawn a new Claude Code session with the correct context."""
        session_id = self.get_next_session_id(context)
        resume_prompt = self.get_resume_prompt(context, task)

        cmd = ["claude", "-p", resume_prompt, "--model", model]

        result = {
            "session_id": session_id,
            "context": context,
            "task": task,
            "model": model,
            "command": " ".join(cmd),
            "spawned_at": datetime.now().isoformat(),
        }

        try:
            terminal_cmd = f'''
            osascript -e 'tell application "Terminal"
                do script "cd \\"{self.project_root}\\" && {" ".join(cmd)}"
                activate
            end tell'
            '''

            subprocess.Popen(terminal_cmd, shell=True, start_new_session=True)
            result["success"] = True

            if self.db:
                from app.models import Session, SessionStatus
                session = Session(
                    session_id=session_id,
                    context=context,
                    task=task,
                    status=SessionStatus.ACTIVE.value,
                    metadata={"model": model},
                )
                self.db.add(session)
                self.db.commit()
                result["db_id"] = session.id

            print(f"[SessionSpawner] Spawned Claude {context} session: {session_id}")

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)

        return result

    def send_handoff(
        self,
        from_context: str,
        to_context: str,
        message_type: str,
        content: Dict,
        priority: str = "normal"
    ) -> Optional[Dict]:
        """
        Send a cross-session handoff message.

        Args:
            from_context: Source context (oracle, dev, dash, crank, pocket)
            to_context: Target context
            message_type: Type of handoff (e.g., "custom_preset_request")
            content: Message content dict
            priority: low, normal, high, urgent

        Returns:
            Message dict if successful, None otherwise
        """
        # Validate handoff is allowed
        rules = HANDOFF_RULES.get(from_context, {})
        allowed_types = rules.get("sends_to", {}).get(to_context, [])

        if message_type not in allowed_types:
            print(f"[SessionSpawner] Invalid handoff: {from_context} cannot send {message_type} to {to_context}")
            return None

        if not self.db:
            print("[SessionSpawner] No database connection - cannot send message")
            return None

        from app.models import Message

        message = Message(
            from_context=from_context,
            to_context=to_context,
            message_type=message_type,
            subject=f"[{message_type}] from {from_context}",
            content=json.dumps(content),
            priority=priority,
        )
        self.db.add(message)
        self.db.commit()

        print(f"[SessionSpawner] Handoff sent: {from_context} → {to_context}: {message_type}")
        return message.to_dict()

    def get_pending_handoffs(self, context: str) -> List[Dict]:
        """Get pending handoff messages for a context."""
        if not self.db:
            return []

        from app.models import Message

        messages = self.db.query(Message).filter(
            Message.to_context == context,
            Message.read_at.is_(None)
        ).order_by(Message.priority.desc(), Message.created_at.desc()).all()

        return [m.to_dict() for m in messages]

    def acknowledge_handoff(self, message_id: int) -> bool:
        """Mark a handoff message as acknowledged."""
        if not self.db:
            return False

        from app.models import Message

        message = self.db.query(Message).filter(Message.id == message_id).first()
        if message:
            message.acknowledge()
            self.db.commit()
            return True
        return False

    def list_sessions(self, context: str = None, status: str = None) -> List[Dict]:
        """List sessions, optionally filtered."""
        if not self.db:
            return []

        from app.models import Session

        query = self.db.query(Session)
        if context:
            query = query.filter(Session.context == context)
        if status:
            query = query.filter(Session.status == status)

        sessions = query.order_by(Session.last_activity.desc()).all()
        return [s.to_dict() for s in sessions]

    def close_session(self, session_id: str) -> bool:
        """Mark a session as closed."""
        if not self.db:
            return False

        from app.models import Session

        session = self.db.query(Session).filter(
            Session.session_id == session_id
        ).first()

        if session:
            session.close()
            self.db.commit()
            return True
        return False

    def print_resume_prompts(self):
        """Print resume prompts for all contexts."""
        print("\n" + "=" * 60)
        print("SESSION RESUME PROMPTS")
        print("=" * 60)

        for context in ContextType.all():
            print(f"\n{'=' * 20} {context.upper()} {'=' * 20}")
            print(self.get_resume_prompt(context))

    def print_handoff_rules(self):
        """Print cross-session handoff rules."""
        print("\n" + "=" * 60)
        print("CROSS-SESSION HANDOFF RULES")
        print("=" * 60)

        for context, rules in HANDOFF_RULES.items():
            print(f"\n{context.upper()}:")
            if rules.get("sends_to"):
                print("  Sends to:")
                for target, types in rules["sends_to"].items():
                    print(f"    → {target}: {', '.join(types)}")
            if rules.get("receives_from"):
                print("  Receives from:")
                for source, types in rules["receives_from"].items():
                    print(f"    ← {source}: {', '.join(types)}")


def main():
    """CLI interface for session spawner."""
    import argparse

    parser = argparse.ArgumentParser(description="Spawn VS Code/Claude Code sessions")
    parser.add_argument("action", choices=["spawn", "prompts", "list", "handoffs", "rules"], help="Action")
    parser.add_argument("--context", "-c", choices=ContextType.all(), help="Context type")
    parser.add_argument("--task", "-t", help="Task description")
    parser.add_argument("--claude", action="store_true", help="Use Claude Code")
    parser.add_argument("--model", default="opus", help="Claude model")

    args = parser.parse_args()

    spawner = SessionSpawner()

    if args.action == "spawn":
        if not args.context:
            print("Error: --context is required for spawn")
            return

        if args.claude:
            result = spawner.spawn_with_claude(args.context, args.task, args.model)
        else:
            result = spawner.spawn(args.context, args.task)

        print(json.dumps(result, indent=2))

    elif args.action == "prompts":
        spawner.print_resume_prompts()

    elif args.action == "rules":
        spawner.print_handoff_rules()

    elif args.action == "list":
        sessions = spawner.list_sessions(args.context)
        for s in sessions:
            print(f"{s['session_id']}: {s['context']} - {s['status']} - {s.get('task', 'No task')}")

    elif args.action == "handoffs":
        if not args.context:
            print("Error: --context is required for handoffs")
            return
        handoffs = spawner.get_pending_handoffs(args.context)
        if handoffs:
            for h in handoffs:
                print(f"[{h['priority']}] {h['from_context']} → {h['message_type']}: {h['content'][:50]}...")
        else:
            print(f"No pending handoffs for {args.context}")


if __name__ == "__main__":
    main()
