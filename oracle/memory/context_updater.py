"""
Context Updater - Automatic Context File Updates from Memory

The context updater analyzes Hippocampus observations to detect patterns
and automatically generate markdown updates for context files.

**Neural Metaphor:** Like how the hippocampus consolidates short-term memories
before transferring them to cortex (long-term storage), this module consolidates
session observations before updating context documentation.

Key Features:
- Pattern detection (repeated files, new features, architectural decisions)
- Markdown generation for context sections
- Validation (line limits, format, no conflicts)
- Auto-apply (confidence > 0.8) or queue for review

Usage:
    from oracle.memory.context_updater import ContextUpdater

    updater = ContextUpdater()

    # Analyze recent observations
    updates = updater.analyze_and_generate(days_back=7)

    # Preview pending updates
    updater.preview_updates()

    # Apply high-confidence updates
    updater.apply_updates(auto_apply_threshold=0.8)

Author: Oracle Brain Cell Architecture (P30 Phase 3)
"""

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from oracle.memory.hippocampus import Hippocampus, ObservationType, PatternType


# Project paths (PROJECT_ROOT already defined above for sys.path)
CONTEXT_DIR = PROJECT_ROOT / "oracle" / "docs" / "context"
UPDATES_QUEUE = PROJECT_ROOT / "oracle" / "data" / "memory" / "context_updates.json"


@dataclass
class ContextUpdate:
    """Represents a proposed update to a context file."""

    context_file: str
    section: str
    update_type: str  # "add", "modify", "replace"
    content: str
    confidence: float
    reason: str
    observation_ids: List[int] = field(default_factory=list)
    timestamp: str = ""
    applied: bool = False

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "context_file": self.context_file,
            "section": self.section,
            "update_type": self.update_type,
            "content": self.content,
            "confidence": self.confidence,
            "reason": self.reason,
            "observation_ids": self.observation_ids,
            "timestamp": self.timestamp,
            "applied": self.applied,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ContextUpdate":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ValidationResult:
    """Result of validating a context update."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ContextUpdater:
    """
    Automatic context file updater using Hippocampus observations.

    Analyzes patterns in observations and generates markdown updates
    for context files, maintaining readability and format standards.
    """

    def __init__(self, hippocampus: Hippocampus = None):
        """
        Initialize context updater.

        Args:
            hippocampus: Hippocampus instance (creates new if None)
        """
        self.hippo = hippocampus or Hippocampus()
        self.context_dir = CONTEXT_DIR
        self.updates_queue_file = UPDATES_QUEUE
        self.pending_updates: List[ContextUpdate] = []

        # Ensure data directory exists
        self.updates_queue_file.parent.mkdir(parents=True, exist_ok=True)

        # Load pending updates
        self._load_pending_updates()

        # Context file mapping
        self.context_files = {
            "Oracle": "ORACLE_CONTEXT.md",
            "Dev": "DEV_CONTEXT.md",
            "Dashboard": "DASHBOARD_CONTEXT.md",
            "Crank": "CRANK_CONTEXT.md",
            "Pocket": "POCKET_CONTEXT.md",
        }

        # Section patterns for each context file
        self.section_patterns = {
            "RECENT CHANGES": r"## RECENT CHANGES\n",
            "PENDING TASKS": r"## PENDING TASKS\n",
            "CURRENT STATE": r"## CURRENT STATE\n",
            "CROSS-SESSION FLAGS": r"### Cross-Session Flags\n",
        }

        # Validation limits
        self.max_section_lines = {
            "RECENT CHANGES": 100,
            "PENDING TASKS": 50,
            "CURRENT STATE": 30,
            "default": 50,
        }

    def analyze_and_generate(self, days_back: int = 7, context: str = None) -> List[ContextUpdate]:
        """
        Analyze recent observations and generate context updates.

        Args:
            days_back: Number of days to look back
            context: Specific context to analyze (None = all contexts)

        Returns:
            List of proposed ContextUpdate objects
        """
        updates = []

        # Detect patterns in recent observations
        patterns = self.hippo.detect_patterns(days_back=days_back)

        # Generate updates for each pattern type
        for pattern in patterns:
            if pattern.pattern_type == PatternType.REPEATED_FILE.value:
                update = self._generate_repeated_file_update(pattern)
                if update:
                    updates.append(update)

            elif pattern.pattern_type == PatternType.NEW_FEATURE.value:
                update = self._generate_new_feature_update(pattern)
                if update:
                    updates.append(update)

            elif pattern.pattern_type == PatternType.DECISION_POINT.value:
                update = self._generate_decision_update(pattern)
                if update:
                    updates.append(update)

            elif pattern.pattern_type == PatternType.ERROR_PATTERN.value:
                update = self._generate_error_pattern_update(pattern)
                if update:
                    updates.append(update)

        # Detect session completion patterns (for RECENT CHANGES)
        session_updates = self._detect_session_completions(days_back=days_back, context=context)
        updates.extend(session_updates)

        # Add to pending queue
        for update in updates:
            self.pending_updates.append(update)

        self._save_pending_updates()

        return updates

    def _generate_repeated_file_update(self, pattern) -> Optional[ContextUpdate]:
        """Generate update for repeated file modifications."""
        if not pattern.related_observations:
            return None

        # Get observation details
        obs_list = []
        for obs_id in pattern.related_observations[:5]:  # Limit to 5
            obs = self.hippo.get_observation(obs_id)
            if obs:
                obs_list.append(obs)

        if not obs_list:
            return None

        # Determine context from observations
        context = obs_list[0].context

        # Generate markdown content
        file_path = obs_list[0].file_path
        count = pattern.occurrence_count

        content = f"- **Active Development: {file_path}** - Modified {count} times in recent sessions\n"
        content += f"  - Observations: {', '.join([obs.summary for obs in obs_list[:3]])}\n"

        return ContextUpdate(
            context_file=self.context_files.get(context, "ORACLE_CONTEXT.md"),
            section="CURRENT STATE",
            update_type="add",
            content=content,
            confidence=min(count / 10.0, 0.9),
            reason=f"Repeated modifications detected: {file_path}",
            observation_ids=pattern.related_observations,
            timestamp=datetime.now().isoformat(),
        )

    def _generate_new_feature_update(self, pattern) -> Optional[ContextUpdate]:
        """Generate update for new feature detection."""
        if not pattern.related_observations:
            return None

        # Get first observation for details
        obs = self.hippo.get_observation(pattern.related_observations[0])
        if not obs:
            return None

        content = f"- **{pattern.description}**\n"
        content += f"  - {obs.summary}\n"
        if obs.details:
            # Extract first line of details as summary
            first_line = obs.details.split('\n')[0]
            content += f"  - {first_line}\n"

        return ContextUpdate(
            context_file=self.context_files.get(obs.context, "ORACLE_CONTEXT.md"),
            section="RECENT CHANGES",
            update_type="add",
            content=content,
            confidence=pattern.confidence,
            reason=f"New feature detected: {pattern.description}",
            observation_ids=pattern.related_observations,
            timestamp=datetime.now().isoformat(),
        )

    def _generate_decision_update(self, pattern) -> Optional[ContextUpdate]:
        """Generate update for architectural decisions."""
        if not pattern.related_observations:
            return None

        obs = self.hippo.get_observation(pattern.related_observations[0])
        if not obs:
            return None

        content = f"- **Decision: {pattern.description}**\n"
        content += f"  - Rationale: {obs.summary}\n"

        return ContextUpdate(
            context_file=self.context_files.get(obs.context, "ORACLE_CONTEXT.md"),
            section="RECENT CHANGES",
            update_type="add",
            content=content,
            confidence=pattern.confidence,
            reason=f"Architectural decision: {pattern.description}",
            observation_ids=pattern.related_observations,
            timestamp=datetime.now().isoformat(),
        )

    def _generate_error_pattern_update(self, pattern) -> Optional[ContextUpdate]:
        """Generate update for error patterns."""
        if not pattern.related_observations:
            return None

        obs = self.hippo.get_observation(pattern.related_observations[0])
        if not obs:
            return None

        content = f"- **Error Pattern: {pattern.description}**\n"
        content += f"  - Occurred {pattern.occurrence_count} times\n"
        content += f"  - Action needed: {obs.summary}\n"

        return ContextUpdate(
            context_file="ORACLE_CONTEXT.md",
            section="CROSS-SESSION FLAGS",
            update_type="add",
            content=content,
            confidence=0.95,  # High confidence for errors
            reason=f"Recurring error pattern: {pattern.description}",
            observation_ids=pattern.related_observations,
            timestamp=datetime.now().isoformat(),
        )

    def _detect_session_completions(self, days_back: int = 7, context: str = None) -> List[ContextUpdate]:
        """
        Detect completed sessions and generate RECENT CHANGES updates.

        Looks for SESSION_EVENT observations marking session end.
        """
        updates = []

        # Search for session events
        session_events = self.hippo.search(
            query="session",
            observation_type=ObservationType.SESSION_EVENT.value,
            days_back=days_back,
            limit=20
        )

        # Group by session_id
        sessions: Dict[str, List] = {}
        for event in session_events:
            session_id = event.get("session_id", "unknown")
            if session_id not in sessions:
                sessions[session_id] = []
            sessions[session_id].append(event)

        # Generate updates for each session
        for session_id, events in sessions.items():
            if context and events[0].get("context") != context:
                continue

            # Get all observations for this session
            session_obs = self.hippo.search(
                query="",
                context=events[0].get("context"),
                days_back=days_back,
                limit=100
            )

            # Filter to this specific session
            session_obs = [o for o in session_obs if o.get("session_id") == session_id]

            if len(session_obs) >= 5:  # Meaningful session
                update = self._generate_session_summary(session_id, session_obs)
                if update:
                    updates.append(update)

        return updates

    def _generate_session_summary(self, session_id: str, observations: List[Dict]) -> Optional[ContextUpdate]:
        """Generate a session summary for RECENT CHANGES."""
        if not observations:
            return None

        context = observations[0].get("context", "Oracle")

        # Group by file
        files_modified = set()
        features = []

        for obs in observations:
            if obs.get("file_path"):
                files_modified.add(obs["file_path"])
            if obs.get("observation_type") == ObservationType.DECISION.value:
                features.append(obs["summary"])

        if not files_modified and not features:
            return None

        # Generate markdown
        date_str = observations[0].get("timestamp", "")[:10]  # YYYY-MM-DD
        content = f"### {date_str} - Session {session_id}\n"

        if features:
            content += "- **Features:**\n"
            for feature in features[:3]:  # Limit to 3
                content += f"  - {feature}\n"

        if files_modified:
            content += f"- **Files Modified:** {len(files_modified)} files\n"
            for file_path in sorted(files_modified)[:5]:  # Limit to 5
                content += f"  - {file_path}\n"

        return ContextUpdate(
            context_file=self.context_files.get(context, "ORACLE_CONTEXT.md"),
            section="RECENT CHANGES",
            update_type="add",
            content=content,
            confidence=0.7,  # Medium confidence - needs review
            reason=f"Session {session_id} completion summary",
            observation_ids=[o["id"] for o in observations],
            timestamp=datetime.now().isoformat(),
        )

    def validate_update(self, update: ContextUpdate) -> ValidationResult:
        """
        Validate a proposed context update.

        Checks:
        - Section exists in target file
        - Content format is valid markdown
        - Line count within limits
        - No duplicate content

        Args:
            update: ContextUpdate to validate

        Returns:
            ValidationResult with valid flag and any errors/warnings
        """
        errors = []
        warnings = []

        # Check context file exists
        context_path = self.context_dir / update.context_file
        if not context_path.exists():
            errors.append(f"Context file not found: {update.context_file}")
            return ValidationResult(valid=False, errors=errors)

        # Read current content
        content = context_path.read_text()

        # Check section exists
        section_pattern = self.section_patterns.get(update.section)
        if section_pattern and not re.search(section_pattern, content):
            errors.append(f"Section not found: {update.section}")

        # Check line count
        new_lines = update.content.count('\n')
        max_lines = self.max_section_lines.get(update.section, self.max_section_lines["default"])

        if new_lines > max_lines:
            warnings.append(f"Update has {new_lines} lines (max: {max_lines})")

        # Check for duplicate content
        if update.content.strip() in content:
            errors.append("Duplicate content - update already present in file")

        # Check markdown format
        if not self._is_valid_markdown(update.content):
            warnings.append("Content may have markdown formatting issues")

        # Check confidence threshold
        if update.confidence < 0.5:
            warnings.append(f"Low confidence: {update.confidence:.2f}")

        valid = len(errors) == 0
        return ValidationResult(valid=valid, errors=errors, warnings=warnings)

    def _is_valid_markdown(self, content: str) -> bool:
        """Basic markdown validation."""
        # Check for balanced markdown
        lines = content.split('\n')

        for line in lines:
            # Check for unclosed code blocks
            if line.count('`') % 2 != 0:
                return False

            # Check for proper list formatting
            if line.strip().startswith('-') and not line.startswith('- '):
                return False

        return True

    def preview_updates(self, min_confidence: float = 0.0) -> str:
        """
        Preview pending updates.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            Formatted preview string
        """
        filtered = [u for u in self.pending_updates if u.confidence >= min_confidence and not u.applied]

        if not filtered:
            return "No pending updates."

        preview = f"Pending Updates: {len(filtered)}\n"
        preview += "=" * 60 + "\n\n"

        for i, update in enumerate(filtered, 1):
            preview += f"{i}. {update.context_file} > {update.section}\n"
            preview += f"   Type: {update.update_type} | Confidence: {update.confidence:.2f}\n"
            preview += f"   Reason: {update.reason}\n"
            preview += f"   Content:\n"
            for line in update.content.split('\n')[:5]:  # Preview first 5 lines
                preview += f"      {line}\n"
            preview += "\n"

        return preview

    def apply_updates(self, auto_apply_threshold: float = 0.8, dry_run: bool = False) -> Dict[str, int]:
        """
        Apply pending updates to context files.

        Args:
            auto_apply_threshold: Auto-apply if confidence >= threshold
            dry_run: Preview changes without applying

        Returns:
            Dict with counts: applied, queued, failed
        """
        stats = {"applied": 0, "queued": 0, "failed": 0}

        for update in self.pending_updates:
            if update.applied:
                continue

            # Validate update
            validation = self.validate_update(update)

            if not validation.valid:
                print(f"[FAILED] {update.context_file} > {update.section}")
                for error in validation.errors:
                    print(f"  ERROR: {error}")
                stats["failed"] += 1
                continue

            # Check confidence threshold
            if update.confidence >= auto_apply_threshold:
                if dry_run:
                    print(f"[DRY RUN] Would apply: {update.context_file} > {update.section}")
                    stats["applied"] += 1
                else:
                    success = self._apply_update(update)
                    if success:
                        update.applied = True
                        stats["applied"] += 1
                        print(f"[APPLIED] {update.context_file} > {update.section}")
                    else:
                        stats["failed"] += 1
            else:
                stats["queued"] += 1
                print(f"[QUEUED] {update.context_file} > {update.section} (confidence: {update.confidence:.2f})")

        if not dry_run:
            self._save_pending_updates()

        return stats

    def _apply_update(self, update: ContextUpdate) -> bool:
        """
        Apply a single update to a context file.

        Returns:
            True if successful, False otherwise
        """
        try:
            context_path = self.context_dir / update.context_file
            content = context_path.read_text()

            # Find section
            section_pattern = self.section_patterns.get(update.section)
            if not section_pattern:
                return False

            match = re.search(section_pattern, content)
            if not match:
                return False

            section_start = match.end()

            # Find next section (or end of file)
            next_section = re.search(r'\n## [A-Z]', content[section_start:])
            if next_section:
                section_end = section_start + next_section.start()
            else:
                section_end = len(content)

            # Insert update at start of section
            new_content = (
                content[:section_start] +
                "\n" + update.content + "\n" +
                content[section_start:section_end] +
                content[section_end:]
            )

            # Write updated content
            context_path.write_text(new_content)
            return True

        except Exception as e:
            print(f"Error applying update: {e}")
            return False

    def _load_pending_updates(self):
        """Load pending updates from queue file."""
        if not self.updates_queue_file.exists():
            self.pending_updates = []
            return

        try:
            with open(self.updates_queue_file) as f:
                data = json.load(f)

            self.pending_updates = [ContextUpdate.from_dict(u) for u in data]
        except Exception as e:
            print(f"Error loading pending updates: {e}")
            self.pending_updates = []

    def _save_pending_updates(self):
        """Save pending updates to queue file."""
        try:
            data = [u.to_dict() for u in self.pending_updates]
            with open(self.updates_queue_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving pending updates: {e}")


def main():
    """CLI interface for context updater."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python context_updater.py [analyze|preview|apply|clear]")
        print()
        print("Commands:")
        print("  analyze [days]    - Analyze observations and generate updates (default: 7 days)")
        print("  preview [min_conf] - Preview pending updates (default: 0.0)")
        print("  apply [threshold]  - Apply updates with confidence >= threshold (default: 0.8)")
        print("  apply --dry-run    - Preview what would be applied")
        print("  clear              - Clear all pending updates")
        return

    command = sys.argv[1]
    updater = ContextUpdater()

    if command == "analyze":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(f"Analyzing observations from last {days} days...")
        updates = updater.analyze_and_generate(days_back=days)
        print(f"Generated {len(updates)} updates")
        print()
        print(updater.preview_updates())

    elif command == "preview":
        min_conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
        print(updater.preview_updates(min_confidence=min_conf))

    elif command == "apply":
        dry_run = "--dry-run" in sys.argv
        threshold = 0.8

        for arg in sys.argv[2:]:
            if arg != "--dry-run":
                try:
                    threshold = float(arg)
                except ValueError:
                    pass

        print(f"Applying updates with confidence >= {threshold}")
        if dry_run:
            print("(DRY RUN MODE)")
        print()

        stats = updater.apply_updates(auto_apply_threshold=threshold, dry_run=dry_run)
        print()
        print(f"Results: {stats['applied']} applied, {stats['queued']} queued, {stats['failed']} failed")

    elif command == "clear":
        updater.pending_updates = []
        updater._save_pending_updates()
        print("Cleared all pending updates")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
