import inspect
import os
from pathlib import Path
import tempfile
from functools import wraps
from typing import Union, Callable, TypeVar, Any, Literal

from dony.find_git_root import find_git_root
from dony.prompts.error import error
from dony.prompts.success import success


F = TypeVar("F", bound=Callable[..., Any])

RunFrom = Literal["git_root", "command_file", "current_dir", "temp_dir"]


def command(
    run_from: Union[str, Path, RunFrom] = "current_dir",
    verbose: bool = True,
) -> Callable[[F], F]:
    """Decorator to mark a function as a dony command.

    Args:
        run_from: Where to run the command from.
                 Can be a Path, path string, or RunFrom literal value.
        verbose: If True, shows success message on completion and error message on failure.
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
