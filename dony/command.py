import inspect
import os
from pathlib import Path
import sys
import tempfile
import types
from functools import wraps
from typing import get_origin, get_args, Union, Callable, TypeVar, Any
from enum import Enum

from dony.find_git_root import find_git_root
from dony.prompts.error import error
from dony.prompts.success import success


if sys.version_info >= (3, 10):
    _union_type = types.UnionType
else:
    _union_type = None  # or skip using it


F = TypeVar("F", bound=Callable[..., Any])


class RunFrom(str, Enum):
    """Enum for specifying where a command should run from."""

    GIT_ROOT = "git_root"
    COMMAND_FILE = "command_file"
    CURRENT = "current"
    TEMP = "temp"


def command(
    run_from: Union[str, Path, RunFrom] = RunFrom.COMMAND_FILE,
    show_success: bool = True,
) -> Callable[[F], F]:
    """Decorator to mark a function as a dony command.

    Args:
        run_from: Where to run the command from.
                 Can be a Path, path string, or RunFrom enum value.
    """

    def decorator(func):
        # - Wrap function

        @wraps(func)
        def wrapper(*args, **kwargs):
            # - Save original directory
            original_dir = Path.cwd()
            temp_dir = None

            try:
                # - Change directory to run_from

                command_dir = Path(inspect.getfile(func)).parent

                if run_from in (RunFrom.GIT_ROOT, "git_root"):
                    os.chdir(find_git_root(start_path=command_dir))
                elif run_from in (RunFrom.COMMAND_FILE, "command_file", "command_dir"):
                    os.chdir(command_dir)
                elif run_from in (RunFrom.TEMP, "temp"):
                    temp_dir = tempfile.mkdtemp()
                    os.chdir(temp_dir)
                elif run_from in (RunFrom.CURRENT, "current"):
                    pass  # Stay in current directory
                else:
                    # Assume it's a path string or Path object
                    os.chdir(Path(run_from))

                # - Run command

                try:
                    result = func(*args, **kwargs)
                    if show_success:
                        success(f"Command '{func.__name__}' succeeded")
                    return result
                except KeyboardInterrupt:
                    return error("Dony command interrupted")
            finally:
                # - Restore original directory
                os.chdir(original_dir)

                # - Clean up temp directory if created
                if temp_dir:
                    import shutil

                    shutil.rmtree(temp_dir, ignore_errors=True)

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
