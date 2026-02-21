#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "rich",
#   "click",
#   "typer",
# ]
# ///
"""
Benchmark TurboTerm against Rich, Click, and Typer.

Measures import time, styling throughput, memory usage, and table rendering.
Saves an SVG chart to assets/benchmark.svg.

Usage:
    uv run python scripts/benchmark.py
"""

import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets"


def _fresh_script_time(script: str, runs: int = 7) -> float:
    """Measure script execution time in a fresh subprocess (median of N runs)."""
    wrapped = (
        "import time as _t, sys as _s\n"
        "_start = _t.perf_counter()\n" + script + "\n"
        "print(_t.perf_counter() - _start, file=_s.stderr)"
    )
    times = []
    for _ in range(runs):
        r = subprocess.run(
            [sys.executable, "-c", wrapped],
            capture_output=True,
            text=True,
            timeout=30,
        )
        times.append(float(r.stderr.strip()))
    return statistics.median(times)


def _fresh_import_time(module: str, runs: int = 7) -> float:
    """Measure import time in a fresh subprocess (median of N runs)."""
    times = []
    for _ in range(runs):
        code = (
            f"import time; t=time.perf_counter(); import {module}; "
            f"print(time.perf_counter()-t)"
        )
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30,
        )
        times.append(float(r.stdout.strip()))
    return statistics.median(times)


def _memory_after_import(module: str | None, runs: int = 5) -> int:
    """Measure peak RSS (KB) after importing a module in a fresh subprocess."""
    if module:
        code = (
            f"import {module}; import resource; "
            f"print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
        )
    else:
        code = (
            "import resource; print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
        )
    values = []
    for _ in range(runs):
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # macOS reports in bytes, Linux in KB
        val = int(r.stdout.strip())
        if sys.platform == "darwin":
            val //= 1024
        values.append(val)
    return statistics.median(values)


def _generate_import_chart(times: dict[str, float]) -> str:
    """Generate a dark-themed SVG bar chart for import time comparison."""
    W = 660
    PAD_L = 24
    LABEL_X = 118  # label right edge (text-anchor=end)
    BAR_X = 126  # bar left edge
    BAR_MAX_W = 352  # max bar pixel width
    VAL_X = BAR_X + BAR_MAX_W + 10  # value text left edge
    MULT_X = W - PAD_L  # multiplier right edge (text-anchor=end)
    TITLE_H = 68
    ROW_H = 42
    BAR_H = 16
    FONT = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"

    os_name = {"darwin": "macOS", "linux": "Linux", "win32": "Windows"}.get(
        sys.platform, sys.platform
    )
    arch = platform.machine()
    subtitle = f"median of 7 runs · {arch} {os_name}"

    max_val = max(times.values())
    tt_val = times.get("turboterm", 1.0)

    total_rows = len(times)
    height = TITLE_H + total_rows * ROW_H + 16

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}">',
        f'  <rect width="{W}" height="{height}" fill="#0d1117" rx="10"/>',
        # Title (left) and subtitle (right)
        f'  <text x="{PAD_L}" y="36" fill="#e6edf3"'
        f' font-family="{FONT}" font-size="14" font-weight="600">Import Time</text>',
        f'  <text x="{W - PAD_L}" y="36" fill="#6e7681"'
        f' font-family="{FONT}" font-size="11" text-anchor="end">{subtitle}</text>',
        # Separator
        f'  <line x1="{PAD_L}" y1="64" x2="{W - PAD_L}" y2="64"'
        f' stroke="#21262d" stroke-width="1"/>',
    ]

    for i, (name, val) in enumerate(times.items()):
        y_center = TITLE_H + i * ROW_H + ROW_H // 2
        bar_w = max(4, int(val / max_val * BAR_MAX_W))

        is_tt = name == "turboterm"
        bar_color = "#3fb950" if is_tt else "#484f58"
        label_color = "#e6edf3" if is_tt else "#8b949e"
        val_color = "#3fb950" if is_tt else "#8b949e"

        # Label (right-aligned)
        lines.append(
            f'  <text x="{LABEL_X}" y="{y_center + 5}" fill="{label_color}"'
            f' font-family="{FONT}" font-size="13" text-anchor="end">{name}</text>'
        )
        # Bar
        lines.append(
            f'  <rect x="{BAR_X}" y="{y_center - BAR_H // 2}"'
            f' width="{bar_w}" height="{BAR_H}" fill="{bar_color}" rx="2"/>'
        )
        # Value
        val_text = f"{val * 1000:.2f} ms"
        lines.append(
            f'  <text x="{VAL_X}" y="{y_center + 5}" fill="{val_color}"'
            f' font-family="{FONT}" font-size="12">{val_text}</text>'
        )
        # Multiplier / badge
        if is_tt:
            lines.append(
                f'  <text x="{MULT_X}" y="{y_center + 5}" fill="#3fb950"'
                f' font-family="{FONT}" font-size="11" text-anchor="end">fastest</text>'
            )
        else:
            mult = val / tt_val
            lines.append(
                f'  <text x="{MULT_X}" y="{y_center + 5}" fill="#6e7681"'
                f' font-family="{FONT}" font-size="11"'
                f' text-anchor="end">{mult:.1f}\u00d7 slower</text>'
            )

    lines.append("</svg>")
    return "\n".join(lines)


def _generate_perf_chart(speedups: dict[str, float], subtitle: str) -> str:
    """Generate a dark-themed SVG bar chart showing speedup vs rich."""
    W = 660
    PAD_L = 24
    LABEL_X = 118
    BAR_X = 126
    BAR_MAX_W = 352
    MULT_X = W - PAD_L
    TITLE_H = 68
    ROW_H = 42
    BAR_H = 16
    FONT = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"

    max_speedup = max(speedups.values())
    sorted_items = sorted(speedups.items(), key=lambda x: -x[1])

    total_rows = len(sorted_items)
    height = TITLE_H + total_rows * ROW_H + 16

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}">',
        f'  <rect width="{W}" height="{height}" fill="#0d1117" rx="10"/>',
        f'  <text x="{PAD_L}" y="36" fill="#e6edf3"'
        f' font-family="{FONT}" font-size="14"'
        f' font-weight="600">Faster than Rich</text>',
        f'  <text x="{W - PAD_L}" y="36" fill="#6e7681"'
        f' font-family="{FONT}" font-size="11" text-anchor="end">{subtitle}</text>',
        f'  <line x1="{PAD_L}" y1="64" x2="{W - PAD_L}" y2="64"'
        f' stroke="#21262d" stroke-width="1"/>',
    ]

    for i, (metric, speedup) in enumerate(sorted_items):
        y_center = TITLE_H + i * ROW_H + ROW_H // 2
        bar_w = max(4, int(speedup / max_speedup * BAR_MAX_W))

        lines.append(
            f'  <text x="{LABEL_X}" y="{y_center + 5}" fill="#e6edf3"'
            f' font-family="{FONT}" font-size="13" text-anchor="end">{metric}</text>'
        )
        lines.append(
            f'  <rect x="{BAR_X}" y="{y_center - BAR_H // 2}"'
            f' width="{bar_w}" height="{BAR_H}" fill="#3fb950" rx="2"/>'
        )
        mult_text = f"{speedup:.1f}\u00d7 faster"
        lines.append(
            f'  <text x="{MULT_X}" y="{y_center + 5}" fill="#3fb950"'
            f' font-family="{FONT}" font-size="12"'
            f' text-anchor="end">{mult_text}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


def bench_import_time() -> dict[str, float]:
    """Benchmark import times. Returns {module: seconds}."""
    print("=" * 60)
    print("IMPORT TIME (median of 7 runs, fresh subprocess)")
    print("=" * 60)

    modules = ["turboterm", "rich", "click", "typer"]
    results: dict[str, float] = {}
    for mod in modules:
        try:
            t = _fresh_import_time(mod)
            results[mod] = t
            print(f"  {mod:<12s}  {t * 1000:8.2f} ms")
        except Exception as e:
            print(f"  {mod:<12s}  SKIPPED ({e})")

    if "turboterm" in results:
        tt = results["turboterm"]
        print()
        for mod, t in results.items():
            if mod != "turboterm":
                print(f"  vs {mod}: {t / tt:.1f}x")
    print()
    return results


def bench_styling() -> float | None:
    """Benchmark markup parsing throughput. Returns speedup vs rich, or None."""
    print("=" * 60)
    print("STYLING THROUGHPUT")
    print("=" * 60)

    try:
        import turboterm
    except ImportError:
        print("  turboterm    SKIPPED (build first: uv run maturin develop)")
        print()
        return None

    try:
        from rich.text import Text as RichText
    except ImportError:
        RichText = None

    markup = "[bold red]Hello, world![/bold red]"
    iterations = 100_000

    # turboterm
    start = time.perf_counter()
    for _ in range(iterations):
        turboterm.apply_styles(markup)
    tt_time = time.perf_counter() - start
    tt_ops = iterations / tt_time
    print(
        f"  turboterm    {iterations:>8,} iters in {tt_time:.4f}s"
        f"  ({tt_ops:,.0f} ops/sec)"
    )

    # rich
    if RichText:
        start = time.perf_counter()
        for _ in range(iterations):
            RichText.from_markup(markup)
        rich_time = time.perf_counter() - start
        rich_ops = iterations / rich_time
        print(
            f"  rich         {iterations:>8,} iters in {rich_time:.4f}s"
            f"  ({rich_ops:,.0f} ops/sec)"
        )
        speedup = rich_time / tt_time
        print(f"\n  turboterm is {speedup:.1f}x faster")
        print()
        return speedup
    print()
    return None


def bench_memory():
    """Benchmark memory usage."""
    print("=" * 60)
    print("MEMORY USAGE (peak RSS after import)")
    print("=" * 60)

    baseline = _memory_after_import(None)
    print(f"  {'baseline':<12s}  {baseline:>8,} KB")

    modules = ["turboterm", "rich", "click", "typer"]
    for mod in modules:
        try:
            rss = _memory_after_import(mod)
            overhead = rss - baseline
            print(f"  {mod:<12s}  {rss:>8,} KB  (+{overhead:,} KB)")
        except Exception as e:
            print(f"  {mod:<12s}  SKIPPED ({e})")
    print()


def bench_tables() -> float | None:
    """Benchmark table rendering. Returns speedup vs rich, or None."""
    print("=" * 60)
    print("TABLE RENDERING (100 rows x 4 columns, 100 iterations)")
    print("=" * 60)

    try:
        from turboterm import PyTable
    except ImportError:
        print("  turboterm    SKIPPED (build first: uv run maturin develop)")
        print()
        return None

    try:
        from rich.table import Table as RichTable
    except ImportError:
        RichTable = None

    rows = [
        [f"Row {i}", f"Value {i}", f"Description for item {i}", "Active"]
        for i in range(100)
    ]
    iterations = 100

    # turboterm
    start = time.perf_counter()
    for _ in range(iterations):
        t = PyTable()
        for row in rows:
            t.add_row(row)
        t.to_string()
    tt_time = time.perf_counter() - start
    print(
        f"  turboterm    {iterations} tables in {tt_time:.4f}s"
        f"  ({iterations / tt_time:,.0f} tables/sec)"
    )

    # rich
    if RichTable:
        from rich.console import Console as RichConsole

        with open("/dev/null", "w") as devnull:
            rc = RichConsole(file=devnull, width=120)
            start = time.perf_counter()
            for _ in range(iterations):
                t = RichTable()
                t.add_column("A")
                t.add_column("B")
                t.add_column("C")
                t.add_column("D")
                for row in rows:
                    t.add_row(*row)
                rc.print(t)
            rich_time = time.perf_counter() - start
        print(
            f"  rich         {iterations} tables in {rich_time:.4f}s"
            f"  ({iterations / rich_time:,.0f} tables/sec)"
        )
        speedup = rich_time / tt_time
        print(f"\n  turboterm is {speedup:.1f}x faster")
        print()
        return speedup
    print()
    return None


def bench_end_to_end():
    """Benchmark a realistic small script end-to-end."""
    print("=" * 60)
    print("END-TO-END SCRIPT (import + style + table, median of 7 runs)")
    print("=" * 60)

    scripts = {
        "turboterm": (
            "import turboterm as tt, io\n"
            "b = io.StringIO()\n"
            "b.write(tt.apply_styles('[bold red]Error:[/bold red] File not found'))\n"
            "b.write(tt.apply_styles('[green]Success:[/green] 3 tests passed'))\n"
            "tbl = tt.PyTable()\n"
            "tbl.add_row(['Test', 'Status', 'Duration'])\n"
            "tbl.add_row(['test_login', 'PASS', '0.3s'])\n"
            "tbl.add_row(['test_signup', 'PASS', '0.8s'])\n"
            "tbl.add_row(['test_checkout', 'FAIL', '1.2s'])\n"
            "b.write(tbl.to_string())\n"
            "b.getvalue()\n"
        ),
        "rich": (
            "from rich.console import Console\n"
            "from rich.table import Table\n"
            "import io\n"
            "buf = io.StringIO()\n"
            "c = Console(file=buf, width=120)\n"
            "c.print('[bold red]Error:[/bold red] File not found')\n"
            "c.print('[green]Success:[/green] 3 tests passed')\n"
            "t = Table()\n"
            "t.add_column('Test')\n"
            "t.add_column('Status')\n"
            "t.add_column('Duration')\n"
            "t.add_row('test_login', 'PASS', '0.3s')\n"
            "t.add_row('test_signup', 'PASS', '0.8s')\n"
            "t.add_row('test_checkout', 'FAIL', '1.2s')\n"
            "c.print(t)\n"
            "buf.getvalue()\n"
        ),
    }

    results = {}
    for name, script in scripts.items():
        try:
            t = _fresh_script_time(script)
            results[name] = t
            print(f"  {name:<12s}  {t * 1000:8.2f} ms")
        except Exception as e:
            print(f"  {name:<12s}  SKIPPED ({e})")

    if "turboterm" in results and "rich" in results:
        print(f"\n  turboterm is {results['rich'] / results['turboterm']:.1f}x faster")
    print()
    return results


if __name__ == "__main__":
    print()
    import_times = bench_import_time()
    e2e_times = bench_end_to_end()
    styling_speedup = bench_styling()
    bench_memory()
    table_speedup = bench_tables()

    ASSETS_DIR.mkdir(exist_ok=True)

    if import_times:
        chart_path = ASSETS_DIR / "benchmark.svg"
        chart_path.write_text(_generate_import_chart(import_times))
        print(f"Chart saved → {chart_path}")

    speedups: dict[str, float] = {}
    if e2e_times and "turboterm" in e2e_times and "rich" in e2e_times:
        speedups["end-to-end"] = e2e_times["rich"] / e2e_times["turboterm"]
    if styling_speedup is not None:
        speedups["styling"] = styling_speedup
    if table_speedup is not None:
        speedups["tables"] = table_speedup

    if speedups:
        os_name = {"darwin": "macOS", "linux": "Linux", "win32": "Windows"}.get(
            sys.platform, sys.platform
        )
        arch = platform.machine()
        subtitle = f"{arch} {os_name}"
        perf_path = ASSETS_DIR / "perf.svg"
        perf_path.write_text(_generate_perf_chart(speedups, subtitle))
        print(f"Chart saved → {perf_path}\n")
