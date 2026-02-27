"""Field/Column models for Metabase tables."""

from typing import Optional
from pydantic import BaseModel, Field as PydanticField


class TableField(BaseModel):
    """Metabase table field/column model."""

    id: int = PydanticField(description="Field ID")
    name: str = PydanticField(description="Field name")
    display_name: str = PydanticField(description="Human-readable display name")
    base_type: str = PydanticField(
        description="Base type (type/BigInteger, type/Text, etc.)"
    )
    semantic_type: Optional[str] = PydanticField(
        default=None, description="Semantic type (PK, Email, Name, etc.)"
    )
    database_type: Optional[str] = PydanticField(
        default=None, description="Database type (BIGINT, VARCHAR, etc.)"
    )
    description: Optional[str] = PydanticField(
        default=None, description="Field description"
    )
    position: int = PydanticField(default=0, description="Column position in table")
    active: bool = PydanticField(default=True, description="Is field active")
    visibility_type: Optional[str] = PydanticField(
        default=None, description="Visibility type"
    )
