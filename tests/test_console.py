import unittest
from unittest.mock import patch
import io
import turboterm
from turboterm.console import Console  # Import Console class directly for type checking


class TestConsole(unittest.TestCase):
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_console_print(self, mock_stdout):
        turboterm.console.print("[b]Hello[/b]")
        self.assertEqual(mock_stdout.getvalue().strip(), "\x1b[1mHello\x1b[0m")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_console_table(self, mock_stdout):
        table_data = [
            ["[b]Header 1[/b]", "[red]Header 2[/red]"],
            ["[b]Row 1 Col 1[/b]", "[u]Row 1 Col 2[/u]"],
        ]
        turboterm.console.table(table_data)

        expected_table_output = """\
┌─────────────┬─────────────┐
│ \x1b[1mHeader 1\x1b[0m    ┆ \x1b[31mHeader 2\x1b[0m    │
├╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ \x1b[1mRow 1 Col 1\x1b[0m ┆ \x1b[4mRow 1 Col 2\x1b[0m │
└─────────────┴─────────────┘"""

        self.assertEqual(mock_stdout.getvalue().strip(), expected_table_output)

    def test_console_singleton_access(self):
        from turboterm import console

        self.assertIsInstance(console, Console)
        self.assertTrue(hasattr(console, "print"))
        self.assertTrue(hasattr(console, "table"))


if __name__ == "__main__":
    unittest.main()
