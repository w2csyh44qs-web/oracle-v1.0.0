"""
Oracle Validation Module
========================

Brain cell modules for codebase integrity verification and assessment.

Modules:
    - topoisomerase: Integrity verification after edits/refactors
    - helicase: Codebase assessment and analysis for new projects

Metaphors:
    - Topoisomerase: Relieves tension from continuous DNA edits (verifies code integrity)
    - Helicase: Opens/unwinds DNA for reading (assesses new codebases)
"""

from pathlib import Path

# Module paths
VALIDATION_DIR = Path(__file__).parent
TEMPLATES_DIR = VALIDATION_DIR / "templates"

__all__ = [
    "VALIDATION_DIR",
    "TEMPLATES_DIR",
]
