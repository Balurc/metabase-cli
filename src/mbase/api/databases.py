"""Database API operations."""

from typing import List, Dict, Any
from mbase.client import get_client
from mbase.models.database import Database
from mbase.models.table import Table
from mbase.models.field import TableField


class DatabasesAPI:
    """API client for database operations."""

    def __init__(self):
        self.client = get_client()

    def list_databases(self) -> List[Database]:
        """List all connected databases."""
        response = self.client.get("/database")

        databases_data = response.get("data", [])

        databases_data.sort(key=lambda x: x.get("id", 0))

        return [Database.model_validate(db) for db in databases_data]

    def get_database(self, database_id: int) -> Database:
        """Get a specific database by ID."""
        response = self.client.get(f"/database/{database_id}")
        return Database.model_validate(response)

    def list_tables(self, database_id: int) -> List[Table]:
        """List all tables in a database."""
        response = self.client.get(f"/database/{database_id}?include=tables")

        # Extract tables from the response
        tables_data = response.get("tables", [])

        tables_data.sort(key=lambda x: x.get("id", 0))

        return [Table.model_validate(table) for table in tables_data]

    def get_table_metadata(self, table_id: int) -> Dict[str, Any]:
        """Get complete table metadata including fields."""
        response = self.client.get(f"/table/{table_id}/query_metadata")

        # Extract fields and sort by position
        fields_data = response.get("fields", [])
        fields_data.sort(key=lambda x: x.get("position", 0))

        # Convert fields to Field models
        fields = [TableField.model_validate(f) for f in fields_data]

        # Return structured data
        return {
            "table": {
                "id": response.get("id"),
                "name": response.get("name"),
                "display_name": response.get("display_name"),
                "schema_name": response.get("schema"),
                "data_layer": response.get("data_layer"),
                "description": response.get("description"),
                "active": response.get("active", True),
                "view_count": response.get("view_count", 0),
                "created_at": response.get("created_at"),
                "updated_at": response.get("updated_at"),
                "db_id": response.get("db_id"),
                "db_name": response.get("db", {}).get("name"),
                "db_engine": response.get("db", {}).get("engine"),
            },
            "fields": fields,
            "fields_count": len(fields),
        }
