import inspect
from collections.abc import Callable
from typing import Any

from .turboterm import register_command as _register
from .turboterm import run_cli as _run_cli

_UNSET = object()


class _Argument:
    """Internal: holds metadata for a positional CLI argument."""

    def __init__(self, help: str = "", default: Any = _UNSET):
        self.help = help
        self.default = default


class _Option:
    """Internal: holds metadata for a CLI option (--flag)."""

    def __init__(self, names: list[str], help: str = "", default: Any = _UNSET):
        self.names = names
        self.help = help
        self.default = default


def Argument(help: str = "", default: Any = _UNSET) -> Any:
    """Marks a parameter as a positional CLI argument."""
    return _Argument(help=help, default=default)


def Option(names: list[str], help: str = "", default: Any = _UNSET) -> Any:
    """Marks a parameter as a CLI option (--flag)."""
    return _Option(names=names, help=help, default=default)


def command(name: str | None = None, after_help: str | None = None):
    """Decorator to register a function as a CLI command."""

    def decorator(func: Callable):
        cmd_name = name if name is not None else func.__name__
        if after_help is not None:
            _COMMAND_AFTER_HELP[cmd_name] = after_help
        sig = inspect.signature(func)
        params = []

        for param_name, param in sig.parameters.items():
            ann = param.annotation
            type_fn = ann if ann is not inspect.Parameter.empty else None
            default = param.default

            if isinstance(default, _Argument):
                p = {
                    "name": param_name,
                    "kind": "positional",
                    "help": default.help,
                    "type": type_fn,
                    "required": default.default is _UNSET,
                }
                if default.default is not _UNSET:
                    p["default"] = default.default

            elif isinstance(default, _Option):
                is_bool = type_fn is bool
                p = {
                    "name": param_name,
                    "kind": "option",
                    "help": default.help,
                    "flags": default.names,
                    "is_bool": is_bool,
                    "required": not is_bool and default.default is _UNSET,
                }
                if is_bool:
                    p["default"] = False
                elif default.default is not _UNSET:
                    p["default"] = default.default

            elif default is inspect.Parameter.empty:
                # Bare parameter with no default — required positional
                p = {
                    "name": param_name,
                    "kind": "positional",
                    "help": "",
                    "type": type_fn,
                    "required": True,
                }

            else:
                # Plain default value (e.g., count: int = 1)
                p = {
                    "name": param_name,
                    "kind": "positional",
                    "help": "",
                    "type": type_fn,
                    "required": False,
                    "default": default,
                }

            params.append(p)

        doc = (func.__doc__ or "").strip() or None
        _register(name=cmd_name, func=func, doc=doc, params=params)
        return func

    return decorator


_COMMAND_AFTER_HELP: dict[str, str] = {}


def run():
    import sys

    args = sys.argv[1:]

    after_help = None
    if "--help" in args or "-h" in args:
        for cmd_name in _COMMAND_AFTER_HELP:
            if cmd_name in args:
                after_help = _COMMAND_AFTER_HELP[cmd_name]
                break
        if after_help is None and _COMMAND_AFTER_HELP:
            after_help = "\n".join(_COMMAND_AFTER_HELP.values())

    _run_cli(args)

    if after_help:
        print(after_help)
