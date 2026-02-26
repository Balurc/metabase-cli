# Metabase CLI

> A type-safe command-line interface for [Metabase](https://www.metabase.com/).

---

## ✨ Features

- 🔍 Browse databases, tables, collections, and saved questions
- 📝 Execute SQL queries from the terminal
- 📊 Export data to CSV, JSON, or pretty tables
- 🤖 Agent-friendly output formats
- ⚡ Built with Python, [Typer](https://typer.tiangolo.com/), and [Rich](https://rich.readthedocs.io/)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/metabase-cli.git
cd metabase-cli

# Install dependencies with uv
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
METABASE_URL=http://localhost:3000
METABASE_API_KEY=your_api_key_here
```

---

## 🚀 Usage

### Health Check

```bash
# Check Metabase health (default table format)
metabase-cli health check

# JSON output for agents/scripts
metabase-cli health check --format json
```

**Example JSON output:**

```json
{
  "status": "ok",
  "url": "http://localhost:3000/api",
  "timestamp": "2026-02-25T12:00:00Z",
  "response_time_ms": 45
}
```

### Output Formats

All commands support multiple output formats via the `--format` flag:

| Flag | Description |
|------|-------------|
| `--format table` | Pretty tables for humans *(default)* |
| `--format json` | Structured JSON for agents and automation |
| `--format csv` | CSV for data export *(where applicable)* |

```bash
# See all commands
metabase-cli --help
```

---

## 🛠️ Local Development

```bash
# Start Metabase locally
docker compose up -d

# Run tests
pytest
```

---

## 📄 License

[MIT](./LICENSE)
