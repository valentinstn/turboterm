# TurboTerm — Next Steps

Last updated: 2026-02-20

## Current State

All 5 original milestones are complete. The comfy-table dependency was replaced with a custom renderer, dropping ~20 transitive crates. Binary is 770 KB (.so), all 103 tests pass.

### Latest Benchmarks (arm64 macOS, release build, 2026-02-20)

| Metric | turboterm | rich | click/typer |
|---|---:|---:|---:|
| Import time | 0.85 ms | 2.7 ms | 12 / 23 ms |
| End-to-end script | 0.79 ms | 28.9 ms | — |
| Styling throughput | 1.85M ops/s | 215K ops/s | — |
| Table rendering | 9,835 tables/s | 99 tables/s | — |
| Memory overhead | +368 KB | +1,664 KB | +5.9 / +10.0 MB |

README benchmarks are accurate. CHANGELOG is up to date.

## Priority: High

### 1. Further binary size reduction

Current: 770 KB. Original target: 400-500 KB. The remaining size is mostly `clap` (~200 KB) and `pyo3` (~300 KB). Options:
- Replace `clap` with a minimal hand-rolled parser or `pico-args` (~5 KB)
- Explore `pyo3` feature flags to strip unused functionality
- Try `opt-level = "z"` (optimize for size over speed)
- Use `cargo-bloat` to identify remaining fat

## Priority: Medium

### 2. Generate `.pyi` type stubs

Milestone 4 mentioned auto-generated type stubs for IDE type-safety. Currently no `.pyi` files exist. Options:
- `pyo3-stub-gen` crate
- Hand-written stubs (small API surface)

### 3. Table features

The custom renderer is minimal. Potential additions:
- Column alignment (left/center/right)
- Header row styling (auto-bold first row)
- Max column width with text wrapping
- Column count mismatch handling (rows with different lengths)

### 4. Progress bars / spinners

Natural extension of the terminal toolkit. Would compete with `rich.progress` and `tqdm`. Implement in Rust for minimal overhead.

## Priority: Low

### 5. Markdown-to-ANSI renderer

Was cancelled earlier due to newline complexity. Could revisit with a simpler scope (inline formatting only, no block elements).

### 6. First PyPI release

All features are in place. Checklist:
- [x] Update README benchmarks
- [x] Update CHANGELOG
- [ ] Generate type stubs
- [ ] Tag v0.1.0
- [ ] Trigger release workflow
