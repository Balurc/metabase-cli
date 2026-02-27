"""Table inspection commands."""

import typer
from rich.console import Console
from rich.table import Table

from mbase.api.databases import DatabasesAPI
from mbase.formatters import get_formatter, OutputFormat

app = typer.Typer()
console = Console()


@app.command()
def inspect(
    table_id: int = typer.Argument(..., help="Table ID"),
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE,
        "--format",
        "-f",
        help="Output format",
    ),
):
    """Inspect a table - show metadata and columns."""
    try:
        api = DatabasesAPI()
        metadata = api.get_table_metadata(table_id)

        table_info = metadata["table"]
        fields = metadata["fields"]
        fields_count = metadata["fields_count"]

        formatter = get_formatter(format)

        if format == OutputFormat.JSON:
            # Build JSON output
            output = {
                "id": table_info["id"],
                "name": table_info["name"],
                "display_name": table_info["display_name"],
                "schema_name": table_info["schema_name"],
                "data_layer": table_info["data_layer"],
                "description": table_info["description"],
                "active": table_info["active"],
                "view_count": table_info["view_count"],
                "created_at": table_info["created_at"],
                "updated_at": table_info["updated_at"],
                "db_id": table_info["db_id"],
                "db_name": table_info["db_name"],
                "db_engine": table_info["db_engine"],
                "fields_count": fields_count,
                "fields": [
                    {
                        "id": f.id,
                        "name": f.name,
                        "display_name": f.display_name,
                        "base_type": f.base_type,
                        "semantic_type": f.semantic_type,
                    }
                    for f in fields
                ],
            }
            console.print(formatter.format_dict(output))
        else:
            # Table format - Section 1: Metadata
            meta_table = Table(title=f"Table Inspection: {table_info['display_name']}")
            meta_table.add_column("Property", style="cyan")
            meta_table.add_column("Value", style="green")

            # Format database display
            db_display = table_info["db_name"] or "N/A"
            if table_info["db_engine"]:
                db_display += f" ({table_info['db_engine']})"

            # Format dates
            updated = "N/A"
            if table_info["updated_at"]:
                from datetime import datetime

                if isinstance(table_info["updated_at"], str):
                    dt = datetime.fromisoformat(
                        table_info["updated_at"].replace("Z", "+00:00")
                    )
                    updated = dt.strftime("%Y-%m-%d %H:%M")
                else:
                    updated = table_info["updated_at"].strftime("%Y-%m-%d %H:%M")

            # Truncate description
            desc = table_info["description"] or ""
            if len(desc) > 50:
                desc = desc[:47] + "..."
            elif not desc:
                desc = "N/A"

            meta_table.add_row("Display Name", table_info["display_name"] or "N/A")
            meta_table.add_row("Database", db_display)
            meta_table.add_row("Schema", table_info["schema_name"] or "N/A")
            meta_table.add_row("Data Layer", table_info["data_layer"] or "N/A")
            meta_table.add_row("Description", desc)
            meta_table.add_row("Active", "Yes" if table_info["active"] else "No")
            meta_table.add_row("Column Count", str(fields_count))
            meta_table.add_row("View Count", str(table_info["view_count"]))
            meta_table.add_row("Last Updated", updated)

            console.print(meta_table)
            console.print()

            # Section 2: Fields Summary
            fields_table = Table(title=f"Columns ({fields_count} total)")
            fields_table.add_column("ID", style="cyan", justify="right", width=4)
            fields_table.add_column("Name", style="green", width=15)
            fields_table.add_column("Base Type", style="blue", width=15)
            fields_table.add_column("Semantic Type", style="yellow", width=20)

            for field in fields:
                # Clean up base_type (remove "type/" prefix)
                base_type = (
                    field.base_type.replace("type/", "") if field.base_type else "N/A"
                )

                # Clean up semantic_type
                semantic = (
                    field.semantic_type.replace("type/", "")
                    if field.semantic_type
                    else ""
                )

                fields_table.add_row(
                    str(field.id),
                    field.name[:15] if len(field.name) > 15 else field.name,
                    base_type,
                    semantic,
                )

            console.print(fields_table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
