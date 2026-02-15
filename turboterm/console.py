from .cli import Argument, Option, command, run
from .turboterm import PyTable, apply_styles


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

    # Expose cli argument parsing functionality
    argument = Argument
    option = Option
    command = command
    run = run


# Pre-configured console singleton
console = Console()
