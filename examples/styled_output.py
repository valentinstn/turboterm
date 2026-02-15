#!/usr/bin/env python3
"""
Styled output example — combines the CLI framework with TurboTerm's
styled text and table rendering.

Usage:
    uv run examples/styled_output.py demo
    uv run examples/styled_output.py users
    uv run examples/styled_output.py users --format table
"""

from turboterm import console
from turboterm.cli import Option, command, run


@command()
def demo():
    """Demonstrate styled console output."""
    console.print("[b]Bold text[/b]")
    console.print("[i]Italic text[/i]")
    console.print("[red]Red text[/red]")
    console.print("[u]Underlined text[/u]")
    console.print("[bold red]Bold red text[/bold red]")
    console.print("[dim]Dim text[/dim]")
    console.print("[s]Strikethrough text[/s]")
    tag = "italic bright_cyan on_blue"
    console.print(f"[{tag}]Italic bright cyan on blue[/{tag}]")
    console.print("[color(208)]256-color orange[/color(208)]")
    console.print("[#ff8000]Hex orange[/#ff8000]")
    console.print("[rgb(100,200,50)]RGB green[/rgb(100,200,50)]")
    console.print("")
    console.print("A styled table:")
    console.table(
        [
            ["[b]Feature[/b]", "[b]Status[/b]"],
            ["Lexer", "[green]Stable[/green]"],
            ["Tables", "[green]Stable[/green]"],
            ["CLI", "[yellow]In Progress[/yellow]"],
        ]
    )


@command()
def users(
    fmt: str = Option(
        ["--format", "-f"], help="Output format (list or table)", default="list"
    ),
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
            + [
                [name, email, f"[red]{role}[/red]" if role == "admin" else role]
                for name, email, role in data
            ]
        )
    else:
        for name, email, role in data:
            console.print(f"  [b]{name}[/b] <{email}> [{role}]")


if __name__ == "__main__":
    run()
