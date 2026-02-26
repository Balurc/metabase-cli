from unittest.mock import Mock, patch
import httpx
from metabase_cli.client import MetabaseClient, get_client


def test_client_initialization():
    """Test MetabaseClient initializes correctly."""
    with patch("metabase_cli.client.get_settings") as mock_get_settings:
        mock_settings = Mock()
        mock_settings.api_base_url = "http://test:3000/api"
        mock_settings.metabase_api_key = "test_key"
        mock_get_settings.return_value = mock_settings

        client = MetabaseClient()

        assert client.base_url == "http://test:3000/api"
        assert client.api_key == "test_key"
        assert isinstance(client.client, httpx.Client)


def test_health_check_returns_data_and_timing():
    """Test that health_check returns tuple of (data, response_time_ms)."""
    with patch("metabase_cli.client.get_settings") as mock_get_settings:
        mock_settings = Mock()
        mock_settings.api_base_url = "http://test:3000/api"
        mock_settings.metabase_api_key = "test_key"
        mock_get_settings.return_value = mock_settings

        client = MetabaseClient()

        # Mock the HTTP client
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status = Mock()

        with patch.object(client.client, "get", return_value=mock_response) as mock_get:
            data, response_time = client.health_check()

            assert data == {"status": "ok"}
            assert isinstance(response_time, int)
            assert response_time >= 0
            mock_get.assert_called_once_with("/health", params=None)


def test_get_client_returns_singleton():
    """Test that get_client returns a MetabaseClient instance."""
    client = get_client()
    assert isinstance(client, MetabaseClient)
