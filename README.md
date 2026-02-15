<h1 align="center">TurboTerm</h1>
<p align="center">
    <em>High-performance terminal styling and CLI toolkit for Python, written in Rust</em>
</p>

## Installation

```
pip install turboterm
```

## Usage

### Styled output

```python
from turboterm import console

# Text attributes, colors, and compound tags
console.print("[b]Bold[/b], [i]italic[/i], [u]underline[/u], [s]strike[/s]")
console.print("[red]Red[/red] [green]Green[/green] [blue]Blue[/blue]")
console.print("[bold red on_blue]Compound: bold + red + blue background[/bold red on_blue]")

# 256-color, truecolor, and hex
console.print("[color(208)]256-color[/color(208)] [rgb(255,128,0)]RGB[/rgb(255,128,0)] [#ff8000]Hex[/#ff8000]")

# Nested styles restore correctly
console.print("[b]Bold then [red]bold-red[/red] then bold again[/b]")
```

### Tables

```python
from turboterm import console

console.table([
    ["[b]Name[/b]", "[b]Status[/b]"],
    ["Alice", "[green]Active[/green]"],
    ["Bob", "[red]Inactive[/red]"],
    ["[dim]Charlie[/dim]", "[yellow]Pending[/yellow]"],
])
```

### CLI framework

```python
from turboterm import console

@console.command()
def greet(name: str = console.argument(help="Name to greet"),
          shout: bool = console.option(["--shout", "-s"], help="Shout the greeting")):
    """Greet someone."""
    msg = f"Hello, {name}!"
    if shout:
        msg = msg.upper()
    console.print(f"[green]{msg}[/green]")

console.run()
```

See the [`examples/`](examples/) folder for more complete examples.

### Direct API

`apply_styles()` returns a plain string, compatible with standard `print()`, logging, and redirects:

```python
import turboterm

styled = turboterm.apply_styles("[bold green]Success[/bold green]")
print(styled)
```

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

### Building wheels

```bash
uv run maturin build --release --out dist
```

## License

MIT License
