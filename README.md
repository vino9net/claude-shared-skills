# Shared Claude Code Skills

This repository contains reusable Claude Code skills for Python development and Google Cloud Platform workflows.

## Skills Included

### python-dev
Python development standards and best practices using modern tooling:
- **ruff** for linting and formatting
- **ty** for type checking
- **uv** for package management
- Modern Python 3.10+ type annotations
- Pre-commit quality gates

### google-cloud
Google Cloud Platform workflows and best practices:
- Cloud Run deployments
- Cloud Storage management
- Authentication and IAM
- Project configuration
- Environment-specific deployments

## Usage

### As Git Submodule

Add to your project:
```bash
git submodule add <repo-url> .claude/skills/shared
git commit -m "Add shared Claude skills"
```

Update to latest:
```bash
git submodule update --remote .claude/skills/shared
```

### Skills Format

These skills follow the **SKILL.md open standard** (https://agentskills.io/), which is supported by:
- Claude Code
- Cursor
- GitHub Copilot
- Gemini CLI
- And 10+ other AI coding tools

## Version Control

Skills are versioned using Git tags:
- Check current version: `git describe --tags`
- List available versions: `git tag -l`

## Contributing

When updating skills:
1. Make changes to SKILL.md files
2. Test with Claude Code
3. Commit changes
4. Tag new version: `git tag -a v1.x.x -m "Description"`
5. Push: `git push && git push --tags`

## License

[Add your license here]
