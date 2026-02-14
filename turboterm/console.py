from .turboterm import apply_styles, PyTable, render_markdown_to_ansi

class Console:
    def print(self, text: str):
        """Prints styled text to the console."""
        print(apply_styles(text))

    def table(self, data: list[list[str]]):
        """Prints a styled table to the console."""
        table_instance = PyTable()
        for row_data in data:
            table_instance.add_row(row_data)
        print(table_instance.to_string())

    def markdown(self, text: str):
        """Renders Markdown to ANSI formatted text and prints it to the console."""
        print(render_markdown_to_ansi(text))

# Pre-configured console singleton
console = Console()
