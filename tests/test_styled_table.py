import unittest
import turboterm

class TestStyledTable(unittest.TestCase):

    def test_styled_table(self):
        table = turboterm.PyTable()
        table.add_row(["[b]Header 1[/b]", "[red]Header 2[/red]"])
        table.add_row(["[b]Row 1 Col 1[/b]", "[u]Row 1 Col 2[/u]"])
        
        expected = """\
┌─────────────┬─────────────┐
│ \x1b[1mHeader 1\x1b[0m    ┆ \x1b[31mHeader 2\x1b[0m    │
├╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ \x1b[1mRow 1 Col 1\x1b[0m ┆ \x1b[4mRow 1 Col 2\x1b[0m │
└─────────────┴─────────────┘"""
        
        actual_output = table.to_string().strip()
        self.assertEqual(actual_output, expected)

if __name__ == '__main__':
    unittest.main()
