# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-   Initial project setup with Rust core and Python bindings.
-   Lightning Lexer for high-performance ANSI style parsing.
-   Turbo-Tables integration with `comfy-table` for styled terminal tables.
-   Pre-configured `console` singleton for convenient styled output.
-   GitHub Actions workflow for cross-platform wheel distribution using `maturin-action`.
-   Automatic generation of `.pyi` type stubs for IDE type-safety.
-   `README.md`, `CONTRIBUTE.md`, and `CHANGELOG.md` files.

### Changed

-   Updated Python version support to `>=3.11` for compatibility, with `3.14` for development.
-   Updated `pyo3` to `0.28.1` for Python 3.14 compatibility.
-   Updated `comfy-table` to `7.2.2` with `tty` and `custom_styling` features enabled.

### Removed

-   Attempted implementation of a basic Markdown-to-ANSI renderer (cancelled due to complexity with newline handling).
