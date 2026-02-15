import unittest

import turboterm


class TestTable(unittest.TestCase):
    def test_basic_table(self):
        table = turboterm.PyTable()
        table.add_row(["Header 1", "Header 2"])
        table.add_row(["Row 1 Col 1", "Row 1 Col 2"])
        table.add_row(["Row 2 Col 1", "Row 2 Col 2"])
        expected = """\
┌─────────────┬─────────────┐
│ Header 1    ┆ Header 2    │
├╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ Row 1 Col 1 ┆ Row 1 Col 2 │
├╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ Row 2 Col 1 ┆ Row 2 Col 2 │
└─────────────┴─────────────┘"""
        self.assertEqual(table.to_string().strip(), expected)

    def test_empty_table(self):
        table = turboterm.PyTable()
        expected = """\
┌┐
└┘"""
        self.assertEqual(table.to_string().strip(), expected)

    def test_single_row(self):
        table = turboterm.PyTable()
        table.add_row(["Only Row"])
        expected = """\
┌──────────┐
│ Only Row │
└──────────┘"""
        self.assertEqual(table.to_string().strip(), expected)

    def test_single_column(self):
        table = turboterm.PyTable()
        table.add_row(["Header"])
        table.add_row(["Item 1"])
        table.add_row(["Item 2"])
        expected = """\
┌────────┐
│ Header │
├╌╌╌╌╌╌╌╌┤
│ Item 1 │
├╌╌╌╌╌╌╌╌┤
│ Item 2 │
└────────┘"""
        self.assertEqual(table.to_string().strip(), expected)

    def test_add_row_with_empty_cells(self):
        table = turboterm.PyTable()
        table.add_row(["", "Cell 2"])
        expected = """\
┌───┬────────┐
│   ┆ Cell 2 │
└───┴────────┘"""
        self.assertEqual(table.to_string().strip(), expected)


if __name__ == "__main__":
    unittest.main()
