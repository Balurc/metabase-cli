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
    # Create mock database objects
    mock_db1 = Mock()
    mock_db1.id = 1
    mock_db1.name = "Sample Database"
    mock_db1.engine = "h2"
    mock_db1.is_sample = True
    mock_db1.display_type = "sample"

    mock_db2 = Mock()
    mock_db2.id = 2
    mock_db2.name = "Production DB"
    mock_db2.engine = "postgres"
    mock_db2.is_sample = False
    mock_db2.display_type = "connected"

    mock_databases_api.list_databases.return_value = [mock_db1, mock_db2]

    result = runner.invoke(app, ["database", "list"])

    assert result.exit_code == 0
    assert "Sample Database" in result.output
    assert "Production DB" in result.output
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
