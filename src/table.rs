use pyo3::prelude::*;

/// Formats a table from Python data.
#[pyclass]
pub struct PyTable {
    rows: Vec<Vec<String>>,
}

#[pymethods]
impl PyTable {
    #[new]
    fn new() -> Self {
        PyTable { rows: Vec::new() }
    }

    /// Add a row to the table.
    /// Expects a list of strings for now.
    fn add_row(&mut self, py_row: Vec<String>) -> PyResult<()> {
        let styled: Vec<String> = py_row
            .into_iter()
            .map(|s| super::lexer::apply_styles(&s))
            .collect();
        self.rows.push(styled);
        Ok(())
    }

    /// Returns the table as a formatted string.
    #[pyo3(name = "to_string")]
    fn render(&self) -> String {
        if self.rows.is_empty() {
            return "┌┐\n└┘".to_string();
        }

        let col_count = self.rows.iter().map(|r| r.len()).max().unwrap_or(0);
        if col_count == 0 {
            return "┌┐\n└┘".to_string();
        }

        // Compute column widths (visible width of content, minimum 1)
        let mut col_widths = vec![1usize; col_count];
        for row in &self.rows {
            for (j, cell) in row.iter().enumerate() {
                let w = super::lexer::visible_width(cell);
                if w > col_widths[j] {
                    col_widths[j] = w;
                }
            }
        }

        let mut out = String::new();

        // Top border
        out.push('┌');
        for (i, &w) in col_widths.iter().enumerate() {
            for _ in 0..w + 2 {
                out.push('─');
            }
            if i < col_count - 1 {
                out.push('┬');
            }
        }
        out.push_str("┐\n");

        // Rows
        for (row_idx, row) in self.rows.iter().enumerate() {
            out.push('│');
            for (j, &w) in col_widths.iter().enumerate() {
                let cell = row.get(j).map(|s| s.as_str()).unwrap_or("");
                let visible_w = super::lexer::visible_width(cell);
                let padding = w - visible_w;
                out.push(' ');
                out.push_str(cell);
                for _ in 0..padding + 1 {
                    out.push(' ');
                }
                if j < col_count - 1 {
                    out.push('┆');
                }
            }
            out.push_str("│\n");

            // Row separator (not after last row)
            if row_idx < self.rows.len() - 1 {
                out.push('├');
                for (i, &w) in col_widths.iter().enumerate() {
                    for _ in 0..w + 2 {
                        out.push('╌');
                    }
                    if i < col_count - 1 {
                        out.push('┼');
                    }
                }
                out.push_str("┤\n");
            }
        }

        // Bottom border
        out.push('└');
        for (i, &w) in col_widths.iter().enumerate() {
            for _ in 0..w + 2 {
                out.push('─');
            }
            if i < col_count - 1 {
                out.push('┴');
            }
        }
        out.push('┘');

        out
    }
}
