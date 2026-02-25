# Metabase CLI

> A command-line interface for [Metabase](https://www.metabase.com/).

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
git clone [https://github.com/YOUR_USERNAME/metabase-cli.git](https://github.com/Balurc/metabase-cli.git)
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

```bash
# Check Metabase health
metabase-cli health check

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
