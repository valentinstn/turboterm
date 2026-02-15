# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-   **Lightning Lexer** — stack-based, single-pass ANSI style parser in Rust.
    -   Text attributes: `bold`/`b`, `dim`, `italic`/`i`, `underline`/`u`, `blink`, `inverse`/`reverse`, `hidden`, `strike`/`s`/`strikethrough`, `overline`.
    -   Standard foreground colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.
    -   Bright foreground colors: `bright_black`/`grey`/`gray`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`.
    -   Standard background colors: `on_black` through `on_white`.
    -   Bright background colors: `on_bright_black`/`on_grey`/`on_gray` through `on_bright_white`.
    -   256-color support: `color(N)` (foreground), `on_color(N)` (background).
    -   Truecolor RGB: `rgb(R,G,B)` (foreground), `on_rgb(R,G,B)` (background).
    -   Hex colors: `#RRGGBB` (foreground), `on_#RRGGBB` (background).
    -   Compound tags: `[bold red on_blue]` applies multiple styles in a single tag.
    -   Nested styles with proper reset/restore on close.
-   **Turbo-Tables** — styled terminal tables with custom UTF-8 renderer and lexer integration for styled cell content.
-   **Console singleton** — pre-configured `console` object with `print()` and `table()` methods.
-   **CLI framework** — decorator-based CLI argument parsing powered by Rust (`clap`).
    -   `@command()` decorator for registering subcommands.
    -   `Argument()` for positional arguments with type conversion and defaults.
    -   `Option()` for named flags (`--flag`, `-f`) with bool, int, float, str support.
    -   Auto-generated help output with docstring integration.
    -   Multiple subcommands in a single app.
-   **CI workflow** (`.github/workflows/ci.yml`) — lint (`cargo fmt`, `clippy`, `ruff`), test (cross-platform), and wheel build on every push/PR.
-   **Release workflow** (`.github/workflows/release.yml`) — cross-platform wheel builds and PyPI upload on release.
-   Example scripts in `examples/` — hello CLI, calculator, server CLI, deploy tool, styled output demo.
-   Comprehensive test suite (103 tests) covering lexer, console, tables, CLI, and all examples.

### Changed

-   Python version support: `>=3.11`, with `3.14` for development.
-   `pyo3` `0.28.1` for Python 3.14 compatibility.
-   Replaced `comfy-table` with custom UTF-8 table renderer — removed ~20 transitive dependencies (crossterm, console, nom, vte, rustix, parking_lot, etc.).
-   Added `unicode-width` for ANSI-aware column width calculation.
-   Binary size reduced from 934 KB to 770 KB.

### Removed

-   Markdown-to-ANSI renderer (cancelled due to complexity with newline handling).
