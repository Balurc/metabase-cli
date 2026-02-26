from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standardized error response for API and CLI errors."""

    message: str = Field(description="Human-readable error message")
    code: str = Field(description="Machine-readable error code")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when error occurred",
    )
    retryable: bool = Field(
        default=False, description="Whether the operation can be retried"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error details"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with ISO format timestamp."""
        data = self.model_dump()
        data["timestamp"] = self.timestamp.isoformat()
        return data


class HealthResponse(BaseModel):
    """Health check response with metadata."""

    status: str = Field(description="Health status")
    url: str = Field(description="Metabase API URL")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp"
    )
    response_time_ms: int = Field(description="Response time in milliseconds")
    version: Optional[str] = Field(default=None, description="Metabase version")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with ISO format timestamp."""
        data = self.model_dump()
        data["timestamp"] = self.timestamp.isoformat()
        return data
