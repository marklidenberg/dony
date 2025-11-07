import inspect
import os
from pathlib import Path
import sys
import types
from functools import wraps
from typing import get_origin, get_args, Union, Literal, Callable, TypeVar, Any

from dony.get_git_root import get_git_root
from dony.prompts.error import error
from dony.prompts.success import success


if sys.version_info >= (3, 10):
    _union_type = types.UnionType
else:
    _union_type = None  # or skip using it


F = TypeVar("F", bound=Callable[..., Any])


def command(
    working_dir: Union[str, Literal["git_root", "command_dir"], None] = "command_dir",
) -> Callable[[F], F]:
    """Decorator to mark a function as a dony command.

    Args:
        working_dir: Optional working directory for the command.
                    Can be a path string, "git_root", "command_dir", or None.
    """

    def decorator(func):
        sig = inspect.signature(func)

        # - Validate that all parameters have default values

        for name, param in sig.parameters.items():
            if param.default is inspect._empty:
                raise ValueError(
                    f"Command '{func.__name__}': parameter '{name}' must have a default value"
                )

        # - Wrap function

        @wraps(func)
        def wrapper(*args, **kwargs):
            # - Change directory to working_dir

            if working_dir:
                command_dir = Path(inspect.getfile(func)).parent

                if working_dir == "git_root":
                    os.chdir(get_git_root(start_path=command_dir))
                elif working_dir == "command_dir":
                    os.chdir(command_dir)
                else:
                    os.chdir(Path(working_dir))

            # - Run command

            try:
                result = func(*args, **kwargs)
                success(f"Command '{func.__name__}' succeeded")
                return result
            except KeyboardInterrupt:
                return error("Dony command interrupted")

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
