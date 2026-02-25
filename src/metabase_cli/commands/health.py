import typer
from rich.console import Console
from rich.table import Table

from metabase_cli.client import get_client

app = typer.Typer()
console = Console()

@app.command()
def check():
    """Check if Metabase is reachable and healthy."""
    try:
        client = get_client()
        result = client.health_check()
        
        status = result.get("status", "unknown")
        
        table = Table(title="Metabase Health Check")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Status", status)
        table.add_row("URL", client.base_url)
        
        console.print(table)
        
        if status == "ok":
            console.print("\n✅ Metabase is healthy!", style="bold green")
        else:
            console.print(f"\n⚠️  Metabase status: {status}", style="bold yellow")
            
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        raise typer.Exit(1)
    finally:
        client.close()

        
if __name__ == "__main__":
    app()
