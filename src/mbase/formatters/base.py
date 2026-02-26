"""Base formatter interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from rich.table import Table


class OutputFormat(str, Enum):
    """Supported output formats."""

    TABLE = "table"
    JSON = "json"
    CSV = "csv"


class BaseFormatter(ABC):
    """Abstract base class for output formatters."""

    @abstractmethod
    def format_dict(
        self, data: Dict[str, Any], title: Optional[str] = None
    ) -> Union[str, Table]:
        """Format a dictionary."""
        pass

    @abstractmethod
    def format_list(
        self, data: List[Dict[str, Any]], title: Optional[str] = None
    ) -> Union[str, Table]:
        """Format a list of dictionaries."""
        pass

    @abstractmethod
    def format_error(self, error: Dict[str, Any]) -> Union[str, Table]:
        """Format an error response."""
        pass
