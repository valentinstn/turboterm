#!/usr/bin/env python3
"""
Benchmark TurboTerm against Rich, Click, and Typer.

Measures import time, styling throughput, memory usage, and table rendering.
Requires: pip install rich click typer

Usage:
    uv run benchmark.py
"""

import statistics
import subprocess
import sys
import time


def _fresh_script_time(script: str, runs: int = 7) -> float:
    """Measure script execution time in a fresh subprocess (median of N runs)."""
    wrapped = (
        "import time as _t, sys as _s\n"
        "_start = _t.perf_counter()\n"
        + script + "\n"
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


def bench_import_time():
    """Benchmark import times."""
    print("=" * 60)
    print("IMPORT TIME (median of 7 runs, fresh subprocess)")
    print("=" * 60)

    modules = ["turboterm", "rich", "click", "typer"]
    results = {}
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


def bench_styling():
    """Benchmark markup parsing throughput."""
    print("=" * 60)
    print("STYLING THROUGHPUT")
    print("=" * 60)

    import turboterm

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
        print(f"\n  turboterm is {rich_time / tt_time:.1f}x faster")
    print()


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


def bench_tables():
    """Benchmark table rendering."""
    print("=" * 60)
    print("TABLE RENDERING (100 rows x 4 columns, 100 iterations)")
    print("=" * 60)

    from turboterm import PyTable

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
        print(f"\n  turboterm is {rich_time / tt_time:.1f}x faster")
    print()


def bench_end_to_end():
    """Benchmark a realistic small script end-to-end."""
    print("=" * 60)
    print("END-TO-END SCRIPT (import + style + table, median of 7 runs)")
    print("=" * 60)

    scripts = {
        "turboterm": (
            "import turboterm, io\n"
            "buf = io.StringIO()\n"
            "buf.write(turboterm.apply_styles('[bold red]Error:[/bold red] File not found'))\n"
            "buf.write(turboterm.apply_styles('[green]Success:[/green] 3 tests passed'))\n"
            "t = turboterm.PyTable()\n"
            "t.add_row(['Test', 'Status', 'Duration'])\n"
            "t.add_row(['test_login', 'PASS', '0.3s'])\n"
            "t.add_row(['test_signup', 'PASS', '0.8s'])\n"
            "t.add_row(['test_checkout', 'FAIL', '1.2s'])\n"
            "buf.write(t.to_string())\n"
            "buf.getvalue()\n"
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


if __name__ == "__main__":
    print()
    bench_import_time()
    bench_end_to_end()
    bench_styling()
    bench_memory()
    bench_tables()
