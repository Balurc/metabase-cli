import typer
from rich.console import Console

from metabase_cli.client import get_client
from metabase_cli.formatters import get_formatter, OutputFormat
from metabase_cli.models.common import HealthResponse, ErrorResponse

from metabase_cli.formatters.table import TableFormatter

app = typer.Typer()
console = Console()


@app.command()
def check(
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE,
        "--format",
        "-f",
        help="Output format",
        case_sensitive=False,
    ),
):
    """Check if Metabase is reachable and healthy."""
    formatter = get_formatter(format)
    client = get_client()

    try:
        result, response_time_ms = client.health_check()

        health_data = HealthResponse(
            status=result.get("status", "unknown"),
            url=client.base_url,
            response_time_ms=response_time_ms,
        )

        if format == OutputFormat.JSON:
            print(formatter.format_dict(health_data.to_dict()))
        else:
            # Table format
            output = formatter.format_dict(
                {
                    "Status": health_data.status,
                    "URL": health_data.url,
                    "Response Time (ms)": health_data.response_time_ms,
                },
                title="Metabase Health Check",
            )
            # Check if output is a Table or string
            if isinstance(formatter, TableFormatter):
                console.print(output)  # Print Table with colors
            else:
                print(output)  # Print string (for other formatters)

            if health_data.status == "ok":
                console.print("\n✅ Metabase is healthy!", style="bold green")
            else:
                console.print(
                    f"\n⚠️  Metabase status: {health_data.status}", style="bold yellow"
                )

    except Exception as e:
        error = ErrorResponse(message=str(e), code="CONNECTION_ERROR", retryable=True)

        if format == OutputFormat.JSON:
            console.print(formatter.format_error(error.to_dict()))
        else:
            console.print(f"\n❌ Error: {e}", style="bold red")

        raise typer.Exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    app()
