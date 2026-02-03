#!/usr/bin/env python3
"""
Helicase - Oracle Brain Cell: Codebase Assessment
==================================================

Brain Metaphor: Helicase opens/unwinds DNA double helix to allow reading
and copying. Similarly, this module "opens up" new codebases for assessment,
understanding, and Oracle integration.

Responsibilities:
- Assess new/existing codebases for Oracle integration
- Build function call graphs for visualization
- Generate CI/CD templates
- Create Oracle configuration for new projects

Commands: assess
"""

import os
import sys
import ast
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

VALIDATION_DIR = Path(__file__).parent
ORACLE_DIR = VALIDATION_DIR.parent
PROJECT_ROOT = ORACLE_DIR.parent
TEMPLATES_DIR = VALIDATION_DIR / "templates"

# Add project root to path for imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")


def debug_log(msg: str, category: str = "helicase"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  [DEBUG] [{timestamp}] [{category}] {msg}")


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class AssessmentIssue:
    """Single assessment finding."""
    severity: str  # "critical", "warning", "info", "suggestion"
    category: str  # "structure", "config", "dependencies", "patterns"
    title: str
    description: str
    suggestion: Optional[str] = None


@dataclass
class CodebaseProfile:
    """Profile of assessed codebase."""
    name: str = ""
    root_path: str = ""
    language: str = "python"
    framework: str = ""
    file_count: int = 0
    line_count: int = 0
    test_coverage: float = 0.0
    has_tests: bool = False
    has_ci: bool = False
    has_docs: bool = False


@dataclass
class AssessmentReport:
    """Complete assessment report."""
    timestamp: datetime = field(default_factory=datetime.now)
    profile: CodebaseProfile = field(default_factory=CodebaseProfile)
    issues: List[AssessmentIssue] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    oracle_ready: bool = False
    summary: str = ""


@dataclass
class CallGraphNode:
    """Node in call graph."""
    id: str
    name: str
    file_path: str
    line_number: int
    node_type: str  # "function", "method", "class"
    layer: Optional[str] = None
    call_count: int = 0


@dataclass
class CallGraphEdge:
    """Edge in call graph."""
    source: str
    target: str
    count: int = 1


# =============================================================================
# CODEBASE ASSESSOR
# =============================================================================

class CodebaseAssessor:
    """Assess new codebases for Oracle integration."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.profile = CodebaseProfile()
        self.issues: List[AssessmentIssue] = []
        self.recommendations: List[str] = []

    def assess(self) -> AssessmentReport:
        """Assess the codebase.

        Returns:
            AssessmentReport with findings
        """
        self.issues = []
        self.recommendations = []

        # Build profile
        self._build_profile()

        # Run assessment checks
        self._assess_structure()
        self._assess_dependencies()
        self._assess_patterns()
        self._assess_oracle_readiness()

        # Generate recommendations
        self._generate_recommendations()

        # Determine oracle readiness
        critical_issues = sum(1 for i in self.issues if i.severity == "critical")
        oracle_ready = critical_issues == 0

        return AssessmentReport(
            profile=self.profile,
            issues=self.issues,
            recommendations=self.recommendations,
            oracle_ready=oracle_ready,
            summary=f"Files: {self.profile.file_count} | Lines: {self.profile.line_count} | Issues: {len(self.issues)} | Oracle Ready: {oracle_ready}"
        )

    def _build_profile(self):
        """Build codebase profile."""
        self.profile.name = self.project_root.name
        self.profile.root_path = str(self.project_root)

        # Count files and lines
        for py_file in self.project_root.rglob("*.py"):
            # Skip venv and common excluded directories
            if any(part in py_file.parts for part in ["venv", "env", ".venv", "node_modules", "__pycache__", ".git"]):
                continue
            try:
                self.profile.file_count += 1
                self.profile.line_count += len(py_file.read_text().splitlines())
            except Exception:
                pass

        # Detect framework
        self._detect_framework()

        # Check for tests
        test_dirs = ["tests", "test", "spec"]
        for test_dir in test_dirs:
            if (self.project_root / test_dir).exists():
                self.profile.has_tests = True
                break

        # Check for CI
        ci_files = [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", ".circleci"]
        for ci_path in ci_files:
            if (self.project_root / ci_path).exists():
                self.profile.has_ci = True
                break

        # Check for docs
        doc_paths = ["docs", "documentation", "README.md"]
        for doc_path in doc_paths:
            if (self.project_root / doc_path).exists():
                self.profile.has_docs = True
                break

    def _detect_framework(self):
        """Detect framework used in project."""
        # Check requirements.txt or pyproject.toml
        req_files = ["requirements.txt", "pyproject.toml", "setup.py"]

        for req_file in req_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                try:
                    content = req_path.read_text().lower()

                    if "flask" in content:
                        self.profile.framework = "Flask"
                    elif "django" in content:
                        self.profile.framework = "Django"
                    elif "fastapi" in content:
                        self.profile.framework = "FastAPI"
                    elif "streamlit" in content:
                        self.profile.framework = "Streamlit"
                    elif "pytorch" in content or "torch" in content:
                        self.profile.framework = "PyTorch"
                    elif "tensorflow" in content:
                        self.profile.framework = "TensorFlow"

                    break
                except Exception:
                    pass

    def _assess_structure(self):
        """Assess project structure."""
        # Check for app/ or src/ directory
        has_app_dir = (self.project_root / "app").exists() or (self.project_root / "src").exists()

        if not has_app_dir:
            self.issues.append(AssessmentIssue(
                severity="warning",
                category="structure",
                title="No app/ or src/ directory",
                description="Project lacks standard source directory structure",
                suggestion="Consider organizing code into app/ or src/ directory"
            ))

        # Check for config directory
        if not (self.project_root / "config").exists():
            self.issues.append(AssessmentIssue(
                severity="info",
                category="structure",
                title="No config/ directory",
                description="Configuration files may be scattered",
                suggestion="Consider centralizing configs in config/ directory"
            ))

        # Check for README
        if not (self.project_root / "README.md").exists():
            self.issues.append(AssessmentIssue(
                severity="warning",
                category="structure",
                title="No README.md",
                description="Project documentation is missing",
                suggestion="Add README.md with project overview"
            ))

    def _assess_dependencies(self):
        """Assess project dependencies."""
        req_path = self.project_root / "requirements.txt"

        if not req_path.exists():
            pyproject = self.project_root / "pyproject.toml"
            if not pyproject.exists():
                self.issues.append(AssessmentIssue(
                    severity="warning",
                    category="dependencies",
                    title="No dependency specification",
                    description="requirements.txt or pyproject.toml not found",
                    suggestion="Create requirements.txt with pip freeze"
                ))

    def _assess_patterns(self):
        """Assess code patterns and anti-patterns."""
        # Check for hardcoded secrets
        secret_patterns = [
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Potential hardcoded API key"),
            (r'password\s*=\s*["\'][^"\']+["\']', "Potential hardcoded password"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Potential hardcoded secret"),
        ]

        import re

        for py_file in self.project_root.rglob("*.py"):
            if any(part in py_file.parts for part in ["venv", "env", ".venv", "__pycache__"]):
                continue
            try:
                content = py_file.read_text()
                for pattern, issue_title in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.issues.append(AssessmentIssue(
                            severity="critical",
                            category="patterns",
                            title=issue_title,
                            description=f"Found in {py_file.name}",
                            suggestion="Move secrets to environment variables"
                        ))
                        break  # One per file
            except Exception:
                pass

    def _assess_oracle_readiness(self):
        """Check if Oracle can be effectively integrated."""
        # Check for oracle directory already
        if (self.project_root / "oracle").exists():
            self.issues.append(AssessmentIssue(
                severity="info",
                category="structure",
                title="Oracle already present",
                description="oracle/ directory exists",
                suggestion="Use verify command instead of assess"
            ))

    def _generate_recommendations(self):
        """Generate recommendations based on assessment."""
        if not self.profile.has_tests:
            self.recommendations.append("Add unit tests in tests/ directory")

        if not self.profile.has_ci:
            self.recommendations.append("Set up CI/CD pipeline (GitHub Actions recommended)")

        if not self.profile.has_docs:
            self.recommendations.append("Add documentation in docs/ directory")

        if self.profile.file_count > 50 and not (self.project_root / "oracle").exists():
            self.recommendations.append("Consider adding Oracle for health monitoring")

        # Framework-specific recommendations
        if self.profile.framework == "Flask":
            self.recommendations.append("Use Flask blueprints for route organization")
        elif self.profile.framework == "Django":
            self.recommendations.append("Run python manage.py check regularly")


# =============================================================================
# CALL GRAPH ANALYZER
# =============================================================================

class CallGraphAnalyzer:
    """Build function call graph for visualization and analysis."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.nodes: Dict[str, CallGraphNode] = {}
        self.edges: List[CallGraphEdge] = []
        self.orphans: List[str] = []
        self.hot_paths: List[List[str]] = []

    def build_graph(self, directories: List[Path] = None) -> Dict:
        """Build function call graph.

        Args:
            directories: Directories to analyze. Defaults to app/

        Returns:
            Dict with nodes, edges, orphans, hot_paths
        """
        if directories is None:
            directories = [self.project_root / "app"]

        self.nodes = {}
        self.edges = []
        self.orphans = []

        # Collect all function definitions
        for directory in directories:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                self._analyze_file(py_file)

        # Find function calls and build edges
        for directory in directories:
            if not directory.exists():
                continue
            for py_file in directory.rglob("*.py"):
                self._find_calls(py_file)

        # Find orphan functions (never called)
        called_functions = set()
        for edge in self.edges:
            called_functions.add(edge.target)

        for node_id, node in self.nodes.items():
            if node_id not in called_functions:
                # Skip main, __init__, etc.
                if node.name not in ("main", "__init__", "cli", "run"):
                    self.orphans.append(node_id)

        # Find hot paths
        self._find_hot_paths()

        return self.export_for_dashboard()

    def _analyze_file(self, file_path: Path):
        """Analyze a single file for function definitions."""
        try:
            content = file_path.read_text()
            tree = ast.parse(content)
        except Exception:
            return

        # Detect layer from path
        layer = None
        for part in file_path.parts:
            if part.startswith("_L") and len(part) == 3:
                layer = part
                break

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                node_id = f"{file_path.stem}.{node.name}"

                self.nodes[node_id] = CallGraphNode(
                    id=node_id,
                    name=node.name,
                    file_path=str(file_path),
                    line_number=node.lineno,
                    node_type="function",
                    layer=layer
                )

            elif isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        node_id = f"{file_path.stem}.{node.name}.{item.name}"

                        self.nodes[node_id] = CallGraphNode(
                            id=node_id,
                            name=f"{node.name}.{item.name}",
                            file_path=str(file_path),
                            line_number=item.lineno,
                            node_type="method",
                            layer=layer
                        )

    def _find_calls(self, file_path: Path):
        """Find function calls in file."""
        try:
            content = file_path.read_text()
            tree = ast.parse(content)
        except Exception:
            return

        # Get current file's functions for context
        current_funcs = [n.id for n in self.nodes.values() if n.file_path == str(file_path)]

        class CallVisitor(ast.NodeVisitor):
            def __init__(self, analyzer, source_file):
                self.analyzer = analyzer
                self.source_file = source_file
                self.current_function = None

            def visit_FunctionDef(self, node):
                old_func = self.current_function
                self.current_function = f"{self.source_file.stem}.{node.name}"
                self.generic_visit(node)
                self.current_function = old_func

            def visit_Call(self, node):
                if self.current_function is None:
                    self.generic_visit(node)
                    return

                target = None

                if isinstance(node.func, ast.Name):
                    # Simple function call
                    func_name = node.func.id
                    # Look for matching node
                    for node_id in self.analyzer.nodes:
                        if node_id.endswith(f".{func_name}"):
                            target = node_id
                            break

                elif isinstance(node.func, ast.Attribute):
                    # Method call
                    attr_name = node.func.attr
                    for node_id in self.analyzer.nodes:
                        if node_id.endswith(f".{attr_name}"):
                            target = node_id
                            break

                if target and target != self.current_function:
                    # Add edge
                    existing_edge = None
                    for edge in self.analyzer.edges:
                        if edge.source == self.current_function and edge.target == target:
                            existing_edge = edge
                            break

                    if existing_edge:
                        existing_edge.count += 1
                    else:
                        self.analyzer.edges.append(CallGraphEdge(
                            source=self.current_function,
                            target=target
                        ))

                    # Increment call count on target node
                    if target in self.analyzer.nodes:
                        self.analyzer.nodes[target].call_count += 1

                self.generic_visit(node)

        visitor = CallVisitor(self, file_path)
        visitor.visit(tree)

    def _find_hot_paths(self, max_paths: int = 5):
        """Find most-called function chains."""
        # Sort nodes by call count
        sorted_nodes = sorted(
            self.nodes.values(),
            key=lambda n: n.call_count,
            reverse=True
        )[:10]

        # Build simple hot paths from most-called functions
        for node in sorted_nodes[:max_paths]:
            path = [node.name]

            # Follow edges from this node
            current = node.id
            visited = {current}

            while True:
                # Find most frequent outgoing edge
                outgoing = [e for e in self.edges if e.source == current]
                if not outgoing:
                    break

                best_edge = max(outgoing, key=lambda e: e.count)
                if best_edge.target in visited:
                    break

                visited.add(best_edge.target)
                target_node = self.nodes.get(best_edge.target)
                if target_node:
                    path.append(target_node.name)
                    current = best_edge.target
                else:
                    break

                if len(path) >= 5:  # Limit path length
                    break

            if len(path) > 1:
                self.hot_paths.append(path)

    def find_orphan_functions(self) -> List[str]:
        """Return list of functions that are never called."""
        return self.orphans

    def export_for_dashboard(self) -> Dict:
        """Export graph in Dashboard-compatible format."""
        return {
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "type": n.node_type,
                    "layer": n.layer,
                    "calls": n.call_count,
                    "file": Path(n.file_path).name,
                    "line": n.line_number
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "count": e.count
                }
                for e in self.edges
            ],
            "orphans": self.orphans,
            "hot_paths": self.hot_paths,
            "stats": {
                "total_functions": len(self.nodes),
                "total_edges": len(self.edges),
                "orphan_count": len(self.orphans)
            }
        }


# =============================================================================
# CI TEMPLATE GENERATOR
# =============================================================================

class CITemplateGenerator:
    """Generate CI/CD pipeline templates for Oracle integration."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT

    def generate_github_actions(self) -> str:
        """Generate GitHub Actions workflow template."""
        return """name: Oracle Health Check

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  oracle-verify:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Oracle Quick Verify
        run: python3 oracle/project_oracle.py verify --quick

      - name: Oracle Full Verify
        run: python3 oracle/project_oracle.py verify

      - name: Performance Check
        run: python3 oracle/project_oracle.py verify --perf
        continue-on-error: true
"""

    def generate_gitlab_ci(self) -> str:
        """Generate GitLab CI template."""
        return """stages:
  - verify
  - test

oracle-verify:
  stage: verify
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python3 oracle/project_oracle.py verify --quick
  only:
    - merge_requests
    - main
    - master

oracle-full:
  stage: test
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python3 oracle/project_oracle.py verify
    - python3 oracle/project_oracle.py verify --perf
  only:
    - main
    - master
  allow_failure: true
"""

    def save_template(self, ci_type: str) -> Path:
        """Save CI template to appropriate location."""
        if ci_type == "github":
            target_dir = self.project_root / ".github" / "workflows"
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / "oracle.yml"
            target_file.write_text(self.generate_github_actions())
        elif ci_type == "gitlab":
            target_file = self.project_root / ".gitlab-ci.yml"
            target_file.write_text(self.generate_gitlab_ci())
        else:
            raise ValueError(f"Unknown CI type: {ci_type}")

        return target_file


# =============================================================================
# PUBLIC INTERFACE
# =============================================================================

def assess(init: bool = False, graph: bool = False, output: str = None,
           ci: str = None, baseline: bool = False) -> Dict:
    """Assess codebase.

    Args:
        init: Generate Oracle config for new project
        graph: Build and export call graph
        output: Output file path for graph JSON
        ci: Generate CI template (github/gitlab)
        baseline: Generate comprehensive baseline

    Returns:
        Dict with assessment results
    """
    results = {}

    # Generate CI template if requested
    if ci:
        generator = CITemplateGenerator()
        try:
            template_path = generator.save_template(ci)
            results["ci_template"] = {
                "type": ci,
                "path": str(template_path),
                "success": True
            }
        except Exception as e:
            results["ci_template"] = {
                "type": ci,
                "error": str(e),
                "success": False
            }
        return results

    # Build call graph if requested
    if graph:
        analyzer = CallGraphAnalyzer()
        graph_data = analyzer.build_graph()

        if output:
            output_path = Path(output)
            with open(output_path, 'w') as f:
                json.dump(graph_data, f, indent=2)
            results["graph"] = {
                "output": str(output_path),
                "stats": graph_data["stats"]
            }
        else:
            results["graph"] = graph_data

        return results

    # Run assessment
    assessor = CodebaseAssessor()
    report = assessor.assess()

    results["assessment"] = {
        "name": report.profile.name,
        "framework": report.profile.framework or "unknown",
        "files": report.profile.file_count,
        "lines": report.profile.line_count,
        "has_tests": report.profile.has_tests,
        "has_ci": report.profile.has_ci,
        "has_docs": report.profile.has_docs,
        "issues": len(report.issues),
        "critical": sum(1 for i in report.issues if i.severity == "critical"),
        "oracle_ready": report.oracle_ready,
        "summary": report.summary
    }

    if report.issues:
        results["issue_details"] = [
            {
                "severity": i.severity,
                "category": i.category,
                "title": i.title,
                "suggestion": i.suggestion
            }
            for i in report.issues
        ]

    if report.recommendations:
        results["recommendations"] = report.recommendations

    return results


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for helicase commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Helicase - Codebase assessment and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 oracle/validation/helicase.py               # Assess current project
  python3 oracle/validation/helicase.py --graph       # Build call graph
  python3 oracle/validation/helicase.py --graph -o g.json  # Export graph
  python3 oracle/validation/helicase.py --ci github   # Generate GitHub Actions
  python3 oracle/validation/helicase.py --ci gitlab   # Generate GitLab CI
        """
    )

    parser.add_argument("--init", action="store_true", help="Initialize Oracle config")
    parser.add_argument("--graph", action="store_true", help="Build call graph")
    parser.add_argument("--output", "-o", help="Output file for graph JSON")
    parser.add_argument("--ci", choices=["github", "gitlab"], help="Generate CI template")
    parser.add_argument("--baseline", action="store_true", help="Comprehensive baseline")

    args = parser.parse_args()

    results = assess(
        init=args.init,
        graph=args.graph,
        output=args.output,
        ci=args.ci,
        baseline=args.baseline
    )

    # Print results
    if "assessment" in results:
        a = results["assessment"]
        print(f"\n{'='*50}")
        print(f"  CODEBASE ASSESSMENT")
        print(f"{'='*50}")
        print(f"  Project: {a['name']}")
        print(f"  Framework: {a['framework']}")
        print(f"  Files: {a['files']} | Lines: {a['lines']}")
        print(f"\n  Has Tests: {'Yes' if a['has_tests'] else 'No'}")
        print(f"  Has CI: {'Yes' if a['has_ci'] else 'No'}")
        print(f"  Has Docs: {'Yes' if a['has_docs'] else 'No'}")
        print(f"\n  Issues: {a['issues']} ({a['critical']} critical)")
        print(f"  Oracle Ready: {'Yes' if a['oracle_ready'] else 'No'}")

        if "issue_details" in results:
            print(f"\n  Issues:")
            for issue in results["issue_details"]:
                print(f"    [{issue['severity']}] {issue['title']}")
                if issue['suggestion']:
                    print(f"           -> {issue['suggestion']}")

        if "recommendations" in results:
            print(f"\n  Recommendations:")
            for rec in results["recommendations"]:
                print(f"    - {rec}")

    elif "graph" in results:
        g = results["graph"]
        if "output" in g:
            print(f"\n  Call graph saved to: {g['output']}")
            print(f"  Stats: {g['stats']['total_functions']} functions, {g['stats']['total_edges']} edges")
        else:
            print(f"\n{'='*50}")
            print(f"  CALL GRAPH")
            print(f"{'='*50}")
            print(f"  Functions: {g['stats']['total_functions']}")
            print(f"  Edges: {g['stats']['total_edges']}")
            print(f"  Orphans: {g['stats']['orphan_count']}")

            if g['hot_paths']:
                print(f"\n  Hot Paths:")
                for path in g['hot_paths'][:5]:
                    print(f"    {' -> '.join(path)}")

            if g['orphans'][:10]:
                print(f"\n  Orphan Functions (sample):")
                for orphan in g['orphans'][:10]:
                    print(f"    - {orphan}")

    elif "ci_template" in results:
        ct = results["ci_template"]
        if ct["success"]:
            print(f"\n  CI template created: {ct['path']}")
        else:
            print(f"\n  Failed to create CI template: {ct['error']}")

    print()


if __name__ == "__main__":
    main()
