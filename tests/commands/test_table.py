"""Tests for table commands."""

import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch

from mbase.main import app

runner = CliRunner()


@pytest.fixture
def mock_databases_api():
    """Fixture to mock DatabasesAPI."""
    with patch("mbase.commands.table.DatabasesAPI") as mock_class:
        mock_instance = Mock()
        mock_class.return_value = mock_instance
        yield mock_instance


def test_table_inspect_table(mock_databases_api):
    """Test table inspect in table format."""
    mock_field = Mock()
    mock_field.id = 1
    mock_field.name = "ID"
    mock_field.display_name = "ID"
    mock_field.base_type = "type/BigInteger"
    mock_field.semantic_type = "type/PK"
    mock_field.position = 0

    mock_databases_api.get_table_metadata.return_value = {
        "table": {
            "id": 1,
            "name": "PEOPLE",
            "display_name": "People",
            "schema_name": "PUBLIC",
            "data_layer": "bronze",
            "description": "Test description",
            "active": True,
            "view_count": 0,
            "created_at": "2026-02-25T08:33:01Z",
            "updated_at": "2026-02-25T08:33:03Z",
            "db_id": 1,
            "db_name": "Sample Database",
            "db_engine": "h2",
        },
        "fields": [mock_field],
        "fields_count": 1,
    }

    result = runner.invoke(app, ["table", "inspect", "1"])

    assert result.exit_code == 0
    assert "People" in result.output
    assert "ID" in result.output


def test_table_inspect_json(mock_databases_api):
    """Test table inspect in JSON format."""
    mock_field = Mock()
    mock_field.id = 1
    mock_field.name = "ID"
    mock_field.display_name = "ID"
    mock_field.base_type = "type/BigInteger"
    mock_field.semantic_type = "type/PK"

    mock_databases_api.get_table_metadata.return_value = {
        "table": {
            "id": 1,
            "name": "PEOPLE",
            "display_name": "People",
            "schema_name": "PUBLIC",
            "data_layer": "bronze",
            "description": "Test",
            "active": True,
            "view_count": 0,
            "created_at": "2026-02-25T08:33:01Z",
            "updated_at": "2026-02-25T08:33:03Z",
            "db_id": 1,
            "db_name": "Sample Database",
            "db_engine": "h2",
        },
        "fields": [mock_field],
        "fields_count": 1,
    }

    result = runner.invoke(app, ["table", "inspect", "1", "--format", "json"])

    assert result.exit_code == 0
    assert '"display_name": "People"' in result.output
    assert '"db_engine": "h2"' in result.output


def test_table_inspect_error(mock_databases_api):
    """Test table inspect with invalid table ID."""
    mock_databases_api.get_table_metadata.side_effect = Exception("Table not found")

    result = runner.invoke(app, ["table", "inspect", "999"])

    assert result.exit_code == 1
