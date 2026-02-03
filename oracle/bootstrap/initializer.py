"""
Oracle Bootstrap - Project Initializer

Implements the `oracle init` command to bootstrap Oracle on any Python project.

Workflow:
1. Detect project structure (framework, dirs, layers, tools)
2. Validate environment (Python 3.9+, permissions)
3. Generate configs (oracle_config.json, layer_registry.json)
4. Scaffold directories (oracle/config/, oracle/docs/)
5. Generate context files from templates
6. Validate installation (paths, imports, CLI)
7. Install git hooks (pre-commit integration)
8. Report success with next steps

Usage:
    from oracle.bootstrap.initializer import OracleInitializer

    initializer = OracleInitializer('/path/to/project')
    success = initializer.init()

Author: Oracle Brain Cell Architecture (P30 Phase 4)
"""

import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from oracle.bootstrap.detector import ProjectDetector, ProjectProfile
from oracle.bootstrap.terminal import (
    print_header,
    print_step,
    print_success,
    print_warning,
    print_info,
    print_verbose,
    format_time,
    TerminalColors,
)


class InitializationError(Exception):
    """Raised when initialization fails."""

    def __init__(self, message: str, recovery_hint: Optional[str] = None):
        """
        Initialize error with message and optional recovery hint.

        Args:
            message: Error description
            recovery_hint: Optional suggestion for fixing the issue
        """
        self.message = message
        self.recovery_hint = recovery_hint
        super().__init__(self.format_message())

    def format_message(self) -> str:
        """Format error with recovery hint if available."""
        msg = f"❌ {self.message}"
        if self.recovery_hint:
            msg += f"\n💡 Recovery: {self.recovery_hint}"
        return msg


class OracleInitializer:
    """
    Oracle initialization system.

    Bootstraps Oracle onto any Python project by detecting structure,
    generating configs, and scaffolding necessary directories.
    """

    def __init__(self, project_root: Path):
        """
        Initialize the initializer.

        Args:
            project_root: Root directory of project to bootstrap
        """
        self.project_root = Path(project_root).resolve()
        self.oracle_dir = self.project_root / "oracle"
        self.profile: Optional[ProjectProfile] = None

    def init(self, dry_run: bool = False) -> bool:
        """
        Bootstrap Oracle on the project.

        Args:
            dry_run: If True, preview changes without applying

        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()

        print_header("🚀 Oracle Bootstrap System")
        print_info(f"Project: {self.project_root}")
        if dry_run:
            print_warning("DRY RUN MODE - No changes will be made")
        print()

        try:
            # Step 1: Validate environment
            print_step("Validating environment", step=1, total=8, emoji="🔍")
            step_start = time.time()
            self._validate_environment()
            print_success("Environment valid", indent=3)
            print_verbose(f"Validation took {format_time(time.time() - step_start)}")

            # Step 2: Detect project structure
            print_step("Detecting project structure", step=2, total=8, emoji="🔬")
            step_start = time.time()
            detector = ProjectDetector(self.project_root)
            self.profile = detector.analyze()
            print_verbose(f"Detection took {format_time(time.time() - step_start)}")

            # Step 3: Check if Oracle already exists
            if self.oracle_dir.exists() and not dry_run:
                print()
                print_warning("Oracle directory already exists")
                response = input(f"   {TerminalColors.YELLOW}Overwrite? [y/N]:{TerminalColors.RESET} ")
                if response.lower() != "y":
                    print()
                    print_warning("Initialization cancelled by user")
                    return False
                print()

            # Step 4: Generate configs
            print_step("Generating configuration files", step=3, total=8, emoji="⚙️")
            step_start = time.time()
            if not dry_run:
                self._generate_configs()
                print_success("oracle_config.json created", indent=3)
                if self.profile.has_layers:
                    print_success("layer_registry.json created", indent=3)
                print_success("tool_registry.json created", indent=3)
            else:
                print_info("Would create oracle_config.json")
                if self.profile.has_layers:
                    print_info("Would create layer_registry.json")
                print_info("Would create tool_registry.json")
            print_verbose(f"Config generation took {format_time(time.time() - step_start)}")

            # Step 5: Scaffold directories
            print_step("Scaffolding directories", step=4, total=8, emoji="📁")
            step_start = time.time()
            if not dry_run:
                self._scaffold_directories()
                dirs = ["config/", "docs/context/", "docs/plans/", "data/memory/", "reports/"]
                for d in dirs:
                    print_success(f"oracle/{d}", indent=3)
            else:
                print_info("Would create oracle/ directory structure")
            print_verbose(f"Directory scaffolding took {format_time(time.time() - step_start)}")

            # Step 6: Generate context files
            print_step("Generating context files", step=5, total=8, emoji="📝")
            step_start = time.time()
            if not dry_run:
                self._generate_context_files()
                print_success(f"{self.profile.project_name.upper()}_CONTEXT.md", indent=3)
                if self.profile.has_layers:
                    print_success("DEV_CONTEXT.md (layer-aware)", indent=3)
            else:
                print_info("Would create PROJECT_CONTEXT.md")
                if self.profile.has_layers:
                    print_info("Would create DEV_CONTEXT.md")
            print_verbose(f"Context generation took {format_time(time.time() - step_start)}")

            # Step 7: Validate installation
            print_step("Validating installation", step=6, total=8, emoji="✅")
            step_start = time.time()
            if not dry_run:
                self._validate_installation()
                print_success("All files created successfully", indent=3)
                print_success("Configuration is valid", indent=3)
                print_success("Directory structure is correct", indent=3)
            else:
                print_info("Would validate installation")
            print_verbose(f"Validation took {format_time(time.time() - step_start)}")

            # Step 8: Install git hooks
            print_step("Installing git hooks", step=7, total=8, emoji="🪝")
            step_start = time.time()
            if not dry_run:
                try:
                    from oracle.validation.topoisomerase import HookManager
                    hook_mgr = HookManager(self.project_root)
                    if hook_mgr.install_hooks():
                        print_success("Pre-commit hooks installed", indent=3)
                        print_info("Hooks will run on: git commit", indent=3)
                        print_verbose(f"Hook installation took {format_time(time.time() - step_start)}")
                    else:
                        print_warning("Could not install git hooks", indent=3)
                        print_info("Run manually: oracle verify --install-hooks", indent=3)
                except ImportError:
                    print_warning("HookManager not available", indent=3)
                    print_info("Git hooks can be installed manually later", indent=3)
                except Exception as e:
                    print_warning(f"Hook installation failed: {e}", indent=3)
                    print_info("This won't affect Oracle functionality", indent=3)
            else:
                print_info("Would install git pre-commit hooks", indent=3)
                print_info("Would create .pre-commit-config.yaml", indent=3)
            print_verbose(f"Hook setup took {format_time(time.time() - step_start)}")

            # Success summary
            total_time = time.time() - start_time
            print(f"\n{'=' * 60}")
            if dry_run:
                print_success(f"Dry run complete in {format_time(total_time)}")
                print_info("No changes were made")
            else:
                print_success(f"✨ Oracle initialized successfully in {format_time(total_time)}")
            print(f"{'=' * 60}\n")

            if not dry_run:
                self._print_next_steps()

            return True

        except InitializationError as e:
            print(f"\n{e}")
            print("\n📋 For more information, see:")
            print("   - Oracle documentation: oracle/docs/")
            print("   - GitHub issues: https://github.com/anthropics/oracle/issues")
            return False
        except KeyboardInterrupt:
            print("\n\n⚠️  Initialization cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("\n💡 This may be a bug. Please report it with:")
            print(f"   - Error message: {e}")
            print(f"   - Project path: {self.project_root}")
            print(f"   - Python version: {sys.version_info.major}.{sys.version_info.minor}")
            print("\n📋 Full traceback:")
            import traceback
            traceback.print_exc()
            return False

    def _validate_environment(self) -> None:
        """Validate Python version, permissions, and project structure."""
        # Check Python version
        if sys.version_info < (3, 9):
            raise InitializationError(
                f"Python 3.9+ required (found {sys.version_info.major}.{sys.version_info.minor})",
                recovery_hint="Upgrade Python using pyenv, conda, or your system package manager"
            )

        # Check project root exists
        if not self.project_root.exists():
            raise InitializationError(
                f"Project root does not exist: {self.project_root}",
                recovery_hint="Verify the path is correct and the directory exists"
            )

        # Check if project has any Python files
        py_files = list(self.project_root.rglob("*.py"))
        if not py_files:
            raise InitializationError(
                "No Python files found in project",
                recovery_hint="Oracle is designed for Python projects. Verify you're in the correct directory."
            )

        # Test write access
        test_file = self.project_root / ".oracle_write_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
        except PermissionError:
            raise InitializationError(
                "No write permission in project root",
                recovery_hint="Run with appropriate permissions or change directory ownership"
            )
        except Exception as e:
            raise InitializationError(
                f"Cannot write to project root: {e}",
                recovery_hint="Check filesystem permissions and available disk space"
            )

    def _generate_configs(self) -> None:
        """Generate oracle_config.json and layer_registry.json."""
        if not self.profile:
            raise InitializationError("Project profile not detected")

        # Create config directory
        config_dir = self.oracle_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        # Generate oracle_config.json
        oracle_config = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "project": {
                "name": self.profile.project_name,
                "framework": self.profile.framework,
                "python_version": self.profile.python_version,
            },
            "paths": {
                "code_dirs": self.profile.code_dirs,
                "layer_location": self.profile.layer_location,
                "preset_location": self.profile.preset_location,
            },
            "structure": {
                "has_layers": self.profile.has_layers,
                "has_presets": self.profile.has_presets,
            },
            "tools": [tool["name"] for tool in self.profile.detected_tools],
            "config_files": self.profile.config_files,
            "metrics": {
                "file_count": self.profile.file_count,
                "line_count": self.profile.line_count,
                "test_framework": self.profile.test_framework,
            },
        }

        config_path = config_dir / "oracle_config.json"
        with open(config_path, "w") as f:
            json.dump(oracle_config, f, indent=2)

        print(f"   📄 Created: {config_path.relative_to(self.project_root)}")

        # Generate layer_registry.json if project has layers
        if self.profile.has_layers and self.profile.layer_location:
            self._generate_layer_registry(config_dir)

        # Generate tool_registry.json
        self._generate_tool_registry(config_dir)

    def _generate_layer_registry(self, config_dir: Path) -> None:
        """Generate layer_registry.json from detected layers."""
        if not self.profile or not self.profile.layer_location:
            return

        layer_base = self.project_root / self.profile.layer_location
        layers = {}

        # Scan for layer directories
        if layer_base.exists():
            for layer_dir in sorted(layer_base.iterdir()):
                if layer_dir.is_dir() and layer_dir.name.startswith("_L"):
                    # Extract layer number (e.g., _L1 -> L1)
                    layer_id = layer_dir.name.lstrip("_")

                    # Get layer name from directory or file
                    layer_name = layer_id
                    layer_file = layer_dir / f"{layer_id}_*.py"
                    layer_files = list(layer_dir.glob(f"{layer_id}_*.py"))
                    if layer_files:
                        # Extract name from filename (e.g., L1_data.py -> Data Ingestion)
                        filename = layer_files[0].stem.replace(f"{layer_id}_", "")
                        layer_name = filename.replace("_", " ").title()

                    layers[layer_id] = {
                        "name": layer_name,
                        "path": str(layer_dir.relative_to(self.project_root)) + "/",
                        "tools": [],  # Could be enhanced with tool detection per layer
                    }

        layer_registry = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "layers": layers,
        }

        registry_path = config_dir / "layer_registry.json"
        with open(registry_path, "w") as f:
            json.dump(layer_registry, f, indent=2)

        print(f"   📄 Created: {registry_path.relative_to(self.project_root)}")

    def _generate_tool_registry(self, config_dir: Path) -> None:
        """Generate tool_registry.json from detected tools."""
        if not self.profile:
            return

        tools = {}
        for tool in self.profile.detected_tools:
            tools[tool["name"]] = {
                "type": tool["type"],
                "detected_in": tool["first_seen"],
                "enabled": True,
            }

        tool_registry = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "tools": tools,
        }

        registry_path = config_dir / "tool_registry.json"
        with open(registry_path, "w") as f:
            json.dump(tool_registry, f, indent=2)

        print(f"   📄 Created: {registry_path.relative_to(self.project_root)}")

    def _scaffold_directories(self) -> None:
        """Create Oracle directory structure."""
        directories = [
            self.oracle_dir / "config",
            self.oracle_dir / "docs" / "context",
            self.oracle_dir / "docs" / "plans",
            self.oracle_dir / "data" / "memory",
            self.oracle_dir / "reports",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"   📁 Created: {directory.relative_to(self.project_root)}")

    def _generate_context_files(self) -> None:
        """Generate context files from templates."""
        context_dir = self.oracle_dir / "docs" / "context"

        # Generate main context file
        main_context = self._generate_main_context()
        main_path = context_dir / f"{self.profile.project_name.upper()}_CONTEXT.md"
        with open(main_path, "w") as f:
            f.write(main_context)
        print(f"   📄 Created: {main_path.relative_to(self.project_root)}")

        # Generate dev context if applicable
        if self.profile.has_layers:
            dev_context = self._generate_dev_context()
            dev_path = context_dir / "DEV_CONTEXT.md"
            with open(dev_path, "w") as f:
                f.write(dev_context)
            print(f"   📄 Created: {dev_path.relative_to(self.project_root)}")

    def _generate_main_context(self) -> str:
        """Generate main context file content."""
        if not self.profile:
            return ""

        content = f"""# {self.profile.project_name} - Oracle Context

**Generated:** {datetime.now().strftime("%B %d, %Y")}
**Framework:** {self.profile.framework}
**Status:** Initialized

---

## PROJECT OVERVIEW

**Name:** {self.profile.project_name}
**Framework:** {self.profile.framework}
**Python:** {self.profile.python_version}

**Structure:**
- Code directories: {", ".join(self.profile.code_dirs)}
- Has layers: {"Yes" if self.profile.has_layers else "No"}
- Has presets: {"Yes" if self.profile.has_presets else "No"}

**Metrics:**
- Files: {self.profile.file_count:,}
- Lines: {self.profile.line_count:,}
- Test framework: {self.profile.test_framework or "None detected"}

---

## DETECTED TOOLS

"""
        if self.profile.detected_tools:
            for tool in self.profile.detected_tools[:10]:  # Top 10
                content += f"- **{tool['name']}** ({tool['type']})\n"
        else:
            content += "No tools detected.\n"

        content += """
---

## LAYER STRUCTURE

"""
        if self.profile.has_layers:
            content += f"Project uses layer-based architecture.\n\n"
            content += f"**Location:** `{self.profile.layer_location}`\n\n"
            content += "See `oracle/config/layer_registry.json` for layer definitions.\n"
        else:
            content += "No layer structure detected.\n"

        content += """
---

## RECENT CHANGES

_(Oracle will automatically update this section based on session observations)_

---

## PENDING TASKS

- [ ] Review generated Oracle configs
- [ ] Customize context files for your project
- [ ] Run first Oracle session: `python oracle/project_oracle.py status`

---

## NOTES

This context file was automatically generated by Oracle Bootstrap.
You can customize it to match your project's specific needs.

**Next Steps:**
1. Review `oracle/config/oracle_config.json`
2. Customize this context file
3. Run `python oracle/project_oracle.py status`
4. Start your first Oracle session

For more information, see the Oracle documentation.
"""
        return content

    def _generate_dev_context(self) -> str:
        """Generate development context file."""
        if not self.profile:
            return ""

        content = f"""# {self.profile.project_name} - Development Context

**Generated:** {datetime.now().strftime("%B %d, %Y")}
**Focus:** Development workflows and layer architecture

---

## CURRENT FOCUS

Development environment initialized. Ready for Oracle sessions.

---

## LAYER WORKFLOW

"""
        if self.profile.has_layers and self.profile.layer_location:
            content += f"**Location:** `{self.profile.layer_location}`\n\n"
            content += "Oracle will track layer-specific changes and patterns.\n"
        else:
            content += "No layer workflow detected.\n"

        content += """
---

## ACTIVE FILES

_(Oracle will automatically track frequently modified files)_

---

## DECISIONS

_(Oracle will capture architectural decisions during sessions)_

---

## NOTES

This development context is automatically maintained by Oracle's memory system.
"""
        return content

    def _validate_installation(self) -> None:
        """Validate that Oracle was installed correctly."""
        errors = []

        # Check config files exist
        config_file = self.oracle_dir / "config" / "oracle_config.json"
        if not config_file.exists():
            errors.append("oracle_config.json not created")

        # Verify config is valid JSON
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                    # Validate required keys
                    required_keys = ["version", "project", "paths", "structure"]
                    missing_keys = [k for k in required_keys if k not in config]
                    if missing_keys:
                        errors.append(f"Config missing required keys: {', '.join(missing_keys)}")
            except json.JSONDecodeError as e:
                errors.append(f"Invalid oracle_config.json: {e}")

        # Check context directory exists
        context_dir = self.oracle_dir / "docs" / "context"
        if not context_dir.exists():
            errors.append("Context directory not created")

        # Check at least one context file exists
        if context_dir.exists():
            context_files = list(context_dir.glob("*.md"))
            if not context_files:
                errors.append("No context files created")

        # Check memory directory exists
        memory_dir = self.oracle_dir / "data" / "memory"
        if not memory_dir.exists():
            errors.append("Memory directory not created")

        if errors:
            error_list = "\n  • ".join(errors)
            raise InitializationError(
                f"Installation validation failed:\n  • {error_list}",
                recovery_hint="Try running 'oracle init' again or check write permissions"
            )

    def _print_next_steps(self) -> None:
        """Print next steps for the user."""
        print("📋 Next Steps:")
        print()
        print(f"1. Review configs:")
        print(f"   cat oracle/config/oracle_config.json")
        print()
        print(f"2. Customize contexts:")
        print(f"   cat oracle/docs/context/{self.profile.project_name.upper()}_CONTEXT.md")
        print()
        print(f"3. Run Oracle status:")
        print(f"   python oracle/project_oracle.py status")
        print()
        print(f"4. Start your first session:")
        print(f"   python oracle/project_oracle.py audit --quick")
        print()
        print("🎉 Oracle is ready to use!")


def main():
    """CLI interface for Oracle initialization."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python initializer.py <project_root> [--dry-run]")
        print()
        print("Examples:")
        print("  python initializer.py /path/to/project")
        print("  python initializer.py /path/to/project --dry-run")
        return

    project_root = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    initializer = OracleInitializer(project_root)
    success = initializer.init(dry_run=dry_run)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
