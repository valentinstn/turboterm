#!/usr/bin/env python3
"""
Formatted help text — TurboTerm markup in CLI help strings.

Help text (docstrings and help= arguments) can contain TurboTerm markup.
The markup is rendered to ANSI when --help is displayed.

Usage:
    python examples/formatted_help.py --help
    python examples/formatted_help.py deploy --help
    python examples/formatted_help.py rollback --help
    python examples/formatted_help.py deploy staging --tag v2.1.0
    python examples/formatted_help.py deploy production --dry-run
"""

from turboterm import console
from turboterm.cli import Argument, Option, command, run


@command()
def deploy(
    env: str = Argument(
        help="Target environment: [green]staging[/green] or [red]production[/red]"
    ),
    tag: str = Option(
        ["--tag", "-t"],
        help="Docker image tag to deploy (e.g. [cyan]v2.1.0[/cyan])",
        default="latest",
    ),
    dry_run: bool = Option(
        ["--dry-run"],
        help="[yellow]Simulate[/yellow] the deploy without making changes",
    ),
):
    """[bold]Deploy[/bold] the application to an environment."""
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] would deploy [cyan]{tag}[/cyan] → {env}")
    else:
        console.print(f"[green]Deployed[/green] [cyan]{tag}[/cyan] → {env}")


@command()
def rollback(
    env: str = Argument(
        help="Target environment: [green]staging[/green] or [red]production[/red]"
    ),
    steps: int = Option(
        ["--steps", "-n"],
        help="Number of versions to roll back ([bold]default: 1[/bold])",
        default=1,
    ),
):
    """[bold]Roll back[/bold] to a previous version.

    Rolls back [italic]steps[/italic] versions in the given environment.
    Use [yellow]--dry-run[/yellow] on the deploy command to preview before reverting.
    """
    console.print(f"[red]Rolled back[/red] {env} by [bold]{steps}[/bold] version(s)")


if __name__ == "__main__":
    run()
