#!/usr/bin/env python3
"""
Real-world-ish example — a deploy tool that mixes positional args,
typed options, and bool flags across multiple subcommands.

Usage:
    uv run examples/deploy_tool.py push staging
    uv run examples/deploy_tool.py push production --tag v1.2.3 --dry-run
    uv run examples/deploy_tool.py rollback production --steps 2
    uv run examples/deploy_tool.py logs staging --lines 50 --follow
    uv run examples/deploy_tool.py --help
"""

from turboterm import console
from turboterm.cli import command, Argument, Option, run


@command()
def push(
    env: str = Argument(help="Target environment (staging, production)"),
    tag: str = Option(["--tag", "-t"], help="Git tag to deploy", default="HEAD"),
    dry_run: bool = Option(["--dry-run"], help="Simulate without actually deploying"),
):
    """Push a deployment to the target environment."""
    if dry_run:
        console.print("[u]DRY RUN[/u] — no changes will be made")
    console.print(f"[b]Deploying[/b] {tag} to [red]{env}[/red]...")
    console.print("  Building image...")
    console.print("  Pushing to registry...")
    console.print("  Updating service...")
    if not dry_run:
        console.print("[b]Deployed[/b] successfully!")
    else:
        console.print("[u]Dry run complete.[/u]")


@command()
def rollback(
    env: str = Argument(help="Target environment"),
    steps: int = Option(
        ["--steps", "-s"], help="Number of versions to roll back", default=1
    ),
):
    """Roll back to a previous deployment."""
    console.print(f"[b]Rolling back[/b] [red]{env}[/red] by {steps} version(s)...")
    console.print("Done.")


@command()
def logs(
    env: str = Argument(help="Target environment"),
    lines: int = Option(["--lines", "-n"], help="Number of log lines", default=20),
    follow: bool = Option(["--follow", "-f"], help="Follow log output in real time"),
):
    """View deployment logs."""
    mode = "streaming" if follow else "static"
    lines = int(lines)
    console.print(
        f"[b]Fetching {lines} log lines[/b] from [red]{env}[/red] ({mode})..."
    )
    for i in range(min(lines, 5)):
        console.print(f"  [{env}] Log line {i + 1}: All systems operational")


if __name__ == "__main__":
    run()
