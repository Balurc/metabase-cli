import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch
from metabase_cli.main import app
from metabase_cli.client import MetabaseClient

runner = CliRunner()


@pytest.fixture
def mock_client():
    """Fixture to mock MetabaseClient."""
    with patch("metabase_cli.commands.health.get_client") as mock_get_client:
        client = Mock(spec=MetabaseClient)
        mock_get_client.return_value = client
        yield client


def test_health_check_success_table(mock_client):
    """Test health check success with default table format."""
    mock_client.health_check.return_value = ({"status": "ok"}, 100)
    mock_client.base_url = "http://localhost:3000/api"

    result = runner.invoke(app, ["health", "check"])

    assert result.exit_code == 0
    assert "Metabase Health Check" in result.output
    assert "ok" in result.output
    assert "100" in result.output  # Response time
    assert "✅" in result.output  # Success emoji


def test_health_check_success_json(mock_client):
    """Test health check success with JSON format."""
    mock_client.health_check.return_value = ({"status": "ok"}, 100)
    mock_client.base_url = "http://localhost:3000/api"

    result = runner.invoke(app, ["health", "check", "--format", "json"])

    assert result.exit_code == 0
    import json

    data = json.loads(result.output)
    assert data["status"] == "ok"
    assert data["url"] == "http://localhost:3000/api"
    assert data["response_time_ms"] == 100
    assert "timestamp" in data


def test_health_check_failure_table(mock_client):
    """Test health check failure with table format."""
    mock_client.health_check.side_effect = Exception("Connection refused")

    result = runner.invoke(app, ["health", "check"])

    assert result.exit_code == 1
    assert "Error" in result.output
    assert "Connection refused" in result.output


def test_health_check_failure_json(mock_client):
    """Test health check failure with JSON format."""
    mock_client.health_check.side_effect = Exception("Connection refused")

    result = runner.invoke(app, ["health", "check", "--format", "json"])

    assert result.exit_code == 1
    import json

    data = json.loads(result.output)
    assert "error" in data
    assert data["error"]["message"] == "Connection refused"
    assert data["error"]["code"] == "CONNECTION_ERROR"
    assert data["error"]["retryable"] is True


def test_health_check_shows_url(mock_client):
    """Test that the Metabase URL is displayed in output."""
    mock_client.health_check.return_value = ({"status": "ok"}, 50)
    mock_client.base_url = "http://custom:8080/api"

    result = runner.invoke(app, ["health", "check"])

    assert result.exit_code == 0
    assert "http://custom:8080/api" in result.output
