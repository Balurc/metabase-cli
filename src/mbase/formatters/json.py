"""JSON formatter for machine-readable output."""

import json
from typing import Any, Dict, List, Optional
from mbase.formatters.base import BaseFormatter


class JSONFormatter(BaseFormatter):
    """Format output as JSON for agents and programmatic use."""

    def __init__(self, indent: int = 2):
        self.indent = indent

    def format_dict(self, data: Dict[str, Any], title: Optional[str] = None) -> str:
        """Format a dictionary as JSON."""
        return json.dumps(data, indent=self.indent, default=str)

    def format_list(
        self, data: List[Dict[str, Any]], title: Optional[str] = None
    ) -> str:
        """Format a list as JSON."""
        return json.dumps(data, indent=self.indent, default=str)

    def format_error(self, error: Dict[str, Any]) -> str:
        """Format an error as JSON."""
        error_wrapper = {"error": error}
        return json.dumps(error_wrapper, indent=self.indent, default=str)
