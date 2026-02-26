import time
from typing import Any, Dict, Optional, Tuple
import httpx
from metabase_cli.config import get_settings


class MetabaseClient:
    def __init__(self):
        settings = get_settings()
        if not settings.metabase_api_key:
            raise ValueError(
                "METABASE_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
        self.base_url = settings.api_base_url
        self.api_key = settings.metabase_api_key
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], int]:
        """Make GET request and return (data, response_time_ms)."""
        start_time = time.time()
        response = self.client.get(path, params=params)
        response_time_ms = int((time.time() - start_time) * 1000)
        response.raise_for_status()
        return response.json(), response_time_ms

    def post(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], int]:
        """Make POST request and return (data, response_time_ms)."""
        start_time = time.time()
        response = self.client.post(path, json=json)
        response_time_ms = int((time.time() - start_time) * 1000)
        response.raise_for_status()
        return response.json(), response_time_ms

    def health_check(self) -> Tuple[Dict[str, Any], int]:
        """Check health and return (data, response_time_ms)."""
        return self.get("/health")

    def close(self) -> None:
        self.client.close()


def get_client() -> MetabaseClient:
    return MetabaseClient()
