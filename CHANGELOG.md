# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-02-21

- **USAGE.md** — full API reference for console output, markup tags, tables, and CLI commands.
- **README quickstart** — minimal CLI example with link to USAGE.md.

[0.1.1]: https://github.com/valentinstn/turboterm/releases/tag/v0.1.1

## [0.1.0] — 2026-02-21

- **Lightning Lexer** — single-pass Rust parser for a custom markup language (`[bold red]text[/]`), supporting 16 named colors, 256-color, truecolor, hex, text attributes, and arbitrary nesting.
- **Turbo-Tables** — custom UTF-8 table renderer with full styled-markup support in cell content.
- **Console singleton** — zero-setup `console.print()` and `console.table()` for immediate styled output.
- **CLI framework** — `@command()`, `Argument()`, and `Option()` decorators backed by Rust's `clap`, with auto-generated help and docstring integration.
- **103 tests**, cross-platform CI, and release workflow for automated PyPI publishing.

[0.1.0]: https://github.com/valentinlamine/turboterm/releases/tag/v0.1.0
