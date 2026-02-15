# PLAN.md: TurboTerm 🚀

**Project Goal:** To become the "uv" of CLI UI. A high-performance, oxidized toolkit that provides beautiful terminal formatting with near-zero overhead.

---

## 1. Core Philosophy
* **Extreme Performance:** 10x–50x faster startup than pure-Python alternatives.
* **Oxidized Core:** 100% of logic (parsing, layout, rendering) happens in Rust via PyO3.
* **Zero-Dependency:** Statically linked; `pip install` should result in a single binary extension.
* **Compatibility:** Python 3.11+ (for general compatibility), Python 3.14 (for development)
* **SISO** (String-In, String-Out) architecture ensures it works with standard `print()`, logging, and redirects.

---

## 2. Technical Architecture
* **Language:** Rust (Engine) + Python (Shallow API).
* **Bindings:** `PyO3` (leveraging `Bound` API for memory efficiency).
* **Key Crates:**
    * `comfy-table`: For optimized table layout.
    * `ansiterm`: For hardware-compatible ANSI generation.
    * `unicode-width`: For accurate cell sizing (Emoji/CJK support).
* **Build System:** `Maturin` + `GitHub Actions`.



---

## 3. Implementation Milestones

### Milestone 1: The Lightning Lexer
* **Task:** Implement a stack-based, single-pass character scanner in Rust.
* **Input:** `[b red]Hello[/b red]` → **Output:** `\x1b[1m\x1b[31mHello\x1b[0m`.
* **Constraint:** O(n) complexity. Avoid regex to minimize binary size and maximize speed.
* **Nesting:** Support nested styles (e.g., `[b]bold [u]underlined[/u][/b]`).

### Milestone 2: Turbo-Tables
* **Task:** Efficiently bridge Python data structures to the `comfy-table` engine.
* **Logic:** Rust calculates all column widths, alignment, and word wrapping.
* **Feature:** Tables must support the "Lightning Lexer" for styled content within cells.

### Milestone 3: The "uv" Experience (DX)
* **Lazy Loading:** Keep `__init__.py` minimal to ensure `import turboterm` takes **< 5ms**.
* **Global Console:** Provide a pre-configured `console` singleton for immediate use.
* **Markdown:** Add a basic Markdown-to-ANSI renderer implemented entirely in Rust.

### Milestone 4: Global Distribution

*   **Automation:** GitHub Actions workflow using `maturin-action`.

*   **Matrix:** Build wheels for Windows (x64), MacOS (Universal), and Linux (manylinux/musllinux).

*   **Quality:** Generate `.pyi` type stubs automatically for 100% IDE type-safety.



### Milestone 5: CLI Framework (Argparse Replacement)

*   **Task:** Implement a Rust-powered, Python-friendly CLI argument parsing framework that replaces `argparse` with rich styling and interactive capabilities.

*   **Pythonic API:** Decorator/Class-based argument definition similar to `Typer` or `Click`, leveraging Python type hints.

*   **Rust Parsing Engine:** Core parsing logic in Rust for performance and robust validation (`clap` or `pico-args` integration).

*   **Styled Help Output:** Automatically generate beautifully styled help messages (syntax highlighting, styled descriptions, tables) using TurboTerm's existing lexer and table rendering.

*   **Interactive Prompts:** Provide styled prompts for missing arguments, confirmations, choices, and text input using `ansiterm` or similar.

*   **`console` Integration:** Expose `console.command()`, `console.argument()`, `console.option()`, and `console.run()` for a seamless user experience.



---



## 4. Performance Targets


| Metric | Target | vs. Competitors |
| :--- | :--- | :--- |
| **Import Time** | < 5ms | ~20x faster than Rich |
| **Table Render** | < 50ms (10k rows) | Significantly lower CPU/Memory usage |
| **Dependency Count** | 0 | Cleaner `site-packages` |

---

## 5. Repository Structure
```text
turboterm/
├── .github/workflows/   # maturin-action release logic
├── src/                 # Rust source code (lib.rs, lexer.rs, table.rs)
├── turboterm/           # Python wrapper & .pyi stubs
├── tests/               # Performance & correctness tests
├── Cargo.toml           # Rust dependencies
└── pyproject.toml       # Maturin build configuration
