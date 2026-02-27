"""Database API operations."""

from typing import List
from mbase.client import get_client
from mbase.models.database import Database
from mbase.models.table import Table


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
