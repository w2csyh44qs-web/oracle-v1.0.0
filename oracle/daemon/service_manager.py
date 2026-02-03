"""
Service Manager - System service integration for Oracle daemon.

Handles platform-specific service installation:
- macOS: launchd (.plist files in ~/Library/LaunchAgents/)
- Linux: systemd (.service files in ~/.config/systemd/user/)

Usage:
    manager = ServiceManager(project_root)
    manager.install()  # Creates service file and enables
    manager.uninstall()  # Removes service file

Author: Oracle Brain Cell Architecture (P31)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Optional


class ServiceManager:
    """
    Cross-platform service manager for Oracle daemon.

    Supports:
    - macOS (launchd)
    - Linux (systemd)
    """

    def __init__(self, project_root: Path):
        """
        Initialize service manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root).resolve()
        self.platform = platform.system()

        # Service identifiers
        self.service_id = "com.oracle.daemon"
        self.service_name = "oracle-daemon"

        # Python executable
        self.python_exe = sys.executable

        # Daemon script path
        self.daemon_script = self.project_root / "oracle" / "daemon" / "oracle_daemon.py"

        # Log paths
        self.log_dir = self.project_root / "oracle" / "data"
        self.stdout_log = self.log_dir / ".oracle_daemon.log"
        self.stderr_log = self.log_dir / ".oracle_daemon.err"

    def _generate_launchd_plist(self) -> str:
        """
        Generate launchd plist configuration for macOS.

        Returns:
            Plist XML content
        """
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{self.service_id}</string>

    <key>ProgramArguments</key>
    <array>
        <string>{self.python_exe}</string>
        <string>{self.daemon_script}</string>
        <string>start</string>
        <string>--project-root</string>
        <string>{self.project_root}</string>
        <string>--foreground</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <dict>
        <key>Crashed</key>
        <true/>
    </dict>

    <key>StandardOutPath</key>
    <string>{self.stdout_log}</string>

    <key>StandardErrorPath</key>
    <string>{self.stderr_log}</string>

    <key>WorkingDirectory</key>
    <string>{self.project_root}</string>

    <key>ProcessType</key>
    <string>Background</string>

    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
"""

    def _generate_systemd_service(self) -> str:
        """
        Generate systemd service configuration for Linux.

        Returns:
            Service file content
        """
        return f"""[Unit]
Description=Oracle Project Intelligence Daemon
After=network.target

[Service]
Type=simple
ExecStart={self.python_exe} {self.daemon_script} start --project-root {self.project_root} --foreground
Restart=on-failure
RestartSec=10s
StandardOutput=append:{self.stdout_log}
StandardError=append:{self.stderr_log}
WorkingDirectory={self.project_root}

[Install]
WantedBy=default.target
"""

    def _get_launchd_plist_path(self) -> Path:
        """
        Get path to launchd plist file.

        Returns:
            Path to plist file
        """
        home = Path.home()
        launch_agents = home / "Library" / "LaunchAgents"
        launch_agents.mkdir(parents=True, exist_ok=True)
        return launch_agents / f"{self.service_id}.plist"

    def _get_systemd_service_path(self) -> Path:
        """
        Get path to systemd service file.

        Returns:
            Path to service file
        """
        home = Path.home()
        systemd_user = home / ".config" / "systemd" / "user"
        systemd_user.mkdir(parents=True, exist_ok=True)
        return systemd_user / f"{self.service_name}.service"

    def install(self) -> bool:
        """
        Install system service.

        Returns:
            True if successful, False otherwise
        """
        if self.platform == "Darwin":  # macOS
            return self._install_launchd()
        elif self.platform == "Linux":
            return self._install_systemd()
        else:
            print(f"❌ Unsupported platform: {self.platform}")
            print("💡 Supported platforms: macOS (Darwin), Linux")
            return False

    def _install_launchd(self) -> bool:
        """
        Install launchd service on macOS.

        Returns:
            True if successful, False otherwise
        """
        try:
            plist_path = self._get_launchd_plist_path()

            # Generate and write plist
            plist_content = self._generate_launchd_plist()
            plist_path.write_text(plist_content)

            print(f"✅ Created launchd plist: {plist_path}")

            # Load service
            result = subprocess.run(
                ["launchctl", "load", str(plist_path)],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ Loaded service: {self.service_id}")
                print(f"   Service will start automatically on boot")
                return True
            else:
                print(f"⚠️  Service file created but not loaded")
                print(f"   Error: {result.stderr}")
                print(f"💡 Try manually: launchctl load {plist_path}")
                return False

        except Exception as e:
            print(f"❌ Failed to install launchd service: {e}")
            return False

    def _install_systemd(self) -> bool:
        """
        Install systemd service on Linux.

        Returns:
            True if successful, False otherwise
        """
        try:
            service_path = self._get_systemd_service_path()

            # Generate and write service file
            service_content = self._generate_systemd_service()
            service_path.write_text(service_content)

            print(f"✅ Created systemd service: {service_path}")

            # Reload systemd
            result = subprocess.run(
                ["systemctl", "--user", "daemon-reload"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"⚠️  Failed to reload systemd: {result.stderr}")

            print(f"💡 To enable auto-start on boot:")
            print(f"   systemctl --user enable {self.service_name}")
            print(f"💡 To start now:")
            print(f"   systemctl --user start {self.service_name}")

            return True

        except Exception as e:
            print(f"❌ Failed to install systemd service: {e}")
            return False

    def uninstall(self) -> bool:
        """
        Uninstall system service.

        Returns:
            True if successful, False otherwise
        """
        if self.platform == "Darwin":  # macOS
            return self._uninstall_launchd()
        elif self.platform == "Linux":
            return self._uninstall_systemd()
        else:
            print(f"❌ Unsupported platform: {self.platform}")
            return False

    def _uninstall_launchd(self) -> bool:
        """
        Uninstall launchd service on macOS.

        Returns:
            True if successful, False otherwise
        """
        try:
            plist_path = self._get_launchd_plist_path()

            if not plist_path.exists():
                print(f"⚠️  Service not installed (plist not found)")
                return True

            # Unload service
            result = subprocess.run(
                ["launchctl", "unload", str(plist_path)],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"⚠️  Failed to unload service: {result.stderr}")

            # Remove plist
            plist_path.unlink()
            print(f"✅ Removed launchd service: {plist_path}")

            return True

        except Exception as e:
            print(f"❌ Failed to uninstall launchd service: {e}")
            return False

    def _uninstall_systemd(self) -> bool:
        """
        Uninstall systemd service on Linux.

        Returns:
            True if successful, False otherwise
        """
        try:
            service_path = self._get_systemd_service_path()

            if not service_path.exists():
                print(f"⚠️  Service not installed (service file not found)")
                return True

            # Stop service
            subprocess.run(
                ["systemctl", "--user", "stop", self.service_name],
                capture_output=True
            )

            # Disable service
            subprocess.run(
                ["systemctl", "--user", "disable", self.service_name],
                capture_output=True
            )

            # Remove service file
            service_path.unlink()
            print(f"✅ Removed systemd service: {service_path}")

            # Reload systemd
            subprocess.run(
                ["systemctl", "--user", "daemon-reload"],
                capture_output=True
            )

            return True

        except Exception as e:
            print(f"❌ Failed to uninstall systemd service: {e}")
            return False

    def enable(self) -> bool:
        """
        Enable service (auto-start on boot).

        Returns:
            True if successful, False otherwise
        """
        if self.platform == "Darwin":
            # launchd services are auto-enabled when loaded
            print(f"✅ launchd service is already enabled")
            return True
        elif self.platform == "Linux":
            try:
                result = subprocess.run(
                    ["systemctl", "--user", "enable", self.service_name],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ Enabled {self.service_name} (will start on boot)")
                    return True
                else:
                    print(f"❌ Failed to enable service: {result.stderr}")
                    return False

            except Exception as e:
                print(f"❌ Failed to enable service: {e}")
                return False
        else:
            print(f"❌ Unsupported platform: {self.platform}")
            return False

    def disable(self) -> bool:
        """
        Disable service (don't auto-start on boot).

        Returns:
            True if successful, False otherwise
        """
        if self.platform == "Darwin":
            # Unload plist to disable
            plist_path = self._get_launchd_plist_path()
            if plist_path.exists():
                try:
                    subprocess.run(
                        ["launchctl", "unload", str(plist_path)],
                        capture_output=True
                    )
                    print(f"✅ Disabled {self.service_id}")
                    return True
                except Exception as e:
                    print(f"❌ Failed to disable service: {e}")
                    return False
            else:
                print(f"⚠️  Service not installed")
                return True

        elif self.platform == "Linux":
            try:
                result = subprocess.run(
                    ["systemctl", "--user", "disable", self.service_name],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ Disabled {self.service_name}")
                    return True
                else:
                    print(f"❌ Failed to disable service: {result.stderr}")
                    return False

            except Exception as e:
                print(f"❌ Failed to disable service: {e}")
                return False
        else:
            print(f"❌ Unsupported platform: {self.platform}")
            return False


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Oracle Service Manager")
    parser.add_argument('command', choices=['install', 'uninstall', 'enable', 'disable'],
                        help='Service management command')
    parser.add_argument('--project-root', default='.',
                        help='Project root directory')

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    manager = ServiceManager(project_root)

    if args.command == 'install':
        manager.install()
    elif args.command == 'uninstall':
        manager.uninstall()
    elif args.command == 'enable':
        manager.enable()
    elif args.command == 'disable':
        manager.disable()


if __name__ == "__main__":
    main()
