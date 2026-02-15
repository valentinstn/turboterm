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
        [sys.executable, "-X", "utf8", script_path] + args,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
    )


# ---------------------------------------------------------------------------
# examples/hello_cli.py
# ---------------------------------------------------------------------------


class TestHelloCli(unittest.TestCase):
    """examples/hello_cli.py — minimal single-command CLI."""

    SCRIPT = "examples/hello_cli.py"

    def test_greet_with_name(self):
        """uv run python examples/hello_cli.py greet Alice"""
        r = _run(self.SCRIPT, ["greet", "Alice"])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "Hello, Alice!")

    def test_greet_default(self):
        """uv run python examples/hello_cli.py greet"""
        r = _run(self.SCRIPT, ["greet"])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "Hello, World!")

    def test_greet_help(self):
        """uv run python examples/hello_cli.py greet --help"""
        r = _run(self.SCRIPT, ["greet", "--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Say hello", r.stdout)
        self.assertIn("Name to greet", r.stdout)


# ---------------------------------------------------------------------------
# examples/calculator.py
# ---------------------------------------------------------------------------


class TestCalculator(unittest.TestCase):
    """examples/calculator.py — multi-command calculator."""

    SCRIPT = "examples/calculator.py"

    def test_add(self):
        """uv run python examples/calculator.py add 10 20"""
        r = _run(self.SCRIPT, ["add", "10", "20"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("10 + 20 = 30", r.stdout)

    def test_multiply(self):
        """uv run python examples/calculator.py multiply 2.5 4.0"""
        r = _run(self.SCRIPT, ["multiply", "2.5", "4.0"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("2.5 * 4.0 = 10.0", r.stdout)

    def test_divide(self):
        """uv run python examples/calculator.py divide 100 3"""
        r = _run(self.SCRIPT, ["divide", "100", "3"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("100.0 / 3.0 =", r.stdout)

    def test_divide_by_zero(self):
        """division by zero should print an error, not crash"""
        r = _run(self.SCRIPT, ["divide", "1", "0"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("division by zero", r.stdout)

    def test_help(self):
        """uv run python examples/calculator.py --help"""
        r = _run(self.SCRIPT, ["--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("add", r.stdout)
        self.assertIn("multiply", r.stdout)
        self.assertIn("divide", r.stdout)


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
        """uv run python examples/server_cli.py start --host 0.0.0.0 -p 3000 --verbose"""
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
# examples/deploy_tool.py
# ---------------------------------------------------------------------------


class TestDeployTool(unittest.TestCase):
    """examples/deploy_tool.py — real-world-ish deploy CLI with styled output."""

    SCRIPT = "examples/deploy_tool.py"

    def test_push_staging(self):
        """uv run python examples/deploy_tool.py push staging"""
        r = _run(self.SCRIPT, ["push", "staging"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Deploying", r.stdout)
        self.assertIn("staging", r.stdout)
        self.assertIn("Deployed", r.stdout)

    def test_push_dry_run(self):
        """uv run python examples/deploy_tool.py push production --tag v1.2.3 --dry-run"""
        r = _run(self.SCRIPT, ["push", "production", "--tag", "v1.2.3", "--dry-run"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("DRY RUN", r.stdout)
        self.assertIn("v1.2.3", r.stdout)
        self.assertIn("production", r.stdout)
        self.assertIn("Dry run complete", r.stdout)

    def test_rollback(self):
        """uv run python examples/deploy_tool.py rollback production --steps 2"""
        r = _run(self.SCRIPT, ["rollback", "production", "--steps", "2"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Rolling back", r.stdout)
        self.assertIn("production", r.stdout)
        self.assertIn("2", r.stdout)

    def test_logs(self):
        """uv run python examples/deploy_tool.py logs staging --lines 50 --follow"""
        r = _run(self.SCRIPT, ["logs", "staging", "--lines", "50", "--follow"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Fetching", r.stdout)
        self.assertIn("staging", r.stdout)
        self.assertIn("streaming", r.stdout)

    def test_logs_static(self):
        """logs without --follow should be static"""
        r = _run(self.SCRIPT, ["logs", "staging"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("static", r.stdout)

    def test_help(self):
        """uv run python examples/deploy_tool.py --help"""
        r = _run(self.SCRIPT, ["--help"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("push", r.stdout)
        self.assertIn("rollback", r.stdout)
        self.assertIn("logs", r.stdout)


# ---------------------------------------------------------------------------
# examples/styled_output.py
# ---------------------------------------------------------------------------


class TestStyledOutput(unittest.TestCase):
    """examples/styled_output.py — styled text + tables demo."""

    SCRIPT = "examples/styled_output.py"

    def test_demo(self):
        """uv run python examples/styled_output.py demo"""
        r = _run(self.SCRIPT, ["demo"])
        self.assertEqual(r.returncode, 0, r.stderr)
        output = r.stdout
        # Text attributes
        self.assertIn("\x1b[1mBold text\x1b[0m", output)
        self.assertIn("\x1b[3mItalic text\x1b[0m", output)
        self.assertIn("\x1b[31mRed text\x1b[0m", output)
        self.assertIn("\x1b[4mUnderlined text\x1b[0m", output)
        # Compound tag
        self.assertIn("\x1b[1m\x1b[31mBold red text\x1b[0m", output)
        # More attributes
        self.assertIn("\x1b[2mDim text\x1b[0m", output)
        self.assertIn("\x1b[9mStrikethrough text\x1b[0m", output)
        # Compound with bg
        self.assertIn("\x1b[3m", output)  # italic
        self.assertIn("\x1b[96m", output)  # bright_cyan
        self.assertIn("\x1b[44m", output)  # on_blue
        # 256-color
        self.assertIn("\x1b[38;5;208m", output)
        # Hex
        self.assertIn("\x1b[38;2;255;128;0m", output)
        # RGB
        self.assertIn("\x1b[38;2;100;200;50m", output)
        # Table present
        self.assertIn("Feature", output)
        self.assertIn("Stable", output)

    def test_users_list(self):
        """uv run python examples/styled_output.py users"""
        r = _run(self.SCRIPT, ["users"])
        self.assertEqual(r.returncode, 0)
        output = r.stdout
        self.assertIn("alice", output)
        self.assertIn("bob", output)
        self.assertIn("charlie", output)
        self.assertIn("alice@example.com", output)

    def test_users_table(self):
        """uv run python examples/styled_output.py users --format table"""
        r = _run(self.SCRIPT, ["users", "--format", "table"])
        self.assertEqual(r.returncode, 0, r.stderr)
        output = r.stdout
        # Table structure
        self.assertIn("Name", output)
        self.assertIn("Email", output)
        self.assertIn("Role", output)
        # Styled admin role
        self.assertIn("\x1b[31madmin\x1b[0m", output)


if __name__ == "__main__":
    unittest.main()
