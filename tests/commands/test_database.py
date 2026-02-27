"""Tests for database commands."""

import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch

from mbase.main import app

runner = CliRunner()


@pytest.fixture
def mock_databases_api():
    """Fixture to mock DatabasesAPI."""
    with patch("mbase.commands.database.DatabasesAPI") as mock_class:
        mock_instance = Mock()
        mock_class.return_value = mock_instance
        yield mock_instance


def test_database_list_table(mock_databases_api):
    """Test database list in table format."""

    mock_db1 = Mock()
    mock_db1.id = 1
    mock_db1.name = "Sample Database"
    mock_db1.engine = "h2"
    mock_db1.is_sample = True
    mock_db1.display_type = "sample"
    mock_db1.description = "Example data"
    mock_db1.created_at = None
    mock_db1.updated_at = None

    mock_db2 = Mock()
    mock_db2.id = 2
    mock_db2.name = "Production DB"
    mock_db2.engine = "postgres"
    mock_db2.is_sample = False
    mock_db2.display_type = "connected"
    mock_db2.description = None
    mock_db2.created_at = None
    mock_db2.updated_at = None

    mock_databases_api.list_databases.return_value = [mock_db1, mock_db2]

    result = runner.invoke(app, ["database", "list"])

    assert result.exit_code == 0
    assert "Sample" in result.output  # Changed from "Sample Database"
    assert "Database" in result.output  # Changed from "Sample Database"
    assert "Production DB" in result.output  # This one fits on one line
    assert "h2" in result.output
    assert "postgres" in result.output


def test_database_list_json(mock_databases_api):
    """Test database list in JSON format."""
    mock_db = Mock()
    mock_db.id = 1
    mock_db.name = "Test DB"
    mock_db.engine = "h2"
    mock_db.model_dump.return_value = {
        "id": 1,
        "name": "Test DB",
        "engine": "h2",
        "is_sample": False,
    }

    mock_databases_api.list_databases.return_value = [mock_db]

    result = runner.invoke(app, ["database", "list", "--format", "json"])

    assert result.exit_code == 0
    assert '"id": 1' in result.output
    assert '"name": "Test DB"' in result.output


def test_database_list_empty(mock_databases_api):
    """Test database list when no databases found."""
    mock_databases_api.list_databases.return_value = []

    result = runner.invoke(app, ["database", "list"])

    assert result.exit_code == 0
    assert "No databases found" in result.output


def test_database_tables_table(mock_databases_api):
    """Test database tables list in table format."""
    mock_table = Mock()
    mock_table.id = 1
    mock_table.name = "orders"
    mock_table.display_name = "Orders"
    mock_table.schema_name = "public"
    mock_table.active = True
    mock_table.updated_at = None

    mock_databases_api.list_tables.return_value = [mock_table]

    result = runner.invoke(app, ["database", "tables", "1"])

    assert result.exit_code == 0
    assert "orders" in result.output
    assert "public" in result.output


def test_database_tables_json(mock_databases_api):
    """Test database tables list in JSON format."""
    mock_table = Mock()
    mock_table.id = 1
    mock_table.name = "orders"
    mock_table.display_name = "Orders"
    mock_table.schema_name = "public"
    mock_table.active = True
    mock_table.entity_type = "entity/TransactionTable"
    mock_table.db_id = 1
    mock_table.is_writable = True
    mock_table.model_dump.return_value = {
        "id": 1,
        "name": "orders",
        "display_name": "Orders",
        "entity_type": "entity/TransactionTable",
        "db_id": 1,
        "is_writable": True,
    }

    mock_databases_api.list_tables.return_value = [mock_table]

    result = runner.invoke(app, ["database", "tables", "1", "--format", "json"])

    assert result.exit_code == 0
    assert '"entity_type"' in result.output
    assert '"db_id"' in result.output
    assert '"is_writable"' in result.output


def test_database_tables_empty(mock_databases_api):
    """Test database tables when no tables found."""
    mock_databases_api.list_tables.return_value = []

    result = runner.invoke(app, ["database", "tables", "1"])

    assert result.exit_code == 0
    assert "No tables found" in result.output


def test_database_tables_invalid_db(mock_databases_api):
    """Test database tables with invalid database ID."""
    mock_databases_api.list_tables.side_effect = Exception("Database not found")

    result = runner.invoke(app, ["database", "tables", "999"])

    assert result.exit_code == 1
