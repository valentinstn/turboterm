# TurboTerm 🚀

**The "uv" of CLI UI: A High-Performance, Oxidized Toolkit for Beautiful Terminal Formatting**

TurboTerm aims to revolutionize command-line interface (CLI) aesthetics and performance. Built with a Rust core and a shallow Python API, it delivers stunning terminal output with near-zero overhead, making it significantly faster than pure-Python alternatives.

## ✨ Features

*   **Lightning Lexer:** A stack-based, single-pass character scanner in Rust for incredibly fast styled text processing (e.g., `[b red]Hello[/b]` → `\x1b[1;31mHello\x1b[0m`). Supports nested styles.
*   **Turbo-Tables:** Efficiently renders complex tables with `comfy-table`, supporting styled content within cells.
*   **Pre-configured Console:** A global `console` singleton for immediate, easy-to-use access to all formatting features.
*   **Extreme Performance:** Designed for < 5ms import times and significantly faster table rendering.
*   **Oxidized Core:** All heavy lifting (parsing, layout, rendering) is done in Rust via PyO3.
*   **Zero-Dependency:** Statically linked for a clean `pip install` experience.
*   **Compatibility:** SISO (String-In, String-Out) architecture ensures compatibility with standard `print()`, logging, and redirects.

## 🚀 Installation

```bash
uv pip install turboterm
```

## 💡 Usage

```python
from turboterm import console

# Print styled text
console.print("[b red]This is bold red text![/b red]")

# Print a styled table
data = [
    ["[b]Header 1[/b]", "[red]Header 2[/red]"],
    ["Row 1 Col 1", "Row 1 Col 2"],
    ["[u]Row 2 Col 1[/u]", "Row 2 Col 2"]
]
console.table(data)
```

## 🧑‍💻 Development

### Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/turboterm.git
    cd turboterm
    ```
2.  Set up a Python virtual environment with `uv`:
    ```bash
    uv venv
    uv add maturin mypy pytest
    ```
3.  Build the Rust extension in editable mode:
    ```bash
    uv run maturin develop
    ```

### Running Tests

```bash
uv run python -m unittest discover tests
```

### Building Wheels

```bash
uv run maturin build --release --out dist
```

## 🤝 Contributing

We welcome contributions! Please see `CONTRIBUTE.md` for guidelines.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
