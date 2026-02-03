"""
Oracle Dashboard - Web-based monitoring and control interface.

Provides real-time monitoring and command execution via web interface:
- Split view: Monitoring panel (left) + Terminal panel (right)
- Black terminal aesthetic (matches seeg/venv experience)
- Real-time updates via WebSocket
- Command execution from web UI
- Mobile-responsive design

Usage:
    from oracle.web_dashboard import DashboardServer

    server = DashboardServer(project_root)
    server.start(port=7777)

Author: Oracle Brain Cell Architecture (P31 Phase 2)
"""

try:
    from oracle.web_dashboard.server.app import DashboardServer
    __all__ = ["DashboardServer"]
except ImportError:
    # Flask dependencies not installed
    DashboardServer = None
    __all__ = []

__version__ = "1.0.0"
