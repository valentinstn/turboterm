use pyo3::prelude::*;
use pyo3::Bound;
use pyo3::types::PyModule;

mod lexer;
mod table;
// Removed mod markdown;

#[pyfunction]
fn apply_styles(text: &str) -> PyResult<String> {
    Ok(lexer::apply_styles(text))
}

// Removed #[pyfunction] fn render_markdown_to_ansi(...)

#[pymodule]
fn turboterm(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(apply_styles, m)?)?;
    // Removed m.add_function(wrap_pyfunction!(render_markdown_to_ansi, m)?)?;
    m.add_class::<table::PyTable>()?;
    Ok(())
}
