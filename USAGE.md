# Usage Guide

Full documentation for the `turboterm` library.

---

## Console output

```python
from turboterm import console

console.print("Hello, world!")
console.print("[bold]Bold text[/bold]")
console.print("[green]Green text[/green]")
console.print("[bold red]Bold and red[/bold red]")
console.print("[u]Underlined[/u]")
```

### Markup tags

| Tag | Effect |
|-----|--------|
| `[b]` / `[bold]` | Bold |
| `[u]` / `[underline]` | Underline |
| `[red]`, `[green]`, `[cyan]`, `[yellow]`, ... | Foreground color |
| `[bold red]` | Combined styles |
| `[/bold]`, `[/red]`, etc. | Close a tag |

---

## Tables

```python
from turboterm import console

rows = [
    ["Name", "Version", "Status"],
    ["turboterm", "0.1.1", "stable"],
    ["myapp", "2.3.1", "beta"],
]
console.table(rows)
```

Markup tags work inside table cells.

---

## CLI commands

### Basic command

```python
from turboterm.cli import command, run

@command
def hello():
    """Say hello."""
    print("Hello!")

if __name__ == "__main__":
    run()
```

### Command with options

```python
from turboterm import console
from turboterm.cli import Option, command, run

@command
def deploy(
    project: str = Option(["--project", "-p"], default="myapp"),
    env: str = Option(["--env", "-e"], default="staging"),
    verbose: bool = Option(["--verbose", "-v"]),
):
    """Deploy a project to the target environment."""
    console.print(f"[bold]Deploying[/bold] {project} → [green]{env}[/green]")
    if verbose:
        console.print("  Verbose mode enabled")

if __name__ == "__main__":
    run()
```

Run it:

```
python app.py --project myapp --env production --verbose
```

### `after_help`

Pass extra content to display after the `--help` output:

```python
@command(after_help="See https://example.com for more.")
def deploy(...):
    ...
```

---

## Applying styles to strings

Use `turboterm.apply_styles()` to render markup into an ANSI-escaped string without printing it:

```python
import turboterm

styled = turboterm.apply_styles("[bold green]OK[/bold green]")
```

This is useful for building content passed to other functions, such as `after_help`.
