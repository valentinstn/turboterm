# TurboTerm — Vision & Architecture

**Goal:** The "uv" of CLI UI. A high-performance, oxidized toolkit that provides beautiful terminal formatting with near-zero overhead.

## Core Philosophy

- **Extreme Performance:** 10x-50x faster startup than pure-Python alternatives.
- **Oxidized Core:** 100% of logic (parsing, layout, rendering) happens in Rust via PyO3.
- **Zero-Dependency:** Statically linked; `pip install` results in a single binary extension.
- **Compatibility:** Python 3.11+ (general), Python 3.14 (development).
- **SISO** (String-In, String-Out) architecture — works with `print()`, logging, redirects.

## Architecture

- **Language:** Rust (engine) + Python (shallow API)
- **Bindings:** PyO3 (Bound API)
- **Key Crates:**
  - `clap` — CLI argument parsing (no default features, minimal footprint)
  - `unicode-width` — accurate cell sizing (CJK/emoji)
  - `pyo3` — Python bindings
- **Build System:** Maturin + GitHub Actions

## Repository Structure

```
turboterm/
├── .github/workflows/   # CI + release workflows
├── src/                 # Rust source
│   ├── lib.rs           # PyO3 module entry point
│   ├── lexer.rs         # Style parser + visible_width()
│   ├── table.rs         # Custom UTF-8 table renderer
│   └── cli.rs           # CLI framework (clap bridge)
├── turboterm/           # Python wrapper & .pyi stubs
├── tests/               # 103 tests (unittest)
├── examples/            # Example scripts
├── scripts/             # Dev scripts
│   └── benchmark.py     # Performance benchmarks
├── Cargo.toml           # Rust dependencies
└── pyproject.toml       # Maturin build config
```

## Milestones

### Milestone 1: Lightning Lexer — DONE

Stack-based, single-pass ANSI style parser in Rust. Supports text attributes, 16/256/truecolor, hex, compound tags, and nested styles with correct reset/restore.

### Milestone 2: Turbo-Tables — DONE

Custom UTF-8 table renderer (replaced `comfy-table` in Feb 2025). Zero external rendering dependencies. Box-drawing output with styled cell content via the lexer. 15x faster than Rich.

### Milestone 3: DX — DONE

- Lazy loading (`import turboterm` < 10ms)
- Global `console` singleton with `print()` and `table()` methods
- Markdown renderer: cancelled (complexity vs. value)

### Milestone 4: Global Distribution — DONE

GitHub Actions CI/CD: lint, test, cross-platform wheel builds, PyPI upload on release.

### Milestone 5: CLI Framework — DONE

Decorator-based CLI parsing powered by Rust's `clap`. Subcommands, arguments, options, auto-help.

---

See [TODO.md](TODO.md) for concrete next steps.
