"""Pydantic models for configuration and credentials."""

from datetime import datetime
from pydantic import BaseModel, Field


class Credentials(BaseModel):
    """Stored credentials for Metabase authentication."""

    url: str = Field(description="Metabase base URL")
    api_key: str = Field(description="Metabase API key")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When credentials were saved"
    )

    def mask_api_key(self) -> str:
        """Return masked API key for display."""
        if len(self.api_key) <= 8:
            return "***"
        return f"{self.api_key[:4]}...{self.api_key[-4:]}"


class Config(BaseModel):
    """CLI configuration settings."""

    default_output_format: str = Field(
        default="table", description="Default output format (table, json, csv)"
    )
    timeout: int = Field(default=30, description="Request timeout in seconds")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")


class Profile(BaseModel):
    """A configured Metabase connection profile."""

    name: str = Field(description="Profile name (e.g., 'prod', 'staging')")
    credentials: Credentials
    config: Config = Field(default_factory=Config)
    is_active: bool = Field(default=False)
