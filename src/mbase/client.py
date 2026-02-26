from typing import Any, Dict, Optional
import httpx
from rich.console import Console
from mbase.config import config_manager
from mbase.models.config import Credentials

console = Console()


class MetabaseClient:
    """Authenticated HTTP client for Metabase API."""

    def __init__(self, credentials: Optional[Credentials] = None):
        """Initialize client with credentials."""
        if credentials is None:
            credentials = config_manager.load_credentials()

        if credentials is None:
            raise AuthenticationError(
                "No credentials found. Run 'mbase login' to authenticate."
            )

        self.credentials = credentials
        self.base_url = credentials.url.rstrip("/")
        self.api_key = credentials.api_key

        # Initialize HTTP client
        self.client = httpx.Client(
            base_url=f"{self.base_url}/api",
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
            timeout=30.0,
            follow_redirects=True,
        )

    def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Metabase API."""
        try:
            response = self.client.request(method, path, json=json, params=params)

            # Handle specific error codes
            if response.status_code == 401:
                raise AuthenticationError(
                    "Invalid API key. Please run 'mbase login' to re-authenticate."
                )
            elif response.status_code == 403:
                raise PermissionError(
                    "You don't have permission to access this resource."
                )
            elif response.status_code == 404:
                raise ResourceNotFoundError(f"Resource not found: {path}")
            elif response.status_code >= 500:
                raise ServerError(
                    f"Metabase server error ({response.status_code}). "
                    "Please try again later."
                )

            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException:
            raise ConnectionError(
                "Request timed out. Check your network connection and Metabase URL."
            )
        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Metabase at {self.base_url}. "
                "Check the URL and ensure Metabase is running."
            )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self.request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request."""
        return self.request("POST", path, json=json)

    def health_check(self) -> Dict[str, Any]:
        """Check Metabase health."""
        return self.get("/health")

    def user_current(self) -> Dict[str, Any]:
        """Get current user info."""
        return self.get("/user/current")

    def close(self) -> None:
        """Close HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class ResourceNotFoundError(Exception):
    """Raised when a resource is not found."""

    pass


class ServerError(Exception):
    """Raised when server returns 5xx error."""

    pass


def get_client() -> MetabaseClient:
    """Get configured Metabase client."""
    return MetabaseClient()
