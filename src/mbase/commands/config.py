"""Configuration management commands."""

import typer
from typing import Union
from rich.console import Console
from rich.table import Table
from mbase.config import config_manager

app = typer.Typer()
console = Console()


@app.command()
def show():
    """Display current configuration."""
    config = config_manager.load_config()
    credentials = config_manager.load_credentials()

    table = Table(title="Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    # Config settings
    table.add_row("Default Output Format", config.default_output_format)
    table.add_row("Timeout", f"{config.timeout}s")
    table.add_row("Verify SSL", str(config.verify_ssl))

    # Credentials info (masked)
    if credentials:
        table.add_row("Metabase URL", credentials.url)
        table.add_row("API Key", credentials.mask_api_key())
    else:
        table.add_row("Authentication", "[red]Not logged in[/red]")

    console.print(table)

    # Show config file location
    console.print(f"\n[dim]Config directory: {config_manager.config_dir}[/dim]")


@app.command()
def set(
    key: str = typer.Argument(..., help="Configuration key to set"),
    value: str = typer.Argument(..., help="Value to set"),
):
    """Set a configuration value."""
    # Load current config
    config = config_manager.load_config()

    # Map keys to config attributes
    valid_keys = {
        "default_output_format": "default_output_format",
        "output_format": "default_output_format",
        "timeout": "timeout",
        "verify_ssl": "verify_ssl",
    }

    if key not in valid_keys:
        console.print(f"[red]Error: Unknown configuration key '{key}'[/red]")
        console.print(f"Valid keys: {', '.join(valid_keys.keys())}")
        raise typer.Exit(1)

    # Convert value to appropriate type
    attr_name = valid_keys[key]
    converted_value: Union[str, int, bool]

    try:
        if attr_name == "timeout":
            converted_value = int(value)
        elif attr_name == "verify_ssl":
            converted_value = value.lower() in ("true", "1", "yes", "on")
        else:
            converted_value = value
    except ValueError:
        console.print(f"[red]Error: Invalid value type for '{key}'[/red]")
        raise typer.Exit(1)

    # Update config
    setattr(config, attr_name, converted_value)
    config_manager.save_config(config)

    console.print(f"[bold green]✓[/bold green] Set {key} = {converted_value}")


if __name__ == "__main__":
    app()
