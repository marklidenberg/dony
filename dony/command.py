import inspect
import os
import re
import sys
import types
from pathlib import Path
from functools import wraps
from dataclasses import make_dataclass, fields, field
from typing import Any, get_origin, get_args, Optional, Union

from dotenv import load_dotenv

from dony.get_donyfiles_root import get_donyfiles_root
from dony.shell import shell
from dony.prompts.error import error
from dony.get_donyfiles_path import get_donyfiles_path
from dony.prompts.success import success


if sys.version_info >= (3, 10):
    _union_type = types.UnionType
else:
    _union_type = None  # or skip using it


def command(path: Optional[str] = None):
    """Decorator to mark a function as a dony command."""

    def decorator(func):
        sig = inspect.signature(func)

        # - Validate that all parameters have default values

        for name, param in sig.parameters.items():
            if param.default is inspect._empty:
                raise ValueError(
                    f"Command '{func.__name__}': parameter '{name}' must have a default value"
                )

        # - Validate all parameters have string or List[str] types

        for name, param in sig.parameters.items():
            # - Extract annotation

            annotation = param.annotation

            # - Extract top-level origin and args for type inspection

            origin = get_origin(annotation)
            args = get_args(annotation)

            # - Remove NoneType from type arguments (to handle Optional[...] which is Union[..., None])

            non_none = tuple(a for a in args if a is not type(None))

            if not (
                (annotation is str)  # str
                or (origin is list and args and args[0] is str)  # List[str]
                or (  # Optional[str] or Optional[List[str]]
                    origin
                    in (
                        Union,
                        _union_type,
                    )  # Check for typing.Union or Python 3.10+ X | None
                    and len(non_none) == 1  # Only one non-None type in the union
                    and (
                        non_none[0] is str
                        or (
                            get_origin(non_none[0]) is list
                            and get_args(non_none[0])
                            and get_args(non_none[0])[0] is str
                        )
                    )
                )
            ):
                raise ValueError(
                    f"Command '{func.__name__}': parameter '{name}' must be str, List[str], Optional[str], or Optional[List[str]]"
                )

        # - Get file_path

        source_file = inspect.getsourcefile(func)
        if not source_file:
            raise RuntimeError(
                f"Could not locate source file for command '{func.__name__}'"
            )
        file_path = Path(source_file).resolve()

        # - Compute or use provided path

        if path is None:
            # - Init path

            func._path = str(file_path)

            # - Get paths

            donyfiles_path = str(get_donyfiles_path(file_path))
            project_path = str(get_donyfiles_root(file_path))

            # - Remove donyfiles prefix if present

            func._path = func._path.replace(donyfiles_path, "")

            # - Remove project prefix if present

            func._path = func._path.replace(project_path, "")

            # - Remove leading /

            if func._path.startswith("/"):
                func._path = func._path[1:]

            # - Remove .py extension

            func._path = func._path.replace(".py", "")
        else:
            func._path = path

        func._dony_command = True

        @wraps(func)
        def wrapper(*args, **kwargs):
            # - Load dotenv in dony path or its parent

            if (
                os.path.basename(inspect.currentframe().f_back.f_code.co_filename)
                == "run_with_list_arguments.py"
            ):
                # running from command client
                donyfiles_path = get_donyfiles_path(
                    inspect.currentframe().f_back.f_back.f_back.f_code.co_filename
                )
            else:
                donyfiles_path = get_donyfiles_path(
                    inspect.currentframe().f_back.f_code.co_filename
                )

            load_dotenv(dotenv_path=donyfiles_path / ".env")
            load_dotenv(dotenv_path=donyfiles_path.parent / ".env")

            # - Bind partial to allow positional or keyword

            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()

            # - Change directory to dony root

            os.chdir(donyfiles_path.parent)

            # - Call original function with resolved args

            try:
                result = func(**bound.arguments)
                success(f"Command '{func.__name__}' succeeded")
                return result
            except KeyboardInterrupt:
                return error("Dony command interrupted")

        # - Attach metadata to wrapper

        wrapper._dony_command = True
        wrapper._path = func._path
        return wrapper

    return decorator


def test():
    try:

        @command()
        def foo(
            a: str,
            b: str = "1",
            c: str = "2",
        ):
            return a + b + c

    except ValueError as e:
        assert str(e) == "Command 'foo': parameter 'a' must have a default value"

    @command()
    def bar(
        a: str = "0",
        b: str = "1",
        c: str = "2",
    ):
        return a + b + c


if __name__ == "__main__":
    test()
