"""Tests for configuration commands."""
import pytest
from typer.testing import CliRunner
from unittest.mock import Mock, patch
from mbase.main import app

runner = CliRunner()


@pytest.fixture
def mock_config_manager():
    """Fixture to mock config manager."""
    with patch("mbase.commands.config.config_manager") as mock:
        yield mock


def test_config_show_with_credentials(mock_config_manager):
    """Test config show with saved credentials."""
    mock_config = Mock()
    mock_config.default_output_format = "table"
    mock_config.timeout = 30
    mock_config.verify_ssl = True

    mock_creds = Mock()
    mock_creds.url = "http://localhost:3000"
    mock_creds.mask_api_key.return_value = "mb_xxxx...xxxx"

    mock_config_manager.load_config.return_value = mock_config
    mock_config_manager.load_credentials.return_value = mock_creds

    result = runner.invoke(app, ["config", "show"])

    assert result.exit_code == 0
    assert "table" in result.output
    assert "http://localhost:3000" in result.output


def test_config_show_without_credentials(mock_config_manager):
    """Test config show without credentials."""
    mock_config = Mock()
    mock_config.default_output_format = "json"
    mock_config.timeout = 60
    mock_config.verify_ssl = False

    mock_config_manager.load_config.return_value = mock_config
    mock_config_manager.load_credentials.return_value = None

    result = runner.invoke(app, ["config", "show"])

    assert result.exit_code == 0
    assert "json" in result.output
    assert "Not logged in" in result.output


def test_config_set_valid_key(mock_config_manager):
    """Test setting a valid config key."""
    mock_config = Mock()
    mock_config.default_output_format = "table"
    mock_config.timeout = 30
    mock_config.verify_ssl = True

    mock_config_manager.load_config.return_value = mock_config

    result = runner.invoke(app, ["config", "set", "timeout", "60"])

    assert result.exit_code == 0
    assert "Set timeout = 60" in result.output
    assert mock_config_manager.save_config.called


def test_config_set_invalid_key(mock_config_manager):
    """Test setting an invalid config key."""
    result = runner.invoke(app, ["config", "set", "invalid_key", "value"])

    assert result.exit_code == 1
    assert "Unknown configuration key" in result.output
