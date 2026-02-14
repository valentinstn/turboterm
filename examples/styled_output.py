#!/usr/bin/env python3
"""
Styled output example — combines the CLI framework with TurboTerm's
styled text and table rendering.

Usage:
    uv run python examples/styled_output.py demo
    uv run python examples/styled_output.py users
    uv run python examples/styled_output.py users --format table
"""
from turboterm import console
from turboterm.cli import command, Option, run


@command()
def demo():
    """Demonstrate styled console output."""
    console.print("[b]Bold text[/b]")
    console.print("[red]Red text[/red]")
    console.print("[u]Underlined text[/u]")
    console.print("[b][red]Bold red text[/red][/b]")
    console.print("")
    console.print("A styled table:")
    console.table([
        ["[b]Feature[/b]", "[b]Status[/b]"],
        ["Lexer", "[red]Stable[/red]"],
        ["Tables", "[red]Stable[/red]"],
        ["CLI", "[u]In Progress[/u]"],
    ])


@command()
def users(
    fmt: str = Option(["--format", "-f"], help="Output format (list or table)", default="list"),
):
    """Display a list of users."""
    data = [
        ("alice", "alice@example.com", "admin"),
        ("bob", "bob@example.com", "user"),
        ("charlie", "charlie@example.com", "user"),
    ]

    if fmt == "table":
        console.table(
            [["[b]Name[/b]", "[b]Email[/b]", "[b]Role[/b]"]]
            + [[name, email, f"[red]{role}[/red]" if role == "admin" else role] for name, email, role in data]
        )
    else:
        for name, email, role in data:
            console.print(f"  [b]{name}[/b] <{email}> [{role}]")


if __name__ == "__main__":
    run()
