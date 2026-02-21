"""Tests that verify every example script in the examples/ folder actually works.

Each test runs an example file as a subprocess with the documented CLI arguments
and asserts on expected output. If an example is added or changed, the
corresponding test here should be updated to match, ensuring examples never go stale.
"""

import subprocess
import sys
import unittest


def _run(script_path: str, args: list[str]) -> subprocess.CompletedProcess:
    """Run an example script in a subprocess and return the result."""
    return subprocess.run(
        [sys.executable, "-X", "utf8", script_path, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
    )


# ---------------------------------------------------------------------------
# examples/server_cli.py
# ---------------------------------------------------------------------------


class TestServerCli(unittest.TestCase):
    """examples/server_cli.py — options and flags demo."""

    SCRIPT = "examples/server_cli.py"

    def test_start_defaults(self):
        """uv run python examples/server_cli.py start"""
        r = _run(self.SCRIPT, ["start"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("127.0.0.1:8080", r.stdout)
        self.assertIn("Workers: 4", r.stdout)
        self.assertNotIn("Verbose", r.stdout)

    def test_start_custom(self):
        """server_cli.py start --host 0.0.0.0 -p 3000 --verbose"""
        r = _run(self.SCRIPT, ["start", "--host", "0.0.0.0", "-p", "3000", "--verbose"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("0.0.0.0:3000", r.stdout)
        self.assertIn("Verbose logging enabled", r.stdout)

    def test_start_workers(self):
        """--workers flag"""
        r = _run(self.SCRIPT, ["start", "-w", "8"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Workers: 8", r.stdout)

    def test_stop(self):
        """uv run python examples/server_cli.py stop"""
        r = _run(self.SCRIPT, ["stop"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Server stopped", r.stdout)

    def test_status(self):
        """uv run python examples/server_cli.py status"""
        r = _run(self.SCRIPT, ["status"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("running", r.stdout)

    def test_help(self):
        """uv run python examples/server_cli.py start --help"""
        r = _run(self.SCRIPT, ["start", "--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("--host", r.stdout)
        self.assertIn("--port", r.stdout)
        self.assertIn("--verbose", r.stdout)


# ---------------------------------------------------------------------------
# examples/formatted_help.py
# ---------------------------------------------------------------------------


class TestFormattedHelp(unittest.TestCase):
    """examples/formatted_help.py — styled markup in help text."""

    SCRIPT = "examples/formatted_help.py"

    def test_deploy_staging(self):
        """deploy staging renders styled output."""
        r = _run(self.SCRIPT, ["deploy", "staging", "--tag", "v2.1.0"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("v2.1.0", r.stdout)
        self.assertIn("staging", r.stdout)

    def test_deploy_dry_run(self):
        """deploy with --dry-run prints DRY RUN notice."""
        r = _run(self.SCRIPT, ["deploy", "production", "--dry-run"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("DRY RUN", r.stdout)
        self.assertIn("production", r.stdout)

    def test_rollback(self):
        """rollback renders styled output."""
        r = _run(self.SCRIPT, ["rollback", "staging", "--steps", "2"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("staging", r.stdout)
        self.assertIn("2", r.stdout)

    def test_deploy_help_contains_ansi(self):
        """deploy --help output contains ANSI codes from markup in help= strings."""
        r = _run(self.SCRIPT, ["deploy", "--help"])
        self.assertEqual(r.returncode, 0)
        # green for "staging", red for "production"
        self.assertIn("\x1b[32m", r.stdout)
        self.assertIn("\x1b[31m", r.stdout)
        # bold from the docstring
        self.assertIn("\x1b[1m", r.stdout)

    def test_top_help_contains_ansi(self):
        """Top-level --help shows styled subcommand descriptions."""
        r = _run(self.SCRIPT, ["--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("deploy", r.stdout)
        self.assertIn("rollback", r.stdout)
        # bold from the docstrings
        self.assertIn("\x1b[1m", r.stdout)


# ---------------------------------------------------------------------------
# examples/combined.py
# ---------------------------------------------------------------------------


class TestCombined(unittest.TestCase):
    """examples/combined.py — colors, bold, tables, and CLI in one script."""

    SCRIPT = "examples/combined.py"

    def test_show_defaults(self):
        """combined.py show — default project and env."""
        r = _run(self.SCRIPT, ["show"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("turboterm", r.stdout)
        self.assertIn("staging", r.stdout)

    def test_show_custom_project(self):
        """combined.py show --project myapp"""
        r = _run(self.SCRIPT, ["show", "--project", "myapp"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("myapp", r.stdout)

    def test_show_verbose(self):
        """combined.py show --verbose includes full benchmark table."""
        r = _run(self.SCRIPT, ["show", "--verbose"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Import time", r.stdout)
        self.assertIn("Styled output", r.stdout)
        self.assertIn("Table render", r.stdout)

    def test_show_help(self):
        """combined.py show --help"""
        r = _run(self.SCRIPT, ["show", "--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Project Overview", r.stdout)
        self.assertIn("--project", r.stdout)
        self.assertIn("--verbose", r.stdout)


if __name__ == "__main__":
    unittest.main()
