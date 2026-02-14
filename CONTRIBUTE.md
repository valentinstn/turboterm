# Contribution Guidelines for TurboTerm

We welcome contributions to TurboTerm! By contributing, you help make our CLI UI toolkit even better.

Please take a moment to review this document to ensure a smooth contribution process.

## 🌟 How to Contribute

### 1. Fork the Repository

First, fork the [TurboTerm repository](https://github.com/valentinstn/turboterm.git) to your own GitHub account.

### 2. Clone Your Fork

Clone your forked repository to your local machine:

```bash
git clone https://github.com/your-username/turboterm.git
cd turboterm
```

### 3. Create a New Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bug-fix-name
```

### 4. Set up Your Development Environment

Ensure you have Rust and Python installed. We recommend using `uv` for Python dependency management.

```bash
# Set up Python virtual environment
uv venv
# Add development dependencies
uv add maturin mypy pytest
# Build the Rust extension in editable mode
uv run maturin develop
```

### 5. Make Your Changes

*   Implement your feature or bug fix.
*   Write comprehensive unit tests for your changes. We use Python's `unittest` framework.
*   Ensure all existing tests pass.
*   Adhere to the existing code style and structure (Rust via `rustfmt`, Python via `black`/`ruff`).
*   Update documentation (e.g., `README.md`, `CHANGELOG.md`) as appropriate.

### 6. Run Tests

Before submitting, ensure all tests pass:

```bash
uv run python -m unittest discover tests
```

### 7. Commit Your Changes

Commit your changes with a clear and concise commit message. Follow conventional commits if possible (e.g., `feat: Add new feature`, `fix: Resolve bug in lexer`).

```bash
git add .
git commit -m "feat: Briefly describe your feature or fix"
```

### 8. Push to Your Fork

Push your changes to your fork on GitHub:

```bash
git push origin feature/your-feature-name
```

### 9. Create a Pull Request (PR)

Go to the original TurboTerm repository on GitHub and open a new Pull Request.
*   Provide a clear title and detailed description of your changes.
*   Reference any related issues.

## 🐛 Reporting Bugs

If you find a bug, please open an issue on the [GitHub Issues page](https://github.com/valentinstn/turboterm/issues).
*   Provide a clear and concise description of the bug.
*   Include steps to reproduce the behavior.
*   Mention your operating system, Python version, and `turboterm` version (if applicable).

## ✨ Suggesting Enhancements

We're always looking for ways to improve TurboTerm! Feel free to open an issue to suggest new features or enhancements.

Thank you for contributing to TurboTerm!
