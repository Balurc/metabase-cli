"""Database management commands."""

import typer
from rich.console import Console
from rich.table import Table

from mbase.api.databases import DatabasesAPI
from mbase.formatters import get_formatter, OutputFormat

app = typer.Typer()
console = Console()


@app.command()
def list(
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE,
        "--format",
        "-f",
        help="Output format",
    ),
):
    """List all connected databases."""
    try:
        api = DatabasesAPI()
        databases = api.list_databases()

        if not databases:
            console.print("[yellow]No databases found.[/yellow]")
            return

        formatter = get_formatter(format)

        if format == OutputFormat.JSON:
            # Output as JSON array with all fields
            output = [db.model_dump() for db in databases]
            console.print(formatter.format_list(output))
        else:
            # Table format with all columns
            table = Table(title="Databases")
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Name", style="green")
            table.add_column("Engine", style="blue")
            table.add_column("Type", style="yellow")
            table.add_column("Description", style="magenta", max_width=30)
            table.add_column("Created", style="dim")
            table.add_column("Updated", style="dim")

            for db in databases:
                # Truncate description
                desc = db.description or ""
                if len(desc) > 27:
                    desc = desc[:27] + "..."
                elif not desc:
                    desc = "N/A"

                # Format dates
                created = db.created_at.strftime("%Y-%m-%d") if db.created_at else "N/A"
                updated = db.updated_at.strftime("%Y-%m-%d") if db.updated_at else "N/A"

                table.add_row(
                    str(db.id),
                    db.name,
                    db.engine,
                    db.display_type,
                    desc,
                    created,
                    updated,
                )

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
