# Oracle - Project-Agnostic Development Intelligence

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/anthropics/oracle)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**"Set and Forget" development intelligence for Python projects**

Oracle is a portable, project-agnostic system that provides automatic memory, health monitoring, and development context management for any Python project.

---

## Quick Start

### 1. Copy Oracle to Your Project

```bash
# Copy the oracle/ folder to your project root
cp -r oracle/ /path/to/your/project/oracle/
```

### 2. Initialize Oracle

```bash
cd /path/to/your/project
python3 oracle/cli.py init .
```

That's it! Oracle is now monitoring your project automatically.

---

## What You Get

Once initialized, Oracle automatically:

- **🔍 Analyzes** - Health scores, circular dependencies, complexity metrics
- **🧠 Learns** - Captures development patterns and decisions
- **🪝 Verifies** - Git hooks check commits automatically (<5s)
- **🌐 Dashboard** - Real-time monitoring at localhost:7777
- **⚡ Daemon** - Background monitoring 24/7
- **🛠️ Auto-Fixes** - Preview and apply code improvements

---

## Code Analysis & Quality

Oracle provides **automated code review** that runs in the background while you code:

### Health Monitoring
Get instant feedback on code quality without manual checks:
```bash
python3 oracle/project_oracle.py audit --quick  # <5 seconds
```
- **0-100 health score** - Clear, actionable metric for code quality
- **Issue categorization** - Critical, warnings, optimizations
- **Trend tracking** - See if your codebase is improving or degrading
- **Auto-fix suggestions** - Preview and apply fixes with one command

### Integrity Verification
Catch structural issues before they cause runtime errors:
```bash
python3 oracle/project_oracle.py verify  # Runs automatically on git commit
```
- **Circular dependency detection** - Find and fix import cycles automatically
- **Performance regression tracking** - Get alerted when code gets slower
- **Auto-fix with preview** - Review proposed changes before applying

### Codebase Assessment
Understand your project's architecture in seconds:
```bash
python3 oracle/project_oracle.py assess --graph
```
- **Dependency visualization** - See how your modules connect
- **Complexity hotspots** - Find files that need refactoring
- **CI/CD templates** - Generate GitHub Actions/GitLab CI configs
- **Export graphs** - Share architecture diagrams with your team

**Why Oracle?** Enterprise-grade code analysis (SonarQube, CodeScene) without the complexity or cost. Perfect for solo developers and small teams who want quality gates without the overhead.

---

## Core Features

### Automatic Memory System
Every session is automatically captured and searchable:
```bash
# Search observations
python3 oracle/memory/hippocampus.py search "API changes"
```

### Background Daemon
Auto-starts on boot, monitors continuously:
```bash
python3 oracle/cli.py daemon install
python3 oracle/cli.py daemon start
```

### Web Dashboard
Real-time monitoring at localhost:7777:
```bash
python3 oracle/cli.py dashboard start
```

### Git Integration
Pre-commit hooks verify changes automatically:
```bash
git commit -m "Your message"
# Oracle hook runs automatically (<5s)
```

### Terminal Dashboard
Lightweight monitoring with command palette:
```bash
python3 oracle/sEEG.py
# Press ':' for command mode
# Press 'd' for diagnostics
```

---

## Portability

Oracle is designed to be **portable and project-agnostic**:

1. **Copy the oracle/ folder** to any Python project
2. **Run `oracle init`** to bootstrap onto the project
3. **Oracle adapts** to your project structure automatically

### What Gets Excluded

When committing Oracle to git, project-specific data is excluded:
- `oracle/data/*.json` - Runtime status and logs
- `oracle/config/*.json` - Generated configs (except examples)
- `oracle/reports/` - Audit reports

This allows you to:
- ✅ Share Oracle code across projects
- ✅ Version Oracle independently
- ✅ Keep project-specific data local

---

## Documentation

### Getting Started
- [Quick Start Guide](oracle/docs/QUICK_START.md) - 5-minute setup
- [Oracle README](oracle/README.md) - Complete feature documentation

### Components
- [Daemon Guide](oracle/docs/DAEMON_GUIDE.md) - Background monitoring
- [Dashboard Guide](oracle/docs/DASHBOARD_GUIDE.md) - Web interface
- [Git Integration](oracle/docs/GIT_INTEGRATION.md) - Git hooks workflow

### Development
- [CONTRIBUTE.md](CONTRIBUTE.md) - Contribution guidelines
- [LICENSE](LICENSE) - MIT License

---

## Requirements

- **Python 3.9+**
- **Git** (optional, for git hooks)
- **Flask** (optional, for web dashboard):
  ```bash
  pip install flask flask-socketio flask-cors python-socketio
  ```

---

## Commands

```bash
# Initialization
oracle init <project_root>          # Bootstrap Oracle onto project
oracle detect <project_root>        # Analyze project structure

# Daemon
oracle daemon install               # Install system service
oracle daemon start                 # Start background daemon
oracle daemon status                # Check daemon status

# Dashboard
oracle dashboard start              # Start web UI (localhost:7777)
oracle dashboard stop               # Stop web UI

# Health
oracle audit --quick                # Quick health check
oracle status                       # Project status
oracle verify                       # Integrity verification

# Monitoring
python3 oracle/sEEG.py              # Terminal dashboard
```

---

## Architecture

Oracle uses a **Brain Cell Architecture** where each module represents a specialized brain cell type:

- **Microglia** - Audit and cleanup
- **Hippocampus** - Memory and learning
- **Astrocytes** - Context stability
- **Oligodendrocytes** - Performance optimization
- **Ependymal** - Documentation flow
- **Schwann Cells** - File change detection
- **Topoisomerase** - Integrity verification

See [oracle/README.md](oracle/README.md) for detailed architecture documentation.

---

## Use Cases

### 1. Onboard New Developers
```bash
oracle init .
oracle status
# New devs get instant project context
```

### 2. Multi-Project Management
```bash
# Copy oracle/ to multiple projects
cp -r oracle/ /project1/
cp -r oracle/ /project2/

# Each project gets independent monitoring
cd /project1 && oracle init .
cd /project2 && oracle init .
```

### 3. Continuous Monitoring
```bash
# Install daemon once
oracle daemon install

# Oracle monitors 24/7
# - Health checks every 5 minutes
# - Git hooks on commits
# - Real-time dashboard updates
```

---

## Performance

- **Initialization:** <3 seconds on medium projects
- **Health Checks:** <5 seconds
- **Daemon CPU:** <1% idle, <5% active
- **Memory:** <50MB footprint
- **Git Hooks:** <5 seconds per commit

---

## Version

**v1.0.0** - February 2026

**Features:**
- ✅ Automatic memory system with semantic search
- ✅ Project-agnostic bootstrap
- ✅ Background daemon with auto-start
- ✅ Web and terminal dashboards
- ✅ Git hooks integration
- ✅ "Set and Forget" operation
- ✅ Full documentation (4 guides, 2150+ lines)

---

## Contributing

We welcome contributions! See [CONTRIBUTE.md](CONTRIBUTE.md) for guidelines.

Areas for contribution:
- Framework support
- Tool detection patterns
- Documentation improvements
- Testing on different projects

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Support

- **Documentation:** [oracle/docs/](oracle/docs/)
- **Issues:** https://github.com/anthropics/oracle/issues
- **Quick Start:** [oracle/docs/QUICK_START.md](oracle/docs/QUICK_START.md)

---

---

**Oracle v1.0** - Transform how you manage Python projects with automatic intelligence

*"Set and Forget" Development Intelligence*
