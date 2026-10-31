from typer.testing import CliRunner

from docguard.cli import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "DocGuard" in result.output
    assert "0.1.0" in result.output


def test_cli_validate_report_nonexistent() -> None:
    result = runner.invoke(app, ["validate-report", "nonexistent.json"])
    assert result.exit_code != 0
