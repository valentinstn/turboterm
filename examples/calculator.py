#!/usr/bin/env python3
"""
Multi-command CLI — a calculator with add, multiply, and divide subcommands.
Demonstrates positional arguments with type conversion (int, float).

Usage:
    uv run examples/calculator.py add 10 20
    uv run examples/calculator.py multiply 2.5 4.0
    uv run examples/calculator.py divide 100 3
    uv run examples/calculator.py --help
"""

from turboterm.cli import Argument, command, run


@command()
def add(
    x: int = Argument(help="First number"), y: int = Argument(help="Second number")
):
    """Add two integers."""
    print(f"{x} + {y} = {x + y}")


@command()
def multiply(
    x: float = Argument(help="First number"), y: float = Argument(help="Second number")
):
    """Multiply two floats."""
    print(f"{x} * {y} = {x * y}")


@command()
def divide(
    x: float = Argument(help="Numerator"), y: float = Argument(help="Denominator")
):
    """Divide two numbers."""
    if y == 0:
        print("Error: division by zero")
    else:
        print(f"{x} / {y} = {x / y}")


if __name__ == "__main__":
    run()
