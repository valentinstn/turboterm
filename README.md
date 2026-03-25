<h1 align="center">TurboTerm</h1>
<p align="center">
    <em>⚡ A high-performance, ultra-concise CLI and styling toolkit for Python, written in Rust 🦀</em>
</p>

`TurboTerm` is minimal and efficient by all means:

- **Less code**: Concise CLI syntax, ~50% less lines of code compared to Python's argparse.
- **Faster import**: Lightweight import and loading times, multiple times faster than `rich`, `click` or `typer`.
- **Faster runtime**: Every formatting/rendering logic is implemented in Rust, and optimized for performance.
- **No additional dependencies**: TurboTerm is installed as a single wheel, without depending on any other Python package.
- **No feature bloat**: TurboTerm focuses on the essentials: Decorators for minimal CLI, styled output, tables, and argument parsing.

## Example

<p align="center">
    <img src="https://raw.githubusercontent.com/valentinstn/turboterm/main/assets/example.png" alt="Example output" width="500">
</p>

## Benchmarks

<p align="center">
    <img src="https://raw.githubusercontent.com/valentinstn/turboterm/main/assets/benchmark.svg" alt="Import time comparison" width="500">
</p>
<p align="center">
    <img src="https://raw.githubusercontent.com/valentinstn/turboterm/main/assets/perf.svg" alt="Performance vs Rich" width="500">
</p>

## Installation

```sh
pip install turboterm
# or
uv add turboterm
```

## Quickstart

```python
from turboterm import console
from turboterm.cli import Option, command, run

@command
def greet(
    name: str = Option(["--name", "-n"], default="World"),
):
    """Greet someone."""
    console.print(f"[bold]Hello, {name}![/bold]")

if __name__ == "__main__":
    run()
```

```
python app.py --name Alice
# Hello, Alice!

python app.py --help
```

For the full API reference see [USAGE.md](https://github.com/valentinstn/turboterm/blob/main/USAGE.md).

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
uv run python scripts/benchmark.py    # full benchmark + regenerate charts
```

## License

MIT License
