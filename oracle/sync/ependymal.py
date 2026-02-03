#!/usr/bin/env python3
"""
Ependymal - Oracle Brain Cell: Documentation Sync, Reports, Knowledge Flow
===========================================================================

Brain Metaphor: Ependymal cells line the brain ventricles and produce cerebrospinal
fluid, maintaining the flow of nutrients and waste products. This module manages
documentation flow, sync, and report generation.

Also known as "Neurons" (unofficial alias) - the documentation/knowledge flow system.

Responsibilities:
- Documentation sync and drift detection
- Desktop sync for Claude Desktop project folder
- Report generation
- Cross-document consistency

Commands: sync, docs, report
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

ORACLE_DIR = Path(__file__).parent.parent  # Up from sync/ to oracle/
PROJECT_ROOT = ORACLE_DIR.parent  # Up from oracle/ to project root
DOCS_DIR = ORACLE_DIR / "docs"
DOCS_OVERVIEW_DIR = DOCS_DIR / "overview"
DOCS_CONTEXT_DIR = DOCS_DIR / "context"
DOCS_CODE_DIR = DOCS_DIR / "code only"
REPORTS_DIR = ORACLE_DIR / "reports"
AUDITS_DIR = REPORTS_DIR / "audits"

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")

def debug_log(msg: str, category: str = "general"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  🔍 [{timestamp}] [{category}] {msg}")

# Constants
MAX_REPORTS = 5

# Historical scripts (deleted/merged) - not flagged as missing
HISTORICAL_SCRIPTS = {
    "configure_calendar.py",
    "configure_segments.py",
    "trend_detection.py",
    "video_assembly.py",
    "instagram_carousel_generator.py",
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def cleanup_old_files(directory: Path, pattern: str, max_keep: int = 5) -> int:
    """Delete old files matching pattern, keeping only the most recent max_keep."""
    if not directory.exists():
        return 0
    files = sorted(directory.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)
    deleted = 0
    for old_file in files[max_keep:]:
        try:
            old_file.unlink()
            deleted += 1
        except Exception:
            pass
    return deleted


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


@dataclass
class AuditReport:
    """Complete audit report."""
    timestamp: datetime = field(default_factory=datetime.now)
    health_score: float = 0.0
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
    doc_sync_status: dict = field(default_factory=dict)
    summary: str = ""


# =============================================================================
# DOC DRIFT AUDITOR
# =============================================================================

class DocDriftAuditor:
    """Check if documentation matches code reality."""

    def __init__(self, project_root: Path, doc_files: dict, scripts_dir: Path):
        self.project_root = project_root
        self.doc_files = doc_files
        self.scripts_dir = scripts_dir
        self.issues = []

    def run(self) -> list:
        """Run all documentation drift checks."""
        self.issues = []

        self._check_script_references()
        self._check_path_references()
        self._check_timestamps()
        self._check_cross_references()

        return self.issues

    def _check_script_references(self):
        """Verify scripts mentioned in docs actually exist."""
        actual_scripts = set()
        if self.scripts_dir.exists():
            actual_scripts = {s.name for s in self.scripts_dir.glob("*.py")}

        oracle_scripts = set()
        oracle_maint = ORACLE_DIR / "maintenance"
        if oracle_maint.exists():
            oracle_scripts = {s.name for s in oracle_maint.glob("*.py")}

        all_scripts = actual_scripts | oracle_scripts

        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            mentioned_scripts = set(re.findall(r'\b(\w+\.py)\b', content))

            for script in mentioned_scripts:
                if script.startswith("test_") or script in ["setup.py", "conftest.py"]:
                    continue
                if script in HISTORICAL_SCRIPTS:
                    continue
                if script not in all_scripts:
                    self.issues.append(Issue(
                        severity="warning",
                        category="docs",
                        title=f"Referenced script not found: {script}",
                        description=f"Mentioned in {doc_name}",
                        file_path=str(doc_path),
                        suggestion="Update documentation or create the script"
                    ))

    def _check_path_references(self):
        """Verify folder paths mentioned in docs exist."""
        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            folder_patterns = [
                r'`(output/[^`]+)`',
                r'`(scripts/[^`]+)`',
                r'`(content/[^`]+)`',
            ]

            for pattern in folder_patterns:
                for match in re.finditer(pattern, content):
                    path = self.project_root / match.group(1).rstrip('/')
                    if '.' in path.name and not path.exists():
                        self.issues.append(Issue(
                            severity="info",
                            category="docs",
                            title=f"Referenced path may not exist: {match.group(1)}",
                            description=f"Mentioned in {doc_name}",
                            file_path=str(doc_path),
                            suggestion="Verify path exists or update documentation"
                        ))

    def _check_timestamps(self):
        """Check for stale 'Last Updated' timestamps."""
        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            timestamp_match = re.search(r'Last Updated[:\s]+(\w+ \d+, \d{4}|\d{4}-\d{2}-\d{2})', content)

            if timestamp_match:
                try:
                    date_str = timestamp_match.group(1)
                    for fmt in ["%B %d, %Y", "%Y-%m-%d", "%b %d, %Y"]:
                        try:
                            doc_date = datetime.strptime(date_str, fmt)
                            days_old = (datetime.now() - doc_date).days

                            if days_old > 30:
                                self.issues.append(Issue(
                                    severity="info",
                                    category="docs",
                                    title=f"Potentially stale documentation: {doc_name}",
                                    description=f"Last updated {days_old} days ago",
                                    file_path=str(doc_path),
                                    suggestion="Review and update if needed"
                                ))
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass

    def _check_cross_references(self):
        """Verify cross-references between docs are valid."""
        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            doc_refs = re.findall(r'(?:See|see|→)\s+([A-Z_]+\.md|docs/[A-Za-z_]+\.md|context/[A-Za-z_]+\.md)', content)

            for ref in doc_refs:
                ref_filename = ref.split("/")[-1] if "/" in ref else ref
                possible_paths = [
                    self.project_root / ref,
                    DOCS_DIR / ref,
                    DOCS_DIR / ref_filename,
                    DOCS_OVERVIEW_DIR / ref_filename,
                    DOCS_CONTEXT_DIR / ref_filename,
                ]

                found = any(p.exists() for p in possible_paths)

                if not found:
                    self.issues.append(Issue(
                        severity="warning",
                        category="docs",
                        title=f"Broken doc reference: {ref}",
                        description=f"Referenced in {doc_name}",
                        file_path=str(doc_path),
                        suggestion="Update reference or create missing doc"
                    ))


# =============================================================================
# DOC OPTIMIZER
# =============================================================================

class DocOptimizer:
    """Automated documentation cleanup, synchronization, and fix application."""

    DOC_TEMPLATES = {
        "DEV_CONTEXT.md": ["Recent Changes", "Pending Tasks", "Architecture"],
        "ORACLE_CONTEXT.md": ["Recent Changes", "Current State", "Pending Tasks"],
        "ARCHITECTURE.md": ["Layer", "Pipeline", "File Structure"],
        "WORKFLOW.md": ["Environment Setup", "Session Management"],
    }

    SCRIPT_RENAMES = {
        "video_assembly.py": "assembly.py",
        "image_overlay.py": "pil_processor.py",
        "generate_idea.py": "idea_creation.py",
    }

    def __init__(self, project_root: Path, config: dict, dry_run: bool = True):
        self.project_root = project_root
        self.config = config
        self.dry_run = dry_run
        self.docs_dir = DOCS_DIR
        self.context_dir = DOCS_CONTEXT_DIR
        self.changes_made = []
        self.backup_files = []
        self.doc_files = self._build_doc_map()

    def _build_doc_map(self) -> dict:
        """Build map of all documentation files."""
        doc_map = {}

        if self.context_dir.exists():
            for md_file in self.context_dir.glob("*.md"):
                doc_map[md_file.name] = md_file

        if DOCS_OVERVIEW_DIR.exists():
            for md_file in DOCS_OVERVIEW_DIR.glob("*.md"):
                doc_map[md_file.name] = md_file

        if DOCS_CODE_DIR.exists():
            for md_file in DOCS_CODE_DIR.glob("*.md"):
                doc_map[md_file.name] = md_file

        return doc_map

    def run_all(self, operations: list = None) -> dict:
        """Run doc optimizer operations."""
        if operations is None:
            operations = ['timestamps', 'dead_refs', 'links', 'structure']

        results = {
            "dry_run": self.dry_run,
            "timestamps_fixed": [],
            "dead_refs_fixed": [],
            "broken_links": [],
            "missing_sections": [],
            "files_modified": []
        }

        if 'timestamps' in operations:
            results["timestamps_fixed"] = self._sync_timestamps()

        if 'dead_refs' in operations:
            results["dead_refs_fixed"] = self._fix_dead_refs()

        if 'links' in operations:
            results["broken_links"] = self._validate_links()

        if 'structure' in operations:
            results["missing_sections"] = self._check_structure()

        results["files_modified"] = self.changes_made
        return results

    def _sync_timestamps(self) -> list:
        """Update 'Last Updated' headers to today's date."""
        fixed = []
        today = datetime.now().strftime("%B %d, %Y")

        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            timestamp_match = re.search(
                r'(\*\*Last Updated:\*\*\s*)(\w+ \d+, \d{4}|\d{4}-\d{2}-\d{2})',
                content
            )

            if timestamp_match:
                current_date = timestamp_match.group(2)
                if today not in current_date:
                    fixed.append({
                        "file": doc_name,
                        "old_date": current_date,
                        "new_date": today,
                        "action": "would update" if self.dry_run else "updated"
                    })

                    if not self.dry_run:
                        new_content = content.replace(
                            timestamp_match.group(0),
                            f"{timestamp_match.group(1)}{today}"
                        )
                        doc_path.write_text(new_content)
                        self.changes_made.append(str(doc_path))

        return fixed

    def _fix_dead_refs(self) -> list:
        """Replace renamed script references with current names."""
        fixed = []

        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            original_content = content
            doc_fixes = []

            for old_name, new_name in self.SCRIPT_RENAMES.items():
                if old_name in content:
                    count = content.count(old_name)
                    doc_fixes.append({
                        "old": old_name,
                        "new": new_name,
                        "count": count
                    })
                    content = content.replace(old_name, new_name)

            if doc_fixes:
                fixed.append({
                    "file": doc_name,
                    "replacements": doc_fixes,
                    "action": "would fix" if self.dry_run else "fixed"
                })

                if not self.dry_run and content != original_content:
                    doc_path.write_text(content)
                    self.changes_made.append(str(doc_path))

        return fixed

    def _validate_links(self) -> list:
        """Check internal markdown links and report broken ones."""
        broken = []

        for doc_name, doc_path in self.doc_files.items():
            if not doc_path.exists():
                continue

            content = doc_path.read_text()
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

            for match in re.finditer(link_pattern, content):
                link_text = match.group(1)
                link_path = match.group(2)

                if link_path.startswith(('http', 'https', '#', 'mailto:')):
                    continue

                if link_path.endswith('.md') or link_path.endswith('.py'):
                    resolved = doc_path.parent / link_path
                    if not resolved.exists():
                        resolved = self.project_root / link_path
                        if not resolved.exists():
                            broken.append({
                                "file": doc_name,
                                "link_text": link_text,
                                "target": link_path,
                                "suggestion": "Update or remove broken link"
                            })

        return broken

    def _check_structure(self) -> list:
        """Verify required sections exist in each doc type."""
        missing = []

        for doc_name, required_sections in self.DOC_TEMPLATES.items():
            doc_path = self.doc_files.get(doc_name)

            if not doc_path or not doc_path.exists():
                continue

            content = doc_path.read_text()

            for section in required_sections:
                if not re.search(rf'#+\s*.*{re.escape(section)}', content, re.IGNORECASE):
                    missing.append({
                        "file": doc_name,
                        "section": section,
                        "suggestion": f"Add missing section: {section}"
                    })

        return missing


# =============================================================================
# DESKTOP SYNC
# =============================================================================

OVERVIEW_FILES = [
    "ARCHITECTURE.md",
    "PHILOSOPHY.md",
    "CODE_HISTORY.md",
    "WORKFLOW.md",
    "TOOLS_REFERENCE.md",
    "IDEAS_BACKLOG.md",
    "STYLE_GUIDE.md",
]

SYNC_FROM_EXTERNAL: List[Tuple[str, str]] = [
    ("assets/branding/brand_colors.json", "brand_colors.json"),
]


def get_file_info(path: Path) -> Dict:
    """Get file modification time and size."""
    if not path.exists():
        return {"exists": False, "mtime": None, "size": 0}
    stat = path.stat()
    return {
        "exists": True,
        "mtime": datetime.fromtimestamp(stat.st_mtime),
        "size": stat.st_size,
    }


def check_external_sync_status() -> Dict[str, Dict]:
    """Check which external files need syncing to overview/."""
    status = {}

    for src_rel, dest_name in SYNC_FROM_EXTERNAL:
        src_path = PROJECT_ROOT / src_rel
        dest_path = DOCS_OVERVIEW_DIR / dest_name

        src_info = get_file_info(src_path)
        dest_info = get_file_info(dest_path)

        needs_sync = False
        reason = ""

        if not src_info["exists"]:
            reason = "source missing"
        elif not dest_info["exists"]:
            needs_sync = True
            reason = "not in overview/"
        elif src_info["mtime"] > dest_info["mtime"]:
            needs_sync = True
            reason = "source newer"
        else:
            reason = "up to date"

        status[dest_name] = {
            "source": str(src_rel),
            "needs_sync": needs_sync,
            "reason": reason,
        }

    return status


def sync_external_files(dry_run: bool = False, force: bool = False) -> Tuple[int, int, List[str]]:
    """Sync external files to overview directory."""
    DOCS_OVERVIEW_DIR.mkdir(parents=True, exist_ok=True)

    status = check_external_sync_status()
    synced = 0
    skipped = 0
    errors = []

    for dest_name, info in status.items():
        src_path = PROJECT_ROOT / info["source"]
        dest_path = DOCS_OVERVIEW_DIR / dest_name

        if not src_path.exists():
            errors.append(f"Source not found: {info['source']}")
            continue

        if info["needs_sync"] or force:
            if dry_run:
                print(f"  Would sync: {dest_name} ({info['reason']})")
                synced += 1
            else:
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"  ✓ Synced: {dest_name}")
                    synced += 1
                except Exception as e:
                    errors.append(f"Failed to copy {dest_name}: {e}")
        else:
            skipped += 1

    return synced, skipped, errors


def print_desktop_status():
    """Print detailed overview folder status."""
    print("\n📁 Desktop Overview Folder Status")
    print("=" * 60)
    print(f"Location: oracle/docs/overview/")
    print()

    status = {}
    for filename in OVERVIEW_FILES:
        path = DOCS_OVERVIEW_DIR / filename
        info = get_file_info(path)
        status[filename] = info

    print("📄 Documentation Files:")
    for filename in OVERVIEW_FILES:
        info = status.get(filename, {})
        if info.get("exists"):
            mtime_str = info["mtime"].strftime("%Y-%m-%d %H:%M") if info["mtime"] else "?"
            size_kb = info["size"] / 1024
            print(f"   ✓ {filename:<25} {mtime_str}  ({size_kb:.1f} KB)")
        else:
            print(f"   ✗ {filename:<25} (missing)")

    print("=" * 60)


# =============================================================================
# REPORT GENERATOR
# =============================================================================

class ReportGenerator:
    """Generate audit reports in markdown format."""

    def __init__(self, project_root: Path, config: dict):
        self.project_root = project_root
        self.config = config
        self.reports_dir = REPORTS_DIR
        self.audits_dir = AUDITS_DIR
        self.reports_dir.mkdir(exist_ok=True)
        self.audits_dir.mkdir(exist_ok=True)

    def generate_full_report(self, issues: list, health_score: float = 0.0) -> str:
        """Generate a full audit report markdown."""
        now = datetime.now()

        lines = [
            f"# Oracle Audit Report",
            "",
            f"**Generated:** {now.strftime('%B %d, %Y %H:%M')}",
            f"**Health Score:** {health_score:.1f}/10",
            "",
            "---",
            "",
        ]

        # Summary
        critical = sum(1 for i in issues if i.severity == "critical")
        warnings = sum(1 for i in issues if i.severity == "warning")
        info_count = sum(1 for i in issues if i.severity == "info")

        lines.extend([
            "## Summary",
            "",
            f"| Severity | Count |",
            f"|----------|-------|",
            f"| Critical | {critical} |",
            f"| Warning | {warnings} |",
            f"| Info | {info_count} |",
            "",
        ])

        # Issues by category
        if issues:
            lines.append("## Issues")
            lines.append("")

            by_category = {}
            for issue in issues:
                if issue.category not in by_category:
                    by_category[issue.category] = []
                by_category[issue.category].append(issue)

            for category, cat_issues in by_category.items():
                lines.append(f"### {category.title()}")
                lines.append("")
                for issue in cat_issues:
                    icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue.severity, "•")
                    lines.append(f"- {icon} **{issue.title}**")
                    lines.append(f"  - {issue.description}")
                    if issue.suggestion:
                        lines.append(f"  - *Suggestion:* {issue.suggestion}")
                lines.append("")

        lines.extend([
            "---",
            "",
            "*Generated by Oracle Ependymal*",
        ])

        return "\n".join(lines)

    def save_report(self, report_content: str) -> Path:
        """Save report to file and cleanup old reports."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.audits_dir / f"ORACLE_REPORT_{timestamp}.md"
        report_path.write_text(report_content)

        cleanup_old_files(self.audits_dir, "ORACLE_REPORT_*.md", MAX_REPORTS)

        return report_path


# =============================================================================
# PUBLIC INTERFACE FUNCTIONS
# =============================================================================

def run_sync(dry_run: bool = True, desktop: bool = False) -> dict:
    """Run documentation sync.

    Args:
        dry_run: If True, only show what would be done
        desktop: If True, also sync desktop files

    Returns:
        Dict with sync results
    """
    results = {"dry_run": dry_run, "doc_optimizer": {}, "desktop_sync": {}}

    # Run doc optimizer
    optimizer = DocOptimizer(PROJECT_ROOT, {}, dry_run=dry_run)
    results["doc_optimizer"] = optimizer.run_all()

    # Desktop sync if requested
    if desktop:
        synced, skipped, errors = sync_external_files(dry_run=dry_run)
        results["desktop_sync"] = {
            "synced": synced,
            "skipped": skipped,
            "errors": errors
        }

    return results


def run_docs() -> dict:
    """Run doc drift audit.

    Returns:
        Dict with audit results
    """
    # Build doc files map
    doc_files = {}
    if DOCS_CONTEXT_DIR.exists():
        for md_file in DOCS_CONTEXT_DIR.glob("*.md"):
            doc_files[md_file.name] = md_file
    if DOCS_OVERVIEW_DIR.exists():
        for md_file in DOCS_OVERVIEW_DIR.glob("*.md"):
            doc_files[md_file.name] = md_file

    auditor = DocDriftAuditor(PROJECT_ROOT, doc_files, PROJECT_ROOT / "scripts")
    issues = auditor.run()

    print(f"\n📄 Documentation Audit Results")
    print("=" * 50)
    print(f"Files checked: {len(doc_files)}")
    print(f"Issues found: {len(issues)}")

    if issues:
        for issue in issues[:10]:
            icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue.severity, "•")
            print(f"  {icon} {issue.title}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")

    return {"issues": issues, "files_checked": len(doc_files)}


def generate_report() -> str:
    """Generate full audit report.

    Returns:
        Path to saved report
    """
    # Gather issues from doc drift audit
    doc_files = {}
    if DOCS_CONTEXT_DIR.exists():
        for md_file in DOCS_CONTEXT_DIR.glob("*.md"):
            doc_files[md_file.name] = md_file

    auditor = DocDriftAuditor(PROJECT_ROOT, doc_files, PROJECT_ROOT / "scripts")
    issues = auditor.run()

    # Calculate health score
    critical = sum(1 for i in issues if i.severity == "critical")
    warnings = sum(1 for i in issues if i.severity == "warning")
    health_score = max(0, 10 - (critical * 2) - (warnings * 0.5))

    # Generate report
    generator = ReportGenerator(PROJECT_ROOT, {})
    report_content = generator.generate_full_report(issues, health_score)
    report_path = generator.save_report(report_content)

    print(f"\n📋 Report saved to: {report_path}")
    print(f"   Health Score: {health_score:.1f}/10")

    return str(report_path)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for ependymal commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Ependymal - Documentation sync, reports, knowledge flow",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync documentation")
    sync_parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    sync_parser.add_argument("--desktop", action="store_true", help="Also sync desktop files")
    sync_parser.add_argument("--apply", action="store_true", help="Actually apply changes")

    # Docs command
    subparsers.add_parser("docs", help="Run doc drift audit")

    # Report command
    subparsers.add_parser("report", help="Generate full audit report")

    args = parser.parse_args()

    if args.command == "sync":
        dry_run = not args.apply
        results = run_sync(dry_run=dry_run, desktop=args.desktop)

        print(f"\n📄 Sync {'(DRY RUN)' if dry_run else ''} Results:")
        if results["doc_optimizer"].get("timestamps_fixed"):
            print(f"  Timestamps: {len(results['doc_optimizer']['timestamps_fixed'])} would be updated")
        if results["doc_optimizer"].get("dead_refs_fixed"):
            print(f"  Dead refs: {len(results['doc_optimizer']['dead_refs_fixed'])} would be fixed")

        if args.desktop:
            print_desktop_status()

    elif args.command == "docs":
        run_docs()

    elif args.command == "report":
        generate_report()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
