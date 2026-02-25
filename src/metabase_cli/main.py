import typer
from metabase_cli.commands import health

app = typer.Typer(
    name="metabase-cli",
    help="CLI for Metabase",
    add_completion=False,
)

app.add_typer(health.app, name="health", help="Health check commands")


@app.callback()
def callback():
    """Metabase CLI - Interact with Metabase from the command line."""
    pass


if __name__ == "__main__":
    app()
