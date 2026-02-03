#!/usr/bin/env python3
"""
cortex.py - Project-Specific Intelligence Brain Cell

The cerebral cortex is responsible for higher cognitive functions, planning,
and project-specific knowledge. This module contains tools that are specific
to this project's architecture (presets, pipeline layers, content types).

Unlike other brain cell modules which are project-agnostic, cortex.py contains
project-specific configurations and analysis tools that understand this
particular codebase's structure.

Commands:
    - presets: Display and analyze script generation presets
    - layers: Show pipeline layer structure and tools
    - pipeline-info: Display pipeline configuration and status

Usage:
    python3 oracle/project_oracle.py presets [--output json|table|markdown] [--save]
    python3 oracle/project_oracle.py layers [--layer L1]
    python3 oracle/project_oracle.py pipeline-info

Author: Oracle Brain Cell Architecture
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Path setup - works from any location
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Up from project/ to oracle/ to root

# Oracle config paths
ORACLE_CONFIG_DIR = PROJECT_ROOT / "oracle" / "config"
ORACLE_CONFIG_FILE = ORACLE_CONFIG_DIR / "oracle_config.json"
LAYER_REGISTRY_FILE = ORACLE_CONFIG_DIR / "layer_registry.json"


def load_oracle_config() -> Dict[str, Any]:
    """
    Load Oracle configuration from oracle/config/oracle_config.json.

    Returns project-specific paths and settings for config-driven operation.

    Returns:
        Dict with project config including paths, structure, health settings
    """
    if not ORACLE_CONFIG_FILE.exists():
        # Fallback: use default paths if config doesn't exist yet
        # This ensures backwards compatibility during migration
        return {
            "paths": {
                "config_dir": "config/",
                "docs_dir": "docs/",
                "oracle_docs": "oracle/docs/",
                "oracle_docs_overview": "oracle/docs/overview/",
                "pipeline_dir": "app/core/pipeline/",
                "layers_dir": "app/core/pipeline/layers/"
            }
        }

    try:
        with open(ORACLE_CONFIG_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {ORACLE_CONFIG_FILE}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error loading Oracle config: {e}")


# Load Oracle configuration
_ORACLE_CONFIG = load_oracle_config()
_PATHS = _ORACLE_CONFIG.get("paths", {})

# Project paths (loaded from oracle_config.json - P30 Phase 1)
CONFIG_DIR = PROJECT_ROOT / _PATHS.get("config_dir", "config/")
DOCS_DIR = PROJECT_ROOT / _PATHS.get("oracle_docs", "oracle/docs/")
DOCS_OVERVIEW_DIR = PROJECT_ROOT / _PATHS.get("oracle_docs_overview", "oracle/docs/overview/")
PIPELINE_DIR = PROJECT_ROOT / _PATHS.get("pipeline_dir", "app/core/pipeline/")
LAYERS_DIR = PROJECT_ROOT / _PATHS.get("layers_dir", "app/core/pipeline/layers/")


def load_layer_registry() -> Dict[str, Dict]:
    """
    Load layer definitions from oracle/config/layer_registry.json.

    This makes cortex.py config-driven and project-agnostic, supporting
    Oracle's export-ready architecture (P30).

    Returns:
        Dict mapping layer IDs (L0-L8) to layer definitions
    """
    if not LAYER_REGISTRY_FILE.exists():
        # Fallback error message if config file is missing
        raise FileNotFoundError(
            f"Layer registry not found: {LAYER_REGISTRY_FILE}\n"
            f"Run `oracle init` to generate project configuration."
        )

    try:
        with open(LAYER_REGISTRY_FILE) as f:
            registry = json.load(f)

        # Extract just the layers dict from the registry
        layers = registry.get("layers", {})

        if not layers:
            raise ValueError(f"No layers found in {LAYER_REGISTRY_FILE}")

        return layers

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {LAYER_REGISTRY_FILE}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error loading layer registry: {e}")


# Load layer definitions from config file (P30 Phase 1)
LAYER_DEFINITIONS = load_layer_registry()


class PresetAnalyzer:
    """Analyze and display preset configurations.

    Loads presets from config/script_presets.json and provides various
    output formats for reference and documentation.
    """

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.config_dir = self.project_root / "config"
        self.presets_file = self.config_dir / "script_presets.json"

    def load_presets(self) -> List[Dict]:
        """Load all presets from script_presets.json."""
        if not self.presets_file.exists():
            return []

        try:
            with open(self.presets_file) as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading presets: {e}")
            return []

        presets = []

        # Load generate_presets
        for preset_id, config in data.get("generate_presets", {}).items():
            if preset_id.startswith("_"):
                continue
            presets.append(self._parse_preset(preset_id, config, "generate"))

        # Load discovery_presets
        for preset_id, config in data.get("discovery_presets", {}).items():
            if preset_id.startswith("_"):
                continue
            presets.append(self._parse_preset(preset_id, config, "discovery"))

        return presets

    def _parse_preset(self, preset_id: str, config: dict, category: str) -> Dict:
        """Parse a single preset configuration."""
        tools = config.get("tools", {})
        layers = config.get("layers", [])

        # If layers is a dict (old format), extract the keys
        if isinstance(layers, dict):
            layers = [k for k, v in layers.items() if v]

        return {
            "id": preset_id,
            "name": config.get("name", preset_id.replace("_", " ").title()),
            "description": config.get("description", ""),
            "category": category,
            "output_type": config.get("output_type", ""),
            "layers": layers if layers else ["L1", "L3", "L5", "L6", "L7"],
            "L1_tool": config.get("L1_tool") or config.get("api_source", "-"),
            "L3_tool": config.get("L3_tool") or tools.get("model") or config.get("preferred_model", "-"),
            "L4_tool": config.get("L4_tool") or tools.get("tts_tool", "-"),
            "L5_tool": config.get("L5_tool") or tools.get("image_tool", "-"),
            "L6_tool": config.get("L6_tool") or tools.get("animation_tool", "-"),
            "aspect_ratio": config.get("aspect_ratio", "-"),
            "slide_count": config.get("slide_count", "-"),
        }

    def print_table(self, presets: List[Dict]) -> None:
        """Print presets as a formatted table."""
        try:
            from rich.console import Console
            from rich.table import Table
            console = Console()

            table = Table(title="📋 Preset Reference", show_header=True, header_style="bold cyan")
            table.add_column("Preset", style="bold")
            table.add_column("Output", style="dim")
            table.add_column("L1 (Data)", style="green")
            table.add_column("L3 (Script)", style="yellow")
            table.add_column("L4 (Audio)", style="blue")
            table.add_column("L5 (Media)", style="magenta")
            table.add_column("L6 (Assembly)", style="red")

            for p in presets:
                table.add_row(
                    p["id"][:25],
                    p["output_type"][:12] if p["output_type"] else "-",
                    str(p["L1_tool"])[:15] if p["L1_tool"] != "-" else "-",
                    str(p["L3_tool"])[:15] if p["L3_tool"] != "-" else "-",
                    str(p["L4_tool"])[:12] if p["L4_tool"] != "-" else "-",
                    str(p["L5_tool"])[:12] if p["L5_tool"] != "-" else "-",
                    str(p["L6_tool"])[:15] if p["L6_tool"] != "-" else "-",
                )

            console.print(table)
            console.print(f"\n[dim]Total: {len(presets)} presets[/dim]")

        except ImportError:
            # Fallback without rich
            print("=" * 120)
            print(f"{'Preset':<30} {'Output':<15} {'L1':<15} {'L3':<15} {'L4':<12} {'L5':<12} {'L6':<15}")
            print("=" * 120)
            for p in presets:
                print(f"{p['id'][:28]:<30} {(p['output_type'] or '-')[:13]:<15} "
                      f"{str(p['L1_tool'])[:13]:<15} {str(p['L3_tool'])[:13]:<15} "
                      f"{str(p['L4_tool'])[:10]:<12} {str(p['L5_tool'])[:10]:<12} "
                      f"{str(p['L6_tool'])[:13]:<15}")
            print("=" * 120)
            print(f"Total: {len(presets)} presets")

    def generate_markdown(self, presets: List[Dict]) -> str:
        """Generate markdown reference document."""
        lines = [
            "# Presets Reference",
            "",
            f"> Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "> Run `python3 oracle/project_oracle.py presets --save` to update",
            "",
            "---",
            "",
            "## Generate Presets",
            "",
            "| Preset | Description | Output | L1 (Data) | L3 (Script) | L4 (Audio) | L5 (Media) | L6 (Assembly) |",
            "|--------|-------------|--------|-----------|-------------|------------|------------|---------------|",
        ]

        generate_presets = [p for p in presets if p["category"] == "generate"]
        for p in generate_presets:
            desc = p["description"][:40] + "..." if len(p["description"]) > 40 else p["description"]
            lines.append(
                f"| **{p['id']}** | {desc} | {p['output_type'] or '-'} | "
                f"{p['L1_tool']} | {p['L3_tool']} | {p['L4_tool']} | {p['L5_tool']} | {p['L6_tool']} |"
            )

        # Discovery presets
        discovery_presets = [p for p in presets if p["category"] == "discovery"]
        if discovery_presets:
            lines.extend([
                "",
                "## Discovery Presets",
                "",
                "| Preset | Description | Mode |",
                "|--------|-------------|------|",
            ])
            for p in discovery_presets:
                lines.append(f"| **{p['id']}** | {p['description']} | discovery |")

        # Tool summary
        lines.extend([
            "",
            "---",
            "",
            "## Tool Reference",
            "",
            "### L1 Data Sources",
            "- `goatedbets_api` - GoatedBets matchup analysis API",
            "- `web_search` - Perplexity/Tavily web search",
            "- `local_assets` - Local video/image assets",
            "- `balldontlie` - Sports data via balldontlie API (NFL/NBA)",
            "",
            "### L3 Script Tools (LLM)",
            "- `gemini` - Google Gemini 1.5 Flash",
            "- `perplexity` - Perplexity Sonar (real-time web)",
            "- `gpt-4o-mini` - OpenAI GPT-4o Mini",
            "- `nano_banana` - Gemini for text-heavy infographics",
            "- `carousel_script` - Carousel slide generation",
            "- `infographic_script` - Infographic content generation",
            "",
            "### L4 Audio Tools",
            "- `elevenlabs` - ElevenLabs TTS",
            "",
            "### L5 Media Tools",
            "- `nano_banana` - Gemini Nano Banana (text-heavy images)",
            "- `imagen4` - Google Imagen 4 (photorealistic)",
            "- `flux_fal` - Flux via FAL.AI",
            "- `pexels` - Pexels stock video/images",
            "- `kling` - Kling AI video generation",
            "",
            "### L6 Assembly Tools",
            "- `carousel_assembly` - Multi-slide carousel assembly",
            "- `reel_converter` - 9:16 static video conversion",
            "- `pil_overlay` - PIL logo/text overlay",
            "- `ken_burns` - Ken Burns effect animation",
            "- `ffmpeg` - FFmpeg video processing",
            "",
        ])

        return "\n".join(lines)

    def get_preset_by_id(self, preset_id: str) -> Optional[Dict]:
        """Get a specific preset by ID."""
        presets = self.load_presets()
        for p in presets:
            if p["id"] == preset_id:
                return p
        return None


class LayerAnalyzer:
    """Analyze pipeline layer structure and configuration."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.layers_dir = self.project_root / "app" / "core" / "pipeline" / "layers"

    def get_layer_status(self) -> Dict[str, Dict]:
        """Get status of all pipeline layers."""
        status = {}

        for layer_id, layer_def in LAYER_DEFINITIONS.items():
            layer_dir = self.layers_dir / f"_{layer_id}"

            status[layer_id] = {
                **layer_def,
                "exists": layer_dir.exists(),
                "files": [],
                "subdirs": []
            }

            if layer_dir.exists():
                for item in layer_dir.iterdir():
                    if item.is_file() and item.suffix == ".py":
                        status[layer_id]["files"].append(item.name)
                    elif item.is_dir() and not item.name.startswith("_"):
                        status[layer_id]["subdirs"].append(item.name)

        return status

    def print_layer_table(self, layer_filter: str = None) -> None:
        """Print layer structure as formatted table."""
        status = self.get_layer_status()

        try:
            from rich.console import Console
            from rich.table import Table
            console = Console()

            table = Table(title="🔄 Pipeline Layers", show_header=True, header_style="bold cyan")
            table.add_column("Layer", style="bold")
            table.add_column("Name", style="dim")
            table.add_column("Status", style="green")
            table.add_column("Primary Script")
            table.add_column("Tools")

            for layer_id in sorted(status.keys(), key=lambda x: int(x[1:])):
                if layer_filter and layer_id != layer_filter:
                    continue

                layer = status[layer_id]
                status_icon = "✓" if layer["exists"] else "✗"
                status_style = "green" if layer["exists"] else "red"

                tools_str = ", ".join(layer["tools"][:3])
                if len(layer["tools"]) > 3:
                    tools_str += f" (+{len(layer['tools']) - 3})"

                table.add_row(
                    layer_id,
                    layer["name"][:25],
                    f"[{status_style}]{status_icon}[/{status_style}]",
                    layer["primary_script"],
                    tools_str
                )

            console.print(table)

        except ImportError:
            # Fallback without rich
            print("=" * 100)
            print(f"{'Layer':<8} {'Name':<28} {'Status':<8} {'Primary Script':<20} {'Tools'}")
            print("=" * 100)

            for layer_id in sorted(status.keys(), key=lambda x: int(x[1:])):
                if layer_filter and layer_id != layer_filter:
                    continue

                layer = status[layer_id]
                status_icon = "OK" if layer["exists"] else "MISS"
                tools_str = ", ".join(layer["tools"][:3])

                print(f"{layer_id:<8} {layer['name'][:26]:<28} {status_icon:<8} "
                      f"{layer['primary_script']:<20} {tools_str}")

            print("=" * 100)

    def get_layer_detail(self, layer_id: str) -> Dict:
        """Get detailed information about a specific layer."""
        if layer_id not in LAYER_DEFINITIONS:
            return {"error": f"Unknown layer: {layer_id}"}

        layer_dir = self.layers_dir / f"_{layer_id}"
        layer_def = LAYER_DEFINITIONS[layer_id].copy()

        layer_def["path"] = str(layer_dir)
        layer_def["exists"] = layer_dir.exists()

        if layer_dir.exists():
            layer_def["files"] = []
            layer_def["subdirs"] = []

            for item in layer_dir.iterdir():
                if item.is_file() and item.suffix == ".py":
                    # Get file size and last modified
                    stat = item.stat()
                    layer_def["files"].append({
                        "name": item.name,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                elif item.is_dir() and not item.name.startswith("_"):
                    layer_def["subdirs"].append(item.name)

        return layer_def


class PipelineAnalyzer:
    """Analyze overall pipeline configuration and health."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or PROJECT_ROOT
        self.config_dir = self.project_root / "config"
        self.pipeline_dir = self.project_root / "app" / "core" / "pipeline"

    def get_tool_config(self) -> Dict:
        """Load tool configuration."""
        tool_config_file = self.config_dir / "tool_config.json"
        if tool_config_file.exists():
            try:
                with open(tool_config_file) as f:
                    return json.load(f)
            except Exception as e:
                return {"error": str(e)}
        return {}

    def get_pipeline_info(self) -> Dict:
        """Get overall pipeline information."""
        layer_analyzer = LayerAnalyzer(self.project_root)
        preset_analyzer = PresetAnalyzer(self.project_root)

        layer_status = layer_analyzer.get_layer_status()
        presets = preset_analyzer.load_presets()
        tool_config = self.get_tool_config()

        return {
            "project_root": str(self.project_root),
            "pipeline_dir": str(self.pipeline_dir),
            "layers": {
                "total": len(layer_status),
                "active": sum(1 for l in layer_status.values() if l["exists"]),
                "status": {k: v["exists"] for k, v in layer_status.items()}
            },
            "presets": {
                "total": len(presets),
                "generate": len([p for p in presets if p["category"] == "generate"]),
                "discovery": len([p for p in presets if p["category"] == "discovery"])
            },
            "tool_config": {
                "loaded": bool(tool_config and "error" not in tool_config),
                "default_tools": tool_config.get("default_tools", {}) if isinstance(tool_config, dict) else {}
            }
        }

    def print_pipeline_info(self) -> None:
        """Print pipeline info in a readable format."""
        info = self.get_pipeline_info()

        print("\n📊 Pipeline Information")
        print("=" * 50)
        print(f"Project Root: {info['project_root']}")
        print(f"Pipeline Dir: {info['pipeline_dir']}")
        print()
        print("Layers:")
        print(f"  Total: {info['layers']['total']}")
        print(f"  Active: {info['layers']['active']}")
        for layer_id, exists in sorted(info['layers']['status'].items(), key=lambda x: int(x[0][1:])):
            status = "✓" if exists else "✗"
            print(f"    {layer_id}: {status}")
        print()
        print("Presets:")
        print(f"  Total: {info['presets']['total']}")
        print(f"  Generate: {info['presets']['generate']}")
        print(f"  Discovery: {info['presets']['discovery']}")
        print()
        print("Tool Config:")
        print(f"  Loaded: {'✓' if info['tool_config']['loaded'] else '✗'}")
        if info['tool_config']['default_tools']:
            for tool_type, tool_name in info['tool_config']['default_tools'].items():
                print(f"    {tool_type}: {tool_name}")
        print("=" * 50)


# ============================================================================
# PUBLIC INTERFACE - Functions called by project_oracle.py
# ============================================================================

def analyze_presets(output_format: str = "table", save: bool = False) -> Dict:
    """
    Analyze and display preset configurations.

    Args:
        output_format: Output format - 'table', 'json', or 'markdown'
        save: If True, save markdown to docs/overview/PRESETS_REFERENCE.md

    Returns:
        Dict with presets data and operation status
    """
    analyzer = PresetAnalyzer()
    presets = analyzer.load_presets()

    if not presets:
        print("❌ No presets found. Check config/script_presets.json exists.")
        return {"success": False, "error": "No presets found", "presets": []}

    if output_format == "json":
        print(json.dumps(presets, indent=2, default=str))
    elif output_format == "markdown" or save:
        markdown = analyzer.generate_markdown(presets)
        if save:
            output_path = DOCS_OVERVIEW_DIR / "PRESETS_REFERENCE.md"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(markdown)
            print(f"✅ Saved to: {output_path}")
        if output_format == "markdown" or not save:
            print(markdown)
    else:
        # Table format (default)
        analyzer.print_table(presets)

    return {
        "success": True,
        "presets": presets,
        "count": len(presets),
        "saved": save
    }


def show_layers(layer_filter: str = None, output_format: str = "table") -> Dict:
    """
    Display pipeline layer structure.

    Args:
        layer_filter: Optional layer ID to filter (e.g., "L1")
        output_format: Output format - 'table' or 'json'

    Returns:
        Dict with layer status data
    """
    analyzer = LayerAnalyzer()

    if output_format == "json":
        status = analyzer.get_layer_status()
        if layer_filter:
            status = {k: v for k, v in status.items() if k == layer_filter}
        print(json.dumps(status, indent=2, default=str))
    else:
        analyzer.print_layer_table(layer_filter)

    return {
        "success": True,
        "layers": analyzer.get_layer_status()
    }


def get_layer_detail(layer_id: str) -> Dict:
    """
    Get detailed information about a specific layer.

    Args:
        layer_id: Layer ID (e.g., "L1", "L3")

    Returns:
        Dict with detailed layer information
    """
    analyzer = LayerAnalyzer()
    return analyzer.get_layer_detail(layer_id)


def show_pipeline_info() -> Dict:
    """
    Display overall pipeline configuration and status.

    Returns:
        Dict with pipeline information
    """
    analyzer = PipelineAnalyzer()
    analyzer.print_pipeline_info()
    return analyzer.get_pipeline_info()


def get_preset(preset_id: str) -> Optional[Dict]:
    """
    Get a specific preset by ID.

    Args:
        preset_id: Preset ID (e.g., "best_bets_slate")

    Returns:
        Preset dict or None if not found
    """
    analyzer = PresetAnalyzer()
    return analyzer.get_preset_by_id(preset_id)


# ============================================================================
# CLI ENTRY POINT (for standalone testing)
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cortex - Project-Specific Intelligence")
    subparsers = parser.add_subparsers(dest="command")

    # presets command
    presets_parser = subparsers.add_parser("presets", help="Display preset configurations")
    presets_parser.add_argument("--output", "-o", choices=["table", "json", "markdown"],
                                default="table", help="Output format")
    presets_parser.add_argument("--save", action="store_true",
                                help="Save markdown to docs/overview/")

    # layers command
    layers_parser = subparsers.add_parser("layers", help="Show pipeline layers")
    layers_parser.add_argument("--layer", "-l", help="Filter to specific layer (e.g., L1)")
    layers_parser.add_argument("--output", "-o", choices=["table", "json"],
                               default="table", help="Output format")

    # pipeline-info command
    pipeline_parser = subparsers.add_parser("pipeline-info", help="Show pipeline info")

    args = parser.parse_args()

    if args.command == "presets":
        analyze_presets(output_format=args.output, save=args.save)
    elif args.command == "layers":
        show_layers(layer_filter=args.layer, output_format=args.output)
    elif args.command == "pipeline-info":
        show_pipeline_info()
    else:
        parser.print_help()
