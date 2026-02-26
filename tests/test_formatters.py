import json
from metabase_cli.formatters import get_formatter, OutputFormat
from metabase_cli.formatters.table import TableFormatter
from metabase_cli.formatters.json import JSONFormatter


def test_get_formatter_table():
    formatter = get_formatter(OutputFormat.TABLE)
    assert isinstance(formatter, TableFormatter)


def test_get_formatter_json():
    formatter = get_formatter(OutputFormat.JSON)
    assert isinstance(formatter, JSONFormatter)


def test_json_formatter_dict():
    formatter = JSONFormatter()
    data = {"status": "ok", "url": "http://localhost:3000/api"}
    result = formatter.format_dict(data)

    # Should be valid JSON
    parsed = json.loads(result)
    assert parsed["status"] == "ok"


def test_json_formatter_list():
    formatter = JSONFormatter()
    data = [{"id": 1, "name": "Test"}, {"id": 2, "name": "Test 2"}]
    result = formatter.format_list(data)

    parsed = json.loads(result)
    assert len(parsed) == 2


def test_json_formatter_error():
    formatter = JSONFormatter()
    error = {"message": "Test error", "code": "TEST_ERROR"}
    result = formatter.format_error(error)

    parsed = json.loads(result)
    assert "error" in parsed
    assert parsed["error"]["message"] == "Test error"
