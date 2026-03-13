from collections.abc import Callable
from typing import Any

from .cli import _Argument, _Option

class Console:
    def print(self, text: str) -> None: ...
    def table(self, data: list[list[str]]) -> None: ...
    @property
    def argument(self) -> Callable[..., _Argument]: ...
    @property
    def option(self) -> Callable[..., _Option]: ...
    @property
    def command(
        self,
    ) -> Callable[..., Callable[[Callable[..., Any]], Callable[..., Any]]]: ...
    @property
    def run(self) -> Callable[[], None]: ...

console: Console
