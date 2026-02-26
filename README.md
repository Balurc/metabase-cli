# mbase

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A command-line interface for [Metabase](https://www.metabase.com/).

---

## ✨ Features

- 🔐 Secure authentication with API keys
- 📊 Multiple output formats (table, JSON) for humans and automation
- ⚡ Fast, type-safe Python implementation
- 🔧 Cross-platform config storage
- 🤖 Perfect for AI agents and automation scripts

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Balurc/metabase-cli.git
cd metabase-cli

# Install with uv
uv venv
source .venv/bin/activate
uv pip install -e .

# Or with pip
pip install -e .
```

---

## 🚀 Quick Start

### 1. Authenticate

```bash
# Interactive login
mbase login

# Or with API key (for automation)
mbase login --token YOUR_API_KEY --url http://localhost:3000
```

### 2. Check Status

```bash
# View connection status
mbase status

# JSON output for scripts
mbase status --format json
```

### 3. Manage Configuration

```bash
# View current config
mbase config show

# Update settings
mbase config set timeout 60
mbase config set default_output_format json
```

---

## 📖 Commands

### Authentication

| Command | Description |
|---------|-------------|
| `mbase login` | Authenticate with Metabase (interactive) |
| `mbase login --token <key> --url <url>` | Authenticate with API key |
| `mbase logout` | Clear stored credentials |
| `mbase status` | Check authentication and connection |

### Configuration

| Command | Description |
|---------|-------------|
| `mbase config show` | Display current configuration |
| `mbase config set <key> <value>` | Update a configuration value |

### Global Options

| Option | Description |
|--------|-------------|
| `--format json` | Output in JSON format (for automation) |

---

## ⚙️ Configuration

Credentials and settings are stored in platform-appropriate locations:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/mbase/` |
| Linux | `~/.config/mbase/` |
| Windows | `%APPDATA%\mbase\` |

**Files:**
- `credentials.yaml` — API keys *(permissions: 600)*
- `config.yaml` — CLI settings

---

## 🛠️ Development

```bash
# Start Metabase locally
docker compose up -d

# Run tests
pytest tests/ -v

# Run code quality checks
mypy src/mbase
ruff check src/mbase
pre-commit run --all-files
```

---

## 🗺️ Roadmap

- [x] Stage 1: Authentication & Configuration
- [ ] Stage 2: Database & Schema Discovery
- [ ] Stage 3: Collections
- [ ] Stage 4: Questions (Read)
- [ ] Stage 5: SQL Runner
- [ ] Stage 6: Dashboards
- [ ] Stage 7: Models
- [ ] Stage 8: Questions (Write)

---

## 📄 License

[MIT](./LICENSE)
