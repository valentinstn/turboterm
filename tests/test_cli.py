import unittest
import sys
from unittest.mock import patch
import io

# We need a fresh command registry for each test. Since the Rust registry is global
# and persists across calls, we import and register commands per-test using subprocess
# isolation. For unit tests, we test the Python-side components directly and use
# subprocess for integration tests.

from turboterm.cli import Argument, Option, _Argument, _Option, command, _register, _run_cli


class TestArgumentOption(unittest.TestCase):
    """Test the Argument and Option factory functions."""

    def test_argument_returns_internal_type(self):
        arg = Argument(help="A number")
        self.assertIsInstance(arg, _Argument)

    def test_argument_defaults(self):
        arg = Argument(help="A number")
        self.assertEqual(arg.help, "A number")
        from turboterm.cli import _UNSET
        self.assertIs(arg.default, _UNSET)

    def test_argument_with_default(self):
        arg = Argument(help="Name", default="World")
        self.assertEqual(arg.help, "Name")
        self.assertEqual(arg.default, "World")

    def test_argument_default_none(self):
        arg = Argument(help="Optional", default=None)
        self.assertIsNone(arg.default)

    def test_option_returns_internal_type(self):
        opt = Option(["--host", "-H"], help="Hostname")
        self.assertIsInstance(opt, _Option)

    def test_option_required_fields(self):
        opt = Option(["--host", "-H"], help="Hostname")
        self.assertEqual(opt.names, ["--host", "-H"])
        self.assertEqual(opt.help, "Hostname")

    def test_option_with_default(self):
        opt = Option(["--port"], help="Port", default=8080)
        self.assertEqual(opt.default, 8080)

    def test_option_bool_no_default(self):
        opt = Option(["--verbose", "-v"], help="Verbose")
        from turboterm.cli import _UNSET
        self.assertIs(opt.default, _UNSET)


class TestCommandDecorator(unittest.TestCase):
    """Test the @command() decorator's parameter inspection logic."""

    def test_decorator_preserves_function(self):
        @command("test_preserved")
        def my_func():
            pass
        # Decorator should return the original function
        self.assertEqual(my_func.__name__, "my_func")
        self.assertTrue(callable(my_func))

    def test_decorator_auto_name(self):
        """Command name defaults to function name."""
        @command()
        def hello_world():
            pass
        # The function is registered under "hello_world"
        # We can't easily inspect the Rust registry, but we can verify no error

    def test_decorator_custom_name(self):
        """Command name can be overridden."""
        @command("my-custom-cmd")
        def something():
            pass


class TestCliIntegration(unittest.TestCase):
    """Integration tests using subprocess to get a clean registry per test."""

    def _run_cli_script(self, script):
        """Run a CLI script in a subprocess and return (stdout, stderr, returncode)."""
        import subprocess
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout, result.stderr, result.returncode

    def test_positional_args_int(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def add(x: int = Argument(help="First"), y: int = Argument(help="Second")):
    print(x + y)

sys.argv = ["app", "add", "10", "20"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "30")

    def test_positional_args_float(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def multiply(x: float = Argument(help="A"), y: float = Argument(help="B")):
    print(x * y)

sys.argv = ["app", "multiply", "2.5", "4.0"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "10.0")

    def test_positional_args_str(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def greet(name: str = Argument(help="Name")):
    print(f"Hello, {name}!")

sys.argv = ["app", "greet", "Alice"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "Hello, Alice!")

    def test_optional_positional_default(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def greet(name: str = Argument(help="Name", default="World")):
    print(f"Hello, {name}!")

sys.argv = ["app", "greet"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "Hello, World!")

    def test_optional_positional_override(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def greet(name: str = Argument(help="Name", default="World")):
    print(f"Hello, {name}!")

sys.argv = ["app", "greet", "Bob"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "Hello, Bob!")

    def test_option_long_flag(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Option, run

@command()
def serve(host: str = Option(["--host"], help="Host", default="localhost")):
    print(host)

sys.argv = ["app", "serve", "--host", "0.0.0.0"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "0.0.0.0")

    def test_option_short_flag(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Option, run

@command()
def serve(port: int = Option(["--port", "-p"], help="Port", default=8080)):
    print(port)

sys.argv = ["app", "serve", "-p", "3000"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "3000")

    def test_option_default_used(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Option, run

@command()
def serve(port: int = Option(["--port", "-p"], help="Port", default=8080)):
    print(port)

sys.argv = ["app", "serve"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "8080")

    def test_bool_flag_present(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Option, run

@command()
def serve(verbose: bool = Option(["--verbose", "-v"], help="Verbose")):
    print(verbose)

sys.argv = ["app", "serve", "--verbose"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "True")

    def test_bool_flag_absent(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Option, run

@command()
def serve(verbose: bool = Option(["--verbose", "-v"], help="Verbose")):
    print(verbose)

sys.argv = ["app", "serve"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "False")

    def test_bool_flag_short(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Option, run

@command()
def serve(verbose: bool = Option(["--verbose", "-v"], help="Verbose")):
    print(verbose)

sys.argv = ["app", "serve", "-v"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "True")

    def test_mixed_args_and_options(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, Option, run

@command()
def deploy(
    target: str = Argument(help="Deploy target"),
    port: int = Option(["--port", "-p"], help="Port", default=443),
    dry_run: bool = Option(["--dry-run"], help="Dry run"),
):
    print(f"{target}:{port} dry={dry_run}")

sys.argv = ["app", "deploy", "production", "--port", "8080", "--dry-run"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "production:8080 dry=True")

    def test_custom_command_name(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, run

@command("say-hello")
def hello():
    print("hi")

sys.argv = ["app", "say-hello"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "hi")

    def test_multiple_commands(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def ping():
    print("pong")

@command()
def echo(msg: str = Argument(help="Message")):
    print(msg)

sys.argv = ["app", "echo", "hello"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "hello")

    def test_missing_required_arg_error(self):
        _, stderr, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def add(x: int = Argument(help="A"), y: int = Argument(help="B")):
    print(x + y)

sys.argv = ["app", "add", "5"]
run()
""")
        self.assertNotEqual(rc, 0)

    def test_invalid_type_error(self):
        _, stderr, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def add(x: int = Argument(help="A"), y: int = Argument(help="B")):
    print(x + y)

sys.argv = ["app", "add", "abc", "5"]
run()
""")
        self.assertNotEqual(rc, 0)

    def test_unknown_command_error(self):
        _, stderr, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, run

@command()
def ping():
    print("pong")

sys.argv = ["app", "nosuchcmd"]
run()
""")
        self.assertNotEqual(rc, 0)

    def test_help_flag(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, Argument, run

@command()
def greet(name: str = Argument(help="Name to greet")):
    '''Say hello.'''
    pass

sys.argv = ["app", "greet", "--help"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertIn("Say hello", stdout)
        self.assertIn("Name to greet", stdout)

    def test_docstring_in_help(self):
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, run

@command()
def mytool():
    '''This is my cool tool.'''
    pass

sys.argv = ["app", "--help"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertIn("mytool", stdout)
        self.assertIn("This is my cool tool", stdout)

    def test_bare_param_no_annotation(self):
        """Parameters without Argument/Option default are treated as required positional."""
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, run

@command()
def echo(msg: str):
    print(msg)

sys.argv = ["app", "echo", "hello"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "hello")

    def test_plain_default_value(self):
        """Parameter with a plain default (not Argument/Option) is optional positional."""
        stdout, _, rc = self._run_cli_script("""
import sys
from turboterm.cli import command, run

@command()
def greet(name: str = "World"):
    print(f"Hello, {name}!")

sys.argv = ["app", "greet"]
run()
""")
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.strip(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
