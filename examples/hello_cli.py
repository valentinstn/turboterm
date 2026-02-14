#!/usr/bin/env python3
"""
Minimal CLI example — a single command with one positional argument.

Usage:
    uv run python examples/hello_cli.py greet Alice
    uv run python examples/hello_cli.py greet --help
"""
from turboterm.cli import command, Argument, run


@command()
def greet(name: str = Argument(help="Name to greet", default="World")):
    """Say hello to someone."""
    print(f"Hello, {name}!")


if __name__ == "__main__":
    run()
