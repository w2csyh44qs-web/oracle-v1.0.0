# Contributing to Oracle

Thank you for your interest in contributing to Oracle! This document provides guidelines and information for contributors.

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of Python project structure
- Familiarity with Oracle's Brain Cell Architecture (see [oracle/README.md](oracle/README.md))

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/oracle.git
   cd oracle
   ```

2. **Initialize Oracle on a test project:**
   ```bash
   python3 oracle/cli.py init /path/to/test/project
   ```

3. **Install development dependencies (optional):**
   ```bash
   pip install flask flask-socketio flask-cors python-socketio  # For dashboard
   ```

---

## How to Contribute

### Areas for Contribution

1. **Framework Support**
   - Add detection patterns for new frameworks
   - File: [oracle/bootstrap/detector.py](oracle/bootstrap/detector.py)
   - Update `FRAMEWORK_PATTERNS` dictionary

2. **Tool Detection**
   - Add patterns for new APIs and libraries
   - File: [oracle/bootstrap/detector.py](oracle/bootstrap/detector.py)
   - Update `TOOL_PATTERNS` dictionary

3. **Documentation**
   - Improve guides in `oracle/docs/`
   - Add examples and use cases
   - Fix typos and clarify instructions

4. **Testing**
   - Test Oracle on different project types
   - Report issues with specific frameworks
   - Validate performance on large projects

5. **Features**
   - Memory system enhancements
   - Dashboard improvements
   - New brain cell modules
   - Performance optimizations

---

## Contribution Guidelines

### Code Style

- **Follow PEP 8** Python style guidelines
- **Use type hints** where appropriate
- **Add docstrings** to functions and classes
- **Keep functions focused** (single responsibility)
- **Use meaningful variable names** (descriptive, not abbreviated)

### Brain Cell Metaphor

Oracle uses a brain cell architecture. When adding new modules:
- Choose an appropriate brain cell type (see [Architecture](oracle/README.md#architecture))
- Follow naming conventions (e.g., `microglia.py` for cleanup, `hippocampus.py` for memory)
- Document the metaphor in module docstrings

### Commit Messages

Use clear, descriptive commit messages:

```
Good examples:
- "Add FastAPI framework detection"
- "Fix memory search with special characters"
- "Improve dashboard responsive design"

Avoid:
- "fix bug"
- "update"
- "wip"
```

### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following style guidelines
   - Add tests if applicable
   - Update documentation

3. **Test your changes:**
   ```bash
   # Test on a sample project
   python3 oracle/cli.py init /path/to/test/project

   # Run health checks
   python3 oracle/project_oracle.py audit --quick
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request:**
   - Go to the original repository
   - Click "New Pull Request"
   - Provide a clear description of your changes
   - Reference any related issues

---

## Reporting Issues

### Before Submitting an Issue

- Check existing issues to avoid duplicates
- Test on the latest version of Oracle
- Try to reproduce the issue on a clean test project

### Issue Template

**Bug Report:**
```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Run `oracle init .`
2. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: macOS 14.2 / Ubuntu 22.04
- Python: 3.9.7
- Oracle Version: 1.0.0
- Project Type: Flask / Django / Other
```

**Feature Request:**
```markdown
**Feature Description:**
Clear description of the proposed feature

**Use Case:**
Why this feature would be useful

**Proposed Implementation:**
(Optional) How you think it could be implemented
```

---

## Development Workflow

### Adding a New Framework

1. **Identify framework patterns:**
   ```python
   "YourFramework": {
       "import_patterns": [r"import yourframework", r"from yourframework"],
       "file_patterns": ["yourframework.config", "yourframework.yaml"],
       "content_patterns": [r"YourFramework\(", r"yourframework\.create_app"]
   }
   ```

2. **Add to `FRAMEWORK_PATTERNS` in detector.py**

3. **Test detection:**
   ```bash
   python3 oracle/cli.py detect /path/to/yourframework/project
   ```

4. **Update documentation in oracle/README.md**

### Adding a New Brain Cell Module

1. **Choose appropriate cell type** (see [Brain Cell Metaphor](oracle/README.md#brain-cell-metaphor))

2. **Create module file:**
   ```python
   # oracle/your_module/cell_name.py
   """
   Cell Name (Brain Cell Type)

   Metaphor: [Biological function]
   Responsibility: [What this module does]
   """

   class CellName:
       def __init__(self, project_root: str):
           self.project_root = project_root

       def your_method(self):
           pass
   ```

3. **Integrate with existing systems**

4. **Document in oracle/README.md**

---

## Testing

### Manual Testing

Test Oracle on different project types:

1. **Small projects** (1-10 files)
2. **Medium projects** (100-1000 files)
3. **Large projects** (10,000+ files)
4. **Different frameworks** (Flask, Django, FastAPI, etc.)

### Performance Testing

```bash
# Time the initialization
time python3 oracle/cli.py init /path/to/project

# Check memory audit performance
time python3 oracle/project_oracle.py audit --quick
```

Expected performance:
- Init: <5 seconds for medium projects
- Audit: <3 seconds for quick check

---

## Documentation

### Adding Documentation

1. **User guides** go in `oracle/docs/`
2. **API documentation** goes in docstrings
3. **Examples** go in module docstrings or `oracle/docs/examples/`

### Documentation Style

- Use clear, concise language
- Provide code examples
- Include expected output
- Add troubleshooting sections where relevant

---

## Community

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for Oracle and its users

### Communication

- **GitHub Issues:** Bug reports and feature requests
- **Pull Requests:** Code contributions and discussions
- **Documentation:** Questions about usage and implementation

---

## Recognition

Contributors will be recognized in:
- Project README.md
- Release notes
- Git commit history

Thank you for contributing to Oracle! 🧠

---

## Questions?

If you have questions about contributing:
1. Check the [README.md](oracle/README.md)
2. Read the documentation in `oracle/docs/`
3. Open a GitHub issue with your question

---

*Oracle v1.0 - Brain Cell Architecture*
*Making Python project management intelligent*
