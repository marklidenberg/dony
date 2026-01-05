import contextvars
import inspect
import os
import sys
from pathlib import Path
import tempfile
from functools import wraps
from typing import Union, Callable, TypeVar, Any, Literal

import typer

from dony.find_git_root import find_git_root
from dony.prompts.error import error
from dony.prompts.success import success


F = TypeVar("F", bound=Callable[..., Any])

RunFrom = Literal["git_root", "command_file", "current_dir", "temp_dir"]

# Track if we're inside a dony command to prevent nested CLI parsing (async-safe)
_inside_command: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "_inside_command", default=False
)


def command(
    run_from: Union[str, Path, RunFrom] = "current_dir",
    verbose: bool = True,
) -> Callable[[F], F]:
    """Decorator to mark a function as a dony command.

    Args:
        run_from: Where to run the command from.
                 Can be a Path, path string, or RunFrom literal value.
        verbose: If True, shows success message on completion and error message on failure.

    When run in __main__, CLI arguments are automatically parsed using typer.
    For hybrid interactive/CLI interface, use Optional arguments with fallback to prompts:

        @dony.command()
        def my_command(arg: str | None = None):
            arg = arg or dony.select("Choose arg:", ["a", "b", "c"])

        if __name__ == "__main__":
            my_command()
    """

    def decorator(func):
        # - Wrap function

        @wraps(func)
        def wrapper(*args, **kwargs):
            # - Save original directory
            original_dir = Path.cwd()
            temp_dir = None
            token = _inside_command.set(True)

            try:
                # - Change directory to run_from

                command_dir = Path(inspect.getfile(func)).parent

                if run_from == "git_root":
                    os.chdir(find_git_root(path=command_dir))
                elif run_from == "command_file":
                    os.chdir(command_dir)
                elif run_from == "temp_dir":
                    temp_dir = tempfile.mkdtemp()
                    os.chdir(temp_dir)
                elif run_from == "current_dir":
                    pass  # Stay in current directory
                else:
                    # Assume it's a path string or Path object
                    os.chdir(Path(run_from))

                # - Run command

                try:
                    result = func(*args, **kwargs)
                    if verbose:
                        success(f"Command '{func.__name__}' succeeded")
                    return result
                except KeyboardInterrupt:
                    if verbose:
                        error("Dony command interrupted")
                    raise
                except Exception:
                    if verbose:
                        error(f"Command '{func.__name__}' failed")
                    raise
            finally:
                _inside_command.reset(token)

                # - Restore original directory
                os.chdir(original_dir)

                # - Clean up temp directory if created
                if temp_dir:
                    import shutil

                    shutil.rmtree(temp_dir, ignore_errors=True)

        @wraps(func)
        def cli_wrapper(*args, **kwargs):
            # If called with no args and not inside another command, use typer
            if not args and not kwargs and not _inside_command.get():
                # Check if there are CLI args (beyond script name)
                if len(sys.argv) > 1:
                    return typer.run(wrapper)
            return wrapper(*args, **kwargs)

        # Store reference to the raw wrapper for direct calls
        cli_wrapper._wrapper = wrapper

        return cli_wrapper

    return decorator


def test():
    # Test that commands with required arguments work (typer handles CLI parsing)
    @command()
    def foo(
        a: str,
        b: str = "1",
        c: str = "2",
    ):
        return a + b + c

    assert foo("x") == "x12"
    assert foo("x", "y") == "xy2"
    assert foo("x", "y", "z") == "xyz"

    # Test that commands with all default arguments work
    @command()
    def bar(
        a: str = "0",
        b: str = "1",
        c: str = "2",
    ):
        return a + b + c

    assert bar() == "012"


if __name__ == "__main__":
    test()
