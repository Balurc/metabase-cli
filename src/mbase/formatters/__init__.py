"""Output formatters for mbase CLI."""

from mbase.formatters.base import BaseFormatter, OutputFormat
from mbase.formatters.table import TableFormatter
from mbase.formatters.json import JSONFormatter


def get_formatter(format_type: OutputFormat) -> BaseFormatter:
    """Factory function to get the appropriate formatter."""
    if format_type == OutputFormat.TABLE:
        return TableFormatter()
    elif format_type == OutputFormat.JSON:
        return JSONFormatter()
    else:
        raise ValueError(f"Unknown format: {format_type}")


__all__ = [
    "BaseFormatter",
    "OutputFormat",
    "TableFormatter",
    "JSONFormatter",
    "get_formatter",
]
