# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-02-21

TurboTerm is a Rust-powered Python terminal toolkit that delivers rich ANSI styling, beautiful tables, and a decorator-based CLI framework — all from a single, lightweight binary extension (~770 KB). At its core is a single-pass, stack-based lexer written in Rust that parses a custom markup language (`[bold red]text[/]`) into ANSI escape sequences with nanosecond-level throughput. The lexer supports the full spectrum of terminal color: 16 named colors, 256-color `color(N)` / `on_color(N)`, truecolor `rgb(R,G,B)`, and hex `#RRGGBB` — in both foreground and background variants. Text attributes including `bold`, `italic`, `underline`, `dim`, `blink`, `strike`, `inverse`, `overline`, and `hidden` can be combined freely in compound tags and nested arbitrarily with correct reset/restore semantics. TurboTerm also ships Turbo-Tables, a custom UTF-8 table renderer with full lexer integration so every cell can contain styled markup. A ready-to-use `console` singleton exposes `console.print()` and `console.table()` for zero-setup terminal output. The built-in CLI framework lets you build multi-subcommand apps with `@command()`, `Argument()`, and `Option()` decorators backed by Rust's `clap` library, with auto-generated help and docstring integration. The package is fully tested (103 tests), published with a CI/CD pipeline for cross-platform wheel builds, and benchmarks 8× faster than Rich for styling and 99× faster for table rendering.

[0.1.0]: https://github.com/valentinlamine/turboterm/releases/tag/v0.1.0
