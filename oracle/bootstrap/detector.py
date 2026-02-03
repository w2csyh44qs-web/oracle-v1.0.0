"""
Oracle Bootstrap - Project Structure Detection

Project-agnostic detection system that analyzes Python projects to determine:
- Framework (Flask, Django, FastAPI, etc.)
- Directory structure
- Layer patterns
- Tool/API configurations

Usage:
    from oracle.bootstrap.detector import ProjectDetector

    detector = ProjectDetector('/path/to/project')
    profile = detector.analyze()

    print(f"Framework: {profile.framework}")
    print(f"Has layers: {profile.has_layers}")
    print(f"Code dirs: {profile.code_dirs}")

Author: Oracle Brain Cell Architecture (P30 Phase 4)
"""

import ast
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from oracle.bootstrap.terminal import (
    print_header,
    print_step,
    print_success,
    print_info,
    print_metric,
    print_verbose,
    is_verbose,
    format_time,
)


@dataclass
class ProjectProfile:
    """Profile of detected project structure."""

    # Basic info
    project_root: Path
    project_name: str
    framework: str = "Unknown"
    python_version: str = "3.9+"

    # Structure
    code_dirs: List[str] = field(default_factory=list)
    has_layers: bool = False
    layer_location: Optional[str] = None
    has_presets: bool = False
    preset_location: Optional[str] = None

    # Tools and APIs
    detected_tools: List[Dict[str, str]] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)

    # Metrics
    file_count: int = 0
    line_count: int = 0
    test_framework: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "project_root": str(self.project_root),
            "project_name": self.project_name,
            "framework": self.framework,
            "python_version": self.python_version,
            "code_dirs": self.code_dirs,
            "has_layers": self.has_layers,
            "layer_location": self.layer_location,
            "has_presets": self.has_presets,
            "preset_location": self.preset_location,
            "detected_tools": self.detected_tools,
            "config_files": self.config_files,
            "file_count": self.file_count,
            "line_count": self.line_count,
            "test_framework": self.test_framework,
        }


class ProjectDetector:
    """
    Project-agnostic structure detection.

    Analyzes Python projects to determine framework, structure, and tools.
    Used by oracle init to bootstrap Oracle on any project.
    """

    # Directories to skip (performance optimization)
    SKIP_DIRS = {
        ".git", ".svn", ".hg",  # Version control
        "node_modules", "bower_components",  # JS dependencies
        "venv", "env", ".venv", ".env",  # Virtual environments
        "__pycache__", ".pytest_cache", ".mypy_cache",  # Python cache
        ".tox", ".nox",  # Testing
        "build", "dist", "*.egg-info",  # Build artifacts
        ".idea", ".vscode",  # IDEs
        "htmlcov", "coverage",  # Coverage reports
    }

    # Maximum directory depth to scan (performance)
    MAX_DEPTH = 8

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        "Flask": ["from flask import", "Flask(__name__)"],
        "Django": ["from django", "django.conf", "INSTALLED_APPS"],
        "FastAPI": ["from fastapi import", "FastAPI("],
        "Streamlit": ["import streamlit", "st."],
        "Gradio": ["import gradio", "gr.Interface"],
        "Tornado": ["import tornado", "tornado.web"],
        "Pyramid": ["from pyramid", "pyramid.config"],
        "Bottle": ["from bottle import", "Bottle("],
        "CherryPy": ["import cherrypy", "cherrypy.quickstart"],
        "Sanic": ["from sanic import", "Sanic("],
        "Quart": ["from quart import", "Quart("],
        "Starlette": ["from starlette", "Starlette("],
        "Dash": ["import dash", "dash.Dash"],
        "Falcon": ["import falcon", "falcon.API"],
        "Hug": ["import hug", "@hug."],
        "Web2py": ["from gluon", "web2py"],
    }

    # Common directory patterns
    COMMON_CODE_DIRS = [
        "app", "src", "lib", "core", "api", "backend", "frontend",
        "services", "modules", "package", "scripts"
    ]

    # Layer detection patterns
    LAYER_PATTERNS = [
        r"_L\d+",  # _L1, _L2, etc.
        r"layer_?\d+",  # layer1, layer_1
        r"layers?/\w+",  # layers/ingestion
    ]

    # Tool detection patterns (API imports)
    TOOL_PATTERNS = {
        # AI/ML APIs
        "openai": ["import openai", "from openai import"],
        "anthropic": ["import anthropic", "from anthropic import"],
        "cohere": ["import cohere", "from cohere import"],
        "huggingface": ["from transformers import", "from huggingface_hub"],
        "langchain": ["from langchain import", "import langchain"],

        # HTTP clients
        "requests": ["import requests", "from requests import"],
        "httpx": ["import httpx", "from httpx import"],
        "aiohttp": ["import aiohttp", "from aiohttp import"],
        "urllib3": ["import urllib3", "from urllib3 import"],

        # Web scraping
        "selenium": ["from selenium import", "webdriver."],
        "beautifulsoup": ["from bs4 import", "BeautifulSoup"],
        "scrapy": ["import scrapy", "from scrapy import"],
        "playwright": ["from playwright import", "playwright."],

        # Data processing
        "pandas": ["import pandas", "pd.DataFrame"],
        "numpy": ["import numpy", "np.array"],
        "polars": ["import polars", "pl.DataFrame"],
        "dask": ["import dask", "from dask import"],

        # Databases
        "sqlalchemy": ["from sqlalchemy import", "create_engine"],
        "psycopg2": ["import psycopg2", "from psycopg2 import"],
        "pymongo": ["import pymongo", "from pymongo import"],
        "redis": ["import redis", "Redis("],

        # Task queues
        "celery": ["from celery import", "Celery("],
        "rq": ["from rq import", "Queue("],

        # Testing
        "pytest": ["import pytest", "from pytest import"],
        "unittest": ["import unittest", "from unittest import"],

        # Async/IO
        "asyncio": ["import asyncio", "from asyncio import"],
        "trio": ["import trio", "from trio import"],

        # Cloud providers
        "boto3": ["import boto3", "from boto3 import"],  # AWS
        "google-cloud": ["from google.cloud import", "import google.cloud"],
        "azure": ["from azure import", "import azure"],
    }

    def __init__(self, project_root: Path):
        """
        Initialize detector.

        Args:
            project_root: Root directory of project to analyze
        """
        self.project_root = Path(project_root).resolve()
        self.profile = ProjectProfile(
            project_root=self.project_root,
            project_name=self.project_root.name
        )
        self._file_cache: Dict[str, str] = {}  # Cache file contents

    def _should_skip_dir(self, dir_path: Path) -> bool:
        """
        Check if directory should be skipped for performance.

        Args:
            dir_path: Directory to check

        Returns:
            True if should skip, False otherwise
        """
        dir_name = dir_path.name
        return any(
            dir_name == skip or dir_name.startswith(skip.rstrip("*"))
            for skip in self.SKIP_DIRS
        )

    def _get_python_files(self, max_files: Optional[int] = None) -> List[Path]:
        """
        Get Python files, with performance optimizations.

        Args:
            max_files: Maximum number of files to return (None for all)

        Returns:
            List of Python file paths
        """
        py_files = []
        for py_file in self.project_root.rglob("*.py"):
            # Skip if in ignored directory
            if any(self._should_skip_dir(parent) for parent in py_file.parents):
                continue

            # Check depth
            try:
                depth = len(py_file.relative_to(self.project_root).parts)
                if depth > self.MAX_DEPTH:
                    continue
            except ValueError:
                continue

            py_files.append(py_file)

            if max_files and len(py_files) >= max_files:
                break

        return py_files

    def analyze(self) -> ProjectProfile:
        """
        Analyze project structure comprehensively.

        Returns:
            ProjectProfile with all detected information
        """
        start_time = time.time()

        print_header(f"🔍 Analyzing Project: {self.profile.project_name}")

        # Step 1: Validate project root
        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {self.project_root}")
        print_verbose(f"Project root: {self.project_root}")

        # Step 2: Detect framework
        print_step("Detecting framework", step=1, total=8, emoji="📦")
        step_start = time.time()
        self.profile.framework = self._detect_framework()
        print_success(f"Framework: {self.profile.framework}", indent=3)
        print_verbose(f"Framework detection took {format_time(time.time() - step_start)}")

        # Step 3: Find code directories
        print_step("Finding code directories", step=2, total=8, emoji="📁")
        step_start = time.time()
        self.profile.code_dirs = self._detect_code_dirs()
        if self.profile.code_dirs:
            print_success(f"Found {len(self.profile.code_dirs)} code directories", indent=3)
            for code_dir in self.profile.code_dirs[:5]:
                print_info(code_dir)
        else:
            print_info("No standard code directories found (using project root)")
        print_verbose(f"Code directory detection took {format_time(time.time() - step_start)}")

        # Step 4: Detect layer structure
        print_step("Detecting layer structure", step=3, total=8, emoji="🔧")
        step_start = time.time()
        self.profile.has_layers, self.profile.layer_location = self._detect_layers()
        if self.profile.has_layers:
            print_success(f"Layers found at: {self.profile.layer_location}", indent=3)
        else:
            print_info("No layer structure detected")
        print_verbose(f"Layer detection took {format_time(time.time() - step_start)}")

        # Step 5: Detect presets
        step_start = time.time()
        self.profile.has_presets, self.profile.preset_location = self._detect_presets()
        if self.profile.has_presets:
            print_success(f"Presets found at: {self.profile.preset_location}", indent=3)
        print_verbose(f"Preset detection took {format_time(time.time() - step_start)}")

        # Step 6: Detect tools and APIs
        print_step("Detecting tools and APIs", step=4, total=8, emoji="🛠️")
        step_start = time.time()
        self.profile.detected_tools = self._detect_tools()
        if self.profile.detected_tools:
            print_success(f"Found {len(self.profile.detected_tools)} tools", indent=3)
            for tool in self.profile.detected_tools[:5]:  # Show first 5
                print_info(tool['name'])
            if len(self.profile.detected_tools) > 5:
                print_info(f"...and {len(self.profile.detected_tools) - 5} more")
        else:
            print_info("No external tools detected")
        print_verbose(f"Tool detection took {format_time(time.time() - step_start)}")

        # Step 7: Find config files
        print_step("Finding config files", step=5, total=8, emoji="⚙️")
        step_start = time.time()
        self.profile.config_files = self._detect_config_files()
        print_success(f"Found {len(self.profile.config_files)} config files", indent=3)
        if is_verbose() and self.profile.config_files:
            for cfg in self.profile.config_files[:5]:
                print_info(cfg)
        print_verbose(f"Config file detection took {format_time(time.time() - step_start)}")

        # Step 8: Collect metrics
        print_step("Collecting metrics", step=6, total=8, emoji="📊")
        step_start = time.time()
        self._collect_metrics()
        print_success("Metrics collected", indent=3)
        print_metric("Python files", str(self.profile.file_count), emoji="📄")
        print_metric("Lines of code", f"{self.profile.line_count:,}", emoji="📝")
        if self.profile.test_framework:
            print_metric("Test framework", self.profile.test_framework, emoji="🧪")
        print_verbose(f"Metrics collection took {format_time(time.time() - step_start)}")

        # Summary
        total_time = time.time() - start_time
        print(f"\n{'=' * 60}")
        print_success(f"Analysis complete in {format_time(total_time)}")
        print(f"{'=' * 60}\n")

        return self.profile

    def _detect_framework(self) -> str:
        """
        Detect web framework by scanning Python files (optimized).

        Returns:
            Framework name or "Unknown"
        """
        # First check requirements files (fastest)
        req_files = ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]
        for req_file in req_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                try:
                    content = req_path.read_text(encoding="utf-8", errors="ignore").lower()
                    for framework in self.FRAMEWORK_PATTERNS.keys():
                        if framework.lower() in content:
                            return framework
                except Exception:
                    continue

        # Then scan Python files (limit to 100 for performance)
        py_files = self._get_python_files(max_files=100)
        for py_file in py_files:
            try:
                # Cache file content
                if str(py_file) not in self._file_cache:
                    self._file_cache[str(py_file)] = py_file.read_text(
                        encoding="utf-8", errors="ignore"
                    )
                content = self._file_cache[str(py_file)]

                for framework, patterns in self.FRAMEWORK_PATTERNS.items():
                    if any(pattern in content for pattern in patterns):
                        return framework  # Early termination
            except Exception:
                continue

        return "Unknown"

    def _detect_code_dirs(self) -> List[str]:
        """
        Find directories containing Python code.

        Returns:
            List of code directory paths (relative to project root)
        """
        code_dirs = []

        # Check common directory names
        for dir_name in self.COMMON_CODE_DIRS:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                # Verify it contains Python files
                if list(dir_path.rglob("*.py")):
                    code_dirs.append(f"{dir_name}/")

        # If no common dirs found, scan for directories with Python files
        if not code_dirs:
            for item in self.project_root.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    if list(item.rglob("*.py")):
                        code_dirs.append(f"{item.name}/")

        return sorted(code_dirs)

    def _detect_layers(self) -> tuple[bool, Optional[str]]:
        """
        Detect if project uses layer-based architecture.

        Returns:
            Tuple of (has_layers, layer_location)
        """
        # Search for layer patterns in directory names
        for py_file in self.project_root.rglob("*.py"):
            for pattern in self.LAYER_PATTERNS:
                if re.search(pattern, str(py_file)):
                    # Found a layer pattern - extract the directory
                    parent = py_file.parent
                    while parent != self.project_root:
                        if re.search(pattern, parent.name):
                            # Get relative path from project root
                            rel_path = parent.relative_to(self.project_root)
                            # Get parent directory of the layer
                            layer_base = rel_path.parent
                            return True, f"{layer_base}/"
                        parent = parent.parent

        return False, None

    def _detect_presets(self) -> tuple[bool, Optional[str]]:
        """
        Detect if project has preset configurations.

        Returns:
            Tuple of (has_presets, preset_location)
        """
        preset_patterns = ["preset", "config", "template"]

        for code_dir in self.profile.code_dirs:
            code_path = self.project_root / code_dir
            for preset_pattern in preset_patterns:
                for item in code_path.rglob(f"*{preset_pattern}*"):
                    if item.is_dir() and list(item.glob("*.py")):
                        rel_path = item.relative_to(self.project_root)
                        return True, f"{rel_path}/"

        return False, None

    def _detect_tools(self) -> List[Dict[str, str]]:
        """
        Detect tools and APIs used in the project (optimized).

        Returns:
            List of detected tools with metadata
        """
        detected = {}

        # Scan Python files for tool imports (limit to 50 files for performance)
        py_files = self._get_python_files(max_files=50)
        for py_file in py_files:
            try:
                # Use cached content if available
                if str(py_file) in self._file_cache:
                    content = self._file_cache[str(py_file)]
                else:
                    content = py_file.read_text(encoding="utf-8", errors="ignore")

                for tool_name, patterns in self.TOOL_PATTERNS.items():
                    if tool_name not in detected:
                        if any(pattern in content for pattern in patterns):
                            detected[tool_name] = {
                                "name": tool_name,
                                "type": "library",
                                "first_seen": str(py_file.relative_to(self.project_root))
                            }

                # Early termination if we found all common tools
                if len(detected) >= len(self.TOOL_PATTERNS):
                    break
            except Exception:
                continue

        return list(detected.values())

    def _detect_config_files(self) -> List[str]:
        """
        Find configuration files in the project.

        Returns:
            List of config file paths (relative to project root)
        """
        config_patterns = [
            "*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg",
            ".env*", "config.py", "settings.py"
        ]

        config_files = []
        for pattern in config_patterns:
            for config_file in self.project_root.glob(pattern):
                if config_file.is_file():
                    rel_path = config_file.relative_to(self.project_root)
                    config_files.append(str(rel_path))

        return sorted(config_files)

    def _collect_metrics(self) -> None:
        """Collect project metrics (file count, line count, etc.) - optimized."""
        file_count = 0
        line_count = 0

        # Use optimized file getter
        py_files = self._get_python_files()
        for py_file in py_files:
            file_count += 1
            try:
                # Use cached content if available
                if str(py_file) in self._file_cache:
                    line_count += self._file_cache[str(py_file)].count('\n') + 1
                else:
                    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                        line_count += sum(1 for _ in f)
            except Exception:
                continue

        self.profile.file_count = file_count
        self.profile.line_count = line_count

        # Detect test framework (check first few test files only)
        test_files = []
        for pattern in ["test_*.py", "*_test.py", "tests.py"]:
            test_files.extend(self.project_root.rglob(pattern))
            if len(test_files) >= 3:  # Check at most 3 files
                break

        for test_file in test_files[:3]:
            # Skip if in ignored directory
            if any(self._should_skip_dir(parent) for parent in test_file.parents):
                continue

            try:
                content = test_file.read_text(encoding="utf-8", errors="ignore")
                if "pytest" in content or "import pytest" in content:
                    self.profile.test_framework = "pytest"
                    break
                elif "unittest" in content or "import unittest" in content:
                    self.profile.test_framework = "unittest"
                    break
            except Exception:
                continue


def main():
    """CLI interface for project detection."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detector.py <project_root> [--output <file>]")
        print()
        print("Examples:")
        print("  python detector.py /path/to/project")
        print("  python detector.py /path/to/project --output profile.json")
        return

    project_root = Path(sys.argv[1])
    output_file = None

    if "--output" in sys.argv:
        output_idx = sys.argv.index("--output")
        if output_idx + 1 < len(sys.argv):
            output_file = sys.argv[output_idx + 1]

    # Run detection
    detector = ProjectDetector(project_root)
    profile = detector.analyze()

    # Save to file if requested
    if output_file:
        with open(output_file, "w") as f:
            json.dump(profile.to_dict(), f, indent=2)
        print(f"\n💾 Profile saved to: {output_file}")
    else:
        print("\n📋 Project Profile:")
        print(json.dumps(profile.to_dict(), indent=2))


if __name__ == "__main__":
    main()
