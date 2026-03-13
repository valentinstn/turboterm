use pyo3_stub_gen::Result;

fn main() -> Result<()> {
    let stub = turboterm::stub_info()?;
    stub.generate()?;
    // pyo3-stub-gen writes to CWD/turboterm.pyi; move it into the Python package dir
    std::fs::rename("turboterm.pyi", "turboterm/turboterm.pyi")
        .expect("failed to move turboterm.pyi into turboterm/");
    // Fix missing blank line between imports and __all__ (ruff format requirement)
    let path = "turboterm/turboterm.pyi";
    let content = std::fs::read_to_string(path).expect("failed to read stub");
    let fixed = content.replace("import typing\n__all__", "import typing\n\n__all__");
    std::fs::write(path, fixed).expect("failed to write stub");
    // Apply ruff formatting (long lines, .pyi blank-line rules)
    let status = std::process::Command::new("ruff")
        .args(["format", path])
        .status()
        .or_else(|_| {
            std::process::Command::new("uvx")
                .args(["ruff", "format", path])
                .status()
        })
        .expect("ruff not found; install with `pip install ruff` or `brew install ruff`");
    assert!(status.success(), "ruff format failed");
    Ok(())
}
