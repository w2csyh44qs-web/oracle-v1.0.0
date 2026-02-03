# Oracle Bootstrap System

**Project-agnostic initialization system for deploying Oracle to any Python project.**

## Overview

The Oracle Bootstrap system enables you to initialize Oracle on any Python project automatically. It detects your project's framework, structure, and tools, then generates appropriate configuration files and documentation.

## Quick Start

### Initialize Oracle on a Project

```bash
# From Oracle project root
python3 oracle/cli.py init /path/to/your/project

# Or preview changes without applying
python3 oracle/cli.py init /path/to/your/project --dry-run
```

### Analyze Project Structure

```bash
# Analyze without initializing
python3 oracle/cli.py detect /path/to/your/project

# Save analysis to file
python3 oracle/cli.py detect /path/to/your/project --output profile.json
```

## What Gets Created

When you run `oracle init`, the following structure is created:

```
your-project/
└── oracle/
    ├── config/
    │   ├── oracle_config.json      # Project configuration
    │   ├── layer_registry.json     # Layer definitions (if detected)
    │   └── tool_registry.json      # Tool/API inventory
    ├── docs/
    │   ├── context/
    │   │   ├── PROJECT_CONTEXT.md  # Main context file
    │   │   └── DEV_CONTEXT.md      # Development context (if layers)
    │   └── plans/                  # Planning documents
    ├── data/
    │   └── memory/                 # Hippocampus memory storage
    └── reports/                    # Audit reports
```

## Supported Frameworks

Oracle automatically detects 16+ Python frameworks:

### Web Frameworks
- **Flask** - Lightweight WSGI web application framework
- **Django** - High-level Python web framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Bottle** - Fast, simple micro web-framework
- **CherryPy** - Minimalist Python web framework
- **Sanic** - Async Python web framework
- **Quart** - Async Python web microframework
- **Tornado** - Asynchronous networking library
- **Pyramid** - Web framework for Python
- **Falcon** - Minimalist ASGI/WSGI framework for web APIs
- **Hug** - Python API framework
- **Web2py** - Full-stack enterprise framework

### Data/UI Frameworks
- **Streamlit** - Framework for data science web apps
- **Gradio** - Framework for ML model demos
- **Dash** - Framework for analytical web applications
- **Starlette** - Lightweight ASGI framework/toolkit

### Fallback
- **Unknown** - Graceful handling for custom or unrecognized frameworks

## Detection Features

### Project Structure Detection

- **Framework identification** - Detects web framework from imports and requirements
- **Code directories** - Finds main code locations (app/, src/, lib/, etc.)
- **Layer architecture** - Detects layer-based patterns (_L1, _L2, etc.)
- **Preset configurations** - Finds preset/config/template directories
- **Tools and APIs** - Discovers third-party libraries in use

### Metrics Collection

- Total Python file count
- Total lines of code
- Test framework detection (pytest, unittest)
- Configuration file inventory

## Configuration Files

### oracle_config.json

Main project configuration file containing:

```json
{
  "version": "1.0.0",
  "project": {
    "name": "your-project",
    "framework": "Flask",
    "python_version": "3.9+"
  },
  "paths": {
    "code_dirs": ["app/", "src/"],
    "layer_location": "app/layers/",
    "preset_location": "app/presets/"
  },
  "structure": {
    "has_layers": true,
    "has_presets": true
  },
  "tools": ["requests", "openai", "pandas"],
  "metrics": {
    "file_count": 150,
    "line_count": 25000,
    "test_framework": "pytest"
  }
}
```

### layer_registry.json

Layer definitions (generated if layer structure detected):

```json
{
  "version": "1.0.0",
  "layers": {
    "L1": {
      "name": "Data Ingestion",
      "path": "app/layers/_L1/",
      "tools": ["requests", "httpx"]
    },
    "L2": {
      "name": "Data Processing",
      "path": "app/layers/_L2/",
      "tools": ["pandas", "numpy"]
    }
  }
}
```

### tool_registry.json

Detected tools and APIs:

```json
{
  "version": "1.0.0",
  "tools": {
    "openai": {
      "type": "library",
      "detected_in": "app/services/llm.py",
      "enabled": true
    },
    "requests": {
      "type": "library",
      "detected_in": "app/api/client.py",
      "enabled": true
    }
  }
}
```

## Performance Optimizations

The bootstrap system is optimized for large projects:

- **Directory skipping** - Automatically skips .git, node_modules, venv, __pycache__, etc.
- **Depth limiting** - Scans up to 8 directory levels by default
- **File caching** - Reuses file contents across detection phases
- **Early termination** - Stops scanning when framework/tools are found
- **Limited sampling** - Checks representative files rather than entire codebase

## Requirements

- **Python 3.9+** - Oracle requires modern Python features
- **Write permissions** - Must be able to create directories and files
- **Python project** - At least one .py file must exist

## Error Handling

Oracle provides helpful error messages and recovery hints:

```
❌ Python 3.9+ required (found 3.8)
💡 Recovery: Upgrade Python using pyenv, conda, or your system package manager
```

Common errors:
- **No Python files found** - Verify you're in a Python project directory
- **No write permission** - Run with appropriate permissions or change ownership
- **Oracle directory exists** - Choose to overwrite or cancel initialization

## Validation

After initialization, Oracle validates:

- ✅ Configuration files exist and are valid JSON
- ✅ Required config keys present
- ✅ Context directory created
- ✅ At least one context file generated
- ✅ Memory directory structure ready

## Next Steps After Initialization

1. **Review configs:**
   ```bash
   cat oracle/config/oracle_config.json
   ```

2. **Customize contexts:**
   ```bash
   cat oracle/docs/context/PROJECT_CONTEXT.md
   ```

3. **Run Oracle status:**
   ```bash
   python oracle/project_oracle.py status
   ```

4. **Start first session:**
   ```bash
   python oracle/project_oracle.py audit --quick
   ```

## Architecture

### Modules

- **detector.py** (~360 lines) - Project structure detection
  - `ProjectDetector` class - Analyzes project structure
  - `ProjectProfile` dataclass - Stores detection results

- **initializer.py** (~450 lines) - Initialization workflow
  - `OracleInitializer` class - Orchestrates bootstrap process
  - 7-step workflow with validation

- **templates/** - Context file templates (inline in initializer.py)

### Bootstrap Workflow

1. **Validate Environment**
   - Check Python version (3.9+)
   - Verify project root exists
   - Check for Python files
   - Test write permissions

2. **Detect Structure**
   - Scan for framework imports
   - Find code directories
   - Detect layer architecture
   - Discover tools and APIs
   - Collect project metrics

3. **Generate Configs**
   - Create oracle_config.json
   - Generate layer_registry.json (if applicable)
   - Generate tool_registry.json

4. **Scaffold Directories**
   - Create oracle/config/
   - Create oracle/docs/context/
   - Create oracle/docs/plans/
   - Create oracle/data/memory/
   - Create oracle/reports/

5. **Generate Contexts**
   - Create PROJECT_CONTEXT.md
   - Create DEV_CONTEXT.md (if layers detected)

6. **Validate Installation**
   - Verify all files created
   - Validate JSON configs
   - Check directory structure

7. **Report Success**
   - Show created files
   - Display next steps

## API Usage

### Python API

```python
from oracle.bootstrap import ProjectDetector, OracleInitializer

# Detect project structure
detector = ProjectDetector('/path/to/project')
profile = detector.analyze()
print(f"Framework: {profile.framework}")
print(f"Files: {profile.file_count}")

# Initialize Oracle
initializer = OracleInitializer('/path/to/project')
success = initializer.init(dry_run=False)
```

### CLI Usage

```bash
# Initialize
python3 oracle/cli.py init /path/to/project
python3 oracle/cli.py init . --dry-run

# Detect
python3 oracle/cli.py detect /path/to/project
python3 oracle/cli.py detect . --output profile.json

# Version
python3 oracle/cli.py version
```

## Troubleshooting

### Oracle directory already exists

If Oracle is already initialized, you'll be prompted to overwrite:

```
⚠️  Oracle directory already exists. Overwrite? [y/N]:
```

Choose 'y' to overwrite or 'N' to cancel.

### Framework not detected

If your framework isn't detected:
1. Check that framework is in requirements.txt or imports
2. Add framework pattern to `FRAMEWORK_PATTERNS` in detector.py
3. Report issue if framework should be supported

### Performance issues on large projects

For very large projects (10k+ files):
1. Bootstrap automatically limits scanning
2. Common directories (.git, node_modules) are skipped
3. Early termination when patterns found

## Contributing

To add support for a new framework:

1. Add pattern to `FRAMEWORK_PATTERNS` in detector.py:
```python
"YourFramework": ["from yourframework import", "YourFramework("]
```

2. Test detection:
```bash
python3 oracle/cli.py detect /path/to/your-framework-project
```

## Version

**Current Version:** 1.0.0
**Part of:** Oracle v1.0 (P30 Phase 4)

## Author

Oracle Brain Cell Architecture (P30 Phase 4)

---

*Oracle Bootstrap - Deploy Oracle to any Python project automatically*
