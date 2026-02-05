---
name: github-issues
description: Read and comment on GitHub issues in Claude Code Web, where the local git proxy prevents gh CLI from working. Only active when CLAUDE_CODE_REMOTE=true.
allowed-tools: Bash(python*), Bash(git*), Read
---

# GitHub Issues for Claude Code Web

In Claude Code Web, the local git proxy breaks `gh issue` commands. This plugin provides a Python script that calls the GitHub API directly to read issues and post comments.

The script **only runs when `CLAUDE_CODE_REMOTE=true`** (set automatically by Claude Code Web). In any other environment it exits with a message to use `gh` CLI instead.

## Commands

```bash
# Get issue details
python gh_issue.py get <issue_number>

# Add comment to issue
python gh_issue.py comment <issue_number> "message"

# List all comments on an issue
python gh_issue.py comments <issue_number>
```

## Workflow

When a user says "work on issue #5":

1. **Read the issue:**
   ```bash
   python .claude/skills/shared/plugins/github-issues/gh_issue.py get 5
   ```

2. **Implement the changes** — Claude Code Web handles branch creation automatically

3. **Commit with proper message:**
   ```bash
   git commit -m "Fix issue #5: Brief description

   Fixes #5"
   ```

4. **Comment on the issue after pushing:**
   ```bash
   BRANCH=$(git branch --show-current)
   COMMIT=$(git rev-parse --short HEAD)
   python .claude/skills/shared/plugins/github-issues/gh_issue.py comment 5 \
     "Work completed in branch \`$BRANCH\` at commit $COMMIT. Ready for review."
   ```

## Authentication

Claude Code Web provides a `GITHUB_TOKEN` automatically. The script also tries `gh auth token` as a fallback.

## Error Handling

| Error | Fix |
|-------|-----|
| `No GitHub token found` | Set `GITHUB_TOKEN` env var |
| `404 Not Found` | Check issue number exists |
| `403 Forbidden` | Token needs `repo` scope |
