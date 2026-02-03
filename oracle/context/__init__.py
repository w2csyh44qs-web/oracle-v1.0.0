"""
Oracle Context Management Package

P25: Dynamic context system with registry-driven configuration.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Registry location
CONTEXT_DIR = Path(__file__).parent
REGISTRY_PATH = CONTEXT_DIR / "context_registry.json"

# Cache for registry data
_registry_cache: Optional[Dict] = None


def load_registry() -> Dict:
    """Load the context registry from JSON file."""
    global _registry_cache

    if _registry_cache is not None:
        return _registry_cache

    if not REGISTRY_PATH.exists():
        # Return default if registry doesn't exist
        return {
            "contexts": [],
            "handoff_rules": {},
            "ports": {"normal": {"backend": 5001, "frontend": 5173}, "fallback": {"backend": 5002, "frontend": 5174}},
            "context_path": "oracle/docs/context/"
        }

    _registry_cache = json.loads(REGISTRY_PATH.read_text())
    return _registry_cache


def get_contexts() -> List[Dict]:
    """Get all context definitions."""
    return load_registry().get("contexts", [])


def get_context(context_id: str) -> Optional[Dict]:
    """Get a specific context by ID."""
    for ctx in get_contexts():
        if ctx.get("id") == context_id:
            return ctx
    return None


def get_context_ids() -> List[str]:
    """Get all context IDs."""
    return [ctx.get("id") for ctx in get_contexts()]


def get_session_prefix(context_id: str) -> str:
    """Get the session prefix for a context (e.g., 'D' for dev)."""
    ctx = get_context(context_id)
    return ctx.get("prefix", "S") if ctx else "S"


def get_context_file(context_id: str) -> Optional[str]:
    """Get the context file name for a context."""
    ctx = get_context(context_id)
    return ctx.get("file") if ctx else None


def get_resume_prompt(context_id: str) -> Optional[str]:
    """Get the resume prompt for a context."""
    ctx = get_context(context_id)
    return ctx.get("resume_prompt") if ctx else None


def get_handoff_rules() -> Dict:
    """Get cross-session handoff rules."""
    return load_registry().get("handoff_rules", {})


def get_ports(fallback: bool = False) -> Dict[str, int]:
    """Get server ports (normal or fallback)."""
    ports = load_registry().get("ports", {})
    return ports.get("fallback" if fallback else "normal", {"backend": 5001, "frontend": 5173})


def get_context_path() -> str:
    """Get the base path for context files."""
    return load_registry().get("context_path", "oracle/docs/context/")


def get_coordinator_context() -> Optional[Dict]:
    """Get the coordinator context (usually Oracle)."""
    for ctx in get_contexts():
        if ctx.get("is_coordinator"):
            return ctx
    return None


def clear_cache():
    """Clear the registry cache (useful for testing)."""
    global _registry_cache
    _registry_cache = None
