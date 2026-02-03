#!/usr/bin/env python3
"""
Oligodendrocytes - Oracle Brain Cell: Performance Optimization, API Cost Tracking
=================================================================================

Brain Metaphor: Oligodendrocytes produce myelin sheaths that speed up neural
transmission. This module focuses on performance optimization, efficiency,
and cost management - making everything run faster and cheaper.

Responsibilities:
- API cost tracking and estimation
- Performance optimization detection
- Efficiency improvements
- Cost logging and analysis

Commands: optimize, api-log
"""

import os
import ast
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from contextlib import contextmanager

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

ORACLE_DIR = Path(__file__).parent.parent  # Up from optimization/ to oracle/
PROJECT_ROOT = ORACLE_DIR.parent  # Up from oracle/ to project root
REPORTS_DIR = ORACLE_DIR / "reports"
DOCS_DIR = ORACLE_DIR / "docs"
CONTEXT_DIR = DOCS_DIR / "context"

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")

def debug_log(msg: str, category: str = "general"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  🔍 [{timestamp}] [{category}] {msg}")


# =============================================================================
# OPTIMIZATION CATEGORIES
# =============================================================================

OPTIMIZATION_CATEGORIES = {
    "code": "Code quality: long functions, duplication, complexity, unused code",
    "workflow": "Workflow: repeated manual steps, friction points",
    "tools": "Tools/Skills: tasks matching available capabilities",
    "architecture": "Architecture: technical debt, placeholders, structure",
    "cost": "Cost: API usage, cheaper alternatives",
    "documentation": "Documentation: staleness, gaps, drift",
    "automation": "Automation: manual processes to script",
}


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
# API CALL LOGGER
# =============================================================================

class APICallLogger:
    """Track external API calls with timing and cost estimation."""

    # Approximate costs per 1K tokens (as of Dec 2024)
    COST_PER_1K = {
        "gpt-4o": {"input": 0.0025, "output": 0.01},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        "elevenlabs": {"chars": 0.00003},
        "fal-ai": {"image": 0.01},
        "pexels": {"request": 0.0},
        "gemini-2.0-flash-exp": {"input": 0.0, "output": 0.0},
        "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
        "gemini-1.5-flash": {"input": 0.000075, "output": 0.0003},
    }

    def __init__(self, log_file: Path = None):
        self.calls = []
        self.log_file = log_file or (REPORTS_DIR / "api_calls.json")
        self.session_start = datetime.now()
        self._current_call = None

    def log_call(self, provider: str, model: str = None, duration: float = 0,
                 tokens_in: int = 0, tokens_out: int = 0, chars: int = 0,
                 images: int = 0, success: bool = True, error: str = None,
                 metadata: dict = None):
        """Log an API call with timing and usage info."""
        cost = self._estimate_cost(provider, model, tokens_in, tokens_out, chars, images)

        call_record = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "duration_s": round(duration, 3),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "chars": chars,
            "images": images,
            "cost_usd": round(cost, 6),
            "success": success,
            "error": error,
            "metadata": metadata or {}
        }

        self.calls.append(call_record)

        if os.environ.get("ORACLE_DEBUG"):
            status = "✓" if success else "✗"
            print(f"  📡 [{provider}] {model or 'N/A'} {status} {duration:.2f}s ${cost:.4f}")

        if os.environ.get("ORACLE_API_LOG"):
            self._save_to_file()

    def _estimate_cost(self, provider: str, model: str, tokens_in: int,
                       tokens_out: int, chars: int, images: int) -> float:
        """Estimate cost based on usage."""
        cost = 0.0

        if model and model in self.COST_PER_1K:
            rates = self.COST_PER_1K[model]
            if "input" in rates:
                cost += (tokens_in / 1000) * rates["input"]
                cost += (tokens_out / 1000) * rates["output"]
            if "chars" in rates:
                cost += chars * rates["chars"]
            if "image" in rates:
                cost += images * rates["image"]
        elif provider == "elevenlabs":
            cost = chars * self.COST_PER_1K.get("elevenlabs", {}).get("chars", 0.00003)
        elif provider == "fal-ai":
            cost = images * self.COST_PER_1K.get("fal-ai", {}).get("image", 0.01)

        return cost

    @contextmanager
    def track(self, provider: str, model: str = None):
        """Context manager for tracking an API call."""
        start_time = datetime.now()
        call_data = {
            "tokens_in": 0,
            "tokens_out": 0,
            "chars": 0,
            "images": 0,
            "success": True,
            "error": None
        }

        class CallContext:
            def __init__(self, data):
                self._data = data

            @property
            def tokens_in(self):
                return self._data["tokens_in"]

            @tokens_in.setter
            def tokens_in(self, value):
                self._data["tokens_in"] = value

            @property
            def tokens_out(self):
                return self._data["tokens_out"]

            @tokens_out.setter
            def tokens_out(self, value):
                self._data["tokens_out"] = value

        context = CallContext(call_data)

        try:
            yield context
        except Exception as e:
            call_data["success"] = False
            call_data["error"] = str(e)
            raise
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_call(
                provider=provider,
                model=model,
                duration=duration,
                tokens_in=call_data["tokens_in"],
                tokens_out=call_data["tokens_out"],
                chars=call_data["chars"],
                images=call_data["images"],
                success=call_data["success"],
                error=call_data["error"]
            )

    def get_summary(self) -> dict:
        """Get summary statistics for the session."""
        if not self.calls:
            return {"total_calls": 0, "total_cost": 0, "total_duration": 0}

        total_cost = sum(c["cost_usd"] for c in self.calls)
        total_duration = sum(c["duration_s"] for c in self.calls)
        success_count = sum(1 for c in self.calls if c["success"])

        by_provider = {}
        for call in self.calls:
            provider = call["provider"]
            if provider not in by_provider:
                by_provider[provider] = {"calls": 0, "cost": 0, "duration": 0}
            by_provider[provider]["calls"] += 1
            by_provider[provider]["cost"] += call["cost_usd"]
            by_provider[provider]["duration"] += call["duration_s"]

        return {
            "total_calls": len(self.calls),
            "successful_calls": success_count,
            "failed_calls": len(self.calls) - success_count,
            "total_cost_usd": round(total_cost, 4),
            "total_duration_s": round(total_duration, 2),
            "by_provider": by_provider,
            "session_start": self.session_start.isoformat(),
        }

    def print_summary(self):
        """Print formatted summary to console."""
        summary = self.get_summary()

        if summary["total_calls"] == 0:
            print("📡 No API calls logged this session.")
            return

        print()
        print("=" * 50)
        print("📡 API CALL SUMMARY")
        print("=" * 50)
        print(f"Total Calls: {summary['total_calls']} ({summary['successful_calls']} success, {summary['failed_calls']} failed)")
        print(f"Total Cost:  ${summary['total_cost_usd']:.4f}")
        print(f"Total Time:  {summary['total_duration_s']:.1f}s")
        print()

        if summary["by_provider"]:
            print("By Provider:")
            for provider, stats in summary["by_provider"].items():
                print(f"  {provider}: {stats['calls']} calls, ${stats['cost']:.4f}, {stats['duration']:.1f}s")

        print("=" * 50)

    def _save_to_file(self):
        """Save calls to JSON file."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if self.log_file.exists():
            try:
                with open(self.log_file) as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        existing_timestamps = {c["timestamp"] for c in existing}
        new_calls = [c for c in self.calls if c["timestamp"] not in existing_timestamps]
        existing.extend(new_calls)

        if len(existing) > 1000:
            existing = existing[-1000:]

        with open(self.log_file, 'w') as f:
            json.dump(existing, f, indent=2)

    def clear(self):
        """Clear logged calls for this session."""
        self.calls = []
        self.session_start = datetime.now()


# =============================================================================
# API COST AUDITOR
# =============================================================================

class APICostAuditor:
    """Analyze API usage and costs."""

    def __init__(self, project_root: Path, api_services: dict):
        self.project_root = project_root
        self.api_services = api_services
        self.issues = []
        self.usage = {}

    def run(self) -> tuple:
        """Analyze API usage patterns."""
        self.issues = []
        self.usage = {}

        self._check_env_config()
        self._analyze_api_usage()
        self._check_cost_logs()

        return self.issues, self.usage

    def _check_env_config(self):
        """Verify API keys are configured."""
        env_path = self.project_root / ".env"

        if not env_path.exists():
            self.issues.append(Issue(
                severity="critical",
                category="cost",
                title="Missing .env file",
                description="API keys not configured",
                suggestion="Create .env file with required API keys"
            ))
            return

        env_content = env_path.read_text()

        for service, info in self.api_services.items():
            key = info.get("env_key", "")
            if key and key not in env_content:
                self.issues.append(Issue(
                    severity="warning",
                    category="cost",
                    title=f"Missing API key: {key}",
                    description=f"Required for {service} in layers {info.get('layers', [])}",
                    suggestion=f"Add {key} to .env file"
                ))
            else:
                self.usage[service] = {"configured": True, "layers": info.get("layers", [])}

    def _analyze_api_usage(self):
        """Find API calls in scripts."""
        scripts_dir = self.project_root / "scripts"

        api_patterns = {
            "openai": [r'openai\.', r'client\.chat\.completions', r'client\.audio'],
            "elevenlabs": [r'elevenlabs', r'ElevenLabs', r'generate\(.*voice'],
            "fal": [r'fal_client', r'fal\.ai'],
            "tavily": [r'tavily', r'TavilyClient'],
            "pexels": [r'pexels', r'PEXELS'],
        }

        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                try:
                    content = script.read_text()

                    for service, patterns in api_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                if service not in self.usage:
                                    self.usage[service] = {"configured": False, "layers": [], "scripts": []}
                                if "scripts" not in self.usage[service]:
                                    self.usage[service]["scripts"] = []
                                if script.name not in self.usage[service]["scripts"]:
                                    self.usage[service]["scripts"].append(script.name)
                except Exception:
                    pass

    def _check_cost_logs(self):
        """Check for existing cost tracking."""
        api_calls_file = REPORTS_DIR / "api_calls.json"

        if not api_calls_file.exists():
            self.issues.append(Issue(
                severity="info",
                category="cost",
                title="No API cost log found",
                description="Consider enabling API call logging",
                suggestion="Set ORACLE_API_LOG=1 to enable logging"
            ))


# =============================================================================
# OPTIMIZATION DETECTOR
# =============================================================================

class OptimizationDetector:
    """Detect quantifiable optimization opportunities."""

    def __init__(self, project_root: Path, config: dict):
        self.project_root = project_root
        self.config = config
        self.scripts_dir = project_root / "scripts"
        self.oracle_dir = project_root / "oracle"
        self.docs_dir = DOCS_DIR
        self.context_dir = CONTEXT_DIR

    def detect_all(self) -> dict:
        """Run all detection checks and return structured results."""
        results = {
            "code": self._detect_code_issues(),
            "documentation": self._detect_doc_staleness(),
            "architecture": self._detect_placeholders(),
            "workflow": self._detect_workflow_patterns(),
            "cost": self._detect_cost_opportunities(),
        }

        return {k: v for k, v in results.items() if v}

    def _detect_code_issues(self) -> list:
        """Detect code-related optimization opportunities."""
        opportunities = []

        scan_dirs = [
            self.scripts_dir,
            self.oracle_dir / "maintenance",
            self.project_root / "app"
        ]

        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                continue

            for script in scan_dir.rglob("*.py"):
                if script.name.startswith("__"):
                    continue

                try:
                    content = script.read_text()
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                            if func_lines > 100:
                                opportunities.append({
                                    "type": "long_function",
                                    "description": f"Function `{node.name}` is {func_lines} lines",
                                    "file": str(script.relative_to(self.project_root)),
                                    "line": node.lineno,
                                    "priority": "medium",
                                })

                    todo_count = len(re.findall(r'#\s*(TODO|FIXME|XXX|HACK)', content, re.IGNORECASE))
                    if todo_count > 5:
                        opportunities.append({
                            "type": "todo_accumulation",
                            "description": f"{todo_count} TODO/FIXME comments in {script.name}",
                            "file": str(script.relative_to(self.project_root)),
                            "priority": "low",
                        })

                except Exception:
                    pass

        return opportunities

    def _detect_doc_staleness(self) -> list:
        """Detect stale documentation."""
        opportunities = []
        now = datetime.now()

        doc_paths = [
            ("oracle/docs/context/DEV_CONTEXT.md", 3),
            ("oracle/docs/context/ORACLE_CONTEXT.md", 3),
            ("oracle/docs/overview/ARCHITECTURE.md", 14),
            ("oracle/docs/overview/PHILOSOPHY.md", 30),
            ("oracle/docs/overview/WORKFLOW.md", 14),
        ]

        for rel_path, threshold_days in doc_paths:
            doc_path = self.project_root / rel_path
            if doc_path.exists():
                mtime = datetime.fromtimestamp(doc_path.stat().st_mtime)
                age_days = (now - mtime).days
                if age_days > threshold_days:
                    opportunities.append({
                        "type": "stale_doc",
                        "description": f"{rel_path} not updated in {age_days} days",
                        "file": rel_path,
                        "age_days": age_days,
                        "threshold": threshold_days,
                        "priority": "low" if age_days < threshold_days * 2 else "medium",
                    })

        return opportunities

    def _detect_placeholders(self) -> list:
        """Detect placeholder/future markers."""
        opportunities = []

        search_paths = [
            self.scripts_dir,
            self.oracle_dir,
        ]

        placeholder_patterns = [
            (r'#\s*PLACEHOLDER', "placeholder marker"),
            (r'#\s*FUTURE:', "future marker"),
            (r'#\s*NOT IMPLEMENTED', "not implemented"),
            (r'pass\s*#\s*TODO', "empty implementation"),
        ]

        for search_dir in search_paths:
            if not search_dir.exists():
                continue

            for file_path in search_dir.rglob("*.py"):
                try:
                    content = file_path.read_text()
                    for pattern, marker_type in placeholder_patterns:
                        matches = list(re.finditer(pattern, content, re.IGNORECASE))
                        if matches:
                            opportunities.append({
                                "type": "placeholder",
                                "description": f"{len(matches)} {marker_type}(s) in {file_path.name}",
                                "file": str(file_path.relative_to(self.project_root)),
                                "count": len(matches),
                                "priority": "low",
                            })
                except Exception:
                    pass

        return opportunities

    def _detect_workflow_patterns(self) -> list:
        """Detect workflow improvement opportunities."""
        opportunities = []

        dev_context = self.context_dir / "DEV_CONTEXT.md"
        if dev_context.exists():
            content = dev_context.read_text()

            if content.count("manually") > 3:
                opportunities.append({
                    "type": "manual_repetition",
                    "description": "Multiple 'manually' mentions suggest automation opportunity",
                    "file": "oracle/docs/context/DEV_CONTEXT.md",
                    "priority": "medium",
                })

        return opportunities

    def _detect_cost_opportunities(self) -> list:
        """Detect cost optimization opportunities."""
        opportunities = []

        api_calls_file = REPORTS_DIR / "api_calls.json"

        if not api_calls_file.exists():
            opportunities.append({
                "type": "no_cost_tracking",
                "description": "No API cost tracking - consider enabling with ORACLE_API_LOG=1",
                "priority": "low",
            })

        return opportunities

    def format_results(self, results: dict = None) -> str:
        """Format detection results for console output."""
        if results is None:
            results = self.detect_all()

        if not results:
            return "No optimization opportunities detected."

        lines = ["🔍 Optimization Opportunities Detected:"]
        lines.append("")

        total = 0
        for category, items in results.items():
            if items:
                lines.append(f"  {category.upper()} ({len(items)} items)")
                for item in items[:5]:
                    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(item.get("priority", "low"), "•")
                    lines.append(f"    {priority_icon} {item['description']}")
                    total += 1
                if len(items) > 5:
                    lines.append(f"    ... and {len(items) - 5} more")

        lines.append("")
        lines.append(f"Total: {total} opportunities.")

        return "\n".join(lines)


# =============================================================================
# SYNAPSES FUNCTIONS - Connection efficiency & optimization
# =============================================================================

def analyze_api_connections() -> dict:
    """Analyze API connection patterns and suggest batching.

    Examines scripts for API call patterns and identifies opportunities
    to batch similar calls for efficiency.

    Returns:
        Dict with connection analysis and batching suggestions
    """
    results = {
        "total_api_points": 0,
        "by_provider": {},
        "batching_opportunities": [],
        "sequential_calls": [],
    }

    scripts_dir = PROJECT_ROOT / "app" / "core" / "pipeline" / "layers"
    if not scripts_dir.exists():
        scripts_dir = PROJECT_ROOT / "scripts"

    api_patterns = {
        "openai": (r'client\.chat\.completions\.create|openai\.ChatCompletion', "OpenAI"),
        "elevenlabs": (r'elevenlabs\.generate|ElevenLabs\(', "ElevenLabs"),
        "fal": (r'fal_client\.run|fal\.subscribe', "Fal.ai"),
        "pexels": (r'pexels\.search|PEXELS_API', "Pexels"),
        "gemini": (r'genai\.GenerativeModel|model\.generate', "Gemini"),
    }

    if scripts_dir.exists():
        for script in scripts_dir.rglob("*.py"):
            if script.name.startswith("__"):
                continue

            try:
                content = script.read_text()
                script_calls = []

                for provider, (pattern, display_name) in api_patterns.items():
                    matches = list(re.finditer(pattern, content))
                    if matches:
                        if provider not in results["by_provider"]:
                            results["by_provider"][provider] = {
                                "name": display_name,
                                "scripts": [],
                                "call_count": 0
                            }
                        results["by_provider"][provider]["scripts"].append(script.name)
                        results["by_provider"][provider]["call_count"] += len(matches)
                        results["total_api_points"] += len(matches)

                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            script_calls.append((provider, line_num))

                # Detect sequential calls to same provider (batching opportunity)
                if len(script_calls) > 1:
                    sorted_calls = sorted(script_calls, key=lambda x: x[1])
                    for i in range(len(sorted_calls) - 1):
                        curr_provider, curr_line = sorted_calls[i]
                        next_provider, next_line = sorted_calls[i + 1]
                        if curr_provider == next_provider and next_line - curr_line < 10:
                            results["batching_opportunities"].append({
                                "file": script.name,
                                "provider": curr_provider,
                                "lines": [curr_line, next_line],
                                "suggestion": f"Consider batching {curr_provider} calls"
                            })

            except Exception:
                pass

    return results


def get_cache_recommendations() -> list:
    """Analyze caching opportunities across pipeline.

    Identifies data that could be cached to reduce redundant API calls
    and improve performance.

    Returns:
        List of caching recommendations
    """
    recommendations = []

    # Check for repeated data fetching patterns
    scripts_dir = PROJECT_ROOT / "app" / "core" / "pipeline" / "layers"
    if not scripts_dir.exists():
        scripts_dir = PROJECT_ROOT / "scripts"

    cache_patterns = [
        (r'fetch_goatedbets|get_matchup|get_predictions', "API data fetch"),
        (r'load_preset|get_preset|read_preset', "Preset loading"),
        (r'Path\(.*\)\.read_text\(\)|json\.load\(open', "File reading"),
    ]

    files_with_fetches = {}

    if scripts_dir.exists():
        for script in scripts_dir.rglob("*.py"):
            if script.name.startswith("__"):
                continue

            try:
                content = script.read_text()

                for pattern, fetch_type in cache_patterns:
                    matches = list(re.finditer(pattern, content))
                    if matches:
                        key = f"{script.name}:{fetch_type}"
                        if key not in files_with_fetches:
                            files_with_fetches[key] = {
                                "file": script.name,
                                "type": fetch_type,
                                "count": 0,
                                "lines": []
                            }
                        files_with_fetches[key]["count"] += len(matches)
                        for m in matches:
                            line_num = content[:m.start()].count('\n') + 1
                            files_with_fetches[key]["lines"].append(line_num)

            except Exception:
                pass

    # Generate recommendations for files with multiple fetches
    for key, info in files_with_fetches.items():
        if info["count"] > 2:
            recommendations.append({
                "file": info["file"],
                "type": info["type"],
                "occurrences": info["count"],
                "suggestion": f"Consider caching {info['type']} results - {info['count']} occurrences",
                "priority": "medium" if info["count"] > 3 else "low"
            })

    # Check if caching infrastructure exists
    cache_dir = PROJECT_ROOT / ".cache"
    if not cache_dir.exists():
        recommendations.append({
            "type": "infrastructure",
            "suggestion": "No .cache directory found - consider adding file-based caching",
            "priority": "low"
        })

    return recommendations


def optimize_batch_calls(calls: list) -> list:
    """Batch similar API calls for efficiency.

    Groups similar API calls that can be combined into single requests.

    Args:
        calls: List of API call specifications

    Returns:
        List of optimized/batched call groups
    """
    if not calls:
        return []

    # Group by provider and model
    groups = {}
    for call in calls:
        provider = call.get("provider", "unknown")
        model = call.get("model", "default")
        key = f"{provider}:{model}"

        if key not in groups:
            groups[key] = {
                "provider": provider,
                "model": model,
                "calls": [],
                "can_batch": False
            }
        groups[key]["calls"].append(call)

    # Mark groups that can be batched
    batched = []
    for key, group in groups.items():
        if len(group["calls"]) > 1:
            # Check if calls can be batched (same type, compatible params)
            call_types = set(c.get("type", "completion") for c in group["calls"])
            if len(call_types) == 1:
                group["can_batch"] = True
                group["batch_size"] = len(group["calls"])
                group["estimated_savings"] = f"{(len(group['calls']) - 1) * 0.5:.1f}s latency"

        batched.append(group)

    return batched


def get_connection_health() -> dict:
    """Check health of external API connections.

    Verifies API keys are configured and tests connectivity status.

    Returns:
        Dict with connection health status for each API
    """
    health = {
        "timestamp": datetime.now().isoformat(),
        "apis": {},
        "overall_status": "healthy"
    }

    # API key environment variables to check
    api_keys = {
        "openai": "OPENAI_API_KEY",
        "elevenlabs": "ELEVEN_API_KEY",
        "fal": "FAL_KEY",
        "pexels": "PEXELS_API_KEY",
        "tavily": "TAVILY_API_KEY",
        "gemini": "GOOGLE_API_KEY",
    }

    env_path = PROJECT_ROOT / ".env"
    env_content = ""
    if env_path.exists():
        try:
            env_content = env_path.read_text()
        except Exception:
            pass

    issues = 0
    for api_name, env_var in api_keys.items():
        # Check if key is in environment or .env file
        has_env = os.environ.get(env_var)
        has_dotenv = env_var in env_content

        status = "configured" if (has_env or has_dotenv) else "missing"

        health["apis"][api_name] = {
            "env_var": env_var,
            "status": status,
            "in_environment": bool(has_env),
            "in_dotenv": has_dotenv
        }

        if status == "missing":
            issues += 1

    if issues > 0:
        health["overall_status"] = "degraded" if issues < 3 else "critical"
        health["issues_count"] = issues

    return health


def print_connection_health():
    """Print formatted connection health status."""
    health = get_connection_health()

    print()
    print("=" * 50)
    print("🔌 API CONNECTION HEALTH")
    print("=" * 50)

    status_icons = {
        "configured": "✅",
        "missing": "❌"
    }

    for api_name, info in health["apis"].items():
        icon = status_icons.get(info["status"], "❓")
        print(f"  {icon} {api_name}: {info['status']}")

    print()
    overall_icon = "✅" if health["overall_status"] == "healthy" else "⚠️"
    print(f"Overall: {overall_icon} {health['overall_status'].upper()}")
    print("=" * 50)


# =============================================================================
# PUBLIC INTERFACE FUNCTIONS
# =============================================================================

# Global API logger instance
api_logger = APICallLogger()


def run_optimize() -> dict:
    """Run optimization detection and return results.

    Returns:
        Dict with optimization results
    """
    detector = OptimizationDetector(PROJECT_ROOT, {})
    results = detector.detect_all()

    print(detector.format_results(results))
    return results


def get_api_log() -> list:
    """Get API call log from disk.

    Returns:
        List of API call records
    """
    log_file = REPORTS_DIR / "api_calls.json"

    if not log_file.exists():
        return []

    try:
        with open(log_file) as f:
            return json.load(f)
    except Exception:
        return []


def print_api_summary():
    """Print API usage summary from log file."""
    calls = get_api_log()

    if not calls:
        print("📡 No API calls logged.")
        return

    total_cost = sum(c.get("cost_usd", 0) for c in calls)
    total_calls = len(calls)

    by_provider = {}
    for call in calls:
        provider = call.get("provider", "unknown")
        if provider not in by_provider:
            by_provider[provider] = {"calls": 0, "cost": 0}
        by_provider[provider]["calls"] += 1
        by_provider[provider]["cost"] += call.get("cost_usd", 0)

    print()
    print("=" * 50)
    print("📡 API USAGE SUMMARY (from log)")
    print("=" * 50)
    print(f"Total Calls: {total_calls}")
    print(f"Total Cost:  ${total_cost:.4f}")
    print()

    if by_provider:
        print("By Provider:")
        for provider, stats in sorted(by_provider.items()):
            print(f"  {provider}: {stats['calls']} calls, ${stats['cost']:.4f}")

    print("=" * 50)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for oligodendrocytes commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Oligodendrocytes - Performance optimization, API cost tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Optimize command
    subparsers.add_parser("optimize", help="Detect optimization opportunities")

    # API-log command
    api_parser = subparsers.add_parser("api-log", help="Show API usage log")
    api_parser.add_argument("--summary", action="store_true", help="Show summary only")
    api_parser.add_argument("--last", type=int, default=20, help="Show last N calls")

    args = parser.parse_args()

    if args.command == "optimize":
        run_optimize()

    elif args.command == "api-log":
        if args.summary:
            print_api_summary()
        else:
            calls = get_api_log()
            if not calls:
                print("📡 No API calls logged.")
            else:
                print(f"\n📡 Last {args.last} API calls:")
                for call in calls[-args.last:]:
                    status = "✓" if call.get("success") else "✗"
                    print(f"  [{call.get('provider')}] {call.get('model', 'N/A')} {status} ${call.get('cost_usd', 0):.4f}")
                print_api_summary()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
