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


@app.command()
def tables(
    database_id: int = typer.Argument(..., help="Database ID"),
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE,
        "--format",
        "-f",
        help="Output format",
    ),
):
    """List all tables in a database."""
    try:
        api = DatabasesAPI()
        tables = api.list_tables(database_id)

        if not tables:
            console.print(
                f"[yellow]No tables found in database {database_id}.[/yellow]"
            )
            return

        formatter = get_formatter(format)

        if format == OutputFormat.JSON:
            # Output as JSON array with all fields
            output = [table.model_dump() for table in tables]
            console.print(formatter.format_list(output))
        else:
            # Get database name for title
            try:
                db = api.get_database(database_id)
                db_name = db.name
            except Exception:
                db_name = f"ID: {database_id}"

            # Table format with 6 columns
            table_view = Table(title=f"Tables in {db_name}")
            table_view.add_column("ID", style="cyan", justify="right", width=4)
            table_view.add_column("Name", style="green", width=15)
            table_view.add_column("Display Name", style="blue", width=15)
            table_view.add_column("Schema", style="yellow", width=10)
            table_view.add_column("Active", style="magenta", width=6)
            table_view.add_column("Last Updated", style="dim", width=19)

            for table in tables:
                # Format updated_at datetime
                updated = "N/A"
                if table.updated_at:
                    updated = table.updated_at.strftime("%Y-%m-%d %H:%M")

                table_view.add_row(
                    str(table.id),
                    table.name[:15] if len(table.name) > 15 else table.name,
                    table.display_name[:15]
                    if len(table.display_name) > 15
                    else table.display_name,
                    table.schema_name or "N/A",
                    "Yes" if table.active else "No",
                    updated,
                )

            console.print(table_view)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
