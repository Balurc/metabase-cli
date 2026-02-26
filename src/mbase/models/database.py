"""Database models for Metabase."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Database(BaseModel):
    """Metabase database model."""

    id: int = Field(description="Database ID")
    name: str = Field(description="Database display name")
    engine: str = Field(description="Database engine (postgres, mysql, h2, etc.)")
    description: Optional[str] = Field(default=None, description="Database description")
    is_sample: bool = Field(default=False, description="Is this the sample database")
    created_at: Optional[datetime] = Field(
        default=None, description="When database was added"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="When database was last updated/synced"
    )
    timezone: Optional[str] = Field(default=None, description="Database timezone")
    is_full_sync: bool = Field(default=True, description="Is schema fully synced")

    @property
    def display_type(self) -> str:
        """Return 'sample' or 'connected' based on is_sample."""
        return "sample" if self.is_sample else "connected"
