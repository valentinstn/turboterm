# TurboTerm — Next Steps

Last updated: 2026-02-15

## Current State

All 5 original milestones are complete. The comfy-table dependency was replaced with a custom renderer, dropping ~20 transitive crates. Binary is 770 KB (.so), all 103 tests pass.

### Latest Benchmarks (arm64 macOS, 2026-02-15)

| Metric | turboterm | rich | click/typer |
|---|---:|---:|---:|
| Import time | 9.5 ms | 2.7 ms | 12 / 23 ms |
| Styling throughput | 280K ops/s | 217K ops/s | — |
| Table rendering | 1,471 tables/s | 98 tables/s | — |
| Memory overhead | +4.9 MB | +1.7 MB | +5.9 / +10.0 MB |

## Priority: High

### 1. Update README benchmarks

The README still references old numbers (2.0M ops/s styling, 2,600 tables/s). Update with the latest benchmark run above. The table rendering is 15x faster than Rich (down from 26x claim — but now without comfy-table overhead).

### 2. Update CHANGELOG for comfy-table removal

Add entry under `[Unreleased]`:
- Replaced `comfy-table` with custom UTF-8 table renderer
- Added `unicode-width` for ANSI-aware column width calculation
- Removed ~20 transitive dependencies
- Binary size: 934 KB -> 770 KB

### 3. Further binary size reduction

Current: 770 KB. Original target: 400-500 KB. The remaining size is mostly `clap` (~200 KB) and `pyo3` (~300 KB). Options:
- Replace `clap` with a minimal hand-rolled parser or `pico-args` (~5 KB)
- Explore `pyo3` feature flags to strip unused functionality
- Try `opt-level = "z"` (optimize for size over speed)
- Use `cargo-bloat` to identify remaining fat

### 4. Reduce memory overhead

Current: +4.9 MB. Target: +2-3 MB. Most of this is pyo3/Python bridge overhead, not application code. Investigate:
- `pyo3` feature trimming
- Lazy initialization of the STYLES HashMap
- Profile with `heaptrack` or `dhat` to find allocations

## Priority: Medium

### 5. Generate `.pyi` type stubs

Milestone 4 mentioned auto-generated type stubs for IDE type-safety. Currently no `.pyi` files exist. Options:
- `pyo3-stub-gen` crate
- Hand-written stubs (small API surface)

### 6. Table features

The custom renderer is minimal. Potential additions:
- Column alignment (left/center/right)
- Header row styling (auto-bold first row)
- Max column width with text wrapping
- Column count mismatch handling (rows with different lengths)

### 7. Progress bars / spinners

Natural extension of the terminal toolkit. Would compete with `rich.progress` and `tqdm`. Implement in Rust for minimal overhead.

## Priority: Low

### 8. Markdown-to-ANSI renderer

Was cancelled earlier due to newline complexity. Could revisit with a simpler scope (inline formatting only, no block elements).

### 9. First PyPI release

All features are in place. Checklist:
- [ ] Update README benchmarks
- [ ] Update CHANGELOG
- [ ] Generate type stubs
- [ ] Tag v0.1.0
- [ ] Trigger release workflow
