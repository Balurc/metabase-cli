"""Table models for Metabase."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Table(BaseModel):
    """Metabase table model."""

    id: int = Field(description="Table ID")
    name: str = Field(description="Table name")
    display_name: str = Field(description="Human-readable display name")
    schema_name: Optional[str] = Field(
        default=None, description="Schema name", alias="schema"
    )
    description: Optional[str] = Field(default=None, description="Table description")
    active: bool = Field(default=True, description="Is table active and synced")
    visibility_type: Optional[str] = Field(
        default=None, description="Visibility type (null or hidden)"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="When table was added"
    )
    updated_at: Optional[datetime] = Field(default=None, description="Last sync time")
    entity_type: Optional[str] = Field(default=None, description="Table entity type")
    db_id: Optional[int] = Field(default=None, description="Database ID")
    is_writable: bool = Field(default=True, description="Can write to this table")

    @property
    def is_visible(self) -> bool:
        """Return True if table is visible (not hidden)."""
        return self.visibility_type is None
