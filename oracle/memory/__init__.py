"""
Oracle Memory Module - Hippocampus Memory Consolidation

The memory module provides automatic observation capture, semantic search,
and token-efficient progressive disclosure for Oracle sessions.

**Neural Metaphor:** The hippocampus consolidates short-term memories before
transfer to cortex (long-term storage). This module consolidates session
observations before updating context files.

Modules:
- hippocampus.py - Core memory manager (LOCATION)
- memory_hooks.py - Lifecycle event capture (coming in Phase 2.5)
- context_updater.py - Auto-update contexts (coming in Phase 3)

Usage:
    from oracle.memory import Hippocampus, ObservationType

    # Initialize memory manager
    hippo = Hippocampus()

    # Capture observation
    hippo.capture(
        observation_type=ObservationType.FILE_CHANGE,
        summary="Modified cortex.py to load from config",
        session_id="O105",
        context="Oracle"
    )

    # Search observations (Layer 1 - summaries only)
    results = hippo.search("cortex config")

    # Get timeline with context (Layer 2)
    timeline = hippo.get_timeline("cortex config")

    # Get full details (Layer 3)
    obs = hippo.get_observation(observation_id=1)

Author: Oracle Brain Cell Architecture (P30)
"""

from oracle.memory.hippocampus import (
    Hippocampus,
    Observation,
    Pattern,
    MemoryStats,
    ObservationType,
    PatternType,
)
from oracle.memory.context_updater import (
    ContextUpdater,
    ContextUpdate,
    ValidationResult,
)
from oracle.memory.autosave_integration import (
    suggest_context_updates,
    review_pending_updates,
    apply_pending_updates,
    clear_pending_updates,
)

__all__ = [
    "Hippocampus",
    "Observation",
    "Pattern",
    "MemoryStats",
    "ObservationType",
    "PatternType",
    "ContextUpdater",
    "ContextUpdate",
    "ValidationResult",
    "suggest_context_updates",
    "review_pending_updates",
    "apply_pending_updates",
    "clear_pending_updates",
]

__version__ = "1.0.0"
