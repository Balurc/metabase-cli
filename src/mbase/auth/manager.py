"""Authentication manager for handling login/logout operations."""

from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from mbase.config import config_manager
from mbase.models.config import Credentials
from mbase.client import MetabaseClient, AuthenticationError

console = Console()


class AuthManager:
    """Manages authentication operations."""

    def login_interactive(self) -> bool:
        """Interactive login prompt."""
        console.print("\n[bold blue]Metabase Login[/bold blue]\n")

        # Get URL
        url = Prompt.ask("Enter Metabase URL", default="http://localhost:3000")

        # Get API key
        api_key = Prompt.ask("Enter API Key", password=True)

        if not api_key:
            console.print("[red]Error: API key is required[/red]")
            return False

        # Validate connection
        credentials = Credentials(url=url, api_key=api_key)

        with console.status("[bold green]Validating credentials..."):
            try:
                client = MetabaseClient(credentials)
                user_info = client.user_current()
                client.close()
            except AuthenticationError as e:
                console.print(f"[red]Authentication failed: {e}[/red]")
                return False
            except Exception as e:
                console.print(f"[red]Connection failed: {e}[/red]")
                return False

        # Save credentials
        config_manager.save_credentials(credentials)

        # Display success
        console.print("\n[bold green]✓[/bold green] Successfully authenticated!")
        console.print(f"  URL: {url}")
        console.print(
            f"  User: {user_info.get('first_name', '')} {user_info.get('last_name', '')}"
        )
        console.print(f"  Email: {user_info.get('email', '')}")

        return True

    def login_with_token(self, url: str, api_key: str) -> bool:
        """Login with provided URL and API key (non-interactive)."""
        credentials = Credentials(url=url, api_key=api_key)

        try:
            client = MetabaseClient(credentials)
            user_info = client.user_current()
            client.close()
        except Exception as e:
            console.print(f"[red]Authentication failed: {e}[/red]")
            return False

        # Save credentials
        config_manager.save_credentials(credentials)

        console.print(
            f"[bold green]✓[/bold green] Successfully authenticated as {user_info.get('email', '')}"
        )
        return True

    def logout(self) -> bool:
        """Logout and clear stored credentials."""
        credentials = config_manager.load_credentials()

        if credentials is None:
            console.print("[yellow]No active session found[/yellow]")
            return False

        # Confirm logout
        if Confirm.ask(f"Logout from {credentials.url}?"):
            config_manager.clear_credentials()
            console.print("[bold green]✓[/bold green] Logged out successfully")
            return True

        return False

    def get_status(self) -> Optional[dict]:
        """Get current authentication status."""
        credentials = config_manager.load_credentials()

        if credentials is None:
            return None

        try:
            with MetabaseClient(credentials) as client:
                health = client.health_check()
                user_info = client.user_current()

                return {
                    "authenticated": True,
                    "url": credentials.url,
                    "user": user_info,
                    "health": health,
                    "api_key_masked": credentials.mask_api_key(),
                }
        except Exception as e:
            return {
                "authenticated": False,
                "url": credentials.url,
                "error": str(e),
                "api_key_masked": credentials.mask_api_key(),
            }


# Global auth manager instance
auth_manager = AuthManager()
