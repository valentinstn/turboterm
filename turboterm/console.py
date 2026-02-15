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

    @property
    def argument(self):
        from .cli import Argument
        return Argument

    @property
    def option(self):
        from .cli import Option
        return Option

    @property
    def command(self):
        from .cli import command
        return command

    @property
    def run(self):
        from .cli import run
        return run


# Pre-configured console singleton
console = Console()
