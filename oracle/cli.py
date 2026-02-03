"""
Oracle CLI - Command Line Interface

Main entry point for Oracle commands, including the new `oracle init` command.

Commands:
- oracle init <project_root> - Bootstrap Oracle on any Python project
- oracle detect <project_root> - Analyze project structure without initialization
- oracle version - Show Oracle version

Usage:
    python oracle/cli.py init /path/to/project
    python oracle/cli.py detect /path/to/project
    python oracle/cli.py version

Author: Oracle Brain Cell Architecture (P30 Phase 4)
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from oracle.bootstrap import OracleInitializer, ProjectDetector
from oracle.bootstrap.terminal import set_verbose, TerminalColors
from oracle.daemon import OracleDaemonService, ServiceManager

# Dashboard import (optional - requires Flask)
try:
    from oracle.web_dashboard import DashboardServer
except ImportError:
    DashboardServer = None


def cmd_init(args):
    """Handle 'oracle init' command."""
    project_root = Path(args.project_root).resolve()

    initializer = OracleInitializer(project_root)
    success = initializer.init(dry_run=args.dry_run)

    return 0 if success else 1


def cmd_detect(args):
    """Handle 'oracle detect' command."""
    project_root = Path(args.project_root).resolve()

    detector = ProjectDetector(project_root)
    profile = detector.analyze()

    if args.output:
        import json
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            json.dump(profile.to_dict(), f, indent=2)
        print(f"\n💾 Profile saved to: {output_path}")
    else:
        import json
        print("\n📋 Project Profile:")
        print(json.dumps(profile.to_dict(), indent=2))

    return 0


def cmd_version(args):
    """Handle 'oracle version' command."""
    from oracle.bootstrap import __version__ as bootstrap_version

    print("Oracle v1.0.0")
    print(f"Bootstrap: v{bootstrap_version}")
    print("Brain Cell Architecture (P23 + P26 + P30 + P31)")
    return 0


def cmd_daemon(args):
    """Handle 'oracle daemon' command."""
    project_root = Path(args.project_root).resolve()

    # Daemon management commands
    if args.daemon_command == 'install':
        # Install system service
        manager = ServiceManager(project_root)
        success = manager.install()
        if success:
            print("\n✅ Daemon service installed successfully!")
            print("💡 The daemon will start automatically on system boot")
            print(f"💡 Logs: {project_root}/oracle/data/.oracle_daemon.log")
        return 0 if success else 1

    elif args.daemon_command == 'uninstall':
        # Uninstall system service
        manager = ServiceManager(project_root)
        success = manager.uninstall()
        if success:
            print("\n✅ Daemon service uninstalled successfully")
        return 0 if success else 1

    elif args.daemon_command == 'enable':
        # Enable auto-start on boot
        manager = ServiceManager(project_root)
        success = manager.enable()
        return 0 if success else 1

    elif args.daemon_command == 'disable':
        # Disable auto-start on boot
        manager = ServiceManager(project_root)
        success = manager.disable()
        return 0 if success else 1

    elif args.daemon_command == 'start':
        # Start daemon
        daemon = OracleDaemonService(project_root)
        success = daemon.start(background=not args.foreground)
        if success and not args.foreground:
            print(f"\n✅ Daemon started successfully in background")
            print(f"💡 Check status: oracle daemon status")
            print(f"💡 View logs: tail -f {project_root}/oracle/data/.oracle_daemon.log")
        return 0 if success else 1

    elif args.daemon_command == 'stop':
        # Stop daemon
        daemon = OracleDaemonService(project_root)
        success = daemon.stop()
        if success:
            print("\n✅ Daemon stopped successfully")
        return 0 if success else 1

    elif args.daemon_command == 'restart':
        # Restart daemon
        daemon = OracleDaemonService(project_root)
        success = daemon.restart()
        if success:
            print("\n✅ Daemon restarted successfully")
        return 0 if success else 1

    elif args.daemon_command == 'status':
        # Get daemon status
        daemon = OracleDaemonService(project_root)
        status = daemon.status()

        import json
        print("\n📊 Daemon Status:")
        print(json.dumps(status, indent=2))

        if status.get('running'):
            print(f"\n✅ Daemon is running (PID: {status.get('pid')})")
        else:
            print("\n⚠️  Daemon is not running")
            print("💡 Start with: oracle daemon start")

        return 0

    elif args.daemon_command == 'logs':
        # Show logs
        log_file = project_root / "oracle" / "data" / ".oracle_daemon.log"
        if log_file.exists():
            print(f"\n📄 Daemon Log ({log_file}):")
            print("=" * 60)
            # Show last 50 lines
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-50:]:
                    print(line, end='')
        else:
            print(f"\n⚠️  Log file not found: {log_file}")
        return 0

    return 1


def cmd_dashboard(args):
    """Handle 'oracle dashboard' command."""
    project_root = Path(args.project_root).resolve()

    # Dashboard commands
    if args.dashboard_command == 'start':
        # Check if DashboardServer is available
        if DashboardServer is None:
            print("\n❌ Dashboard dependencies not installed")
            print("💡 Install with: pip install flask flask-socketio flask-cors python-socketio")
            return 1

        # Start dashboard server
        try:
            server = DashboardServer(project_root, host=args.host, port=args.port)
            print(f"\n🚀 Starting Oracle Dashboard...")
            print(f"📡 Server: http://{args.host}:{args.port}")
            print(f"📁 Project: {project_root}")
            print(f"\n💡 Press Ctrl+C to stop\n")
            server.start()
        except Exception as e:
            print(f"\n❌ Failed to start dashboard: {e}")
            return 1
        return 0

    elif args.dashboard_command == 'stop':
        # Stop dashboard server (kill by port)
        import signal
        try:
            # Find process using the port
            result = subprocess.run(
                ["lsof", "-ti", f":{args.port}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"✅ Stopped dashboard (PID: {pid})")
                    except ProcessLookupError:
                        pass
                return 0
            else:
                print(f"⚠️  No dashboard running on port {args.port}")
                return 0
        except FileNotFoundError:
            print("⚠️  Cannot check port (lsof not available)")
            return 1
        except Exception as e:
            print(f"❌ Error stopping dashboard: {e}")
            return 1

    elif args.dashboard_command == 'status':
        # Check dashboard status
        try:
            import urllib.request
            url = f"http://{args.host}:{args.port}/api/status"
            response = urllib.request.urlopen(url, timeout=2)
            print(f"\n✅ Dashboard is running")
            print(f"📡 URL: http://{args.host}:{args.port}")
            return 0
        except Exception:
            print(f"\n⚠️  Dashboard is not running")
            print(f"💡 Start with: oracle dashboard start")
            return 0

    return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="oracle",
        description="Oracle - Project-Agnostic Development Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Bootstrap
  oracle init /path/to/project              Bootstrap Oracle on a project
  oracle init . --dry-run                   Preview changes without applying
  oracle init . --verbose                   Show detailed progress

  # Analysis
  oracle detect /path/to/project            Analyze project structure
  oracle detect . --output profile.json     Save analysis to file

  # Daemon Management
  oracle daemon install                     Install system service (auto-start)
  oracle daemon start                       Start daemon
  oracle daemon stop                        Stop daemon
  oracle daemon status                      Check daemon status
  oracle daemon logs                        View daemon logs

  # Dashboard
  oracle dashboard start                    Start web dashboard (port 7777)
  oracle dashboard start --port 8080        Start on custom port
  oracle dashboard stop                     Stop web dashboard
  oracle dashboard status                   Check dashboard status

  # Info
  oracle version                            Show version information

For more information, see the Oracle documentation.
        """,
    )

    # Global flags
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress and timing information",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-essential output",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # oracle init
    parser_init = subparsers.add_parser(
        "init",
        help="Bootstrap Oracle on any Python project",
        description="Initialize Oracle on a Python project by detecting structure and generating configs.",
    )
    parser_init.add_argument(
        "project_root",
        help="Root directory of project to initialize",
    )
    parser_init.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them",
    )
    parser_init.set_defaults(func=cmd_init)

    # oracle detect
    parser_detect = subparsers.add_parser(
        "detect",
        help="Analyze project structure without initialization",
        description="Detect framework, structure, and tools in a Python project.",
    )
    parser_detect.add_argument(
        "project_root",
        help="Root directory of project to analyze",
    )
    parser_detect.add_argument(
        "--output",
        "-o",
        help="Save profile to JSON file",
    )
    parser_detect.set_defaults(func=cmd_detect)

    # oracle version
    parser_version = subparsers.add_parser(
        "version",
        help="Show Oracle version information",
    )
    parser_version.set_defaults(func=cmd_version)

    # oracle daemon
    parser_daemon = subparsers.add_parser(
        "daemon",
        help="Manage Oracle background daemon",
        description="Start, stop, and manage the Oracle daemon service.",
    )
    parser_daemon.add_argument(
        "daemon_command",
        choices=["install", "uninstall", "enable", "disable", "start", "stop", "restart", "status", "logs"],
        help="Daemon management command",
    )
    parser_daemon.add_argument(
        "--project-root",
        default=".",
        help="Root directory of project (default: current directory)",
    )
    parser_daemon.add_argument(
        "--foreground",
        action="store_true",
        help="Run daemon in foreground (for start command)",
    )
    parser_daemon.set_defaults(func=cmd_daemon)

    # oracle dashboard
    parser_dashboard = subparsers.add_parser(
        "dashboard",
        help="Manage Oracle web dashboard",
        description="Start, stop, and manage the Oracle web dashboard (monitoring + terminal UI).",
    )
    parser_dashboard.add_argument(
        "dashboard_command",
        choices=["start", "stop", "status"],
        help="Dashboard command",
    )
    parser_dashboard.add_argument(
        "--project-root",
        default=".",
        help="Root directory of project (default: current directory)",
    )
    parser_dashboard.add_argument(
        "--host",
        default="localhost",
        help="Dashboard server host (default: localhost)",
    )
    parser_dashboard.add_argument(
        "--port",
        type=int,
        default=7777,
        help="Dashboard server port (default: 7777)",
    )
    parser_dashboard.set_defaults(func=cmd_dashboard)

    # Parse arguments
    args = parser.parse_args()

    # Handle global flags
    if args.verbose:
        set_verbose(True)

    if args.no_color or os.environ.get('NO_COLOR'):
        TerminalColors.disable()

    # Quiet mode overrides verbose
    if args.quiet:
        set_verbose(False)
        # TODO: Implement quiet mode (suppress all but errors)

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    try:
        return args.func(args)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
