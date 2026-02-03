"""
Oracle Dashboard Server - Flask app with WebSocket support.

Real-time monitoring and command execution via web interface.

Architecture:
- Flask: Web server and REST API
- Flask-SocketIO: WebSocket for real-time updates
- Background thread: Polls Oracle status and broadcasts updates
- Command execution: Subprocess-based Oracle command execution

Endpoints:
- GET /: Dashboard UI (serves index.html)
- GET /api/status: Current Oracle status (REST)
- GET /api/health: Health score and metrics (REST)
- POST /api/command: Execute Oracle command (REST)
- WebSocket /: Real-time status updates

Author: Oracle Brain Cell Architecture (P31 Phase 2)
"""

import json
import logging
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from flask import Flask, jsonify, render_template, request, send_from_directory
    from flask_socketio import SocketIO, emit
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    # Define placeholder classes so module can still be imported
    Flask = None
    SocketIO = None
    CORS = None


class DashboardServer:
    """
    Web dashboard server for Oracle monitoring and control.

    Provides:
    - Real-time status monitoring via WebSocket
    - Command execution from web UI
    - Health metrics and activity tracking
    - Black terminal aesthetic
    """

    def __init__(self, project_root: Path, host: str = "localhost", port: int = 7777):
        """
        Initialize dashboard server.

        Args:
            project_root: Root directory of the project
            host: Server host (default: localhost)
            port: Server port (default: 7777)
        """
        if not FLASK_AVAILABLE:
            raise ImportError(
                "Flask dependencies not installed. "
                "Install with: pip install flask flask-socketio flask-cors python-socketio"
            )

        self.project_root = Path(project_root).resolve()
        self.host = host
        self.port = port

        # Oracle directories
        self.oracle_dir = self.project_root / "oracle"
        self.data_dir = self.oracle_dir / "data"
        self.status_file = self.data_dir / ".oracle_status.json"
        self.daemon_log = self.data_dir / ".oracle_daemon.log"

        # Flask app setup
        self.app = Flask(
            __name__,
            template_folder=str(self.oracle_dir / "web_dashboard" / "static"),
            static_folder=str(self.oracle_dir / "web_dashboard" / "static"),
        )
        self.app.config["SECRET_KEY"] = "oracle-dashboard-secret"

        # CORS for development
        CORS(self.app)

        # SocketIO setup
        self.socketio = SocketIO(
            self.app,
            cors_allowed_origins="*",
            async_mode="threading",
            logger=False,
            engineio_logger=False,
        )

        # Status tracking
        self.last_status: Optional[Dict[str, Any]] = None
        self.update_thread: Optional[threading.Thread] = None
        self.running = False

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("oracle.dashboard")

        # Register routes
        self._register_routes()
        self._register_socketio_events()

    def _register_routes(self):
        """Register Flask routes."""

        @self.app.route("/")
        def index():
            """Serve dashboard UI."""
            static_dir = self.oracle_dir / "web_dashboard" / "static"
            return send_from_directory(static_dir, "index.html")

        @self.app.route("/css/<path:filename>")
        def serve_css(filename):
            """Serve CSS files."""
            static_dir = self.oracle_dir / "web_dashboard" / "static" / "css"
            return send_from_directory(static_dir, filename)

        @self.app.route("/js/<path:filename>")
        def serve_js(filename):
            """Serve JS files."""
            static_dir = self.oracle_dir / "web_dashboard" / "static" / "js"
            return send_from_directory(static_dir, filename)

        @self.app.route("/api/status")
        def api_status():
            """Get current Oracle status."""
            try:
                status = self._get_oracle_status()
                return jsonify(status)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health")
        def api_health():
            """Get health metrics."""
            try:
                health = self._get_health_metrics()
                return jsonify(health)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/activity")
        def api_activity():
            """Get recent activity."""
            try:
                activity = self._get_recent_activity()
                return jsonify(activity)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/command", methods=["POST"])
        def api_command():
            """Execute Oracle command."""
            try:
                data = request.get_json()
                command = data.get("command", "")

                if not command:
                    return jsonify({"error": "No command provided"}), 400

                result = self._execute_command(command)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/logs")
        def api_logs():
            """Get daemon logs."""
            try:
                logs = self._get_daemon_logs(lines=50)
                return jsonify({"logs": logs})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def _register_socketio_events(self):
        """Register SocketIO events."""

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection."""
            self.logger.info("Client connected")
            # Send initial status
            status = self._get_oracle_status()
            emit("status_update", status)

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection."""
            self.logger.info("Client disconnected")

        @self.socketio.on("command")
        def handle_command(data):
            """Handle command from client."""
            command = data.get("command", "")
            self.logger.info(f"Received command: {command}")

            result = self._execute_command(command)
            emit("command_result", result)

    def _get_oracle_status(self) -> Dict[str, Any]:
        """
        Get current Oracle status.

        Returns:
            Status dictionary with daemon state, activity, etc.
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "daemon": self._get_daemon_status(),
            "health": self._get_health_metrics(),
            "activity": self._get_recent_activity(),
            "autosave": self._get_autosave_status(),
        }

        return status

    def _get_daemon_status(self) -> Dict[str, Any]:
        """Get daemon status from status file."""
        if not self.status_file.exists():
            return {
                "running": False,
                "message": "Status file not found",
            }

        try:
            with open(self.status_file) as f:
                status = json.load(f)

            return {
                "running": status.get("daemon_active", False),
                "pid": status.get("pid"),
                "uptime": status.get("uptime_seconds", 0),
                "last_update": status.get("last_update"),
                "active_context": status.get("active_context"),
            }
        except Exception as e:
            return {
                "running": False,
                "error": str(e),
            }

    def _get_health_metrics(self) -> Dict[str, Any]:
        """Get health score and metrics."""
        try:
            # Try to run quick audit
            result = subprocess.run(
                [sys.executable, str(self.oracle_dir / "project_oracle.py"), "audit", "--quick"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Parse output for health score
            health_score = 85  # Default
            for line in result.stdout.split("\n"):
                if "Health Score:" in line or "Score:" in line:
                    try:
                        score_str = line.split(":")[-1].strip().rstrip("%")
                        health_score = float(score_str)
                    except:
                        pass

            # Try to read detailed health data from status file
            health_data = {
                "score": health_score,
                "status": "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical",
                "last_check": datetime.now().isoformat(),
                "issues": {"critical": 0, "warnings": 0},
                "optimizations_pending": 0,
                "cost_today": 0.0,
            }

            # Try to read from health status file for additional metrics
            health_status_file = self.data_dir / ".oracle_health_status.json"
            if health_status_file.exists():
                try:
                    with open(health_status_file) as f:
                        status_data = json.load(f)
                        health_data["issues"] = status_data.get("issues", {"critical": 0, "warnings": 0})
                        health_data["optimizations_pending"] = status_data.get("optimizations_pending", 0)
                        health_data["cost_today"] = status_data.get("cost_today", 0.0)
                except:
                    pass

            return health_data

        except Exception as e:
            return {
                "score": 0,
                "status": "unknown",
                "error": str(e),
                "issues": {"critical": 0, "warnings": 0},
                "optimizations_pending": 0,
                "cost_today": 0.0,
            }

    def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """Get recent activity from daemon logs."""
        try:
            logs = self._get_daemon_logs(lines=10)
            activity = []

            for log in logs:
                # Parse log line for activity
                if any(keyword in log.lower() for keyword in ["file", "change", "audit", "health"]):
                    activity.append({
                        "timestamp": datetime.now().isoformat(),  # Could parse from log
                        "message": log.strip(),
                        "type": "info",
                    })

            return activity
        except:
            return []

    def _get_autosave_status(self) -> Dict[str, Any]:
        """Get autosave status from health status file."""
        health_status_file = self.data_dir / ".oracle_health_status.json"
        if health_status_file.exists():
            try:
                with open(health_status_file) as f:
                    data = json.load(f)
                    # Calculate minutes since last autosave
                    last_save = data.get("last_autosave", datetime.now().isoformat())
                    last_save_dt = datetime.fromisoformat(last_save)
                    age_minutes = int((datetime.now() - last_save_dt).total_seconds() / 60)

                    return {
                        "last_minutes": age_minutes,
                        "status": "ok" if age_minutes < 20 else "overdue"
                    }
            except:
                pass

        return {"last_minutes": 0, "status": "unknown"}

    def _get_daemon_logs(self, lines: int = 50) -> List[str]:
        """Get daemon log lines."""
        if not self.daemon_log.exists():
            return []

        try:
            with open(self.daemon_log) as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except:
            return []

    def _execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute Oracle command.

        Args:
            command: Command string (e.g., "audit --quick")

        Returns:
            Result dictionary with output, status, etc.
        """
        try:
            # Parse command
            parts = command.strip().split()
            if not parts:
                return {"success": False, "error": "Empty command"}

            # Build command
            cmd = [sys.executable, str(self.oracle_dir / "project_oracle.py")] + parts

            # Execute
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "exit_code": result.returncode,
                "command": command,
                "timestamp": datetime.now().isoformat(),
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timeout (>30s)",
                "command": command,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
            }

    def _background_update_loop(self):
        """Background thread that polls status and broadcasts updates."""
        self.logger.info("Starting background update loop")

        while self.running:
            try:
                # Get current status
                status = self._get_oracle_status()

                # Broadcast if changed
                if status != self.last_status:
                    self.socketio.emit("status_update", status)
                    self.last_status = status

                # Sleep 2 seconds between updates
                time.sleep(2)

            except Exception as e:
                self.logger.error(f"Update loop error: {e}")
                time.sleep(5)

        self.logger.info("Background update loop stopped")

    def start(self, background: bool = False):
        """
        Start dashboard server.

        Args:
            background: If True, run in background (non-blocking)
        """
        self.running = True

        # Start background update thread
        self.update_thread = threading.Thread(
            target=self._background_update_loop,
            daemon=True,
        )
        self.update_thread.start()

        # Print startup info
        print(f"\n{'=' * 60}")
        print("🧠 Oracle Dashboard Server")
        print(f"{'=' * 60}")
        print(f"📡 Starting on http://{self.host}:{self.port}")
        print(f"📁 Project: {self.project_root}")
        print(f"{'=' * 60}\n")

        # Start Flask server
        try:
            self.socketio.run(
                self.app,
                host=self.host,
                port=self.port,
                debug=False,
                use_reloader=False,
                log_output=False,
                allow_unsafe_werkzeug=True,  # For development
            )
        except KeyboardInterrupt:
            print("\n\n⚠️  Server stopped by user")
            self.stop()
        except Exception as e:
            print(f"\n❌ Server error: {e}")
            self.stop()

    def stop(self):
        """Stop dashboard server."""
        self.running = False

        if self.update_thread:
            self.update_thread.join(timeout=2)

        print("✅ Dashboard server stopped")


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Oracle Dashboard Server")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=7777, help="Server port")

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    server = DashboardServer(project_root, host=args.host, port=args.port)
    server.start()


if __name__ == "__main__":
    main()
