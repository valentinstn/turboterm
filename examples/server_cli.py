#!/usr/bin/env python3
"""
Options and flags example — a mock server CLI with --host, --port, and --verbose.
Demonstrates long/short flags, typed options with defaults, and bool flags.

Usage:
    uv run examples/server_cli.py start
    uv run examples/server_cli.py start --host 0.0.0.0 -p 3000 --verbose
    uv run examples/server_cli.py start --help
    uv run examples/server_cli.py status
"""

from turboterm.cli import Option, command, run


@command()
def start(
    host: str = Option(["--host", "-H"], help="Host to bind to", default="127.0.0.1"),
    port: int = Option(["--port", "-p"], help="Port number", default=8080),
    workers: int = Option(["--workers", "-w"], help="Number of workers", default=4),
    verbose: bool = Option(["--verbose", "-v"], help="Enable verbose logging"),
):
    """Start the web server."""
    print(f"Starting server on {host}:{port}")
    print(f"Workers: {workers}")
    if verbose:
        print("Verbose logging enabled")
    print("Server ready!")


@command()
def stop():
    """Stop the running server."""
    print("Stopping server...")
    print("Server stopped.")


@command()
def status():
    """Check server status."""
    print("Server is running on 127.0.0.1:8080 (PID 12345)")


if __name__ == "__main__":
    run()
