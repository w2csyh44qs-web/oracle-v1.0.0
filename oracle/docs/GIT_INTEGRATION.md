# Oracle Git Integration Guide

**Complete guide to Oracle's Git hooks and workflow integration**

Oracle integrates seamlessly with Git through pre-commit hooks that verify code quality, maintain context, and track changes—all automatically during your normal commit workflow.

---

## Overview

### What are Git Hooks?

Git hooks are scripts that run automatically at specific points in the Git workflow. Oracle uses **pre-commit hooks** to:

- Validate commit structure and quality
- Run health checks before commits
- Update development context
- Track file changes and patterns
- Log commit activity

### How Oracle Uses Git Hooks

```
Developer makes changes
        ↓
git add .
        ↓
git commit -m "message"
        ↓
Oracle Pre-Commit Hook Runs
        ↓
├─ Validates commit
├─ Runs health check
├─ Updates context
└─ Logs activity
        ↓
Commit proceeds (if valid)
```

**Time impact:** <5 seconds per commit

---

## Installation

### Automatic Installation (Recommended)

Git hooks are installed automatically during `oracle init`:

```bash
python3 oracle/cli.py init .
```

Output will include:
```
Step 7/8: Installing git hooks 🪝
  ✓ Pre-commit hooks installed
  💡 Hooks will run on: git commit
```

### Manual Installation

If hooks weren't installed during init:

```bash
python3 oracle/cli.py verify --install-hooks
```

Or use the HookManager directly:
```python
from oracle.validation.topoisomerase import HookManager
hook_mgr = HookManager('/path/to/project')
hook_mgr.install_hooks()
```

### Verification

Check if hooks are installed:

```bash
# Check for pre-commit config
ls -la .git/hooks/

# Should see:
# - pre-commit (executable script)
# - .pre-commit-config.yaml (configuration)
```

---

## Pre-Commit Hook Behavior

### What Happens on Commit

When you run `git commit`:

1. **Hook Triggers**: Git calls Oracle's pre-commit hook
2. **Health Check**: Quick audit runs (< 3 seconds)
3. **Validation**: Checks for common issues
4. **Context Update**: Development context refreshed
5. **Activity Log**: Commit logged to daemon
6. **Result**: Commit proceeds if all checks pass

### Success Flow

```bash
$ git commit -m "Add feature X"
Oracle Pre-Commit Check...
✓ Health score: 85
✓ No critical issues
✓ Context updated
[main abc1234] Add feature X
 2 files changed, 45 insertions(+)
```

**Total time:** ~4 seconds

### Failure Flow

```bash
$ git commit -m "wip"
Oracle Pre-Commit Check...
✗ Health score: 45 (critical)
✗ Found 3 critical issues:
  - Missing docstrings in api.py
  - Unused imports in utils.py
  - TODO markers in core.py

Commit blocked. Fix issues and try again.
```

**What happens:**
- Commit is **blocked** (not created)
- Issues are reported
- You fix issues and retry commit

---

## Hook Configuration

### Configuration File

`.pre-commit-config.yaml` in project root:

```yaml
repos:
  - repo: local
    hooks:
      - id: oracle-health-check
        name: Oracle Health Check
        entry: python3 oracle/validation/topoisomerase.py
        language: system
        stages: [commit]
        always_run: true
```

### Customization

Edit `.pre-commit-config.yaml` to adjust behavior:

**Skip certain files:**
```yaml
- id: oracle-health-check
  name: Oracle Health Check
  entry: python3 oracle/validation/topoisomerase.py
  language: system
  stages: [commit]
  always_run: true
  exclude: '^(docs/|tests/)'  # Skip docs and tests
```

**Change hook timing:**
```yaml
stages: [commit]        # Run on commit only
stages: [push]          # Run on push only
stages: [commit, push]  # Run on both
```

---

## Bypassing Hooks

### Temporarily Skip Hook

Use `--no-verify` flag:

```bash
git commit -m "WIP: temporary work" --no-verify
```

**When to use:**
- Temporary commits (WIP, experiments)
- Emergency hotfixes
- CI/CD environments (if desired)

**Warning:** Bypassing hooks means:
- No health check
- No context update
- No activity logging

### Disable Hooks Permanently

**Not recommended**, but possible:

```bash
# Remove pre-commit hook
rm .git/hooks/pre-commit

# Or remove config
rm .pre-commit-config.yaml
```

To re-enable:
```bash
python3 oracle/cli.py verify --install-hooks
```

---

## Health Check Details

### What is Checked

Pre-commit health check validates:

1. **Code Quality**
   - Missing docstrings
   - Unused imports
   - TODO/FIXME markers
   - Dead code detection

2. **Project Structure**
   - File organization
   - Layer violations (if applicable)
   - Missing dependencies

3. **Context Integrity**
   - Context file freshness
   - Memory observations validity
   - Configuration consistency

### Health Score Thresholds

- **85-100**: Commit proceeds (healthy)
- **70-84**: Commit proceeds with warning
- **50-69**: Commit blocked (warning)
- **0-49**: Commit blocked (critical)

**Customize thresholds** in `oracle/config/oracle_config.json`:
```json
{
  "validation": {
    "min_health_score": 70,
    "block_on_critical": true
  }
}
```

### Quick Check vs Full Audit

Pre-commit runs **quick check** by default:
- Takes 2-4 seconds
- Checks critical issues only
- Skips deep analysis

Full audit (manual) takes 10-30 seconds:
```bash
python3 oracle/project_oracle.py audit
```

---

## Integration with Daemon

### How Hooks and Daemon Interact

```
Git Hook Runs
     ↓
Updates oracle/data/.oracle_status.json
     ↓
Daemon Detects Update
     ↓
Logs Activity
     ↓
Dashboard Shows Update
```

**Result:** Commits appear in dashboard activity feed in real-time.

### Daemon Not Required

Git hooks work **independently** of daemon:
- Hooks run even if daemon is stopped
- Activity is logged to files
- Daemon picks up logs when restarted

---

## Workflow Examples

### Standard Commit Workflow

```bash
# Make changes
vim app.py

# Stage changes
git add app.py

# Commit (hook runs automatically)
git commit -m "Add user authentication"

# Output:
# Oracle Pre-Commit Check...
# ✓ Health score: 90
# ✓ No critical issues
# [main abc1234] Add user authentication
#  1 file changed, 50 insertions(+)

# Push
git push origin main
```

**Total time:** ~5-10 seconds (4s for hook, rest is git)

### WIP Commit (Skip Hook)

```bash
# Temporary work, skip hook
git commit -m "WIP: experimenting with API" --no-verify

# Later, proper commit with hook
git commit --amend -m "Implement new API endpoint"
```

### Fix Hook Failure

```bash
# Attempt commit
git commit -m "Add feature"

# Output:
# ✗ Health score: 55
# ✗ Critical: Missing docstring in api.py

# Fix issue
vim api.py  # Add docstring

# Retry commit
git commit -m "Add feature"

# Output:
# ✓ Health score: 85
# [main abc1234] Add feature
```

### Amend Commit (Hook Runs Again)

```bash
# Initial commit
git commit -m "Add feature"

# Amend commit (hook runs again)
git commit --amend -m "Add feature with tests"

# Oracle hook runs on amended commit too
```

---

## CI/CD Integration

### Running Hooks in CI

**Option 1: Enable hooks in CI**
```yaml
# .github/workflows/test.yml (GitHub Actions)
- name: Install Oracle Hooks
  run: python3 oracle/cli.py verify --install-hooks

- name: Run Tests
  run: pytest

# Commits in CI will trigger hooks
```

**Option 2: Skip hooks in CI**
```yaml
# Use --no-verify for CI commits
- name: Commit Results
  run: git commit -m "CI: test results" --no-verify
```

**Recommendation:** Run Oracle health check as separate CI step:
```yaml
- name: Oracle Health Check
  run: python3 oracle/project_oracle.py audit
```

### Pre-Push Hooks

Oracle currently uses pre-commit hooks. To add pre-push:

Edit `.pre-commit-config.yaml`:
```yaml
- id: oracle-health-check
  stages: [commit, push]  # Run on both
```

---

## Troubleshooting

### Hook Doesn't Run

**Symptom:** Commits succeed without Oracle output

**Diagnosis:**
```bash
# Check if hook exists
ls -la .git/hooks/pre-commit

# Check if executable
stat -f "%Sp" .git/hooks/pre-commit  # macOS
stat -c "%a" .git/hooks/pre-commit   # Linux
```

**Solutions:**
```bash
# Reinstall hooks
python3 oracle/cli.py verify --install-hooks

# Make hook executable
chmod +x .git/hooks/pre-commit
```

### Hook Blocks All Commits

**Symptom:** Every commit fails health check

**Diagnosis:**
```bash
# Run manual audit to see issues
python3 oracle/project_oracle.py audit
```

**Solutions:**
```bash
# Fix reported issues, OR

# Lower health threshold in config
# Edit oracle/config/oracle_config.json:
{
  "validation": {
    "min_health_score": 50
  }
}

# OR skip hook temporarily
git commit -m "message" --no-verify
```

### Hook is Too Slow

**Symptom:** Commits take >10 seconds

**Cause:** Large project or slow health check

**Solutions:**
```bash
# Use faster health check
# Edit oracle/validation/topoisomerase.py:
# Change: audit --quick
# To: audit --minimal (if available)

# OR skip certain checks in config
```

### Hook Fails with Import Error

**Symptom:**
```
Traceback (most recent call last):
  File "oracle/validation/topoisomerase.py", line 10, in <module>
    from oracle.core import HealthAuditor
ImportError: No module named 'oracle'
```

**Cause:** Python path not set correctly in hook

**Solution:**
Edit `.git/hooks/pre-commit`:
```bash
#!/bin/bash
export PYTHONPATH="/path/to/project:$PYTHONPATH"
python3 oracle/validation/topoisomerase.py
```

### Commits Succeed But No Dashboard Update

**Symptom:** Hook runs, commit succeeds, but dashboard shows no activity

**Cause:** Daemon not running or status file not updated

**Solution:**
```bash
# Start daemon
python3 oracle/cli.py daemon start

# Verify daemon is running
python3 oracle/cli.py daemon status
```

---

## Advanced Usage

### Custom Hook Logic

Extend Oracle's pre-commit hook:

**Edit `.git/hooks/pre-commit`:**
```bash
#!/bin/bash

# Run Oracle health check
python3 oracle/validation/topoisomerase.py
ORACLE_RESULT=$?

# Run custom checks
python3 scripts/custom_lint.py
CUSTOM_RESULT=$?

# Block commit if either fails
if [ $ORACLE_RESULT -ne 0 ] || [ $CUSTOM_RESULT -ne 0 ]; then
    exit 1
fi

exit 0
```

### Conditional Hooks

Run Oracle hook only on certain branches:

```bash
#!/bin/bash

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "develop" ]; then
    # Run Oracle hook on main/develop only
    python3 oracle/validation/topoisomerase.py
    exit $?
fi

# Skip hook on feature branches
exit 0
```

### Multi-Project Hooks

Use Oracle hooks across multiple projects:

**Shared hook script:**
```bash
# ~/.git-templates/hooks/pre-commit
#!/bin/bash

PROJECT_ROOT=$(git rev-parse --show-toplevel)

if [ -f "$PROJECT_ROOT/oracle/validation/topoisomerase.py" ]; then
    python3 "$PROJECT_ROOT/oracle/validation/topoisomerase.py"
fi
```

**Configure git to use template:**
```bash
git config --global init.templatedir ~/.git-templates
```

Now all new repos get Oracle hooks automatically.

---

## Best Practices

### Development Workflow

1. **Let hooks run on every commit** (don't use `--no-verify` by default)
2. **Fix issues immediately** when hook fails
3. **Use meaningful commit messages** (Oracle logs these)
4. **Keep commits atomic** (single logical change per commit)

### Team Collaboration

1. **Commit hooks to repo**:
   ```bash
   git add .pre-commit-config.yaml
   git commit -m "Add Oracle pre-commit hooks"
   ```

2. **Document hook setup in README**:
   ```markdown
   ## Setup
   1. Clone repo
   2. Run: python3 oracle/cli.py init .
   3. Hooks install automatically
   ```

3. **Share Oracle config**:
   ```bash
   git add oracle/config/oracle_config.json
   git commit -m "Add Oracle configuration"
   ```

### When to Bypass Hooks

**Acceptable:**
- WIP commits on feature branches
- Experimental commits that will be squashed
- Emergency hotfixes (then fix issues immediately after)

**Not acceptable:**
- Regularly skipping hooks to avoid fixing issues
- Bypassing hooks because they're "slow" (optimize instead)
- Skipping hooks in production/main branches

---

## Hook Manager API

### Python API

```python
from oracle.validation.topoisomerase import HookManager

# Initialize
hook_mgr = HookManager('/path/to/project')

# Install hooks
success = hook_mgr.install_hooks()

# Check if installed
is_installed = hook_mgr.is_installed()

# Uninstall hooks
hook_mgr.uninstall_hooks()

# Get hook status
status = hook_mgr.get_status()
```

### CLI Commands

```bash
# Install hooks (during init)
python3 oracle/cli.py init .

# Install hooks (standalone)
python3 oracle/cli.py verify --install-hooks

# Check hook status
python3 oracle/cli.py verify --check-hooks

# Uninstall hooks
python3 oracle/cli.py verify --uninstall-hooks
```

---

## FAQ

**Q: Do hooks run on `git commit --amend`?**
A: Yes, pre-commit hooks run on amended commits too.

**Q: Do hooks run on `git rebase`?**
A: Depends on rebase type. Interactive rebase (`-i`) may skip hooks.

**Q: Can I use Oracle hooks with other pre-commit tools?**
A: Yes, Oracle uses standard `.pre-commit-config.yaml` format. Compatible with pre-commit.com framework.

**Q: Do hooks work on Windows?**
A: Yes, but requires Git Bash or WSL. Native Windows support is limited.

**Q: Will hooks slow down my commits significantly?**
A: No, quick health check takes <5 seconds. Full audit takes longer but isn't run on commits.

**Q: Can I customize which files hooks check?**
A: Yes, use `exclude` pattern in `.pre-commit-config.yaml`.

**Q: Do I need daemon running for hooks to work?**
A: No, hooks work independently. But daemon enhances integration by logging activity.

**Q: Can hooks prevent bad commits?**
A: Yes, if health score is too low, commit is blocked.

**Q: How do I update hooks after Oracle update?**
A: Run `python3 oracle/cli.py verify --install-hooks` again.

---

*Oracle v1.0 - Brain Cell Architecture*
*Automated Git Workflow Integration*
