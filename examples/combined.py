#!/usr/bin/env python3
"""
Combined example — showcases colors, bold, underline, and tables,
including inside --help output.

Usage:
    uv run examples/combined.py show --help
    uv run examples/combined.py show
    uv run examples/combined.py show --project myapp --verbose
"""

import turboterm
from turboterm import console
from turboterm.cli import Option, command, run

# ── table shown in --help ──────────────────────────────────────────────────
# Col1 visible width = 16, Col2 visible width = 22
# Border = ┌/├/└ + 18x─ + ┬/┼/┴ + 24x─ + ┐/┤/┘  (total 45 chars)
_H = "┌" + "─" * 18 + "┬" + "─" * 24 + "┐"
_M = "├" + "─" * 18 + "┼" + "─" * 24 + "┤"
_F = "└" + "─" * 18 + "┴" + "─" * 24 + "┘"


def _row(c1: str, c1_vis: int, c2: str, c2_vis: int) -> str:
    """Build one table row; c1_vis/c2_vis are the visible lengths of c1/c2."""
    return "│ " + c1 + " " * (16 - c1_vis) + " │ " + c2 + " " * (22 - c2_vis) + " │"


_MARKUP_TABLE = turboterm.apply_styles(
    "\nSupported markup tags:\n"
    + _H + "\n"
    + _row("Tag", 3, "Renders as", 10) + "\n"
    + _M + "\n"
    + _row("[b]bold[/b]", 4, "[b]bold text[/b]", 9) + "\n"
    + _row("[u]underline[/u]", 9, "[u]underlined text[/u]", 15) + "\n"
    + _row("[red]color[/red]",             5,  "[red]red foreground[/red]",      14) + "\n"
    + _row("[bold red]combined[/bold red]", 8, "[bold red]bold + colored[/bold red]", 14) + "\n"
    + _F
)

# ── command ────────────────────────────────────────────────────────────────


@command(after_help=_MARKUP_TABLE)
def show(
    project: str = Option(
        ["--project", "-p"],
        help="[bold]Project[/bold] name — e.g. [cyan]turboterm[/cyan] or [cyan]myapp[/cyan]",
        default="turboterm",
    ),
    env: str = Option(
        ["--env", "-e"],
        help="Target environment: [green]staging[/green] or [red]production[/red]",
        default="staging",
    ),
    verbose: bool = Option(
        ["--verbose", "-v"],
        help="Show [u]all[/u] benchmark metrics instead of a [bold]summary[/bold]",
    ),
):
    """[bold green]Project Overview[/bold green] — [u]styled output[/u], tables, and CLI in one package.

    Demonstrates [bold]bold[/bold], [u]underline[/u], [green]colors[/green], and
    [bold cyan]table rendering[/bold cyan] — all from a single Rust-backed import.

    Run with [yellow]--verbose[/yellow] to see the full benchmark table.
    """
    console.print(
        f"[bold green underline]Project Overview: {project}[/bold green underline]"
    )
    console.print("")

    env_tag = "[green]staging[/green]" if env == "staging" else "[red]production[/red]"
    console.print(f"[bold]Environment:[/bold]  {env_tag}")
    console.print("[bold]Language:[/bold]    Python + Rust (PyO3)")
    console.print("[bold]Version:[/bold]     [cyan]v0.3.0[/cyan]")
    console.print("[bold]Build:[/bold]       [green]passing[/green]")
    console.print("[bold]Coverage:[/bold]    [yellow]74%[/yellow]  ← needs improvement")
    console.print("")

    console.print("[underline]Recent changes[/underline]")
    console.print(
        "  • [green]feat:[/green] [bold]table renderer[/bold]"
        " — 10× faster, zero dependencies"
    )
    console.print(
        "  • [green]feat:[/green] [bold]CLI framework[/bold]"
        " — clap-backed argument parsing"
    )
    console.print(
        "  • [yellow]fix:[/yellow]  [bold]ANSI-aware column widths[/bold]"
        " — correct alignment with escape codes"
    )
    console.print("  • [red]break:[/red] dropped Python 3.10 support")
    console.print("")

    rows = [
        ["[b]Metric[/b]", "[b]TurboTerm[/b]", "[b]rich[/b]", "[b]Speedup[/b]"],
        ["Import time", "[green]0.85 ms[/green]", "2.70 ms", "[bold cyan]3×[/bold cyan]"],
        ["Styled output", "[green]1.85M/s[/green]", "215K/s", "[bold cyan]9×[/bold cyan]"],
        ["Table render", "[green]9 835/s[/green]", "99/s", "[bold cyan]99×[/bold cyan]"],
        ["End-to-end", "[green]0.79 ms[/green]", "28.9 ms", "[bold cyan]37×[/bold cyan]"],
    ]
    if not verbose:
        rows = [rows[0], rows[-1]]

    console.print("[underline]Benchmarks vs [bold]rich[/bold][/underline]")
    console.table(rows)


if __name__ == "__main__":
    run()
