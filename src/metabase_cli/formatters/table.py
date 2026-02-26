from typing import Any, Dict, List, Optional, Union
from rich.console import Console
from rich.table import Table
from metabase_cli.formatters.base import BaseFormatter


class TableFormatter(BaseFormatter):
    """Format output as pretty Rich tables for humans."""

    def __init__(self):
        self.console = Console()

    def format_dict(
        self, data: Dict[str, Any], title: Optional[str] = None
    ) -> Union[str, Table]:
        """Format a dictionary as a clean table - returns Table object for colors."""
        table = Table(title=title)
        table.add_column("Property", style="cyan")  # Cyan for headers
        table.add_column("Value", style="green")  # Green for values

        for key, value in data.items():
            table.add_row(str(key), str(value))

        return table  # Return Table object, not string

    def format_list(
        self, data: List[Dict[str, Any]], title: Optional[str] = None
    ) -> Union[str, Table]:
        """Format a list of dictionaries as a table."""
        if not data:
            return "No data found."

        table = Table(title=title)

        first_item = data[0]
        for key in first_item.keys():
            table.add_column(str(key), style="cyan")

        for item in data:
            row_values = [str(item.get(k, "")) for k in first_item.keys()]
            table.add_row(*row_values)

        return table

    def format_error(self, error: Dict[str, Any]) -> Union[str, Table]:
        """Format an error as a table."""
        table = Table(title="Error", style="red")
        table.add_column("Property", style="red")
        table.add_column("Value", style="red")

        for key, value in error.items():
            table.add_row(str(key), str(value))

        return table
