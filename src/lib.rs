use pyo3::prelude::*;
use pyo3::Bound;
use pyo3::types::PyModule;

mod lexer;
mod table;
mod cli; // Add this line

#[pyfunction]
fn apply_styles(text: &str) -> PyResult<String> {
    Ok(lexer::apply_styles(text))
}

#[pymodule]
fn turboterm(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(apply_styles, m)?)?;
    m.add_class::<table::PyTable>()?;
    m.add_function(wrap_pyfunction!(cli::register_command, m)?)?;
    m.add_function(wrap_pyfunction!(cli::run_cli, m)?)?;
    Ok(())
}
