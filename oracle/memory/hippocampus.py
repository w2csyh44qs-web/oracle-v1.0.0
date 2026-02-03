#!/usr/bin/env python3
"""
hippocampus.py - Memory Consolidation Brain Cell (LOCATION)

The hippocampus consolidates short-term observations into long-term memories
stored in the cortex (context files). This module provides automatic observation
capture, semantic search, and token-efficient progressive disclosure.

**Neural Metaphor:** The hippocampus consolidates short-term memories before
transfer to cortex (long-term storage). Similarly, this module consolidates
session observations before updating context files.

**Note:** Hippocampus and Cortex are LOCATIONS (brain regions), unlike other
modules which are CELL TYPES (microglia, astrocytes, etc.)

Key Features:
- Automatic observation capture (file changes, tool usage, session events)
- 3-layer progressive disclosure (summaries → context → full details)
- Pattern detection for context auto-updates
- Semantic search with token efficiency (50% reduction)
- Cross-context memory sharing

Commands:
    search <query>              - Search observations (Layer 1: summaries)
    timeline <query>            - Get timeline with context (Layer 2)
    details <observation_id>    - Get full details (Layer 3)
    capture <type> <data>       - Manually capture observation
    patterns                    - Show detected patterns
    stats                       - Show memory statistics

Usage:
    python3 oracle/memory/hippocampus.py search "L6 carousel changes"
    python3 oracle/memory/hippocampus.py patterns
    python3 oracle/memory/hippocampus.py stats

Author: Oracle Brain Cell Architecture (P30)
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# PATH SETUP
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
ORACLE_DATA_DIR = PROJECT_ROOT / "oracle" / "data"
MEMORY_DIR = ORACLE_DATA_DIR / "memory"
MEMORY_DB = MEMORY_DIR / "observations.db"
MEMORY_CONFIG = MEMORY_DIR / "memory_config.json"


# ============================================================================
# ENUMS & DATACLASSES
# ============================================================================

class ObservationType(Enum):
    """Types of observations that can be captured."""
    FILE_CHANGE = "file_change"
    TOOL_USAGE = "tool_usage"
    SESSION_EVENT = "session_event"
    HEALTH_AUDIT = "health_audit"
    DECISION = "decision"
    ERROR = "error"


class PatternType(Enum):
    """Types of patterns detected in observations."""
    REPEATED_FILE = "repeated_file"
    NEW_FEATURE = "new_feature"
    DECISION_POINT = "decision_point"
    ERROR_PATTERN = "error_pattern"
    LAYER_CHANGE = "layer_change"


@dataclass
class Observation:
    """A single memory observation."""
    id: Optional[int] = None
    timestamp: str = ""
    session_id: str = ""
    context: str = ""  # Oracle/Dev/Dash/Crank/Pocket
    observation_type: str = ""
    summary: str = ""  # ~50 tokens - Layer 1
    details: str = ""  # ~500 tokens - Layer 3
    file_path: Optional[str] = None
    layer_id: Optional[str] = None
    confidence: float = 1.0
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Observation':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Pattern:
    """A detected pattern in observations."""
    id: Optional[int] = None
    pattern_type: str = ""
    description: str = ""
    first_seen: str = ""
    last_seen: str = ""
    occurrence_count: int = 0
    confidence: float = 0.0
    related_observations: List[int] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class MemoryStats:
    """Memory system statistics."""
    total_observations: int = 0
    observations_by_context: Dict[str, int] = None
    observations_by_type: Dict[str, int] = None
    total_patterns: int = 0
    date_range: Tuple[str, str] = None
    db_size_mb: float = 0.0


# ============================================================================
# DATABASE SCHEMA
# ============================================================================

SCHEMA_VERSION = "1.0"

OBSERVATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    session_id TEXT NOT NULL,
    context TEXT NOT NULL,
    observation_type TEXT NOT NULL,
    summary TEXT NOT NULL,
    details TEXT,
    file_path TEXT,
    layer_id TEXT,
    confidence REAL DEFAULT 1.0,
    metadata TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

OBSERVATIONS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_timestamp ON observations(timestamp);
CREATE INDEX IF NOT EXISTS idx_session ON observations(session_id);
CREATE INDEX IF NOT EXISTS idx_context ON observations(context);
CREATE INDEX IF NOT EXISTS idx_type ON observations(observation_type);
CREATE INDEX IF NOT EXISTS idx_file_path ON observations(file_path);
CREATE INDEX IF NOT EXISTS idx_layer ON observations(layer_id);
"""

PATTERNS_TABLE = """
CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_type TEXT NOT NULL,
    description TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    confidence REAL DEFAULT 0.0,
    related_observations TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

PATTERNS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_pattern_type ON patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_pattern_confidence ON patterns(confidence);
"""

SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context TEXT NOT NULL,
    session_number INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    summary TEXT,
    observation_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SESSIONS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_session_context ON sessions(context);
CREATE INDEX IF NOT EXISTS idx_session_start ON sessions(start_time);
"""

METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


# ============================================================================
# HIPPOCAMPUS MEMORY MANAGER
# ============================================================================

class Hippocampus:
    """
    Core memory manager for Oracle observations and semantic search.

    Provides automatic observation capture, pattern detection, and
    token-efficient progressive disclosure queries.
    """

    def __init__(self, db_path: Path = None, auto_init: bool = True):
        """
        Initialize Hippocampus memory manager.

        Args:
            db_path: Path to SQLite database (default: oracle/data/memory/observations.db)
            auto_init: Automatically initialize database if it doesn't exist
        """
        self.db_path = db_path or MEMORY_DB
        self.memory_dir = self.db_path.parent

        if auto_init:
            self._ensure_database()

    def _ensure_database(self) -> None:
        """Ensure database and directory structure exists."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            # Create tables
            conn.execute(OBSERVATIONS_TABLE)

            # Create indexes (execute separately)
            for index_sql in OBSERVATIONS_INDEXES.strip().split(';'):
                if index_sql.strip():
                    conn.execute(index_sql)

            conn.execute(PATTERNS_TABLE)

            for index_sql in PATTERNS_INDEXES.strip().split(';'):
                if index_sql.strip():
                    conn.execute(index_sql)

            conn.execute(SESSIONS_TABLE)

            for index_sql in SESSIONS_INDEXES.strip().split(';'):
                if index_sql.strip():
                    conn.execute(index_sql)

            conn.execute(METADATA_TABLE)

            # Set schema version
            conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                ("schema_version", SCHEMA_VERSION)
            )
            conn.commit()

    # ========================================================================
    # LAYER 1: SEARCH - Summaries Only (~50 tokens/result)
    # ========================================================================

    def search(
        self,
        query: str,
        context: Optional[str] = None,
        observation_type: Optional[str] = None,
        limit: int = 10,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Search observations - Layer 1: Returns summaries only.

        This is the most token-efficient search mode, returning only
        brief summaries without full details.

        Args:
            query: Search query (searches summary and details fields)
            context: Filter by context (Oracle/Dev/Dash/Crank/Pocket)
            observation_type: Filter by type (file_change, tool_usage, etc.)
            limit: Maximum results to return
            days_back: Only search last N days

        Returns:
            List of observations with summary field only (~50 tokens each)
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Build query
            sql = """
                SELECT id, timestamp, session_id, context, observation_type,
                       summary, file_path, layer_id
                FROM observations
                WHERE (summary LIKE ? OR details LIKE ?)
                  AND timestamp >= datetime('now', '-' || ? || ' days')
            """
            params = [f"%{query}%", f"%{query}%", days_back]

            if context:
                sql += " AND context = ?"
                params.append(context)

            if observation_type:
                sql += " AND observation_type = ?"
                params.append(observation_type)

            sql += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(sql, params)
            results = [dict(row) for row in cursor.fetchall()]

            return results

    # ========================================================================
    # LAYER 2: TIMELINE - Context + Relationships (~200 tokens/result)
    # ========================================================================

    def get_timeline(
        self,
        query: str,
        context: Optional[str] = None,
        limit: int = 5,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Get timeline with context - Layer 2: Summaries + relationships.

        Returns observations with their temporal context and relationships
        to other observations (same file, same session, related patterns).

        Args:
            query: Search query
            context: Filter by context
            limit: Maximum results
            days_back: Only search last N days

        Returns:
            List of observations with summary + context (~200 tokens each)
        """
        # Get base observations
        observations = self.search(query, context, limit=limit, days_back=days_back)

        # Enrich with context
        enriched = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            for obs in observations:
                # Get related observations (same file, same session)
                related_sql = """
                    SELECT id, summary, observation_type
                    FROM observations
                    WHERE (file_path = ? OR session_id = ?)
                      AND id != ?
                    ORDER BY timestamp DESC
                    LIMIT 3
                """
                related = conn.execute(
                    related_sql,
                    (obs.get("file_path"), obs.get("session_id"), obs["id"])
                ).fetchall()

                obs["related"] = [dict(r) for r in related]
                obs["related_count"] = len(related)
                enriched.append(obs)

        return enriched

    # ========================================================================
    # LAYER 3: DETAILS - Full Observation (~500 tokens)
    # ========================================================================

    def get_observation(self, observation_id: int) -> Optional[Observation]:
        """
        Get full observation details - Layer 3: Complete information.

        Use this only when you need full context. For most queries,
        Layer 1 (search) or Layer 2 (timeline) is sufficient.

        Args:
            observation_id: Observation ID

        Returns:
            Full Observation object with all details
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT id, timestamp, session_id, context, observation_type,
                       summary, details, file_path, layer_id, confidence, metadata
                FROM observations WHERE id = ?
                """,
                (observation_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            obs_dict = dict(row)
            if obs_dict.get("metadata"):
                obs_dict["metadata"] = json.loads(obs_dict["metadata"])

            return Observation.from_dict(obs_dict)

    # ========================================================================
    # CAPTURE - Add New Observations
    # ========================================================================

    def capture(
        self,
        observation_type: ObservationType,
        summary: str,
        details: str = "",
        session_id: str = "",
        context: str = "Oracle",
        file_path: Optional[str] = None,
        layer_id: Optional[str] = None,
        confidence: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Capture a new observation.

        Args:
            observation_type: Type of observation
            summary: Brief summary (~50 tokens) - used in Layer 1 searches
            details: Full details (~500 tokens) - only loaded in Layer 3
            session_id: Session identifier (e.g., "O105", "D107")
            context: Context name (Oracle/Dev/Dash/Crank/Pocket)
            file_path: Related file path if applicable
            layer_id: Related layer ID if applicable (L0-L8)
            confidence: Confidence score (0.0-1.0)
            metadata: Additional metadata dict

        Returns:
            Observation ID
        """
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO observations (
                    timestamp, session_id, context, observation_type,
                    summary, details, file_path, layer_id, confidence, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    timestamp,
                    session_id,
                    context,
                    observation_type.value,
                    summary,
                    details,
                    file_path,
                    layer_id,
                    confidence,
                    json.dumps(metadata) if metadata else None
                )
            )
            conn.commit()
            return cursor.lastrowid

    def capture_file_change(
        self,
        file_path: str,
        change_type: str,
        session_id: str,
        context: str = "Oracle",
        layer_id: Optional[str] = None,
        summary: Optional[str] = None
    ) -> int:
        """
        Capture a file change observation (convenience method).

        Args:
            file_path: Path to changed file
            change_type: Type of change (created, modified, deleted)
            session_id: Session ID
            context: Context name
            layer_id: Layer ID if file is in a layer
            summary: Optional custom summary

        Returns:
            Observation ID
        """
        if not summary:
            filename = Path(file_path).name
            summary = f"{change_type.capitalize()} {filename}"
            if layer_id:
                summary += f" ({layer_id})"

        details = f"File: {file_path}\nChange: {change_type}\nSession: {session_id}"

        return self.capture(
            observation_type=ObservationType.FILE_CHANGE,
            summary=summary,
            details=details,
            session_id=session_id,
            context=context,
            file_path=file_path,
            layer_id=layer_id
        )

    # ========================================================================
    # PATTERNS - Pattern Detection
    # ========================================================================

    def detect_patterns(self, days_back: int = 7) -> List[Pattern]:
        """
        Detect patterns in recent observations.

        Looks for:
        - Repeated file modifications
        - New feature development
        - Decision points
        - Error patterns

        Args:
            days_back: Analyze last N days

        Returns:
            List of detected patterns
        """
        patterns = []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Pattern 1: Repeated file modifications
            cursor = conn.execute(
                """
                SELECT file_path, COUNT(*) as count,
                       GROUP_CONCAT(id) as obs_ids
                FROM observations
                WHERE file_path IS NOT NULL
                  AND timestamp >= datetime('now', '-' || ? || ' days')
                GROUP BY file_path
                HAVING count >= 2
                ORDER BY count DESC
                """,
                (days_back,)
            )

            for row in cursor.fetchall():
                patterns.append(Pattern(
                    pattern_type=PatternType.REPEATED_FILE.value,
                    description=f"File modified {row['count']} times: {row['file_path']}",
                    first_seen=datetime.now().isoformat(),  # Would need to query actual first
                    last_seen=datetime.now().isoformat(),
                    occurrence_count=row['count'],
                    confidence=min(row['count'] / 10.0, 1.0),
                    related_observations=[int(x) for x in row['obs_ids'].split(',')]
                ))

            # Pattern 2: New feature development
            # Look for DECISION or FILE_CHANGE observations with "new feature" keywords
            cursor = conn.execute(
                """
                SELECT id, summary, details, observation_type, file_path
                FROM observations
                WHERE (observation_type IN ('decision', 'file_change'))
                  AND (summary LIKE '%new%' OR summary LIKE '%add%' OR summary LIKE '%implement%'
                       OR summary LIKE '%create%' OR details LIKE '%new feature%'
                       OR details LIKE '%implement%' OR summary LIKE '%feature%')
                  AND timestamp >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
                """,
                (days_back,)
            )

            feature_obs = cursor.fetchall()
            if feature_obs:
                # Group related observations (same file or similar summaries)
                feature_groups = {}
                for obs in feature_obs:
                    # Try to extract feature name from summary
                    key = obs['file_path'] if obs['file_path'] else obs['summary'][:50]
                    if key not in feature_groups:
                        feature_groups[key] = []
                    feature_groups[key].append(obs['id'])

                # Create patterns for significant feature groups
                for key, obs_ids in feature_groups.items():
                    if len(obs_ids) >= 1:  # At least 1 observation
                        first_obs = next(o for o in feature_obs if o['id'] == obs_ids[0])
                        patterns.append(Pattern(
                            pattern_type=PatternType.NEW_FEATURE.value,
                            description=f"Feature development: {first_obs['summary'][:80]}",
                            first_seen=datetime.now().isoformat(),
                            last_seen=datetime.now().isoformat(),
                            occurrence_count=len(obs_ids),
                            confidence=0.7,  # Medium confidence
                            related_observations=obs_ids
                        ))

            # Pattern 3: Decision points
            # Look for DECISION observation type
            cursor = conn.execute(
                """
                SELECT id, summary, details, file_path, session_id
                FROM observations
                WHERE observation_type = 'decision'
                  AND timestamp >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
                """,
                (days_back,)
            )

            decision_obs = cursor.fetchall()
            for obs in decision_obs:
                patterns.append(Pattern(
                    pattern_type=PatternType.DECISION_POINT.value,
                    description=f"Decision: {obs['summary'][:100]}",
                    first_seen=datetime.now().isoformat(),
                    last_seen=datetime.now().isoformat(),
                    occurrence_count=1,
                    confidence=0.9,  # High confidence for explicit decisions
                    related_observations=[obs['id']]
                ))

            # Pattern 4: Error patterns
            # Look for ERROR observation type or observations with error keywords
            cursor = conn.execute(
                """
                SELECT summary, COUNT(*) as count, GROUP_CONCAT(id) as obs_ids
                FROM observations
                WHERE (observation_type = 'error'
                       OR summary LIKE '%error%' OR summary LIKE '%failed%'
                       OR summary LIKE '%exception%' OR summary LIKE '%bug%')
                  AND timestamp >= datetime('now', '-' || ? || ' days')
                GROUP BY summary
                HAVING count >= 2
                ORDER BY count DESC
                """,
                (days_back,)
            )

            for row in cursor.fetchall():
                patterns.append(Pattern(
                    pattern_type=PatternType.ERROR_PATTERN.value,
                    description=f"Recurring error: {row['summary'][:100]}",
                    first_seen=datetime.now().isoformat(),
                    last_seen=datetime.now().isoformat(),
                    occurrence_count=row['count'],
                    confidence=min(row['count'] / 5.0, 1.0),  # Higher weight for errors
                    related_observations=[int(x) for x in row['obs_ids'].split(',')]
                ))

        return patterns

    def save_pattern(self, pattern: Pattern) -> int:
        """
        Save a detected pattern to database.

        Args:
            pattern: Pattern to save

        Returns:
            Pattern ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO patterns (
                    pattern_type, description, first_seen, last_seen,
                    occurrence_count, confidence, related_observations
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pattern.pattern_type,
                    pattern.description,
                    pattern.first_seen,
                    pattern.last_seen,
                    pattern.occurrence_count,
                    pattern.confidence,
                    json.dumps(pattern.related_observations) if pattern.related_observations else None
                )
            )
            conn.commit()
            return cursor.lastrowid

    # ========================================================================
    # STATISTICS
    # ========================================================================

    def get_stats(self) -> MemoryStats:
        """
        Get memory system statistics.

        Returns:
            MemoryStats object with counts and breakdown
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Total observations
            total = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]

            # By context
            by_context = {}
            for row in conn.execute(
                "SELECT context, COUNT(*) as count FROM observations GROUP BY context"
            ):
                by_context[row['context']] = row['count']

            # By type
            by_type = {}
            for row in conn.execute(
                "SELECT observation_type, COUNT(*) as count FROM observations GROUP BY observation_type"
            ):
                by_type[row['observation_type']] = row['count']

            # Total patterns
            total_patterns = conn.execute("SELECT COUNT(*) FROM patterns").fetchone()[0]

            # Date range
            date_range = conn.execute(
                "SELECT MIN(timestamp), MAX(timestamp) FROM observations"
            ).fetchone()

            # DB size
            db_size_mb = self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0.0

            return MemoryStats(
                total_observations=total,
                observations_by_context=by_context,
                observations_by_type=by_type,
                total_patterns=total_patterns,
                date_range=date_range,
                db_size_mb=round(db_size_mb, 2)
            )

    def print_stats(self) -> None:
        """Print memory statistics in a readable format."""
        stats = self.get_stats()

        print("\n🧠 Hippocampus Memory Statistics")
        print("=" * 60)
        print(f"Total Observations: {stats.total_observations}")
        print(f"Total Patterns: {stats.total_patterns}")
        print(f"Database Size: {stats.db_size_mb} MB")

        if stats.date_range and stats.date_range[0]:
            print(f"Date Range: {stats.date_range[0]} to {stats.date_range[1]}")

        print("\nBy Context:")
        for context, count in sorted(stats.observations_by_context.items()):
            print(f"  {context}: {count}")

        print("\nBy Type:")
        for obs_type, count in sorted(stats.observations_by_type.items()):
            print(f"  {obs_type}: {count}")

        print("=" * 60)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for Hippocampus memory manager."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Hippocampus - Oracle Memory Consolidation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # search command
    search_parser = subparsers.add_parser("search", help="Search observations (Layer 1)")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--context", help="Filter by context")
    search_parser.add_argument("--type", help="Filter by observation type")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results")
    search_parser.add_argument("--days", type=int, default=30, help="Days to search back")

    # timeline command
    timeline_parser = subparsers.add_parser("timeline", help="Get timeline (Layer 2)")
    timeline_parser.add_argument("query", help="Search query")
    timeline_parser.add_argument("--context", help="Filter by context")
    timeline_parser.add_argument("--limit", type=int, default=5, help="Max results")
    timeline_parser.add_argument("--days", type=int, default=30, help="Days to search back")

    # details command
    details_parser = subparsers.add_parser("details", help="Get full details (Layer 3)")
    details_parser.add_argument("observation_id", type=int, help="Observation ID")

    # patterns command
    patterns_parser = subparsers.add_parser("patterns", help="Show detected patterns")
    patterns_parser.add_argument("--days", type=int, default=7, help="Days to analyze")

    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show memory statistics")

    # capture command (for testing)
    capture_parser = subparsers.add_parser("capture", help="Manually capture observation")
    capture_parser.add_argument("type", choices=[t.value for t in ObservationType])
    capture_parser.add_argument("summary", help="Summary text")
    capture_parser.add_argument("--details", help="Full details")
    capture_parser.add_argument("--session", default="test", help="Session ID")
    capture_parser.add_argument("--context", default="Oracle", help="Context")

    args = parser.parse_args()

    # Initialize Hippocampus
    hippo = Hippocampus()

    if args.command == "search":
        results = hippo.search(
            args.query,
            context=args.context,
            observation_type=args.type,
            limit=args.limit,
            days_back=args.days
        )
        print(f"\n🔍 Found {len(results)} observations:\n")
        for r in results:
            print(f"[{r['id']}] {r['timestamp'][:19]} | {r['context']} | {r['observation_type']}")
            print(f"    {r['summary']}")
            if r.get('file_path'):
                print(f"    📄 {r['file_path']}")
            print()

    elif args.command == "timeline":
        results = hippo.get_timeline(
            args.query,
            context=args.context,
            limit=args.limit,
            days_back=args.days
        )
        print(f"\n📅 Timeline ({len(results)} observations):\n")
        for r in results:
            print(f"[{r['id']}] {r['timestamp'][:19]} | {r['context']}")
            print(f"    {r['summary']}")
            if r.get('related_count', 0) > 0:
                print(f"    🔗 {r['related_count']} related observations")
            print()

    elif args.command == "details":
        obs = hippo.get_observation(args.observation_id)
        if obs:
            print(f"\n📋 Observation {obs.id}:\n")
            print(f"Timestamp: {obs.timestamp}")
            print(f"Session: {obs.session_id}")
            print(f"Context: {obs.context}")
            print(f"Type: {obs.observation_type}")
            print(f"\nSummary:")
            print(f"  {obs.summary}")
            if obs.details:
                print(f"\nDetails:")
                print(f"  {obs.details}")
            if obs.file_path:
                print(f"\nFile: {obs.file_path}")
            if obs.layer_id:
                print(f"Layer: {obs.layer_id}")
        else:
            print(f"❌ Observation {args.observation_id} not found")

    elif args.command == "patterns":
        patterns = hippo.detect_patterns(days_back=args.days)
        print(f"\n🔍 Detected {len(patterns)} patterns:\n")
        for p in patterns:
            print(f"• {p.pattern_type}: {p.description}")
            print(f"  Confidence: {p.confidence:.2f} | Occurrences: {p.occurrence_count}")
            print()

    elif args.command == "stats":
        hippo.print_stats()

    elif args.command == "capture":
        obs_type = ObservationType(args.type)
        obs_id = hippo.capture(
            observation_type=obs_type,
            summary=args.summary,
            details=args.details or "",
            session_id=args.session,
            context=args.context
        )
        print(f"✅ Captured observation {obs_id}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
