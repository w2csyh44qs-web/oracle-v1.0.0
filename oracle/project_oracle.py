#!/usr/bin/env python3
"""
Project Oracle - Central Orchestrator
======================================

The main CLI orchestrator that routes commands to specialized brain cell modules:

Brain Cell Modules:
    - microglia.py (maintenance/) - Error detection, cleanup, debugging
    - astrocytes.py (context/) - Context management, snapshots, environment
    - oligodendrocytes.py (optimization/) - Performance, API costs
    - ependymal.py (sync/) - Documentation sync, reports
    - cortex.py (project/) - Project-specific tools (presets, layers)
    - seeg.py (oracle/) - Real-time monitoring dashboard
    - topoisomerase.py (validation/) - Codebase integrity verification
    - helicase.py (validation/) - Codebase assessment

Commands (15 total):
    audit       - Run health audits (microglia)
    clean       - Cleanup code issues (microglia)
    debug-script - Script execution tracing (microglia)
    status      - Quick health summary (astrocytes)
    context     - Context file management (astrocytes)
    snapshot    - Capture session state (astrocytes)
    optimize    - Performance optimization (oligodendrocytes)
    api-log     - API call tracking (oligodendrocytes)
    sync        - Documentation sync (ependymal)
    docs        - Doc optimization (ependymal)
    report      - Generate full report (ependymal)
    presets     - Show preset configurations (cortex)
    monitor     - Real-time dashboard (seeg)
    verify      - Codebase integrity verification (topoisomerase)
    assess      - Codebase assessment (helicase)
    config      - Show parsed configuration

Usage:
    python3 oracle/project_oracle.py <command> [options]
    python3 oracle/project_oracle.py --help

Author: Oracle Brain Cell Architecture
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent  # Up from oracle/ to root
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# CONFIGURATION
# =============================================================================
ORACLE_DIR = PROJECT_ROOT / "oracle"
LAYERS_DIR = PROJECT_ROOT / "app" / "core" / "pipeline" / "layers"
DOCS_DIR = ORACLE_DIR / "docs"
DOCS_CONTEXT_DIR = DOCS_DIR / "context"
REPORTS_DIR = ORACLE_DIR / "reports"
CONTEXT_FILE = DOCS_CONTEXT_DIR / "DEV_CONTEXT.md"

# All context files (for auto-archive, sync)
CONTEXT_FILES = [
    DOCS_CONTEXT_DIR / "DEV_CONTEXT.md",
    DOCS_CONTEXT_DIR / "ORACLE_CONTEXT.md",
    DOCS_CONTEXT_DIR / "CRANK_CONTEXT.md",
    DOCS_CONTEXT_DIR / "POCKET_CONTEXT.md",
    DOCS_CONTEXT_DIR / "DASHBOARD_CONTEXT.md",
]

# Debug mode
DEBUG = os.environ.get("ORACLE_DEBUG", "").lower() in ("1", "true", "yes")


def debug_log(msg: str, category: str = "general"):
    """Print debug message if DEBUG mode is enabled."""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  [DEBUG] [{timestamp}] [{category}] {msg}")


# =============================================================================
# CONTEXT PARSER (Minimal - for config loading)
# =============================================================================

class ContextParser:
    """Parse DEV_CONTEXT.md for project configuration."""

    def __init__(self, context_file: Path):
        self.context_file = context_file
        self.parse_errors = []

    def parse(self) -> dict:
        """Parse context file and return configuration dict."""
        config = {
            "doc_files": {},
            "layers": {},
            "api_services": {},
            "current_focus": "",
            "pending_tasks": [],
        }

        if not self.context_file.exists():
            self.parse_errors.append(f"Context file not found: {self.context_file}")
            return config

        try:
            content = self.context_file.read_text()

            # Parse layers section
            import re
            layer_pattern = r'\| L(\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|'
            for match in re.finditer(layer_pattern, content):
                layer_num = match.group(1)
                config["layers"][layer_num] = {
                    "name": match.group(2).strip(),
                    "scripts": match.group(3).strip(),
                    "output": match.group(4).strip(),
                }

            # Parse API services
            api_pattern = r'\| ([A-Za-z]+) \| \$([0-9.]+)/(\w+) \| ([^|]+) \|'
            for match in re.finditer(api_pattern, content):
                config["api_services"][match.group(1)] = {
                    "cost": float(match.group(2)),
                    "unit": match.group(3),
                    "use_case": match.group(4).strip(),
                }

        except Exception as e:
            self.parse_errors.append(f"Parse error: {e}")

        return config

    def get_parse_summary(self) -> str:
        """Return summary of parsed configuration."""
        config = self.parse()
        lines = [
            "=" * 50,
            "CONFIGURATION SUMMARY",
            "=" * 50,
            f"Layers: {len(config['layers'])}",
            f"API Services: {len(config['api_services'])}",
            f"Doc Files: {len(config['doc_files'])}",
        ]

        if self.parse_errors:
            lines.append(f"\nParse Warnings: {len(self.parse_errors)}")
            for err in self.parse_errors[:5]:
                lines.append(f"  - {err}")

        lines.append("=" * 50)
        return "\n".join(lines)


# =============================================================================
# MAIN CLI
# =============================================================================

def main():
    """Main CLI entry point - routes commands to brain cell modules."""

    parser = argparse.ArgumentParser(
        description="Project Oracle - Central Orchestrator for Project Health & Optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Brain Cell Modules:
  microglia        Error detection, cleanup, debugging
  astrocytes       Context management, snapshots
  oligodendrocytes Performance, API costs
  ependymal        Documentation sync, reports
  cortex           Project-specific tools
  seeg             Real-time monitoring
  topoisomerase    Integrity verification (verify)
  helicase         Codebase assessment (assess)

Examples:
  python3 oracle/project_oracle.py audit --quick   # Quick health check
  python3 oracle/project_oracle.py status          # One-line summary
  python3 oracle/project_oracle.py monitor         # Real-time dashboard
  python3 oracle/project_oracle.py sync --dry-run  # Preview doc sync
  python3 oracle/project_oracle.py presets         # Show presets table
  python3 oracle/project_oracle.py verify --quick  # Quick integrity check
  python3 oracle/project_oracle.py assess          # Assess codebase
        """
    )

    parser.add_argument("--debug", action="store_true",
                        help="Enable verbose debug logging")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # =========================================================================
    # MICROGLIA COMMANDS (maintenance/microglia.py)
    # =========================================================================

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Run health audits")
    audit_parser.add_argument("--quick", action="store_true", help="Quick audit")
    audit_parser.add_argument("--deep", action="store_true", help="Deep audit")
    audit_parser.add_argument("--code", action="store_true", help="Code-only audit")

    # clean command
    clean_parser = subparsers.add_parser("clean", help="Cleanup code issues")
    clean_parser.add_argument("--apply", action="store_true", help="Apply fixes")
    clean_parser.add_argument("--reports", action="store_true", help="Clean old reports")
    clean_parser.add_argument("--tasks", action="store_true", help="Prune completed tasks")
    clean_parser.add_argument("--dead-code", action="store_true", help="Remove dead code")

    # debug-script command
    debug_parser = subparsers.add_parser("debug-script", help="Script execution tracing")
    debug_parser.add_argument("script", help="Script path")
    debug_parser.add_argument("script_args", nargs="*", help="Script arguments")
    debug_parser.add_argument("--trace-calls", action="store_true")
    debug_parser.add_argument("--trace-lines", action="store_true")
    debug_parser.add_argument("--watch-vars", type=str, default="")
    debug_parser.add_argument("--output", "-o", type=str)

    # =========================================================================
    # ASTROCYTES COMMANDS (context/astrocytes.py)
    # =========================================================================

    # status command
    status_parser = subparsers.add_parser("status", help="Quick health summary")

    # context command
    context_parser_cmd = subparsers.add_parser("context", help="Context file management")

    # snapshot command
    snapshot_parser = subparsers.add_parser("snapshot", help="Capture session state")
    snapshot_parser.add_argument("--sync", action="store_true", help="Autosave mode")
    snapshot_parser.add_argument("--task", "-t", help="Current task")
    snapshot_parser.add_argument("--file", "-f", help="Last file worked on")

    # =========================================================================
    # OLIGODENDROCYTES COMMANDS (optimization/oligodendrocytes.py)
    # =========================================================================

    # optimize command
    optimize_parser = subparsers.add_parser("optimize", help="Performance optimization")
    optimize_parser.add_argument("--apply", action="store_true", help="Apply optimizations")
    optimize_parser.add_argument("--clean", action="store_true", help="Clean mode")
    optimize_parser.add_argument("--prune", action="store_true", help="Prune mode")
    optimize_parser.add_argument("--check", action="store_true", help="Check mode")
    optimize_parser.add_argument("--all", action="store_true", help="All checks")

    # api-log command
    api_log_parser = subparsers.add_parser("api-log", help="API call tracking")
    api_log_parser.add_argument("--last", "-n", type=int, default=20)
    api_log_parser.add_argument("--provider", "-p", type=str)
    api_log_parser.add_argument("--summary", "-s", action="store_true")
    api_log_parser.add_argument("--clear", action="store_true")

    # =========================================================================
    # EPENDYMAL COMMANDS (sync/ependymal.py)
    # =========================================================================

    # sync command
    sync_parser = subparsers.add_parser("sync", help="Documentation sync")
    sync_parser.add_argument("--apply", action="store_true", help="Apply changes")
    sync_parser.add_argument("--dry-run", action="store_true", help="Preview only")
    sync_parser.add_argument("--desktop", action="store_true", help="Include desktop sync")

    # docs command
    docs_parser = subparsers.add_parser("docs", help="Doc optimization")
    docs_parser.add_argument("--apply", action="store_true", help="Apply fixes")
    docs_parser.add_argument("--timestamps", action="store_true")
    docs_parser.add_argument("--session-count", action="store_true")
    docs_parser.add_argument("--dead-refs", action="store_true")
    docs_parser.add_argument("--links", action="store_true")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate full report")
    report_parser.add_argument("--output", "-o", help="Output file path")

    # =========================================================================
    # CORTEX COMMANDS (project/cortex.py)
    # =========================================================================

    # presets command
    presets_parser = subparsers.add_parser("presets", help="Show preset configurations")
    presets_parser.add_argument("--output", "-o", choices=["table", "markdown", "json"],
                                default="table")
    presets_parser.add_argument("--save", "-s", action="store_true")

    # layers command
    layers_parser = subparsers.add_parser("layers", help="Show pipeline layers")
    layers_parser.add_argument("--layer", "-l", help="Filter to specific layer")

    # pipeline-info command
    pipeline_parser = subparsers.add_parser("pipeline-info", help="Show pipeline info")

    # =========================================================================
    # SEEG COMMANDS (oracle/seeg.py)
    # =========================================================================

    # monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Real-time monitoring dashboard")
    monitor_parser.add_argument("--mode", choices=["full", "compact", "minimal"],
                                default="full")
    monitor_parser.add_argument("--once", action="store_true", help="Run once and exit")

    # =========================================================================
    # VALIDATION COMMANDS (validation/topoisomerase.py, validation/helicase.py)
    # =========================================================================

    # verify command (topoisomerase)
    verify_parser = subparsers.add_parser("verify", help="Codebase integrity verification")
    verify_parser.add_argument("--quick", action="store_true", help="Quick verification (~5s)")
    verify_parser.add_argument("--full", action="store_true", help="Full verification")
    verify_parser.add_argument("--perf", action="store_true", help="Performance regression check")
    verify_parser.add_argument("--baseline", action="store_true", help="Save new performance baseline")
    verify_parser.add_argument("--fix", action="store_true", help="Preview auto-fixes")
    verify_parser.add_argument("--apply", action="store_true", help="Apply auto-fixes")
    verify_parser.add_argument("--install-hooks", action="store_true", help="Install pre-commit hooks")

    # assess command (helicase)
    assess_parser = subparsers.add_parser("assess", help="Codebase assessment")
    assess_parser.add_argument("--init", action="store_true", help="Generate Oracle config")
    assess_parser.add_argument("--graph", action="store_true", help="Build call graph")
    assess_parser.add_argument("--output", "-o", help="Output file for graph JSON")
    assess_parser.add_argument("--ci", choices=["github", "gitlab"], help="Generate CI template")
    assess_parser.add_argument("--baseline", action="store_true", help="Comprehensive baseline")

    # =========================================================================
    # CONFIG COMMAND (local)
    # =========================================================================

    config_parser_cmd = subparsers.add_parser("config", help="Show parsed configuration")
    config_parser_cmd.add_argument("--verbose", "-v", action="store_true")

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Enable debug mode
    global DEBUG
    if args.debug:
        DEBUG = True
        os.environ["ORACLE_DEBUG"] = "1"
        print("Debug mode enabled\n")

    # Load configuration
    quiet_mode = args.command in ("status", "snapshot")
    if not quiet_mode:
        debug_log(f"Loading config from: {CONTEXT_FILE}", "parse")

    context_parser = ContextParser(CONTEXT_FILE)
    config = context_parser.parse()

    # =========================================================================
    # COMMAND ROUTING
    # =========================================================================

    # CONFIG command (local)
    if args.command == "config":
        print(context_parser.get_parse_summary())
        if getattr(args, 'verbose', False):
            print("\nLayers:")
            for num, info in config["layers"].items():
                print(f"  L{num}: {info['name']}")
        return

    # MICROGLIA commands
    if args.command in ("audit", "clean", "debug-script"):
        from oracle.maintenance.microglia import run_audit, run_clean, run_debug_script

        if args.command == "audit":
            result = run_audit(
                quick=getattr(args, 'quick', False),
                deep=getattr(args, 'deep', False),
                code_only=getattr(args, 'code', False)
            )
            print(f"\nHealth Score: {result.health_score:.1f}/10")
            print(f"Issues: {len(result.issues)} ({sum(1 for i in result.issues if i.severity == 'critical')} critical)")

        elif args.command == "clean":
            result = run_clean(
                reports=getattr(args, 'reports', False),
                tasks=getattr(args, 'tasks', False),
                dead_code=getattr(args, 'dead_code', False)
            )
            print(f"Cleaned: {result.get('files_removed', 0)} files")

        elif args.command == "debug-script":
            watch_vars = [v.strip() for v in args.watch_vars.split(',') if v.strip()]
            exit_code = run_debug_script(
                script_path=args.script,
                script_args=args.script_args,
                trace_calls=args.trace_calls,
                trace_lines=args.trace_lines,
                watch_vars=watch_vars,
                output_file=args.output
            )
            sys.exit(exit_code)

    # ASTROCYTES commands
    elif args.command in ("status", "context", "snapshot"):
        from oracle.context.astrocytes import get_status, manage_context, create_snapshot

        if args.command == "status":
            print(get_status())

        elif args.command == "context":
            manage_context()

        elif args.command == "snapshot":
            result = create_snapshot(
                sync=getattr(args, 'sync', False),
                active_task=getattr(args, 'task', None),
                last_file=getattr(args, 'file', None)
            )
            if result.get("snapshot_path"):
                print(f"Snapshot saved: {result['snapshot_path']}")

    # OLIGODENDROCYTES commands
    elif args.command in ("optimize", "api-log"):
        from oracle.optimization.oligodendrocytes import run_optimize, get_api_log, print_api_summary

        if args.command == "optimize":
            result = run_optimize(
                apply=getattr(args, 'apply', False),
                clean=getattr(args, 'clean', False),
                prune=getattr(args, 'prune', False),
                check=getattr(args, 'check', False),
                all_checks=getattr(args, 'all', False)
            )
            print(f"\nOptimizations found: {result.get('total_findings', 0)}")

        elif args.command == "api-log":
            if getattr(args, 'clear', False):
                from oracle.optimization.oligodendrocytes import api_logger
                api_logger.clear()
                print("API log cleared.")
            elif getattr(args, 'summary', False):
                print_api_summary()
            else:
                calls = get_api_log()
                # Filter by provider if specified
                provider = getattr(args, 'provider', None)
                if provider:
                    calls = [c for c in calls if c.get("provider") == provider]
                # Limit to last N
                last_n = args.last
                calls = calls[-last_n:] if len(calls) > last_n else calls

                if calls:
                    print(f"\nAPI Calls (last {len(calls)}):")
                    for call in calls:
                        print(f"  {call.get('timestamp', '?')[:19]} | {call.get('provider', '?')} | ${call.get('cost_usd', 0):.4f}")
                else:
                    print("No API calls logged.")

    # EPENDYMAL commands
    elif args.command in ("sync", "docs", "report"):
        from oracle.sync.ependymal import run_sync, run_docs, generate_report

        if args.command == "sync":
            result = run_sync(
                dry_run=not getattr(args, 'apply', False),
                desktop=getattr(args, 'desktop', False)
            )
            print(f"\nSync complete. Changes: {result.get('changes_made', 0)}")

        elif args.command == "docs":
            result = run_docs()
            print(f"\nDoc issues found: {result.get('issues_found', 0)}")

        elif args.command == "report":
            report_path = generate_report()
            print(f"\nReport generated: {report_path}")

    # CORTEX commands
    elif args.command in ("presets", "layers", "pipeline-info"):
        from oracle.project.cortex import analyze_presets, show_layers, show_pipeline_info

        if args.command == "presets":
            analyze_presets(
                output_format=getattr(args, 'output', 'table'),
                save=getattr(args, 'save', False)
            )

        elif args.command == "layers":
            show_layers(layer_filter=getattr(args, 'layer', None))

        elif args.command == "pipeline-info":
            show_pipeline_info()

    # SEEG commands
    elif args.command == "monitor":
        from oracle import seeg
        seeg.run_monitor(
            mode=getattr(args, 'mode', 'full'),
            once=getattr(args, 'once', False)
        )

    # VALIDATION commands (topoisomerase, helicase)
    elif args.command == "verify":
        from oracle.validation.topoisomerase import verify

        # Determine mode
        mode = "standard"
        if getattr(args, 'quick', False):
            mode = "quick"
        elif getattr(args, 'full', False):
            mode = "full"

        results = verify(
            mode=mode,
            perf=getattr(args, 'perf', False),
            baseline=getattr(args, 'baseline', False),
            fix=getattr(args, 'fix', False),
            apply=getattr(args, 'apply', False),
            install_hooks=getattr(args, 'install_hooks', False)
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
                print(f"\n  Issues (top 10):")
                for issue in results["issue_details"][:10]:
                    print(f"    [{issue['severity']}] {issue['title']}")

        elif "performance" in results:
            p = results["performance"]
            print(f"\n  Performance Comparison:")
            if "error" in p:
                print(f"  {p['error']}")
            else:
                print(f"  Files: {p['file_count']['current']} ({p['file_count']['diff']:+d})")
                print(f"  Lines: {p['line_count']['current']} ({p['line_count']['diff']:+d})")

        elif "baseline" in results:
            print(f"\n  Baseline saved: {results['baseline']['files']} files, {results['baseline']['lines']} lines")

        elif "proposed_fixes" in results:
            print(f"\n  Proposed Fixes: {len(results['proposed_fixes'])}")
            for fix in results["proposed_fixes"][:5]:
                print(f"    - {fix['description']}")

        elif "fixes" in results:
            print(f"\n  Fixes Applied: {results['fixes']['applied']}")

        elif "hooks_installed" in results:
            print(f"\n  Pre-commit hooks: {'installed' if results['hooks_installed'] else 'failed'}")

    elif args.command == "assess":
        from oracle.validation.helicase import assess

        results = assess(
            init=getattr(args, 'init', False),
            graph=getattr(args, 'graph', False),
            output=getattr(args, 'output', None),
            ci=getattr(args, 'ci', None),
            baseline=getattr(args, 'baseline', False)
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
            print(f"  Tests: {'Yes' if a['has_tests'] else 'No'} | CI: {'Yes' if a['has_ci'] else 'No'} | Docs: {'Yes' if a['has_docs'] else 'No'}")
            print(f"  Issues: {a['issues']} ({a['critical']} critical)")
            print(f"  Oracle Ready: {'Yes' if a['oracle_ready'] else 'No'}")

            if "recommendations" in results:
                print(f"\n  Recommendations:")
                for rec in results["recommendations"][:5]:
                    print(f"    - {rec}")

        elif "graph" in results:
            g = results["graph"]
            if "output" in g:
                print(f"\n  Call graph saved to: {g['output']}")
            else:
                print(f"\n  Call Graph: {g['stats']['total_functions']} functions, {g['stats']['total_edges']} edges")
                print(f"  Orphans: {g['stats']['orphan_count']}")

        elif "ci_template" in results:
            ct = results["ci_template"]
            if ct["success"]:
                print(f"\n  CI template created: {ct['path']}")
            else:
                print(f"\n  Failed: {ct['error']}")

    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()
