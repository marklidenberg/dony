import inspect
import sys
import types
from functools import wraps
from typing import get_origin, get_args, Union

from dony.prompts.error import error
from dony.prompts.success import success


if sys.version_info >= (3, 10):
    _union_type = types.UnionType
else:
    _union_type = None  # or skip using it


def command():
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

        # - Wrap function

        @wraps(func)
        def wrapper(*args, **kwargs):
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
