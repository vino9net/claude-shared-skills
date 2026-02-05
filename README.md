# Claude Code Skills Marketplace

A collection of reusable plugins for AI coding tools.

## TL;DR

1. Run `claude` to start Claude Code
2. Type `/plugins` to open the plugin manager
3. Navigate to **Marketplaces** → **Add Marketplace**
4. Enter `vino9net/vino9-claude-marketplace` as the source
5. Browse and enable the plugins you want

## Available Plugins

| Plugin | Source | Description |
|--------|--------|-------------|
| [boot-gcp-vm](plugins/boot-gcp-vm/) | local | Start a GCP VM and update local SSH config with its new IP address |
| [github-issues](plugins/github-issues/) | local | Read and comment on GitHub issues in Claude Code Web (where gh CLI doesn't work) |
| [python-dev](https://github.com/vino9net/claude-python-skill) | remote | Python project scaffolding, quality standards (ruff, ty), and test runner |

Plugins are registered in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). Local plugins live in `plugins/`, remote plugins are referenced by GitHub repo.

## Contributing

To add a plugin:
1. **Local**: create `plugins/<name>/SKILL.md` and add an entry to `.claude-plugin/marketplace.json`
2. **Remote**: just add a `.claude-plugin/marketplace.json` entry pointing to the GitHub repo

## License
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
