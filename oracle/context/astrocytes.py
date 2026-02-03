#!/usr/bin/env python3
"""
Astrocytes - Oracle Brain Cell: Context Management, Environment Support, Snapshots
==================================================================================

Brain Metaphor: Astrocytes are the support cells of the brain. They maintain the
neural environment, regulate homeostasis, support synaptic function, and help
store memory (context).

Responsibilities:
- Context file health and management
- Session snapshots and diff tracking
- Environment support and validation
- Cross-session briefings and state transfer

Commands: status, context, snapshot
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

ORACLE_DIR = Path(__file__).parent.parent  # Up from context/ to oracle/
PROJECT_ROOT = ORACLE_DIR.parent  # Up from oracle/ to project root
DOCS_DIR = ORACLE_DIR / "docs"
DOCS_CONTEXT_DIR = DOCS_DIR / "context"
DOCS_OVERVIEW_DIR = DOCS_DIR / "overview"
DOCS_CODE_DIR = DOCS_DIR / "code only"
CONTEXT_DIR = DOCS_CONTEXT_DIR  # Alias for backward compatibility
REPORTS_DIR = ORACLE_DIR / "reports"
SNAPSHOTS_DIR = REPORTS_DIR / "snapshots"
DIFFS_DIR = REPORTS_DIR / "diffs"
CONTEXT_FILE = CONTEXT_DIR / "DEV_CONTEXT.md"

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")

def debug_log(msg: str, category: str = "general"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  🔍 [{timestamp}] [{category}] {msg}")

# Constants
MAX_REPORTS = 5
MAX_SNAPSHOTS = 5


# =============================================================================
# UTILITY - cleanup_old_files
# =============================================================================

def cleanup_old_files(directory: Path, pattern: str, max_keep: int = 5) -> int:
    """Delete old files matching pattern, keeping only the most recent max_keep."""
    if not directory.exists():
        return 0
    files = sorted(directory.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)
    deleted = 0
    for old_file in files[max_keep:]:
        try:
            old_file.unlink()
            deleted += 1
        except Exception:
            pass
    return deleted


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Issue:
    """Represents a single issue found during audit."""
    severity: str
    category: str
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


# =============================================================================
# CONTEXT PARSER
# =============================================================================

class ContextParser:
    """Parse DEV_CONTEXT.md to extract configuration."""

    def __init__(self, context_path: Path):
        self.context_path = context_path
        self.content = ""
        self.parse_errors = []

    def parse(self) -> dict:
        """Parse DEV_CONTEXT.md and return configuration dict."""
        if not self.context_path.exists():
            self.parse_errors.append(f"Context file not found at {self.context_path}")
            return self._get_defaults()

        self.content = self.context_path.read_text()

        config = {
            "layers": self._parse_layers(),
            "api_services": self._parse_api_services(),
            "doc_files": self._parse_doc_files(),
            "scripts": self._parse_scripts(),
            "mcps": self._parse_mcps(),
            "session_rules": self._parse_session_rules(),
            "pending_tasks": self._parse_pending_tasks(),
            "last_updated": self._parse_last_updated(),
        }

        config = self._validate_and_fill(config)
        return config

    def _parse_layers(self) -> dict:
        """Extract layer definitions from Pipeline Status section."""
        layers = {}
        layer_pattern = r'[✅⬜🔄❌]\s*Layer\s*(\d+):\s*([^→\n]+?)\s*(?:→\s*([^\n]+))?$'

        for match in re.finditer(layer_pattern, self.content, re.MULTILINE):
            layer_num = int(match.group(1))
            layer_name = match.group(2).strip()
            output_path = match.group(3).strip() if match.group(3) else ""

            if output_path.startswith("output/"):
                output_path = output_path[7:]

            layers[layer_num] = {
                "name": layer_name,
                "output": output_path,
                "scripts": []
            }

        return layers

    def _parse_api_services(self) -> dict:
        """Extract API services from API KEYS section."""
        services = {}
        api_pattern = r'\|\s*(\w+_(?:API_)?KEY)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'

        for match in re.finditer(api_pattern, self.content):
            env_key = match.group(1).strip()
            service_desc = match.group(2).strip()
            layers_str = match.group(3).strip()
            status = match.group(4).strip()
            layer_nums = [int(x) for x in re.findall(r'L?(\d+)', layers_str)]
            service_name = env_key.replace("_API_KEY", "").replace("_KEY", "").lower()

            services[service_name] = {
                "env_key": env_key,
                "layers": layer_nums,
                "description": service_desc,
                "active": "✅" in status or "Active" in status
            }

        return services

    def _parse_doc_files(self) -> dict:
        """Extract documentation file references."""
        doc_files = {
            "dev_context": CONTEXT_DIR / "DEV_CONTEXT.md",
            "oracle_context": CONTEXT_DIR / "ORACLE_CONTEXT.md",
            "readme": DOCS_DIR / "README.md",
        }

        # Apply path corrections for V2 structure
        corrections = {
            "dev_context": DOCS_CONTEXT_DIR / "DEV_CONTEXT.md",
            "oracle_context": DOCS_CONTEXT_DIR / "ORACLE_CONTEXT.md",
            "readme": DOCS_DIR / "README.md",
            "architecture": DOCS_OVERVIEW_DIR / "ARCHITECTURE.md",
            "philosophy": DOCS_OVERVIEW_DIR / "PHILOSOPHY.md",
            "workflow": DOCS_OVERVIEW_DIR / "WORKFLOW.md",
            "code_history": DOCS_OVERVIEW_DIR / "CODE_HISTORY.md",
            "tools_reference": DOCS_OVERVIEW_DIR / "TOOLS_REFERENCE.md",
            "ideas_backlog": DOCS_OVERVIEW_DIR / "IDEAS_BACKLOG.md",
            "style_guide": DOCS_OVERVIEW_DIR / "STYLE_GUIDE.md",
            "ux_rules": DOCS_CODE_DIR / "UX_RULES.md",
            "setup": DOCS_CODE_DIR / "SETUP.md",
            "changelog": DOCS_CODE_DIR / "CHANGELOG.md",
        }

        for key, correct_path in corrections.items():
            doc_files[key] = correct_path

        return doc_files

    def _parse_scripts(self) -> list:
        """Extract all script references."""
        scripts = set()
        script_pattern = r'\b(\w+\.py)\b'

        for match in re.finditer(script_pattern, self.content):
            script_name = match.group(1)
            if not script_name.startswith(("test_", "setup", "conftest")):
                scripts.add(script_name)

        return sorted(list(scripts))

    def _parse_mcps(self) -> dict:
        """Extract MCP server configurations."""
        mcps = {}
        mcp_pattern = r'\|\s*(\w+[-\w]*)\s*\|\s*([^|]+)\s*\|\s*([^|]*[✅❌][^|]*)\s*\|'
        mcp_section = re.search(r'###\s*MCP Servers.*?(?=###|\Z)', self.content, re.DOTALL)

        if mcp_section:
            section_text = mcp_section.group(0)
            for match in re.finditer(mcp_pattern, section_text):
                server_name = match.group(1).strip()
                purpose = match.group(2).strip()
                status = match.group(3).strip()
                if server_name.lower() not in ["server", "service", "name"]:
                    mcps[server_name] = {
                        "purpose": purpose,
                        "configured": "✅" in status
                    }

        return mcps

    def _parse_session_rules(self) -> list:
        """Extract session rules."""
        rules = []
        rule_pattern = r'\d+\.\s*\*\*([^*]+)\*\*:\s*([^\n]+)'
        rules_section = re.search(r'###\s*Session Rules.*?(?=###|\Z)', self.content, re.DOTALL)

        if rules_section:
            section_text = rules_section.group(0)
            for match in re.finditer(rule_pattern, section_text):
                rule_name = match.group(1).strip()
                rule_desc = match.group(2).strip()
                rules.append({"name": rule_name, "description": rule_desc})

        return rules

    def _parse_pending_tasks(self) -> list:
        """Extract pending tasks."""
        tasks = []
        pending_section = re.search(r'###\s*Pending Tasks.*?(?=###|##|\Z)', self.content, re.DOTALL | re.IGNORECASE)

        if pending_section:
            section_text = pending_section.group(0)
            task_pattern = r'^(?:\d+\.\s*|\-\s*(?:\[[ x]\])?\s*)(.+)$'

            for match in re.finditer(task_pattern, section_text, re.MULTILINE):
                task = match.group(1).strip()
                if task and not task.startswith("|"):
                    task_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', task)
                    tasks.append(task_clean)

        return tasks

    def _parse_last_updated(self) -> Optional[str]:
        """Extract last updated timestamp."""
        update_pattern = r'\*\*Last Updated[:\*]*\s*([^\n\*]+)'
        match = re.search(update_pattern, self.content)
        if match:
            return match.group(1).strip()
        return None

    def _validate_and_fill(self, config: dict) -> dict:
        """Validate parsed config and fill gaps with defaults."""
        defaults = self._get_defaults()

        if not config["layers"]:
            self.parse_errors.append("Could not parse layers, using defaults")
            config["layers"] = defaults["layers"]

        if not config["api_services"]:
            self.parse_errors.append("Could not parse API services, using defaults")
            config["api_services"] = defaults["api_services"]

        if not config["doc_files"] or len(config["doc_files"]) < 3:
            for key, path in defaults["doc_files"].items():
                if key not in config["doc_files"]:
                    config["doc_files"][key] = path

        return config

    def _get_defaults(self) -> dict:
        """Return default configuration."""
        return {
            "layers": {
                1: {"name": "Trend Detection", "scripts": ["web_search_trend_detector.py"], "output": "all_trends.json"},
                2: {"name": "Calendar & Segments", "scripts": ["calendar_config.py"], "output": "segments_config.json"},
                3: {"name": "Idea Creation", "scripts": ["idea_creation.py"], "output": "ideas_approved.json"},
                5: {"name": "Media Components", "scripts": ["media_generation.py"], "output": "media/"},
                6: {"name": "Video Assembly", "scripts": ["assembly.py"], "output": "assembled/"},
                7: {"name": "Distribution", "scripts": ["distribution.py"], "output": "final/"},
            },
            "api_services": {
                "openai": {"env_key": "OPENAI_API_KEY", "layers": [1, 3]},
                "fal": {"env_key": "FAL_KEY", "layers": [5]},
            },
            "doc_files": {
                "dev_context": CONTEXT_DIR / "DEV_CONTEXT.md",
                "oracle_context": CONTEXT_DIR / "ORACLE_CONTEXT.md",
                "readme": DOCS_DIR / "README.md",
            },
            "scripts": [],
            "mcps": {},
            "session_rules": [],
            "pending_tasks": [],
            "last_updated": None,
        }


# =============================================================================
# CONTEXT HEALTH AUDITOR
# =============================================================================

class ContextHealthAuditor:
    """Audit the health of context files."""

    def __init__(self, context_path: Path, config: dict):
        self.context_path = context_path
        self.config = config
        self.issues = []

    def run(self) -> list:
        """Run context health checks."""
        self.issues = []

        if not self.context_path.exists():
            self.issues.append(Issue(
                severity="critical",
                category="docs",
                title="Context file missing",
                description="Primary context file not found",
                suggestion="Create context file for session continuity"
            ))
            return self.issues

        content = self.context_path.read_text()

        self._check_required_sections(content)
        self._check_timestamp_freshness()
        self._check_pending_tasks()
        self._check_completeness(content)

        return self.issues

    def _check_required_sections(self, content: str):
        """Verify required sections exist."""
        required_sections = [
            ("SESSION RESUME PROTOCOL", "Session resume instructions"),
            ("CURRENT STATE", "Current project state"),
            ("Pipeline Status", "Layer status tracking"),
        ]

        for section, description in required_sections:
            if section.lower() not in content.lower():
                self.issues.append(Issue(
                    severity="warning",
                    category="docs",
                    title=f"Missing section: {section}",
                    description=f"Context should have {description}",
                    file_path=str(self.context_path),
                    suggestion=f"Add ## {section} section"
                ))

    def _check_timestamp_freshness(self):
        """Check if last updated is recent."""
        last_updated = self.config.get("last_updated")

        if not last_updated:
            self.issues.append(Issue(
                severity="info",
                category="docs",
                title="No 'Last Updated' timestamp",
                description="Consider adding timestamp for tracking",
                file_path=str(self.context_path),
                suggestion="Add **Last Updated:** [date] at top of file"
            ))
            return

        try:
            for fmt in ["%B %d, %Y", "%Y-%m-%d", "%b %d, %Y"]:
                try:
                    date_str = re.sub(r'\s*\(Session \d+\)', '', last_updated)
                    doc_date = datetime.strptime(date_str.strip(), fmt)
                    days_old = (datetime.now() - doc_date).days

                    if days_old > 7:
                        self.issues.append(Issue(
                            severity="info",
                            category="docs",
                            title="Context file may be stale",
                            description=f"Last updated {days_old} days ago",
                            file_path=str(self.context_path),
                            suggestion="Update timestamp and verify content"
                        ))
                    break
                except ValueError:
                    continue
        except Exception:
            pass

    def _check_pending_tasks(self):
        """Check for task accumulation."""
        pending = self.config.get("pending_tasks", [])

        if len(pending) > 15:
            self.issues.append(Issue(
                severity="warning",
                category="docs",
                title="Too many pending tasks",
                description=f"Found {len(pending)} pending tasks",
                file_path=str(self.context_path),
                suggestion="Complete, defer, or remove stale tasks"
            ))

    def _check_completeness(self, content: str):
        """Check for incomplete placeholders."""
        placeholder_patterns = [
            (r'\[TODO\]', "TODO placeholder"),
            (r'\[TBD\]', "TBD placeholder"),
            (r'\[PLACEHOLDER\]', "PLACEHOLDER marker"),
        ]

        for pattern, description in placeholder_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.issues.append(Issue(
                    severity="info",
                    category="docs",
                    title=f"Found {description}",
                    description=f"Found {len(matches)} instances",
                    file_path=str(self.context_path),
                    suggestion="Replace placeholders with actual content"
                ))


# =============================================================================
# SESSION DIFF TRACKER
# =============================================================================

class SessionDiffTracker:
    """Track and report changes made during a session."""

    def __init__(self, project_root: Path, config: dict):
        self.project_root = project_root
        self.config = config
        self.reports_dir = REPORTS_DIR
        self.diffs_dir = DIFFS_DIR
        self.snapshots_dir = SNAPSHOTS_DIR
        self.reports_dir.mkdir(exist_ok=True)
        self.diffs_dir.mkdir(exist_ok=True)
        self.snapshots_dir.mkdir(exist_ok=True)
        self.session_start = datetime.now()

    def capture_current_state(self) -> dict:
        """Capture current project state for comparison."""
        state = {
            "timestamp": datetime.now().isoformat(),
            "scripts": self._get_file_mtimes(self.project_root / "scripts", "*.py"),
            "app": self._get_file_mtimes(self.project_root / "app", "*.py"),
            "configs": self._get_file_mtimes(self.project_root / "config", "*.json"),
            "docs": self._get_file_mtimes(DOCS_DIR, "*.md"),
            "context": self._get_file_mtimes(CONTEXT_DIR, "*.md"),
        }
        return state

    def _get_file_mtimes(self, directory: Path, pattern: str) -> dict:
        """Get modification times for files matching pattern."""
        files = {}
        if directory.exists():
            for f in directory.rglob(pattern):
                if not f.name.startswith("_"):
                    try:
                        rel_path = f.relative_to(self.project_root)
                        files[str(rel_path)] = f.stat().st_mtime
                    except ValueError:
                        files[str(f)] = f.stat().st_mtime
        return files

    def compare_states(self, before: dict, after: dict) -> dict:
        """Compare two states and identify changes."""
        diff = {
            "files_modified": [],
            "files_created": [],
            "files_deleted": [],
            "recent_changes_added": [],
            "tasks_completed": [],
            "tasks_added": [],
        }

        for category in ["scripts", "app", "configs", "docs", "context"]:
            before_files = before.get(category, {})
            after_files = after.get(category, {})

            for f, mtime in after_files.items():
                if f not in before_files:
                    diff["files_created"].append(f)
                elif mtime > before_files[f]:
                    diff["files_modified"].append(f)

            for f in before_files:
                if f not in after_files:
                    diff["files_deleted"].append(f)

        return diff

    def save_snapshot(self, state: dict, name: str = "latest") -> Path:
        """Save state snapshot for later comparison."""
        if name == "latest":
            snapshot_path = self.snapshots_dir / "SESSION_SNAPSHOT_latest.json"
        else:
            snapshot_path = self.snapshots_dir / f"SESSION_SNAPSHOT_{name}.json"

        serializable = json.loads(json.dumps(state, default=str))
        snapshot_path.write_text(json.dumps(serializable, indent=2))
        return snapshot_path

    def load_snapshot(self, name: str = "latest") -> dict:
        """Load a previous snapshot."""
        if name == "latest":
            snapshot_path = self.snapshots_dir / "SESSION_SNAPSHOT_latest.json"
        else:
            snapshot_path = self.snapshots_dir / f"SESSION_SNAPSHOT_{name}.json"

        if snapshot_path.exists():
            return json.loads(snapshot_path.read_text())
        return {}

    def generate_context_snapshot(self, active_task: str = None,
                                   last_file: str = None,
                                   pending_decisions: str = None,
                                   blockers: str = None) -> tuple:
        """Generate a unified Context Snapshot combining current state + diff."""
        before = self.load_snapshot("latest")
        after = self.capture_current_state()

        diff = self.compare_states(before, after) if before else None

        now = datetime.now()
        lines = [
            f"# Context Snapshot - {now.strftime('%B %d, %Y %H:%M')}",
            "",
            "**Purpose:** Resume context after compaction or session break",
            "",
            "## Current State",
        ]

        if active_task:
            lines.append(f"- **Active Task:** {active_task}")
        else:
            lines.append("- **Active Task:** (none specified)")

        if last_file:
            lines.append(f"- **Last File Edited:** {last_file}")
        elif diff and diff.get("files_modified"):
            lines.append(f"- **Last File Edited:** {diff['files_modified'][-1]}")

        if pending_decisions:
            lines.append(f"- **Pending Decisions:** {pending_decisions}")
        else:
            lines.append("- **Pending Decisions:** None")

        if blockers:
            lines.append(f"- **Blockers:** {blockers}")
        else:
            lines.append("- **Blockers:** None")

        lines.append("")
        lines.append("## Changes Since Last Snapshot")

        if not before:
            lines.append("*First snapshot - no previous state to compare*")
        elif diff:
            if diff.get("files_modified"):
                files_list = ", ".join(Path(f).name for f in diff["files_modified"][:5])
                if len(diff["files_modified"]) > 5:
                    files_list += f" (+{len(diff['files_modified']) - 5} more)"
                lines.append(f"- 📝 Modified: {files_list}")

            if diff.get("files_created"):
                for f in diff["files_created"][:3]:
                    lines.append(f"- ➕ Added: {Path(f).name}")

            if diff.get("files_deleted"):
                for f in diff["files_deleted"][:3]:
                    lines.append(f"- 🗑️ Removed: {Path(f).name}")

            if not any([diff.get("files_modified"), diff.get("files_created"), diff.get("files_deleted")]):
                lines.append("*No changes detected since last snapshot*")

        lines.append("")
        lines.append("## Quick Resume Prompt")
        if active_task:
            resume_prompt = f"Continue with: {active_task}"
        elif diff and diff.get("files_modified"):
            resume_prompt = f"Continue from last session. Modified: {', '.join(Path(f).name for f in diff['files_modified'][:3])}"
        else:
            resume_prompt = "Review context file for current state"

        lines.extend([
            "```",
            resume_prompt,
            "```",
            "",
            "---",
            "*Generated by Astrocytes `snapshot` command*",
        ])

        snapshot_md = "\n".join(lines)

        timestamp = now.strftime("%Y%m%d_%H%M%S")
        snapshot_path = self.snapshots_dir / f"SNAPSHOT_{timestamp}.md"
        snapshot_path.write_text(snapshot_md)

        cleanup_old_files(self.snapshots_dir, "SNAPSHOT_*.md", MAX_SNAPSHOTS)
        self.save_snapshot(after, "latest")

        return snapshot_md, snapshot_path


# =============================================================================
# CROSS-SESSION BRIEFING
# =============================================================================

class CrossSessionBriefing:
    """Generate cross-session briefings to surface relevant information."""

    def __init__(self, project_root: Path, config: dict):
        self.project_root = project_root
        self.config = config
        self.reports_dir = REPORTS_DIR
        self.dev_context = CONTEXT_DIR / "DEV_CONTEXT.md"
        self.oracle_context = CONTEXT_DIR / "ORACLE_CONTEXT.md"

    def detect_session_type(self) -> str:
        """Detect which session type is active based on context file freshness."""
        try:
            dev_atime = self.dev_context.stat().st_atime if self.dev_context.exists() else 0
            oracle_atime = self.oracle_context.stat().st_atime if self.oracle_context.exists() else 0

            if abs(dev_atime - oracle_atime) < 60:
                dev_mtime = self.dev_context.stat().st_mtime if self.dev_context.exists() else 0
                oracle_mtime = self.oracle_context.stat().st_mtime if self.oracle_context.exists() else 0
                return "maintenance" if oracle_mtime > dev_mtime else "dev"

            return "maintenance" if oracle_atime > dev_atime else "dev"
        except Exception:
            return "dev"

    def get_briefing(self, session_type: str = None) -> dict:
        """Get cross-session briefing for the specified session type."""
        if session_type is None:
            session_type = self.detect_session_type()

        items = []

        if session_type == "dev":
            items.extend(self._get_oracle_findings())
        else:
            items.extend(self._get_dev_changes())

        severity_order = {"critical": 0, "warning": 1, "info": 2}
        items.sort(key=lambda x: severity_order.get(x.get("severity", "info"), 3))

        has_critical = any(i.get("severity") == "critical" for i in items)

        if not items:
            summary = "No cross-session updates."
        else:
            critical_count = sum(1 for i in items if i.get("severity") == "critical")
            warning_count = sum(1 for i in items if i.get("severity") == "warning")
            info_count = sum(1 for i in items if i.get("severity") == "info")
            parts = []
            if critical_count:
                parts.append(f"{critical_count} critical")
            if warning_count:
                parts.append(f"{warning_count} warning")
            if info_count:
                parts.append(f"{info_count} info")
            summary = f"Cross-session: {', '.join(parts)}"

        return {
            "session_type": session_type,
            "items": items,
            "summary": summary,
            "has_critical": has_critical,
        }

    def _get_oracle_findings(self) -> list:
        """Get relevant oracle findings for dev session."""
        items = []
        audits_dir = REPORTS_DIR / "audits"

        if audits_dir.exists():
            reports = sorted(audits_dir.glob("ORACLE_REPORT_*.md"),
                           key=lambda f: f.stat().st_mtime, reverse=True)
            if reports:
                latest_report = reports[0]
                try:
                    content = latest_report.read_text()
                    score_match = re.search(r'Health Score[:\s]+(\d+\.?\d*)/10', content)
                    if score_match:
                        score = float(score_match.group(1))
                        if score < 5.0:
                            items.append({
                                "type": "health",
                                "severity": "critical",
                                "message": f"Health score is low: {score:.1f}/10",
                                "source": latest_report.name,
                            })
                        elif score < 7.0:
                            items.append({
                                "type": "health",
                                "severity": "warning",
                                "message": f"Health score needs attention: {score:.1f}/10",
                                "source": latest_report.name,
                            })
                except Exception:
                    pass

        return items

    def _get_dev_changes(self) -> list:
        """Get relevant dev session changes for maintenance session."""
        items = []

        if self.dev_context.exists():
            try:
                dev_content = self.dev_context.read_text()
                recent_match = re.search(
                    r'## 📝 RECENT CHANGES\s*\n(.*?)(?=\n## |\Z)',
                    dev_content, re.DOTALL
                )
                if recent_match:
                    recent_text = recent_match.group(1)
                    layer_mentions = re.findall(r'L[1-8]|Layer [1-8]', recent_text)
                    if layer_mentions:
                        unique_layers = list(set(layer_mentions))
                        items.append({
                            "type": "layer_changes",
                            "severity": "info",
                            "message": f"Dev session modified layers: {', '.join(sorted(unique_layers))}",
                            "source": "DEV_CONTEXT.md",
                        })
            except Exception:
                pass

        return items

    def format_briefing(self, briefing: dict = None) -> str:
        """Format briefing for console output."""
        if briefing is None:
            briefing = self.get_briefing()

        if not briefing["items"]:
            return ""

        lines = [f"\n📋 Cross-Session Briefing ({briefing['session_type']} session):"]

        for item in briefing["items"]:
            severity = item.get("severity", "info")
            icon = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}.get(severity, "•")
            lines.append(f"  {icon} {item['message']}")

        return "\n".join(lines)


# =============================================================================
# PUBLIC INTERFACE FUNCTIONS
# =============================================================================

def get_status() -> str:
    """Get one-line health summary.

    Returns:
        Health status string
    """
    parser = ContextParser(CONTEXT_FILE)
    config = parser.parse()

    auditor = ContextHealthAuditor(CONTEXT_FILE, config)
    issues = auditor.run()

    critical = sum(1 for i in issues if i.severity == "critical")
    warnings = sum(1 for i in issues if i.severity == "warning")

    last_updated = config.get("last_updated", "Unknown")
    pending_count = len(config.get("pending_tasks", []))

    if critical > 0:
        health = "❌ CRITICAL"
    elif warnings > 0:
        health = "⚠️ WARNINGS"
    else:
        health = "✅ HEALTHY"

    return f"{health} | Last updated: {last_updated} | Pending tasks: {pending_count} | Issues: {critical}C/{warnings}W"


def manage_context() -> None:
    """Interactive context file management."""
    parser = ContextParser(CONTEXT_FILE)
    config = parser.parse()

    print("\n📄 Context File Summary")
    print("=" * 50)
    print(f"  File: {CONTEXT_FILE}")
    print(f"  Last Updated: {config.get('last_updated', 'Unknown')}")
    print(f"  Layers: {len(config.get('layers', {}))}")
    print(f"  API Services: {len(config.get('api_services', {}))}")
    print(f"  Pending Tasks: {len(config.get('pending_tasks', []))}")

    if parser.parse_errors:
        print("\n  ⚠️ Parse warnings:")
        for error in parser.parse_errors:
            print(f"    - {error}")

    auditor = ContextHealthAuditor(CONTEXT_FILE, config)
    issues = auditor.run()

    if issues:
        print(f"\n  Issues: {len(issues)}")
        for issue in issues[:5]:
            print(f"    [{issue.severity}] {issue.title}")


def create_snapshot(sync: bool = False, active_task: str = None,
                    last_file: str = None) -> dict:
    """Create context snapshot.

    Args:
        sync: If True, save snapshot for autosave
        active_task: Current active task
        last_file: Last file being edited

    Returns:
        Dict with snapshot_path and content
    """
    parser = ContextParser(CONTEXT_FILE)
    config = parser.parse()

    tracker = SessionDiffTracker(PROJECT_ROOT, config)
    snapshot_md, snapshot_path = tracker.generate_context_snapshot(
        active_task=active_task,
        last_file=last_file
    )

    return {
        "snapshot_path": str(snapshot_path),
        "content": snapshot_md,
        "sync": sync
    }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for astrocytes commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Astrocytes - Context management, environment support, snapshots",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Status command
    subparsers.add_parser("status", help="One-line health summary")

    # Context command
    subparsers.add_parser("context", help="Context file management")

    # Snapshot command
    snapshot_parser = subparsers.add_parser("snapshot", help="Create context snapshot")
    snapshot_parser.add_argument("--sync", action="store_true", help="Sync/autosave mode")
    snapshot_parser.add_argument("--task", help="Current active task")
    snapshot_parser.add_argument("--file", help="Last file being edited")

    args = parser.parse_args()

    if args.command == "status":
        print(get_status())

    elif args.command == "context":
        manage_context()

    elif args.command == "snapshot":
        result = create_snapshot(
            sync=args.sync,
            active_task=args.task,
            last_file=args.file
        )
        print(f"\n📸 Snapshot created: {result['snapshot_path']}")
        print("\n" + result['content'])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
