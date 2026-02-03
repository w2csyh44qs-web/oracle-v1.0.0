"""
Oracle Control Center - Brain Cell Architecture
================================================

Brain Cell Modules:
    - maintenance/microglia.py - Error detection, cleanup, debugging
    - context/astrocytes.py - Context management, snapshots, environment
    - optimization/oligodendrocytes.py - Performance, API costs
    - sync/ependymal.py - Documentation sync, reports
    - project/cortex.py - Project-specific tools (presets, layers)
    - seeg.py - Real-time monitoring dashboard (stereoEEG metaphor)

Utilities:
    - context/context_manager.py - Context file management
    - context/daemon.py - Cross-session daemon
    - context/session_spawner.py - Session spawning

Main Entry Point:
    - project_oracle.py - Central CLI orchestrator
"""

from oracle.context.context_manager import ContextManager, ContextType, ContextPaths
from oracle.context.session_spawner import SessionSpawner, HANDOFF_RULES

__all__ = [
    "ContextManager",
    "ContextType",
    "ContextPaths",
    "SessionSpawner",
    "HANDOFF_RULES",
]
