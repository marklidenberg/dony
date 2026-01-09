from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def command() -> Callable[[F], F]:
    """Marker decorator for commands. Currently a no-op."""

    def decorator(func: F) -> F:
        return func

    return decorator
