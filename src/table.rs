use comfy_table::{presets, Cell, Row, Table};
use pyo3::prelude::*; // Add presets for now

/// Formats a table from Python data.
#[pyclass]
pub struct PyTable {
    table: Table,
}

#[pymethods]
impl PyTable {
    #[new]
    fn new() -> Self {
        let mut table = Table::new();
        table.load_preset(presets::UTF8_FULL);
        PyTable { table }
    }

    /// Add a row to the table.
    /// Expects a list of strings for now.
    fn add_row(&mut self, py_row: Vec<String>) -> PyResult<()> {
        let cells: Vec<Cell> = py_row
            .into_iter()
            .map(|s| {
                let styled_content = super::lexer::apply_styles(&s);
                Cell::new(styled_content)
            })
            .collect();
        self.table.add_row(Row::from(cells));
        Ok(())
    }

    /// Returns the table as a formatted string.
    #[pyo3(name = "to_string")]
    fn render(&self) -> String {
        self.table.to_string()
    }
}
