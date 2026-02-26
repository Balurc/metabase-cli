"""Authentication commands for mbase CLI."""

import typer
from rich.console import Console
from rich.table import Table
from mbase.auth.manager import auth_manager
from mbase.formatters import get_formatter, OutputFormat

app = typer.Typer()
console = Console()


@app.command()
def login(
    token: str = typer.Option(
        None, "--token", "-t", help="API key for non-interactive login"
    ),
    url: str = typer.Option(
        None, "--url", "-u", help="Metabase URL (required with --token)"
    ),
):
    """Authenticate with Metabase."""
    if token:
        # Non-interactive login
        if not url:
            console.print("[red]Error: --url is required when using --token[/red]")
            raise typer.Exit(1)

        success = auth_manager.login_with_token(url, token)
        if not success:
            raise typer.Exit(1)
    else:
        # Interactive login
        success = auth_manager.login_interactive()
        if not success:
            raise typer.Exit(1)


@app.command()
def logout():
    """Logout and clear stored credentials."""
    auth_manager.logout()


@app.command()
def status(
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE, "--format", "-f", help="Output format"
    ),
):
    """Show authentication and connection status."""
    status_info = auth_manager.get_status()

    if status_info is None:
        console.print(
            "[yellow]Not authenticated. Run 'mbase login' to authenticate.[/yellow]"
        )
        raise typer.Exit(0)

    formatter = get_formatter(format)

    if format == OutputFormat.JSON:
        console.print(formatter.format_dict(status_info))
    else:
        # Table format
        table = Table(title="Authentication Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("URL", status_info["url"])
        table.add_row("API Key", status_info["api_key_masked"])

        if status_info.get("authenticated"):
            table.add_row("Status", "[green]✓ Connected[/green]")
            user = status_info.get("user", {})
            table.add_row(
                "User",
                f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
            )
            table.add_row("Email", user.get("email", "N/A"))

            health = status_info.get("health", {})
            table.add_row("Metabase Status", health.get("status", "unknown"))
        else:
            table.add_row("Status", "[red]✗ Disconnected[/red]")
            table.add_row("Error", status_info.get("error", "Unknown error"))

        console.print(table)


if __name__ == "__main__":
    app()
