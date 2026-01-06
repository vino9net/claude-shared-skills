---
name: python-dev-standards
description: Apply Python development standards using ruff, ty, and uv. Use when writing Python code, reviewing code quality, or preparing commits. Reads Python version from .python-version file.
allowed-tools: Bash(ruff*), Bash(ty*), Bash(uv*), Bash(pytest*), Read, Grep, Edit
---

# Python Development Standards

This skill ensures Python code follows team standards using standardized tooling: **ruff** (linting/formatting), **ty** (type checking), and **uv** (package management).

## Core Principles

1. **Format and lint ONLY before commits** - Not during normal code changes
2. **Detect Python version** from `.python-version` file in project root
3. **Use standardized tools** - ruff, ty, uv (no alternatives)
4. **Modern type annotations** - Python 3.10+ syntax

## When to Apply Standards

### During Development (Normal Code Changes)
- Write code following PEP8 conventions
- Use modern type annotation syntax:
  - `str | None` instead of `Optional[str]`
  - `list[str]` instead of `List[str]`
  - `dict[str, int]` instead of `Dict[str, int]`
- Import statements at top of file
- Keep line length reasonable (will be enforced by ruff later)

**DO NOT run linting/formatting during normal development** - This saves time and reduces token usage from failures.

### Before Commits (Pre-Commit Quality Gates)

When preparing to commit code, run these checks in order:

1. **Format with ruff:**
   ```bash
   ruff format .
   ```

2. **Lint with ruff (auto-fix):**
   ```bash
   ruff check . --fix
   ```

3. **Check for remaining linting issues:**
   ```bash
   ruff check .
   ```

4. **Type checking with ty:**
   ```bash
   ty check
   ```

5. **Run tests:**
   ```bash
   pytest
   ```

Only proceed with commit if ALL checks pass.

## Project Configuration Detection

### Python Version
Read from `.python-version` file in project root:
```bash
cat .python-version
```

Use this version for tooling decisions and dependency compatibility.

### Project Settings
Check `pyproject.toml` for:
- Line length configuration (typically 88-90 characters)
- Ruff-specific settings
- Test configuration
- Dependencies managed by uv

### Project-Specific Rules
Check `CLAUDE.md` in project for:
- Additional project-specific standards
- Domain-specific conventions
- Architecture guidelines

## Code Quality Standards

### Line Length
- Configured in `pyproject.toml` (typically 90 characters)
- ruff enforces this automatically

### Indentation
- 4 spaces (Python standard)
- Never use tabs

### Import Organization
- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetically sorted within each group
- Imports ALWAYS at top of file

### Type Annotations (Python 3.10+)

**Use modern syntax:**
```python
# ✅ Correct - Modern syntax
def process(data: str | None) -> list[dict[str, int]]:
    items: set[str] = set()
    return []

# ❌ Incorrect - Old syntax
from typing import Optional, List, Dict, Set
def process(data: Optional[str]) -> List[Dict[str, int]]:
    items: Set[str] = set()
    return []
```

**Remove unused typing imports** when converting to modern syntax.

### PEP8 Standards
- Follow all PEP8 conventions
- ruff will enforce these automatically

## Workflow Integration

### Normal Code Changes
```
Write Code → Edit Files → Continue Development
```
**No linting/formatting runs** - Focus on functionality.

### Before Commit
```
1. ruff format .
2. ruff check . --fix
3. ruff check .
4. ty check
5. pytest
6. Commit if all pass
```

### After Failed Checks
- Read error messages carefully
- Fix issues one at a time
- Re-run the specific check that failed
- Continue through the checklist

## Package Management with uv

### Installing Dependencies
```bash
uv add package-name
```

### Syncing Dependencies
```bash
uv sync
```

### Running Commands in Virtual Environment
```bash
uv run python script.py
uv run pytest
```

## Common Scenarios

### Scenario 1: New Feature Development
1. Write code with proper type hints
2. Ensure imports are at top
3. Follow PEP8 conventions naturally
4. **Do not run linting yet**
5. When feature is complete and ready to commit:
   - Run full pre-commit checklist
   - Fix any issues
   - Commit

### Scenario 2: Bug Fix
1. Identify and fix the bug
2. Add/update tests
3. Before committing:
   - Run pre-commit checklist
   - Ensure tests pass
   - Commit

### Scenario 3: Code Review
1. Read the code changes
2. Check for:
   - Modern type annotations
   - Proper import organization
   - PEP8 compliance
   - Test coverage
3. Suggest improvements
4. **Do not run linting** unless reviewing for commit

### Scenario 4: Failed Linting
If ruff check fails:
1. Read the specific errors
2. Run `ruff check . --fix` to auto-fix simple issues
3. Manually fix remaining issues
4. Re-run `ruff check .`
5. Continue to next check (ty check)

### Scenario 5: Failed Type Checking
If ty check fails:
1. Read type errors carefully
2. Add missing type annotations
3. Fix incorrect type usage
4. Re-run `ty check`
5. Continue to next check (pytest)

## File Types

### Apply standards to:
- `**/*.py` - All Python files in source
- Tests in `tests/` directory
- Scripts in project root

### Do NOT apply to:
- `*.js`, `*.html`, `*.md` - Non-Python files
- One-off scripts outside main project
- Third-party code in `vendor/` or similar

## Error Handling

### When Pre-Commit Checks Fail
1. **Do not force commit** - Fix the issues
2. Read error messages completely
3. Fix issues methodically
4. Re-run checks
5. Only commit when all pass

### When Tests Fail
1. Identify the failing test
2. Debug the issue
3. Fix the code or test
4. Re-run tests
5. Ensure all pass before committing

## Integration with CLAUDE.md

This skill works alongside project-specific `CLAUDE.md` files:
- SKILL.md: General Python standards (this file)
- CLAUDE.md: Project-specific rules and conventions

When both exist, follow both - CLAUDE.md may provide additional context like:
- Project Python version
- GCP project settings
- Domain-specific naming conventions
- Architecture decisions

## Tools Reference

### ruff
- **Format:** `ruff format <file>` or `ruff format .`
- **Lint:** `ruff check <file>` or `ruff check .`
- **Auto-fix:** `ruff check . --fix`
- **Config:** `pyproject.toml`

### ty
- **Check types:** `ty check`
- **Check specific file:** `ty check <file>`

### uv
- **Add package:** `uv add <package>`
- **Sync deps:** `uv sync`
- **Run command:** `uv run <command>`

### pytest
- **Run all tests:** `pytest`
- **Run specific test:** `pytest tests/test_file.py`
- **Verbose:** `pytest -v`

## Remember

- ✅ Write clean code during development
- ✅ Run full checks before commits
- ❌ Don't run linting during normal changes
- ✅ Fix all issues before committing
- ✅ Read .python-version for project Python version
- ✅ Check pyproject.toml for project config
- ✅ Check CLAUDE.md for project-specific rules
