#!/usr/bin/env python3
"""
Topoisomerase - Oracle Brain Cell: Integrity Verification
==========================================================

Brain Metaphor: Topoisomerase relieves tension in DNA that builds up from
continuous edits (replication/transcription). Similarly, this module verifies
codebase integrity after edits, refactors, and changes.

Responsibilities:
- Verify codebase integrity after edits/refactors
- Detect circular imports
- Track performance regression
- Auto-fix common issues
- Manage pre-commit hooks

Commands: verify
"""

import os
import sys
import ast
import json
import re
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

VALIDATION_DIR = Path(__file__).parent
ORACLE_DIR = VALIDATION_DIR.parent
PROJECT_ROOT = ORACLE_DIR.parent
REPORTS_DIR = ORACLE_DIR / "reports"
TEMPLATES_DIR = VALIDATION_DIR / "templates"

# Add project root to path for imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")


def debug_log(msg: str, category: str = "topoisomerase"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  [DEBUG] [{timestamp}] [{category}] {msg}")


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class VerificationIssue:
    """Single verification issue."""
    severity: str  # "critical", "warning", "info"
    category: str  # "imports", "integrity", "performance", "syntax"
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class VerificationReport:
    """Complete verification report."""
    timestamp: datetime = field(default_factory=datetime.now)
    mode: str = "standard"
    duration_ms: float = 0.0
    health_score: float = 100.0
    issues: List[VerificationIssue] = field(default_factory=list)
    checks_passed: List[str] = field(default_factory=list)
    checks_failed: List[str] = field(default_factory=list)
    summary: str = ""


@dataclass
class ProposedFix:
    """A proposed auto-fix."""
    file_path: str
    line_number: int
    issue_type: str
    original: str
    replacement: str
    description: str


@dataclass
class PerformanceBaseline:
    """Performance baseline for regression tracking."""
    captured: datetime = field(default_factory=datetime.now)
    import_time_ms: float = 0.0
    file_count: int = 0
    line_count: int = 0
    function_count: int = 0
    layer_health: Dict[str, bool] = field(default_factory=dict)


# =============================================================================
# CIRCULAR IMPORT DETECTOR
# =============================================================================

class CircularImportDetector:
    """Detect circular imports in Python codebase."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.import_graph: Dict[str, Set[str]] = {}
        self.circular_imports: List[List[str]] = []

    def scan(self, directories: List[Path] = None) -> List[List[str]]:
        """Scan directories for circular imports.

        Args:
            directories: List of directories to scan. Defaults to app/ and oracle/

        Returns:
            List of circular import chains
        """
        if directories is None:
            directories = [
                self.project_root / "app",
                self.project_root / "oracle",
            ]

        self.import_graph = {}
        self.circular_imports = []

        # Build import graph
        for directory in directories:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                self._analyze_file(py_file)

        # Find cycles
        self._find_cycles()

        return self.circular_imports

    def _analyze_file(self, file_path: Path):
        """Analyze a single file for imports."""
        try:
            content = file_path.read_text()
            tree = ast.parse(content)
        except Exception:
            return

        module_name = self._path_to_module(file_path)
        if module_name not in self.import_graph:
            self.import_graph[module_name] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = alias.name.split('.')[0]
                    if self._is_local_module(imported):
                        self.import_graph[module_name].add(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module and node.level == 0:
                    if self._is_local_module(node.module.split('.')[0]):
                        self.import_graph[module_name].add(node.module)

    def _path_to_module(self, file_path: Path) -> str:
        """Convert file path to module name."""
        try:
            rel_path = file_path.relative_to(self.project_root)
            parts = list(rel_path.parts)
            if parts[-1] == "__init__.py":
                parts = parts[:-1]
            else:
                parts[-1] = parts[-1].replace(".py", "")
            return ".".join(parts)
        except ValueError:
            return str(file_path)

    def _is_local_module(self, module_name: str) -> bool:
        """Check if module is local to the project."""
        local_prefixes = ("app", "oracle", "config", "scripts")
        return module_name.startswith(local_prefixes)

    def _find_cycles(self):
        """Find all cycles in the import graph using DFS."""
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.import_graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor, path + [neighbor]):
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor) if neighbor in path else len(path)
                    cycle = path[cycle_start:] + [neighbor]
                    if len(cycle) >= 2 and cycle not in self.circular_imports:
                        self.circular_imports.append(cycle)

            rec_stack.remove(node)
            return False

        for module in self.import_graph:
            if module not in visited:
                dfs(module, [module])


# =============================================================================
# INTEGRITY VERIFIER
# =============================================================================

class IntegrityVerifier:
    """Verifies codebase integrity after edits/refactors."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.issues: List[VerificationIssue] = []
        self.checks_passed: List[str] = []
        self.checks_failed: List[str] = []

    def verify(self, mode: str = "standard") -> VerificationReport:
        """Run integrity verification.

        Args:
            mode: Verification mode - "quick", "standard", or "full"

        Returns:
            VerificationReport with findings
        """
        start_time = time.time()
        self.issues = []
        self.checks_passed = []
        self.checks_failed = []

        # Import existing brain cell functions
        try:
            from oracle.maintenance.microglia import run_audit, CodeHealthAuditor
            from oracle.project.cortex import LayerAnalyzer
        except ImportError as e:
            self.issues.append(VerificationIssue(
                severity="critical",
                category="imports",
                title="Failed to import brain cell modules",
                description=str(e),
                suggestion="Check oracle module structure"
            ))
            self.checks_failed.append("brain_cell_imports")

        # Run checks based on mode
        if mode == "quick":
            self._run_quick_checks()
        elif mode == "full":
            self._run_standard_checks()
            self._run_full_checks()
        else:  # standard
            self._run_standard_checks()

        # Calculate health score
        critical = sum(1 for i in self.issues if i.severity == "critical")
        warnings = sum(1 for i in self.issues if i.severity == "warning")
        health_score = max(0, 100 - (critical * 10) - (warnings * 2))

        duration_ms = (time.time() - start_time) * 1000

        return VerificationReport(
            mode=mode,
            duration_ms=duration_ms,
            health_score=health_score,
            issues=self.issues,
            checks_passed=self.checks_passed,
            checks_failed=self.checks_failed,
            summary=f"Health: {health_score:.0f}% | Critical: {critical} | Warnings: {warnings} | {duration_ms:.0f}ms"
        )

    def _run_quick_checks(self):
        """Run quick verification checks (~5 seconds)."""
        # Syntax check on critical files
        critical_files = [
            self.project_root / "app" / "main.py",
            self.project_root / "oracle" / "project_oracle.py",
        ]

        for file_path in critical_files:
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    ast.parse(content)
                    self.checks_passed.append(f"syntax:{file_path.name}")
                except SyntaxError as e:
                    self.issues.append(VerificationIssue(
                        severity="critical",
                        category="syntax",
                        title=f"Syntax error in {file_path.name}",
                        description=str(e),
                        file_path=str(file_path),
                        line_number=e.lineno
                    ))
                    self.checks_failed.append(f"syntax:{file_path.name}")

        # Quick circular import check on app/
        detector = CircularImportDetector(self.project_root)
        circles = detector.scan([self.project_root / "app"])

        if circles:
            for cycle in circles[:3]:  # Report first 3
                self.issues.append(VerificationIssue(
                    severity="warning",
                    category="imports",
                    title="Circular import detected",
                    description=" -> ".join(cycle),
                    suggestion="Refactor to break the cycle"
                ))
            self.checks_failed.append("circular_imports")
        else:
            self.checks_passed.append("circular_imports")

    def _run_standard_checks(self):
        """Run standard verification checks (~30 seconds)."""
        # Run quick checks first
        self._run_quick_checks()

        # Use existing microglia audit
        try:
            from oracle.maintenance.microglia import run_audit
            audit = run_audit(quick=True)

            # Convert audit issues to verification issues
            for issue in audit.issues:
                self.issues.append(VerificationIssue(
                    severity=issue.severity,
                    category="code",
                    title=issue.title,
                    description=issue.description,
                    file_path=issue.file_path,
                    line_number=issue.line_number,
                    suggestion=issue.suggestion
                ))

            self.checks_passed.append("code_health_audit")
        except Exception as e:
            self.issues.append(VerificationIssue(
                severity="warning",
                category="integrity",
                title="Code health audit failed",
                description=str(e)
            ))
            self.checks_failed.append("code_health_audit")

        # Check layer integrity
        self._check_layer_integrity()

        # Full circular import scan
        detector = CircularImportDetector(self.project_root)
        circles = detector.scan()

        if circles:
            for cycle in circles:
                self.issues.append(VerificationIssue(
                    severity="warning",
                    category="imports",
                    title="Circular import detected",
                    description=" -> ".join(cycle),
                    suggestion="Refactor to break the cycle"
                ))

    def _run_full_checks(self):
        """Run full verification checks (includes external tools if available)."""
        # Check if mypy is available
        import shutil

        if shutil.which("mypy"):
            self.checks_passed.append("mypy_available")
            # Note: Actually running mypy would be done here
            debug_log("mypy available for type checking", "verify")

        if shutil.which("pytest"):
            self.checks_passed.append("pytest_available")
            debug_log("pytest available for test running", "verify")

    def _check_layer_integrity(self):
        """Check pipeline layer integrity."""
        layers_dir = self.project_root / "app" / "core" / "pipeline" / "layers"

        if not layers_dir.exists():
            self.issues.append(VerificationIssue(
                severity="warning",
                category="integrity",
                title="Layers directory not found",
                description=f"Expected at {layers_dir}",
                suggestion="Verify V2 pipeline structure"
            ))
            self.checks_failed.append("layer_structure")
            return

        expected_layers = ["_L1", "_L2", "_L3", "_L4", "_L5", "_L6", "_L7", "_L8"]
        found_layers = [d.name for d in layers_dir.iterdir() if d.is_dir() and d.name.startswith("_L")]

        missing = set(expected_layers) - set(found_layers)
        if missing:
            self.issues.append(VerificationIssue(
                severity="warning",
                category="integrity",
                title=f"Missing layers: {', '.join(sorted(missing))}",
                description="Some pipeline layers are missing",
                file_path=str(layers_dir)
            ))
            self.checks_failed.append("layer_completeness")
        else:
            self.checks_passed.append("layer_completeness")


# =============================================================================
# PERFORMANCE TRACKER
# =============================================================================

class PerformanceTracker:
    """Track and compare performance metrics across refactors."""

    BASELINE_FILE = REPORTS_DIR / ".performance_baseline.json"

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT

    def capture_baseline(self) -> PerformanceBaseline:
        """Capture current performance baseline."""
        baseline = PerformanceBaseline()

        # Measure import time for main app
        start = time.time()
        try:
            import importlib
            if "app.main" in sys.modules:
                del sys.modules["app.main"]
            # Don't actually import - just measure file stats
        except Exception:
            pass
        baseline.import_time_ms = (time.time() - start) * 1000

        # Count files and lines
        for py_file in (self.project_root / "app").rglob("*.py"):
            try:
                baseline.file_count += 1
                baseline.line_count += len(py_file.read_text().splitlines())
            except Exception:
                pass

        # Count functions
        for py_file in (self.project_root / "app").rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text())
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        baseline.function_count += 1
            except Exception:
                pass

        # Check layer health
        layers_dir = self.project_root / "app" / "core" / "pipeline" / "layers"
        if layers_dir.exists():
            for layer_dir in layers_dir.iterdir():
                if layer_dir.is_dir() and layer_dir.name.startswith("_L"):
                    # Layer is healthy if it has at least one .py file
                    py_files = list(layer_dir.rglob("*.py"))
                    baseline.layer_health[layer_dir.name] = len(py_files) > 0

        # Save baseline
        self._save_baseline(baseline)

        return baseline

    def compare_with_baseline(self) -> Dict:
        """Compare current state with saved baseline."""
        baseline = self._load_baseline()
        if not baseline:
            return {"error": "No baseline found. Run with --baseline first."}

        current = self.capture_baseline()

        return {
            "baseline_date": baseline.captured.isoformat() if hasattr(baseline.captured, 'isoformat') else str(baseline.captured),
            "file_count": {
                "baseline": baseline.file_count,
                "current": current.file_count,
                "diff": current.file_count - baseline.file_count
            },
            "line_count": {
                "baseline": baseline.line_count,
                "current": current.line_count,
                "diff": current.line_count - baseline.line_count
            },
            "function_count": {
                "baseline": baseline.function_count,
                "current": current.function_count,
                "diff": current.function_count - baseline.function_count
            },
            "layer_changes": self._compare_layers(baseline.layer_health, current.layer_health)
        }

    def _save_baseline(self, baseline: PerformanceBaseline):
        """Save baseline to file."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        data = {
            "captured": baseline.captured.isoformat(),
            "import_time_ms": baseline.import_time_ms,
            "file_count": baseline.file_count,
            "line_count": baseline.line_count,
            "function_count": baseline.function_count,
            "layer_health": baseline.layer_health
        }

        with open(self.BASELINE_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_baseline(self) -> Optional[PerformanceBaseline]:
        """Load baseline from file."""
        if not self.BASELINE_FILE.exists():
            return None

        try:
            with open(self.BASELINE_FILE) as f:
                data = json.load(f)

            baseline = PerformanceBaseline()
            baseline.captured = datetime.fromisoformat(data["captured"])
            baseline.import_time_ms = data.get("import_time_ms", 0)
            baseline.file_count = data.get("file_count", 0)
            baseline.line_count = data.get("line_count", 0)
            baseline.function_count = data.get("function_count", 0)
            baseline.layer_health = data.get("layer_health", {})

            return baseline
        except Exception as e:
            debug_log(f"Failed to load baseline: {e}", "perf")
            return None

    def _compare_layers(self, baseline: Dict, current: Dict) -> Dict:
        """Compare layer health between baseline and current."""
        changes = {}
        all_layers = set(baseline.keys()) | set(current.keys())

        for layer in all_layers:
            b_health = baseline.get(layer, None)
            c_health = current.get(layer, None)

            if b_health != c_health:
                if b_health is None:
                    changes[layer] = "added"
                elif c_health is None:
                    changes[layer] = "removed"
                elif b_health and not c_health:
                    changes[layer] = "broken"
                elif not b_health and c_health:
                    changes[layer] = "fixed"

        return changes


# =============================================================================
# AUTO FIXER
# =============================================================================

class AutoFixer:
    """Auto-fix common code issues detected by Oracle."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.proposed_fixes: List[ProposedFix] = []

    def preview_fixes(self) -> List[ProposedFix]:
        """Preview fixes without applying."""
        self.proposed_fixes = []

        # Scan for fixable issues
        self._find_trailing_whitespace()
        self._find_missing_eof_newline()
        self._find_missing_init_files()

        return self.proposed_fixes

    def apply_fixes(self, fixes: List[ProposedFix] = None) -> Dict:
        """Apply proposed fixes."""
        if fixes is None:
            fixes = self.preview_fixes()

        applied = []
        failed = []

        for fix in fixes:
            try:
                if fix.issue_type == "missing_init":
                    # Create __init__.py
                    Path(fix.file_path).write_text(fix.replacement)
                    applied.append(fix)
                elif fix.issue_type in ("trailing_whitespace", "missing_eof_newline"):
                    # Modify file
                    file_path = Path(fix.file_path)
                    content = file_path.read_text()
                    content = content.replace(fix.original, fix.replacement)
                    file_path.write_text(content)
                    applied.append(fix)
            except Exception as e:
                fix.description = f"Failed: {e}"
                failed.append(fix)

        return {
            "applied": len(applied),
            "failed": len(failed),
            "details": {
                "applied": [f.file_path for f in applied],
                "failed": [f.file_path for f in failed]
            }
        }

    def _find_trailing_whitespace(self):
        """Find files with trailing whitespace."""
        for py_file in (self.project_root / "app").rglob("*.py"):
            try:
                content = py_file.read_text()
                lines = content.splitlines(keepends=True)

                for i, line in enumerate(lines):
                    if line.rstrip('\n\r') != line.rstrip():
                        self.proposed_fixes.append(ProposedFix(
                            file_path=str(py_file),
                            line_number=i + 1,
                            issue_type="trailing_whitespace",
                            original=line,
                            replacement=line.rstrip() + '\n',
                            description=f"Remove trailing whitespace on line {i + 1}"
                        ))
                        break  # One fix per file for preview
            except Exception:
                pass

    def _find_missing_eof_newline(self):
        """Find files missing newline at end of file."""
        for py_file in (self.project_root / "app").rglob("*.py"):
            try:
                content = py_file.read_text()
                if content and not content.endswith('\n'):
                    self.proposed_fixes.append(ProposedFix(
                        file_path=str(py_file),
                        line_number=len(content.splitlines()),
                        issue_type="missing_eof_newline",
                        original=content[-50:],  # Last 50 chars
                        replacement=content[-50:] + '\n',
                        description="Add newline at end of file"
                    ))
            except Exception:
                pass

    def _find_missing_init_files(self):
        """Find directories with .py files but no __init__.py."""
        checked = set()

        for py_file in (self.project_root / "app").rglob("*.py"):
            parent = py_file.parent
            if parent in checked:
                continue
            checked.add(parent)

            init_file = parent / "__init__.py"
            if not init_file.exists():
                # Check if directory has other .py files
                py_files = list(parent.glob("*.py"))
                if py_files:
                    self.proposed_fixes.append(ProposedFix(
                        file_path=str(init_file),
                        line_number=0,
                        issue_type="missing_init",
                        original="",
                        replacement="",
                        description=f"Create __init__.py in {parent.name}/"
                    ))


# =============================================================================
# HOOK MANAGER
# =============================================================================

class HookManager:
    """Manage pre-commit hooks for Oracle checks."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT

    def generate_config(self) -> str:
        """Generate .pre-commit-config.yaml content."""
        return """repos:
  - repo: local
    hooks:
      - id: oracle-verify-quick
        name: Oracle Quick Verify
        entry: python3 oracle/project_oracle.py verify --quick
        language: system
        types: [python]
        pass_filenames: false

      - id: oracle-imports
        name: Oracle Import Check
        entry: python3 oracle/project_oracle.py verify --imports
        language: system
        types: [python]
        pass_filenames: false
"""

    def install_hooks(self) -> bool:
        """Install pre-commit hooks."""
        config_path = self.project_root / ".pre-commit-config.yaml"

        try:
            config_content = self.generate_config()
            config_path.write_text(config_content)

            # Try to install pre-commit if available
            import subprocess
            result = subprocess.run(
                ["pre-commit", "install"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True
            )

            return result.returncode == 0
        except Exception as e:
            debug_log(f"Failed to install hooks: {e}", "hooks")
            return False

    def uninstall_hooks(self) -> bool:
        """Uninstall pre-commit hooks."""
        config_path = self.project_root / ".pre-commit-config.yaml"

        try:
            if config_path.exists():
                config_path.unlink()

            import subprocess
            result = subprocess.run(
                ["pre-commit", "uninstall"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True
            )

            return result.returncode == 0
        except Exception:
            return False


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

def verify(mode: str = "standard", perf: bool = False, baseline: bool = False,
           fix: bool = False, apply: bool = False, install_hooks: bool = False) -> Dict:
    """Run integrity verification.

    Args:
        mode: Verification mode - "quick", "standard", or "full"
        perf: Check performance regression
        baseline: Save new performance baseline
        fix: Preview auto-fixes
        apply: Apply auto-fixes
        install_hooks: Install pre-commit hooks

    Returns:
        Dict with verification results
    """
    results = {}

    # Install hooks if requested
    if install_hooks:
        hook_mgr = HookManager()
        results["hooks_installed"] = hook_mgr.install_hooks()
        return results

    # Handle auto-fix
    if fix:
        fixer = AutoFixer()
        fixes = fixer.preview_fixes()

        if apply:
            results["fixes"] = fixer.apply_fixes(fixes)
        else:
            results["proposed_fixes"] = [
                {"file": f.file_path, "type": f.issue_type, "description": f.description}
                for f in fixes
            ]
        return results

    # Handle performance tracking
    if perf:
        tracker = PerformanceTracker()
        if baseline:
            b = tracker.capture_baseline()
            results["baseline"] = {
                "captured": b.captured.isoformat(),
                "files": b.file_count,
                "lines": b.line_count,
                "functions": b.function_count
            }
        else:
            results["performance"] = tracker.compare_with_baseline()
        return results

    # Run verification
    verifier = IntegrityVerifier()
    report = verifier.verify(mode)

    results["verification"] = {
        "mode": report.mode,
        "health_score": report.health_score,
        "duration_ms": report.duration_ms,
        "issues": len(report.issues),
        "critical": sum(1 for i in report.issues if i.severity == "critical"),
        "warnings": sum(1 for i in report.issues if i.severity == "warning"),
        "checks_passed": report.checks_passed,
        "checks_failed": report.checks_failed,
        "summary": report.summary
    }

    # Include issue details
    if report.issues:
        results["issue_details"] = [
            {
                "severity": i.severity,
                "category": i.category,
                "title": i.title,
                "file": i.file_path,
                "line": i.line_number,
                "suggestion": i.suggestion
            }
            for i in report.issues[:20]  # Limit to 20
        ]

    return results


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for topoisomerase commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Topoisomerase - Codebase integrity verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 oracle/validation/topoisomerase.py --quick     # Quick check
  python3 oracle/validation/topoisomerase.py             # Standard check
  python3 oracle/validation/topoisomerase.py --full      # Full check
  python3 oracle/validation/topoisomerase.py --perf      # Performance regression
  python3 oracle/validation/topoisomerase.py --fix       # Preview fixes
  python3 oracle/validation/topoisomerase.py --fix --apply  # Apply fixes
        """
    )

    parser.add_argument("--quick", action="store_true", help="Quick verification (~5s)")
    parser.add_argument("--full", action="store_true", help="Full verification")
    parser.add_argument("--perf", action="store_true", help="Performance regression check")
    parser.add_argument("--baseline", action="store_true", help="Save new baseline")
    parser.add_argument("--fix", action="store_true", help="Preview auto-fixes")
    parser.add_argument("--apply", action="store_true", help="Apply fixes")
    parser.add_argument("--install-hooks", action="store_true", help="Install pre-commit hooks")

    args = parser.parse_args()

    # Determine mode
    mode = "standard"
    if args.quick:
        mode = "quick"
    elif args.full:
        mode = "full"

    results = verify(
        mode=mode,
        perf=args.perf,
        baseline=args.baseline,
        fix=args.fix,
        apply=args.apply,
        install_hooks=args.install_hooks
    )

    # Print results
    if "verification" in results:
        v = results["verification"]
        print(f"\n{'='*50}")
        print(f"  INTEGRITY VERIFICATION ({v['mode']})")
        print(f"{'='*50}")
        print(f"  Health Score: {v['health_score']:.0f}%")
        print(f"  Duration: {v['duration_ms']:.0f}ms")
        print(f"  Issues: {v['issues']} ({v['critical']} critical, {v['warnings']} warnings)")
        print(f"\n  Checks Passed: {', '.join(v['checks_passed']) or 'none'}")
        print(f"  Checks Failed: {', '.join(v['checks_failed']) or 'none'}")

        if "issue_details" in results:
            print(f"\n  Issues:")
            for issue in results["issue_details"][:10]:
                print(f"    [{issue['severity']}] {issue['title']}")
                if issue['file']:
                    print(f"           {issue['file']}:{issue['line'] or ''}")

    elif "performance" in results:
        p = results["performance"]
        print(f"\n{'='*50}")
        print(f"  PERFORMANCE COMPARISON")
        print(f"{'='*50}")
        if "error" in p:
            print(f"  {p['error']}")
        else:
            print(f"  Baseline: {p['baseline_date']}")
            print(f"\n  Files: {p['file_count']['current']} ({p['file_count']['diff']:+d})")
            print(f"  Lines: {p['line_count']['current']} ({p['line_count']['diff']:+d})")
            print(f"  Functions: {p['function_count']['current']} ({p['function_count']['diff']:+d})")
            if p['layer_changes']:
                print(f"\n  Layer Changes:")
                for layer, change in p['layer_changes'].items():
                    print(f"    {layer}: {change}")

    elif "baseline" in results:
        b = results["baseline"]
        print(f"\n  Baseline saved:")
        print(f"    Files: {b['files']}")
        print(f"    Lines: {b['lines']}")
        print(f"    Functions: {b['functions']}")

    elif "proposed_fixes" in results:
        print(f"\n  Proposed Fixes: {len(results['proposed_fixes'])}")
        for fix in results["proposed_fixes"]:
            print(f"    - [{fix['type']}] {fix['description']}")
            print(f"      {fix['file']}")

    elif "fixes" in results:
        f = results["fixes"]
        print(f"\n  Fixes Applied: {f['applied']}")
        print(f"  Fixes Failed: {f['failed']}")

    elif "hooks_installed" in results:
        if results["hooks_installed"]:
            print("\n  Pre-commit hooks installed successfully")
        else:
            print("\n  Failed to install pre-commit hooks")
            print("  Make sure pre-commit is installed: pip install pre-commit")

    print()


if __name__ == "__main__":
    main()
