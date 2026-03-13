from collections.abc import Callable
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

class _Argument:
    help: str
    default: Any
    def __init__(self, help: str = ..., default: Any = ...) -> None: ...

class _Option:
    names: list[str]
    help: str
    default: Any
    def __init__(
        self, names: list[str], help: str = ..., default: Any = ...
    ) -> None: ...

def Argument(help: str = ..., default: Any = ...) -> _Argument: ...
def Option(names: list[str], help: str = ..., default: Any = ...) -> _Option: ...
def command(
    name: str | None = None,
    after_help: str | None = None,
) -> Callable[[_F], _F]: ...
def run() -> None: ...
