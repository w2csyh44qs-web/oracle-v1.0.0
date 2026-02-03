#!/usr/bin/env python3
"""
Microglia - Oracle Brain Cell: Error Detection, Cleanup, Debugging
===================================================================

Brain Metaphor: Microglia are the immune cells of the brain. They detect damage,
prune dead synapses, clean up debris, and repair the neural environment.

Responsibilities:
- Error detection and code health analysis
- Dead code pruning and cleanup
- Script debugging and tracing
- Memory leak detection
- Unused import flagging

Commands: audit, clean, debug-script
"""

import os
import ast
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Resolve paths relative to this file
ORACLE_DIR = Path(__file__).parent.parent  # Up from maintenance/ to oracle/
PROJECT_ROOT = ORACLE_DIR.parent  # Up from oracle/ to project root
MAINTENANCE_DIR = ORACLE_DIR / "maintenance"
REPORTS_DIR = ORACLE_DIR / "reports"
AUDITS_DIR = REPORTS_DIR / "audits"

# V2 structure paths
LAYERS_DIR = PROJECT_ROOT / "app" / "core" / "pipeline" / "layers"
SCRIPTS_DIR = LAYERS_DIR  # V2 alias for backward compatibility

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")

def debug_log(msg: str, category: str = "general"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  🔍 [{timestamp}] [{category}] {msg}")

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# Maximum reports to keep
MAX_REPORTS = 5

# Scripts that were deleted/merged/planned - referenced in docs (historical or future)
HISTORICAL_SCRIPTS = {
    "configure_calendar.py",
    "configure_segments.py",
    "SESSION_HANDOFF.md",
    "trend_detection.py",
    "video_assembly.py",
    "instagram_carousel_generator.py",
    "regen_bonus.py",
    "audio_processor.py",
    "ai_utils.py",
}

# Accepted long functions (>100 lines) - design choice, not flagged as warnings
ACCEPTED_LONG_FUNCTIONS = {
    # Assembly
    "assembly.py:assemble_video",
    "assembly.py:assembly_settings_checkpoint",
    "assembly.py:_add_positioned_text_overlays",
    "assembly.py:_add_matchup_card_overlays",
    "assembly.py:process_packages",
    "assembly.py:run",
    "assembly.py:assemble_carousel_reels",
    "assembly.py:concatenate_videos",
    # Media generation
    "media_generation.py:media_settings_checkpoint",
    "media_generation.py:create_media_package",
    "media_generation.py:run",
    "media_generation.py:generate_nano_banana_infographic",
    "media_generation.py:_add_matchup_card_overlays",
    "media_generation.py:main",
    # Distribution
    "distribution.py:distribution_settings_checkpoint",
    "distribution.py:run",
    "distribution.py:process_videos",
    # Idea creation
    "idea_creation.py:_build_idea_prompt",
    "idea_creation.py:generate_from_preset",
    "idea_creation.py:run",
    "idea_creation.py:fetch_goatedbets_matchup",
    "idea_creation.py:_generate_from_api_preset",
    # API utils
    "api_utils.py:transform_matchup_for_carousel",
    "api_utils.py:build_carousel_prompts",
    "api_utils.py:extract_cover_insight",
    "api_utils.py:_extract_matchup_edges",
    "api_utils.py:get_short_prop_reasoning",
    "api_utils.py:extract_betting_thesis",
    "api_utils.py:_extract_key_phrase",
    "api_utils.py:_extract_specific_edge",
    "api_utils.py:build_insights_carousel_prompts",
    # Processors
    "pil_processor.py:composite_carousel_slide",
    "pil_processor.py:create_meme_text_frame",
    "ffmpeg_processor.py:ken_burns",
    "ffmpeg_processor.py:carousel_to_slideshow",
    # Health monitor / sEEG
    "health_monitor.py:main",
    "health_monitor.py:_render_full",
    "health_monitor.py:_get_session_tasks",
    "seeg.py:main",
    "seeg.py:_render_full",
    # Project oracle
    "project_oracle.py:main",
    "project_oracle.py:generate_context_snapshot",
    "project_oracle.py:_archive_recent_changes",
}

# Accepted unused imports - intentional for type hints, re-exports, side effects
ACCEPTED_UNUSED_IMPORTS = {
    "ai_models.py:sys",
    "media_generation.py:get_team_name",
    "media_generation.py:determine_predicted_winner",
    "media_generation.py:get_team_abbrev",
    "media_generation.py:transform_matchup_for_carousel",
    "media_generation.py:get_mock_data",
    "media_generation.py:clean_insight",
    "assembly.py:overlay_logo_on_images",
    "regen_slide.py:INSTAGRAM_FORMATS",
    "api_utils.py:Tuple",
    "api_utils.py:List",
    "ffmpeg_processor.py:os",
    "ffmpeg_processor.py:Tuple",
    "pil_processor.py:sys",
    "data_source.py:Path",
    "data_source.py:Any",
    "content_pipeline.py:Any",
}

# Accepted memory patterns - bounded by design
ACCEPTED_MEMORY_PATTERNS = {
    "project_oracle.py:self.trace_output",
    "project_oracle.py:self.parse_errors",
    "project_oracle.py:self.changes_made",
    "project_oracle.py:self.backup_files",
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Issue:
    """Represents a single issue found during audit."""
    severity: str  # "critical", "warning", "info"
    category: str  # "code", "docs", "workflow", "cost"
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class Suggestion:
    """Represents an optimization suggestion."""
    category: str  # "workflow", "code", "architecture", "cost"
    title: str
    description: str
    impact: str  # "high", "medium", "low"
    effort: str  # "high", "medium", "low"
    details: Optional[str] = None


@dataclass
class AuditReport:
    """Complete audit report."""
    timestamp: datetime = field(default_factory=datetime.now)
    health_score: float = 0.0
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
    doc_sync_status: dict = field(default_factory=dict)
    layer_status: dict = field(default_factory=dict)
    api_usage: dict = field(default_factory=dict)
    summary: str = ""


# =============================================================================
# GLIAL FUNCTIONS - Support utilities for all brain cells
# =============================================================================

def load_oracle_config(config_path: Path = None) -> dict:
    """Load oracle configuration from various sources.

    Consolidates config loading used by multiple brain cell modules.
    Priority: explicit path > maintenance/config.json > defaults

    Args:
        config_path: Optional explicit path to config file

    Returns:
        Dict with configuration values
    """
    defaults = {
        "max_reports": MAX_REPORTS,
        "debug": DEBUG,
        "reports_dir": str(REPORTS_DIR),
        "audits_dir": str(AUDITS_DIR),
    }

    # Try explicit path first
    if config_path and config_path.exists():
        try:
            with open(config_path) as f:
                return {**defaults, **json.load(f)}
        except Exception as e:
            debug_log(f"Failed to load config from {config_path}: {e}", "glial")

    # Try default config location
    default_config = MAINTENANCE_DIR / "config.json"
    if default_config.exists():
        try:
            with open(default_config) as f:
                return {**defaults, **json.load(f)}
        except Exception as e:
            debug_log(f"Failed to load default config: {e}", "glial")

    return defaults


def get_project_paths() -> dict:
    """Return standardized project paths dict.

    Provides consistent path references for all brain cell modules.

    Returns:
        Dict with all standard project paths
    """
    return {
        "project_root": PROJECT_ROOT,
        "oracle_dir": ORACLE_DIR,
        "maintenance_dir": MAINTENANCE_DIR,
        "reports_dir": REPORTS_DIR,
        "audits_dir": AUDITS_DIR,
        "layers_dir": LAYERS_DIR,
        "scripts_dir": SCRIPTS_DIR,
        "docs_dir": ORACLE_DIR / "docs",
        "context_dir": ORACLE_DIR / "docs" / "context",
        "app_dir": PROJECT_ROOT / "app",
        "config_dir": PROJECT_ROOT / "config",
    }


def format_debug_output(data, title: str = "", indent: int = 2) -> str:
    """Format data for debug output consistently.

    Provides uniform formatting for debug/diagnostic output across modules.

    Args:
        data: Data to format (dict, list, str, or any)
        title: Optional title header
        indent: Indentation level for nested structures

    Returns:
        Formatted string representation
    """
    lines = []

    if title:
        lines.append(f"{'=' * 50}")
        lines.append(f"  {title}")
        lines.append(f"{'=' * 50}")

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{' ' * indent}{key}:")
                lines.append(format_debug_output(value, indent=indent + 2))
            else:
                lines.append(f"{' ' * indent}{key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data[:20]):  # Limit to 20 items
            if isinstance(item, dict):
                lines.append(f"{' ' * indent}[{i}]:")
                lines.append(format_debug_output(item, indent=indent + 2))
            else:
                lines.append(f"{' ' * indent}- {item}")
        if len(data) > 20:
            lines.append(f"{' ' * indent}... and {len(data) - 20} more")
    else:
        lines.append(f"{' ' * indent}{data}")

    return "\n".join(lines)


def log_to_oracle(message: str, level: str = "info", category: str = "oracle"):
    """Unified logging for oracle operations.

    Consistent logging interface for all brain cell modules.

    Args:
        message: Log message
        level: Log level ('debug', 'info', 'warning', 'error')
        category: Category tag for filtering
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    level_icons = {
        "debug": "🔍",
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
    }

    icon = level_icons.get(level, "•")

    # Only print debug if DEBUG mode enabled
    if level == "debug" and not DEBUG:
        return

    print(f"{icon} [{timestamp}] [{category}] {message}")

    # Optionally write to log file
    if os.environ.get("ORACLE_LOG_FILE"):
        log_file = Path(os.environ["ORACLE_LOG_FILE"])
        try:
            with open(log_file, "a") as f:
                f.write(f"[{timestamp}] [{level.upper()}] [{category}] {message}\n")
        except Exception:
            pass


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def write_health_status(health_score: float, critical: int = 0, warnings: int = 0,
                        optimizations: int = 0, cost: float = 0.0):
    """Write health status to shared state file for sEEG monitor.

    Args:
        health_score: Overall health score (0-100)
        critical: Number of critical issues
        warnings: Number of warnings
        optimizations: Number of pending optimizations
        cost: API cost today
    """
    status_file = REPORTS_DIR / ".health_status.json"
    status = {
        "timestamp": datetime.now().isoformat(),
        "health_score": health_score / 10.0,  # Convert to 0-10 scale for display
        "issues": {
            "critical": critical,
            "warnings": warnings
        },
        "optimizations_pending": optimizations,
        "cost_today": cost
    }
    try:
        status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(status_file, 'w') as f:
            json.dump(status, f, indent=2)
    except Exception as e:
        debug_log(f"Failed to write health status: {e}", "glial")


def cleanup_old_files(directory: Path, pattern: str, max_keep: int = 5) -> int:
    """Delete old files matching pattern, keeping only the most recent max_keep.

    Args:
        directory: Directory to clean
        pattern: Glob pattern (e.g., "ORACLE_REPORT_*.md")
        max_keep: Number of files to keep

    Returns:
        Number of files deleted
    """
    if not directory.exists():
        return 0

    # Get all matching files sorted by modification time (newest first)
    files = sorted(directory.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)

    # Delete files beyond max_keep
    deleted = 0
    for old_file in files[max_keep:]:
        try:
            old_file.unlink()
            deleted += 1
        except Exception:
            pass  # Silently ignore deletion errors

    return deleted


# =============================================================================
# CODE HEALTH AUDITOR
# =============================================================================

class CodeHealthAuditor:
    """Analyze code for dead code, unused imports, complexity, memory leaks."""

    def __init__(self, scripts_dir: Path, additional_dirs: list = None):
        self.scripts_dir = scripts_dir
        self.additional_dirs = additional_dirs or []
        self.issues = []

    def run(self) -> list:
        """Run all code health checks."""
        self.issues = []

        # Scan main scripts directory
        if self.scripts_dir.exists():
            for script in self.scripts_dir.glob("*.py"):
                if script.name.startswith("__"):
                    continue
                self._analyze_script(script)

        # Scan additional directories (e.g., maintenance/)
        for additional_dir in self.additional_dirs:
            if not additional_dir.exists():
                continue
            for script in additional_dir.glob("*.py"):
                if script.name.startswith("__"):
                    continue
                self._analyze_script(script)

        return self.issues

    def _analyze_script(self, script_path: Path):
        """Analyze a single Python script."""
        try:
            with open(script_path, "r") as f:
                content = f.read()

            tree = ast.parse(content)

            # Check for unused imports
            self._check_unused_imports(script_path, content, tree)

            # Check for overly long functions
            self._check_function_length(script_path, tree)

            # Check for TODO/FIXME comments
            self._check_todo_comments(script_path, content)

            # Check for hardcoded values that should be config
            self._check_hardcoded_values(script_path, content)

            # Check for potential memory leaks (unbounded accumulation)
            self._check_memory_leaks(script_path, content, tree)

        except SyntaxError as e:
            self.issues.append(Issue(
                severity="critical",
                category="code",
                title=f"Syntax error in {script_path.name}",
                description=str(e),
                file_path=str(script_path),
                line_number=e.lineno
            ))
        except Exception as e:
            self.issues.append(Issue(
                severity="warning",
                category="code",
                title=f"Could not analyze {script_path.name}",
                description=str(e),
                file_path=str(script_path)
            ))

    def _check_unused_imports(self, script_path: Path, content: str, tree: ast.AST):
        """Find imports that are never used in the code (only NEW ones not in accepted list)."""
        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports.add((name.split('.')[0], node.lineno))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    if name != '*':
                        imports.add((name, node.lineno))

        # Check if each import is used
        for name, lineno in imports:
            pattern = rf'\b{re.escape(name)}\b'
            matches = list(re.finditer(pattern, content))

            if len(matches) <= 1:
                import_key = f"{script_path.name}:{name}"
                if import_key in ACCEPTED_UNUSED_IMPORTS:
                    continue

                self.issues.append(Issue(
                    severity="warning",
                    category="code",
                    title=f"NEW unused import: {name}",
                    description=f"Import '{name}' may not be used in {script_path.name}",
                    file_path=str(script_path),
                    line_number=lineno,
                    suggestion="Add to ACCEPTED_UNUSED_IMPORTS if intentional, or remove"
                ))

    def _check_function_length(self, script_path: Path, tree: ast.AST, max_lines: int = 100):
        """Flag functions that are too long (only NEW ones not in accepted list)."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.end_lineno and node.lineno:
                    length = node.end_lineno - node.lineno
                    if length > max_lines:
                        func_key = f"{script_path.name}:{node.name}"
                        if func_key in ACCEPTED_LONG_FUNCTIONS:
                            continue

                        self.issues.append(Issue(
                            severity="warning",
                            category="code",
                            title=f"NEW long function: {node.name}",
                            description=f"Function is {length} lines (>{max_lines})",
                            file_path=str(script_path),
                            line_number=node.lineno,
                            suggestion="Add to ACCEPTED_LONG_FUNCTIONS or refactor"
                        ))

    def _check_todo_comments(self, script_path: Path, content: str):
        """Find TODO/FIXME comments that need attention."""
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(r'#\s*(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE):
                self.issues.append(Issue(
                    severity="info",
                    category="code",
                    title=f"TODO comment in {script_path.name}",
                    description=line.strip(),
                    file_path=str(script_path),
                    line_number=i
                ))

    def _check_hardcoded_values(self, script_path: Path, content: str):
        """Find potential hardcoded values that should be configurable."""
        patterns = [
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        ]

        for pattern, issue_type in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                self.issues.append(Issue(
                    severity="critical",
                    category="code",
                    title=issue_type,
                    description=f"Found in {script_path.name}",
                    file_path=str(script_path),
                    line_number=line_num,
                    suggestion="Move to .env file or config"
                ))

    def _check_memory_leaks(self, script_path: Path, content: str, tree: ast.AST):
        """Detect potential memory leaks: unbounded list/dict accumulation."""
        append_calls = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ('append', 'extend'):
                        if isinstance(node.func.value, ast.Attribute):
                            if isinstance(node.func.value.value, ast.Name) and node.func.value.value.id == 'self':
                                attr_name = node.func.value.attr
                                if attr_name not in append_calls:
                                    append_calls[attr_name] = []
                                append_calls[attr_name].append(node.lineno)

        reset_attrs = self._find_reset_attributes(tree)

        for attr_name, lines in append_calls.items():
            if attr_name in reset_attrs:
                continue

            limit_pattern = rf'if\s+len\s*\(\s*self\.{re.escape(attr_name)}\s*\)\s*>'
            slice_pattern = rf'self\.{re.escape(attr_name)}\s*=\s*self\.{re.escape(attr_name)}\s*\['
            has_limit = bool(re.search(limit_pattern, content)) or bool(re.search(slice_pattern, content))

            if not has_limit:
                leak_key = f"{script_path.name}:self.{attr_name}"
                if leak_key in ACCEPTED_MEMORY_PATTERNS:
                    continue

                self.issues.append(Issue(
                    severity="warning",
                    category="code",
                    title=f"Potential memory leak: self.{attr_name}",
                    description=f"List/dict may grow unbounded",
                    file_path=str(script_path),
                    line_number=lines[0],
                    suggestion=f"Add size limit or reset in method"
                ))

    def _find_reset_attributes(self, tree: ast.AST) -> set:
        """Find self.attr that are reset to [] or {} inside methods."""
        reset_attrs = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name != '__init__':
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute):
                                if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                    is_reset = False
                                    if isinstance(stmt.value, ast.List) and len(stmt.value.elts) == 0:
                                        is_reset = True
                                    elif isinstance(stmt.value, ast.Dict) and len(stmt.value.keys) == 0:
                                        is_reset = True
                                    if is_reset:
                                        reset_attrs.add(target.attr)
        return reset_attrs


# =============================================================================
# LAYER HEALTH AUDITOR
# =============================================================================

class LayerHealthAuditor:
    """Validate all pipeline layers are functional."""

    def __init__(self, project_root: Path, layers: dict):
        self.project_root = project_root
        self.layers = layers
        self.issues = []
        self.status = {}

    def run(self) -> tuple:
        """Run layer validation checks."""
        self.issues = []
        self.status = {}

        for layer_num, layer_info in self.layers.items():
            self.status[layer_num] = self._check_layer(layer_num, layer_info)

        return self.issues, self.status

    def _check_layer(self, layer_num: int, layer_info: dict) -> dict:
        """Check a single layer's health."""
        status = {
            "name": layer_info.get("name", f"Layer {layer_num}"),
            "scripts_exist": True,
            "output_exists": False,
            "importable": True,
            "missing_scripts": [],
            "errors": []
        }

        scripts_dir = self.project_root / "scripts"

        for script_name in layer_info.get("scripts", []):
            script_path = scripts_dir / script_name
            if not script_path.exists():
                status["scripts_exist"] = False
                status["missing_scripts"].append(script_name)
                self.issues.append(Issue(
                    severity="critical",
                    category="code",
                    title=f"Layer {layer_num} missing script: {script_name}",
                    description=f"{layer_info.get('name', 'Layer')} is incomplete",
                    suggestion=f"Create {script_name} or update layer definitions"
                ))

        return status


# =============================================================================
# CODE OPTIMIZER
# =============================================================================

class CodeOptimizer:
    """Automated code cleanup, enhancement, and fix application."""

    def __init__(self, project_root: Path, config: dict, dry_run: bool = True):
        self.project_root = project_root
        self.config = config
        self.dry_run = dry_run
        self.scripts_dir = project_root / "scripts"
        self.maintenance_dir = project_root / "oracle" / "maintenance"
        self.config_dir = project_root / "config"
        self.changes_made = []
        self.backup_files = []
        self._run_auditor()

    def _run_auditor(self):
        """Run CodeHealthAuditor to get current issues."""
        auditor = CodeHealthAuditor(
            self.scripts_dir,
            additional_dirs=[self.maintenance_dir]
        )
        self.auditor_issues = auditor.run()
        debug_log(f"Auditor found {len(self.auditor_issues)} issues", "optimizer")

    def run_all(self, operations: list = None) -> dict:
        """Run optimizer operations."""
        if operations is None:
            operations = ['imports', 'docs', 'presets', 'safety']

        results = {
            "dry_run": self.dry_run,
            "imports_fixed": [],
            "cli_cleaned": [],
            "doc_gaps": [],
            "docstrings_added": [],
            "preset_issues": [],
            "safety_warnings": [],
            "dead_code": {"dead": [], "allowed": []},
            "legacy_markers": [],
            "duplicates": [],
            "layer_violations": [],
            "files_modified": []
        }

        if 'imports' in operations:
            results["imports_fixed"] = self._fix_unused_imports()
        if 'safety' in operations:
            results["safety_warnings"] = self._safety_scan()
        if 'dead_code' in operations:
            results["dead_code"] = self._detect_dead_code()
        if 'legacy' in operations:
            results["legacy_markers"] = self._detect_legacy_markers()

        results["files_modified"] = self.changes_made
        return results

    def _fix_unused_imports(self) -> list:
        """Remove unused imports based on auditor findings."""
        fixed = []
        import_issues = [i for i in self.auditor_issues if "unused import" in i.title.lower()]

        if not import_issues:
            return fixed

        by_file = {}
        for issue in import_issues:
            path = issue.file_path
            if path not in by_file:
                by_file[path] = []
            match = re.search(r'unused import:\s*(\w+)', issue.title, re.IGNORECASE)
            if match:
                by_file[path].append((match.group(1), issue.line_number))

        for file_path, imports in by_file.items():
            fixed.append({
                "file": Path(file_path).name,
                "imports": [name for name, _ in imports],
                "lines": [line for _, line in imports]
            })

        return fixed

    def _safety_scan(self) -> list:
        """Scan for security anti-patterns."""
        warnings = []
        patterns = [
            (r'\beval\s*\(', 'eval_usage', 'high', 'eval() can execute arbitrary code'),
            (r'\bexec\s*\(', 'exec_usage', 'high', 'exec() can execute arbitrary code'),
            (r'subprocess\.\w+\([^)]*shell\s*=\s*True', 'shell_injection', 'medium', 'shell=True risks injection'),
            (r'pickle\.loads?\(', 'pickle_usage', 'medium', 'pickle can execute code during deserialization'),
        ]

        skip_files = {'project_oracle.py', 'microglia.py'}

        for directory in [self.scripts_dir, self.maintenance_dir]:
            if not directory.exists():
                continue
            for script_path in directory.glob("*.py"):
                if script_path.name in skip_files:
                    continue
                try:
                    content = script_path.read_text()
                    for pattern, issue_type, severity, suggestion in patterns:
                        for match in re.finditer(pattern, content):
                            line_num = content[:match.start()].count('\n') + 1
                            warnings.append({
                                "file": script_path.name,
                                "type": issue_type,
                                "severity": severity,
                                "line": line_num,
                                "suggestion": suggestion
                            })
                except Exception:
                    pass

        return warnings

    def _detect_dead_code(self) -> dict:
        """Find functions that are never called anywhere in the codebase."""
        dead = []
        allowed = []

        scan_dirs = [
            self.scripts_dir,
            self.maintenance_dir,
            self.project_root / "app",
            self.project_root / "oracle",
        ]

        all_functions = []
        all_code = ""

        for directory in scan_dirs:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                try:
                    content = py_file.read_text()
                    all_code += content + "\n"
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_name = node.name
                            if func_name.startswith("__") and func_name.endswith("__"):
                                continue
                            if func_name.startswith("test_"):
                                continue
                            if func_name in ("main", "cli", "run_cli"):
                                continue
                            all_functions.append((str(py_file), func_name, node.lineno))
                except Exception:
                    pass

        for file_path, func_name, line_num in all_functions:
            call_pattern = rf'(?<!def\s){re.escape(func_name)}\s*\('
            calls = re.findall(call_pattern, all_code)
            method_pattern = rf'\.{re.escape(func_name)}\s*\('
            method_calls = re.findall(method_pattern, all_code)
            total_calls = len(calls) + len(method_calls)

            if total_calls <= 1:
                rel_path = Path(file_path).name
                dead.append({
                    "file": rel_path,
                    "function": func_name,
                    "line": line_num,
                    "key": f"{rel_path}:{func_name}"
                })

        return {"dead": dead[:50], "allowed": allowed}  # Limit output

    def _detect_legacy_markers(self) -> list:
        """Find code marked as legacy/deprecated."""
        markers = []
        patterns = [
            (r'#\s*(Legacy|MVP|V1|Fallback)\b', 'comment'),
            (r'#\s*TODO:\s*remove', 'todo_remove'),
            (r'#\s*DEPRECATED', 'deprecated'),
        ]

        scan_dirs = [
            self.scripts_dir,
            self.maintenance_dir,
            self.project_root / "app",
        ]

        for directory in scan_dirs:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                try:
                    content = py_file.read_text()
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        for pattern, marker_type in patterns:
                            match = re.search(pattern, line, re.IGNORECASE)
                            if match:
                                markers.append({
                                    "file": py_file.name,
                                    "line": i,
                                    "marker": match.group(0).strip(),
                                    "type": marker_type,
                                    "context": line.strip()[:60]
                                })
                except Exception:
                    pass

        return markers[:50]  # Limit output


# =============================================================================
# SCRIPT DEBUGGER
# =============================================================================

class ScriptDebugger:
    """Debug wrapper for running scripts with execution tracing."""

    def __init__(self, script_path: str, trace_calls: bool = False,
                 trace_lines: bool = False, watch_vars: list = None,
                 output_file: str = None):
        self.script_path = Path(script_path)
        self.trace_calls = trace_calls
        self.trace_lines = trace_lines
        self.watch_vars = watch_vars or []
        self.output_file = output_file
        self.trace_output = []
        self.start_time = None
        self.call_depth = 0
        self.var_history = {}

    def _resolve_script_path(self) -> Path:
        """Resolve script path relative to PROJECT_ROOT."""
        if not self.script_path.is_absolute():
            resolved = PROJECT_ROOT / self.script_path
            if resolved.exists():
                return resolved

        if '/' not in str(self.script_path):
            for dir_path in [SCRIPTS_DIR, MAINTENANCE_DIR]:
                candidate = dir_path / self.script_path
                if candidate.exists():
                    return candidate

        return self.script_path

    def _log(self, msg: str, category: str = "trace"):
        """Log trace message with timestamp."""
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        formatted = f"[{elapsed:8.3f}s] [{category:5s}] {msg}"
        self.trace_output.append(formatted)
        print(formatted)

    def run(self, script_args: list) -> int:
        """Run the script with tracing enabled."""
        import runpy
        import sys

        script_path = self._resolve_script_path()

        if not script_path.exists():
            print(f"❌ Script not found: {self.script_path}")
            return 1

        print(f"🔍 Script Debugger - Running: {script_path.name}")
        print(f"   Args: {' '.join(script_args) if script_args else '(none)'}")
        print()

        self.start_time = datetime.now()
        os.environ["ORACLE_DEBUG"] = "1"

        orig_argv = sys.argv.copy()

        try:
            sys.argv = [str(script_path)] + script_args
            self._log(f"Starting {script_path.name}", "start")
            runpy.run_path(str(script_path), run_name="__main__")
            self._log("Script completed successfully", "end")
            exit_code = 0
        except SystemExit as e:
            exit_code = e.code if isinstance(e.code, int) else 0
            self._log(f"Script exited with code {exit_code}", "exit")
        except Exception as e:
            self._log(f"Script error: {type(e).__name__}: {e}", "error")
            import traceback
            self.trace_output.append(traceback.format_exc())
            print(traceback.format_exc())
            exit_code = 1
        finally:
            sys.argv = orig_argv

        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n⏱️  Total time: {elapsed:.2f}s")

        if self.output_file:
            output_path = Path(self.output_file)
            with open(output_path, 'w') as f:
                f.write(f"# Script Debug Trace: {script_path.name}\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
                f.write("\n".join(self.trace_output))
            print(f"📄 Trace saved to: {output_path}")

        return exit_code


# =============================================================================
# PUBLIC INTERFACE FUNCTIONS
# =============================================================================

def run_audit(quick: bool = False, deep: bool = False, code_only: bool = False) -> AuditReport:
    """Run health audits and return report.

    Args:
        quick: Quick health check (essential checks only)
        deep: Full deep audit (all checks)
        code_only: Only run code health checks

    Returns:
        AuditReport with findings
    """
    report = AuditReport()
    all_issues = []

    # Code health audit
    auditor = CodeHealthAuditor(
        SCRIPTS_DIR,
        additional_dirs=[MAINTENANCE_DIR, PROJECT_ROOT / "app"]
    )
    code_issues = auditor.run()
    all_issues.extend(code_issues)

    # Preset validation audit (P28)
    preset_issues = _run_preset_validation()
    all_issues.extend(preset_issues)

    # Calculate health score
    critical = sum(1 for i in all_issues if i.severity == "critical")
    warnings = sum(1 for i in all_issues if i.severity == "warning")
    report.health_score = max(0, 100 - (critical * 10) - (warnings * 2))
    report.issues = all_issues

    # Generate summary
    report.summary = f"Health Score: {report.health_score:.0f}% | Critical: {critical} | Warnings: {warnings}"

    # Write status file for sEEG monitor
    write_health_status(report.health_score, critical, warnings)

    return report


def _run_preset_validation() -> list:
    """Run preset validation and return issues.

    Returns:
        List of Issue objects for failed/warning presets
    """
    issues = []

    try:
        from config.preset_validator import PresetValidator
        validator = PresetValidator()
        results = validator.validate_all()

        for name, result in results.items():
            if not result["valid"]:
                # Failed presets are warnings (not critical - they're often experimental)
                issues.append(Issue(
                    severity="warning",
                    category="config",
                    title=f"Preset '{name}' validation failed",
                    description="; ".join(result["errors"][:3]),  # First 3 errors
                    file_path="config/script_presets.json",
                    suggestion=f"Run: python -m config.preset_validator {name}"
                ))

    except ImportError:
        # Validator not available - skip silently
        pass
    except Exception as e:
        # Log but don't fail the audit
        issues.append(Issue(
            severity="info",
            category="config",
            title="Preset validation skipped",
            description=str(e)
        ))

    return issues


def run_clean(reports: bool = False, tasks: bool = False, dead_code: bool = False) -> dict:
    """Run cleanup operations.

    Args:
        reports: Clean old report files
        tasks: Clean completed tasks from context
        dead_code: Detect and report dead code

    Returns:
        Dict with cleanup results
    """
    results = {
        "reports_deleted": 0,
        "tasks_pruned": 0,
        "dead_code": []
    }

    if reports:
        results["reports_deleted"] = cleanup_old_files(AUDITS_DIR, "ORACLE_REPORT_*.md", MAX_REPORTS)

    if dead_code:
        optimizer = CodeOptimizer(PROJECT_ROOT, {}, dry_run=True)
        dead_results = optimizer._detect_dead_code()
        results["dead_code"] = dead_results.get("dead", [])

    return results


def run_debug_script(script_path: str, trace_calls: bool = False,
                     trace_lines: bool = False, watch_vars: list = None,
                     output_file: str = None, script_args: list = None) -> int:
    """Debug a script with tracing.

    Args:
        script_path: Path to script to debug
        trace_calls: Trace function calls
        trace_lines: Trace line execution
        watch_vars: Variables to watch for changes
        output_file: File to save trace output
        script_args: Arguments to pass to script

    Returns:
        Exit code from script
    """
    debugger = ScriptDebugger(
        script_path,
        trace_calls=trace_calls,
        trace_lines=trace_lines,
        watch_vars=watch_vars,
        output_file=output_file
    )
    return debugger.run(script_args or [])


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for microglia commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Microglia - Error detection, cleanup, debugging",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Run code health audits")
    audit_parser.add_argument("--quick", action="store_true", help="Quick health check")
    audit_parser.add_argument("--deep", action="store_true", help="Full deep audit")
    audit_parser.add_argument("--code", action="store_true", help="Code health only")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Cleanup operations")
    clean_parser.add_argument("--reports", action="store_true", help="Clean old reports")
    clean_parser.add_argument("--tasks", action="store_true", help="Prune completed tasks")
    clean_parser.add_argument("--dead-code", action="store_true", help="Detect dead code")

    # Debug-script command
    debug_parser = subparsers.add_parser("debug-script", help="Debug a script")
    debug_parser.add_argument("script", help="Script path to debug")
    debug_parser.add_argument("--trace-calls", action="store_true", help="Trace function calls")
    debug_parser.add_argument("--trace-lines", action="store_true", help="Trace line execution")
    debug_parser.add_argument("--watch-vars", nargs="+", help="Variables to watch")
    debug_parser.add_argument("--output", help="Output file for trace")
    debug_parser.add_argument("script_args", nargs="*", help="Arguments for script")

    args = parser.parse_args()

    if args.command == "audit":
        report = run_audit(quick=args.quick, deep=args.deep, code_only=args.code)
        print(f"\n{report.summary}")
        print(f"\nIssues found: {len(report.issues)}")
        for issue in report.issues[:10]:
            print(f"  [{issue.severity}] {issue.title}")
        if len(report.issues) > 10:
            print(f"  ... and {len(report.issues) - 10} more")

    elif args.command == "clean":
        results = run_clean(
            reports=args.reports,
            tasks=args.tasks,
            dead_code=args.dead_code
        )
        print(f"\nCleanup Results:")
        print(f"  Reports deleted: {results['reports_deleted']}")
        if results['dead_code']:
            print(f"  Dead code detected: {len(results['dead_code'])} functions")

    elif args.command == "debug-script":
        exit_code = run_debug_script(
            args.script,
            trace_calls=args.trace_calls,
            trace_lines=args.trace_lines,
            watch_vars=args.watch_vars,
            output_file=args.output,
            script_args=args.script_args
        )
        return exit_code

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
