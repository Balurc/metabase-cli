"""Tests for authentication commands."""
import pytest
from typer.testing import CliRunner
from unittest.mock import patch
from mbase.main import app

runner = CliRunner()


@pytest.fixture
def mock_auth_manager():
    """Fixture to mock auth manager."""
    with patch("mbase.commands.auth.auth_manager") as mock:
        yield mock


def test_login_interactive_success(mock_auth_manager):
    """Test interactive login success."""
    mock_auth_manager.login_interactive.return_value = True

    result = runner.invoke(app, ["login"])

    assert result.exit_code == 0
    mock_auth_manager.login_interactive.assert_called_once()


def test_login_interactive_failure(mock_auth_manager):
    """Test interactive login failure."""
    mock_auth_manager.login_interactive.return_value = False

    result = runner.invoke(app, ["login"])

    assert result.exit_code == 1


def test_login_with_token_success(mock_auth_manager):
    """Test token-based login success."""
    mock_auth_manager.login_with_token.return_value = True

    result = runner.invoke(
        app, ["login", "--token", "mb_test_key", "--url", "http://localhost:3000"]
    )

    assert result.exit_code == 0
    mock_auth_manager.login_with_token.assert_called_once_with(
        "http://localhost:3000", "mb_test_key"
    )


def test_login_with_token_missing_url(mock_auth_manager):
    """Test token login fails without URL."""
    result = runner.invoke(app, ["login", "--token", "mb_test_key"])

    assert result.exit_code == 1
    assert "Error: --url is required" in result.output


def test_logout_success(mock_auth_manager):
    """Test logout success."""
    mock_auth_manager.logout.return_value = True

    result = runner.invoke(app, ["logout"])

    assert result.exit_code == 0
    mock_auth_manager.logout.assert_called_once()


def test_status_authenticated(mock_auth_manager):
    """Test status when authenticated."""
    mock_auth_manager.get_status.return_value = {
        "authenticated": True,
        "url": "http://localhost:3000",
        "user": {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
        },
        "api_key_masked": "mb_xxxx...xxxx",
    }

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Connected" in result.output
    assert "admin@example.com" in result.output


def test_status_not_authenticated(mock_auth_manager):
    """Test status when not authenticated."""
    mock_auth_manager.get_status.return_value = None

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Not authenticated" in result.output
