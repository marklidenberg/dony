import inspect
import os
import re
import sys
from pathlib import Path
from functools import wraps
from dataclasses import make_dataclass, fields, field
from typing import Any, get_origin, get_args

from dotenv import load_dotenv

from dony.shell import shell
from dony.prompts.error import error
from dony.get_donyfiles_path import get_donyfiles_path
from dony.prompts.success import success


def command(path: str = None):
    """
    Decorator to mark a function as a dony command.
    - Builds a lazy dataclass of all parameters, allowing cascading defaults.
    - Executes callable defaults when their fields are accessed.
    - Ensures every parameter has a default value and the function name matches its filename.
    """

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
            if not (
                param.annotation is str
                or get_origin(param.annotation) is list
                and get_args(param.annotation)[0] is str
            ):
                raise ValueError(
                    f"Command '{func.__name__}': parameter '{name}' must have a string or List[str] type"
                )

        # - Get file_path

        source_file = inspect.getsourcefile(func)
        if not source_file:
            raise RuntimeError(
                f"Could not locate source file for command '{func.__name__}'"
            )
        file_path = Path(source_file).resolve()

        # - Validate file_path is in donyfiles

        assert (
            "donyfiles" in file_path.parts
        ), f"Command '{func.__name__}' must be in 'donyfiles' directory"

        # - Compute or use provided path

        if path is None:
            parts = file_path.parts
            try:
                idx = parts.index("donyfiles")
            except ValueError:
                raise RuntimeError(
                    f"Cannot derive path: 'donyfiles' not found in '{file_path}'"
                )
            relative = Path(*parts[idx:]).as_posix()
            func._path = relative
        else:
            func._path = path

        # - Crop to last dony folder

        func._path = re.sub(r"^.*/donyfiles/", "", func._path).replace(".py", "")

        if func._path.startswith("donyfiles/commands/"):
            func._path = func._path[len("donyfiles/commands/") :]

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

    try:

        @command()
        def bar(
            a: str = "0",
            b: str = "1",
            c: str = "2",
        ):
            return a + b + c
    except ValueError as e:
        assert str(e) == "Command name 'bar' does not match filename 'command.py'"


if __name__ == "__main__":
    test()
