"""Main entry point for mbase CLI."""

import typer
from rich.console import Console
from mbase.commands import auth, config, database, table

app = typer.Typer(
    name="mbase",
    help="A professional CLI for Metabase",
    add_completion=True,
)
console = Console()

# Add subcommands
app.add_typer(auth.app, name="auth", help="Authentication commands")
app.add_typer(config.app, name="config", help="Configuration commands")
app.add_typer(database.app, name="database", help="Database operations")
app.add_typer(table.app, name="table", help="Table operations")

# Add direct commands
app.command()(auth.login)
app.command()(auth.logout)
app.command()(auth.status)


@app.callback()
def callback():
    """mbase - Professional CLI for Metabase."""
    pass


@app.command()
def version():
    """Show version information."""
    console.print("[bold]mbase[/bold] version 0.1.0")


if __name__ == "__main__":
    app()
