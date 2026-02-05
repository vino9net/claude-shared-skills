# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

A plugin marketplace of reusable Claude Code plugins following the **SKILL.md open standard** (https://agentskills.io/). Plugins can be local (in `plugins/`) or referenced from remote GitHub repos via `.claude-plugin/marketplace.json`.

## Repository Architecture

### Structure

```
.
├── .claude-plugin/
│   └── marketplace.json              # Marketplace catalog
├── plugins/
│   ├── boot-gcp-vm/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json           # Plugin manifest
│   │   └── skills/
│   │       └── boot-gcp-vm/
│   │           └── SKILL.md
│   └── github-issues/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── github-issues/
│               ├── SKILL.md
│               └── gh_issue.py
├── CLAUDE.md
├── README.md
└── .claude/settings.json
```

### Marketplace Catalog (`.claude-plugin/marketplace.json`)

All plugins are registered in `.claude-plugin/marketplace.json` using the Claude Code marketplace format. Plugins can be:

- **Local**: source files live in `plugins/<name>/`, referenced with `"source": "./plugins/<name>"`
- **Remote**: referenced by GitHub repo, source lives elsewhere

```json
{
  "name": "vino9-claude-marketplace",
  "owner": { "name": "vino9net" },
  "plugins": [
    {
      "name": "boot-gcp-vm",
      "description": "Start a GCP VM and update local SSH config",
      "source": "./plugins/boot-gcp-vm"
    },
    {
      "name": "python-dev",
      "source": { "source": "github", "repo": "vino9net/claude-python-skill" }
    }
  ]
}
```

### Plugin Manifest (`plugin.json`)

Each local plugin has its own `.claude-plugin/plugin.json` that declares the plugin name, description, and references its skills:

```json
{
  "name": "boot-gcp-vm",
  "description": "Start a GCP VM and update local SSH config",
  "strict": false,
  "skills": ["./skills/boot-gcp-vm"]
}
```

### Plugins

**boot-gcp-vm** (local): Start GCP VMs and update SSH config
- Start a Compute Engine VM and update `~/.ssh/config` with the new IP
- Quick reference for listing, stopping, and connecting to VMs

**github-issues** (local): Read and comment on GitHub issues in Claude Code Web
- Only active when `CLAUDE_CODE_REMOTE=true` (set by Claude Code Web)
- Works around the local git proxy that breaks `gh` CLI
- Python script (stdlib only) calling GitHub API directly

**python-dev** (remote → `vino9net/claude-python-skill`): Python project scaffolding, quality standards, and test runner
- `/py:scaffold` — generate new Python projects with components (API, ORM, CLI)
- Quality skill auto-invoked for linting (ruff), type checking (ty), formatting
- `/py:pytest` — run tests in isolated subagent
- Uses `uv`, Python 3.13+, src layout

## Working with This Repository

### Adding a Local Plugin

1. Create the plugin directory structure:
   ```
   plugins/<plugin-name>/
   ├── .claude-plugin/
   │   └── plugin.json
   └── skills/
       └── <skill-name>/
           └── SKILL.md
   ```
2. Add an entry to `.claude-plugin/marketplace.json` with `"source": "./plugins/<plugin-name>"`

### Adding a Remote Plugin

1. Add an entry to `.claude-plugin/marketplace.json` with a GitHub source: `"source": {"source": "github", "repo": "owner/repo"}`
2. No local files needed — the source lives in the referenced repo

### SKILL.md Format

Each skill follows the SKILL.md standard with:
- **Frontmatter**: `name`, `description`, `allowed-tools` in YAML format
- **Content**: Detailed instructions, code examples, common patterns
- **Workflows**: Step-by-step procedures for common tasks

### Version Control

Plugins use Git tags for versioning:
```bash
git describe --tags
git tag -a v1.x.x -m "Description of changes"
git push && git push --tags
```

## Key Design Principles

1. **Self-Contained**: Each plugin works standalone without requiring other plugins
2. **Clear Triggers**: Description field states when to use the plugin
3. **Local or Remote**: Plugins can live in this repo or be referenced from GitHub
4. **Tool Restrictions**: `allowed-tools` field limits what the plugin can execute

## License

Apache License 2.0
