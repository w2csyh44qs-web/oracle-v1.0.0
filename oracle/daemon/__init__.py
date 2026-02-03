"""
Oracle Daemon - Production daemon service with auto-start.

Wraps the existing context/daemon.py with system service integration,
PID management, logging, and scheduled health checks.

Usage:
    from oracle.daemon import OracleDaemonService

    service = OracleDaemonService(project_root)
    service.start(background=True)

Author: Oracle Brain Cell Architecture (P31 Final Enhancements)
"""

from oracle.daemon.oracle_daemon import OracleDaemonService
from oracle.daemon.service_manager import ServiceManager

__all__ = [
    "OracleDaemonService",
    "ServiceManager",
]

__version__ = "1.0.0"
