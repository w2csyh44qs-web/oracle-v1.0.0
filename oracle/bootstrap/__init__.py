"""
Oracle Bootstrap Module

Project-agnostic initialization system for deploying Oracle to any Python project.

Modules:
- detector.py - Project structure detection
- initializer.py - Oracle init command
- templates/ - Config and context file templates

Usage:
    from oracle.bootstrap import ProjectDetector, OracleInitializer

    detector = ProjectDetector('/path/to/project')
    profile = detector.analyze()

    initializer = OracleInitializer('/path/to/project')
    initializer.init()

Author: Oracle Brain Cell Architecture (P30 Phase 4)
"""

from oracle.bootstrap.detector import ProjectDetector, ProjectProfile
from oracle.bootstrap.initializer import OracleInitializer, InitializationError

__all__ = [
    "ProjectDetector",
    "ProjectProfile",
    "OracleInitializer",
    "InitializationError",
]

__version__ = "1.0.0"
