from typing import Any, Dict, Optional
import httpx
from metabase_cli.config import settings

class MetabaseClient:
    def __init__(self):
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
    
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.client.post(path, json=json)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        return self.get("/health")
    
    def close(self) -> None:
        self.client.close()


def get_client() -> MetabaseClient:
    return MetabaseClient()
