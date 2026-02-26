"""Table formatter for human-readable output."""

from typing import Any, Dict, List, Optional, Union
from rich.console import Console
from rich.table import Table
from mbase.formatters.base import BaseFormatter


class TableFormatter(BaseFormatter):
    """Format output as pretty Rich tables for humans."""

    def __init__(self):
        self.console = Console()

    def format_dict(
        self, data: Dict[str, Any], title: Optional[str] = None
    ) -> Union[str, Table]:
        """Format a dictionary as a table."""
        table = Table(title=title)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        return table

    def format_list(
        self, data: List[Dict[str, Any]], title: Optional[str] = None
    ) -> Union[str, Table]:
        """Format a list of dictionaries as a table."""
        if not data:
            return "No data found."

        table = Table(title=title)

        # Use keys from first item as column headers
        first_item = data[0]
        for key in first_item.keys():
            table.add_column(str(key), style="cyan")

        # Add rows
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
