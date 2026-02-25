from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    metabase_url: str = Field(
        default="http://localhost:3000",
        validation_alias="METABASE_URL"
    )
    metabase_api_key: str = Field(
        validation_alias="METABASE_API_KEY"
    )
    
    @property
    def api_base_url(self) -> str:
        return f"{self.metabase_url.rstrip('/')}/api"
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
