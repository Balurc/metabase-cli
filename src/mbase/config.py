"""Configuration and credentials management."""

import os
import yaml  # type: ignore
from pathlib import Path
from typing import Optional
import appdirs  # type: ignore
from mbase.models.config import Config, Credentials
from datetime import datetime


class ConfigManager:
    """Manages CLI configuration and credentials storage."""

    APP_NAME = "mbase"
    APP_AUTHOR = "mbase"

    def __init__(self):
        # Get platform-appropriate config directory
        self.config_dir = Path(appdirs.user_config_dir(self.APP_NAME, self.APP_AUTHOR))
        self.config_file = self.config_dir / "config.yaml"
        self.credentials_file = self.config_dir / "credentials.yaml"

        # Ensure directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save_credentials(
        self, credentials: Credentials, profile_name: str = "default"
    ) -> None:
        """Save credentials to file with restricted permissions."""
        # Load existing or create new
        all_creds = self._load_all_credentials()

        # Deactivate other profiles if this one is active
        if profile_name == "default":
            for name in all_creds:
                all_creds[name]["is_active"] = False

        # Save new credentials
        all_creds[profile_name] = {
            "url": credentials.url,
            "api_key": credentials.api_key,
            "created_at": credentials.created_at.isoformat(),
            "is_active": True,
        }

        # Write with restricted permissions (user read/write only)
        with open(self.credentials_file, "w") as f:
            yaml.dump(all_creds, f, default_flow_style=False)

        # Set file permissions (Unix-like systems)
        os.chmod(self.credentials_file, 0o600)

    def load_credentials(
        self, profile_name: Optional[str] = None
    ) -> Optional[Credentials]:
        """Load credentials from file."""
        if not self.credentials_file.exists():
            return None

        all_creds = self._load_all_credentials()

        if profile_name:
            if profile_name not in all_creds:
                return None
            creds_data = all_creds[profile_name]
        else:
            # Find active profile or default
            active_profile = None
            for name, data in all_creds.items():
                if data.get("is_active", False):
                    active_profile = data
                    break

            if active_profile is None and "default" in all_creds:
                active_profile = all_creds["default"]

            if active_profile is None:
                return None

            creds_data = active_profile

        return Credentials(
            url=creds_data["url"],
            api_key=creds_data["api_key"],
            created_at=datetime.fromisoformat(creds_data["created_at"]),
        )

    def clear_credentials(self) -> None:
        """Remove all stored credentials."""
        if self.credentials_file.exists():
            self.credentials_file.unlink()

    def save_config(self, config: Config, profile_name: str = "default") -> None:
        """Save configuration settings."""
        all_configs = self._load_all_configs()
        all_configs[profile_name] = {
            "default_output_format": config.default_output_format,
            "timeout": config.timeout,
            "verify_ssl": config.verify_ssl,
        }

        with open(self.config_file, "w") as f:
            yaml.dump(all_configs, f, default_flow_style=False)

    def load_config(self, profile_name: Optional[str] = None) -> Config:
        """Load configuration settings."""
        if not self.config_file.exists():
            return Config()

        all_configs = self._load_all_configs()

        if profile_name and profile_name in all_configs:
            config_data = all_configs[profile_name]
        elif "default" in all_configs:
            config_data = all_configs["default"]
        else:
            return Config()

        return Config(**config_data)

    def _load_all_credentials(self) -> dict:
        """Load all credentials from file."""
        if not self.credentials_file.exists():
            return {}

        with open(self.credentials_file, "r") as f:
            return yaml.safe_load(f) or {}

    def _load_all_configs(self) -> dict:
        """Load all configs from file."""
        if not self.config_file.exists():
            return {}

        with open(self.config_file, "r") as f:
            return yaml.safe_load(f) or {}


# Global config manager instance
config_manager = ConfigManager()
