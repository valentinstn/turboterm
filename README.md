<h1 align="center">TurboTerm</h1>
<p align="center">
    <em>⚡ A high-performance terminal styling and CLI toolkit for Python, written in Rust 🦀</em>
</p>

## Why TurboTerm?

Python's CLI ecosystem is split: one library for colors, another for argument parsing, another for tables.
TurboTerm combines all three in a single package backed by Rust — so your CLI renders faster and you don't need to juggle dependencies.

| Benchmark | turboterm | rich | click/typer |
|---|---:|---:|---:|
| End-to-end script | **0.8 ms** | 29 ms | — |
| Styling throughput | **1.8M ops/s** | 217K ops/s | — |
| Table rendering (100 rows) | **9,700 tables/s** | 98 tables/s | — |
| Memory overhead | **+400 KB** | +1.7 MB | +5.9 / +9.9 MB |
| Import time | **0.7 ms** | 2.7 ms | 12 / 23 ms |

> **36x faster** end-to-end scripts, **8x faster** styling, **99x faster** tables than rich — with just 400 KB memory overhead.
> Reproduce with `uv run benchmark.py`.

## Installation

```
pip install turboterm
```

## Usage

### CLI framework

Define subcommands, arguments, and flags with decorators — powered by Rust's `clap` under the hood:

```python
# deploy.py
from turboterm import console
from turboterm.cli import command, Argument, Option, run

@command()
def push(env: str = Argument(help="Target environment"),
         tag: str = Option(["--tag", "-t"], help="Image tag", default="latest"),
         dry_run: bool = Option(["--dry-run"], help="Simulate the deploy")):
    """Push a deployment to an environment."""
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] would deploy {tag} to {env}")
    else:
        console.print(f"[green]Deployed {tag} to {env}[/green]")

@command()
def rollback(env: str = Argument(help="Target environment"),
             steps: int = Option(["--steps", "-n"], help="Versions to roll back", default=1)):
    """Roll back to a previous version."""
    console.print(f"[red]Rolled back {env} by {steps} version(s)[/red]")

run()
```

```
$ python deploy.py push staging --tag v2.1.0
Deployed v2.1.0 to staging

$ python deploy.py push production --dry-run
DRY RUN: would deploy latest to production

$ python deploy.py rollback production --steps 2
Rolled back production by 2 version(s)

$ python deploy.py --help
Usage: deploy.py <COMMAND>

Commands:
  push       Push a deployment to an environment.
  rollback   Roll back to a previous version.
```

### Styled output

```python
from turboterm import console

# Attributes and colors
console.print("[b]Bold[/b], [i]italic[/i], [u]underline[/u], [s]strike[/s]")
console.print("[red]Red[/red] [green]Green[/green] [blue]Blue[/blue]")

# Compound tags — multiple styles in one
console.print("[bold red on_blue]Bold red on blue background[/bold red on_blue]")

# 256-color, truecolor, and hex
console.print("[color(208)]Orange[/color(208)] [rgb(255,128,0)]RGB[/rgb(255,128,0)] [#ff8000]Hex[/#ff8000]")

# Nesting restores correctly
console.print("[b]Bold then [red]bold-red[/red] back to bold[/b]")
```

### Tables

```python
from turboterm import console

console.table([
    ["[b]Name[/b]", "[b]Email[/b]", "[b]Role[/b]"],
    ["Alice", "alice@example.com", "[green]admin[/green]"],
    ["Bob", "bob@example.com", "user"],
    ["Charlie", "charlie@example.com", "[yellow]pending[/yellow]"],
])
```

### Direct API

`apply_styles()` returns a plain string — works with `print()`, logging, file writes, anything:

```python
import turboterm

styled = turboterm.apply_styles("[bold green]OK[/bold green]")
print(styled)
```

See [`examples/`](examples/) for more complete examples.

## Development

```bash
git clone https://github.com/valentinstn/turboterm.git
cd turboterm
uv run maturin develop
```

### Running tests

```bash
uv run python -m unittest discover tests
```

### Running benchmarks

```bash
uv run benchmark.py
```

## License

MIT License
