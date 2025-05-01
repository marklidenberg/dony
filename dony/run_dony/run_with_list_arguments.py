from typing import Callable, Any, get_origin, List
import inspect


def run_with_list_arguments(func: Callable, list_kwargs: dict) -> Any:
    """
    Calls `func` by unpacking `list_kwargs`, where each value in `list_kwargs` is a list.
    - If the corresponding parameter annotation is a list (e.g. list[str]),
      the entire list is passed.
    - Otherwise, the first element of the list is passed.

    Example:
        def f(a: str, b: list[str]) -> str:
            return a + b[0]

        run_with_list_arguments(f, {"a": ["hello"], "b": ["world"]})

        # calls f(a="hello", b=["world"])
    """
    sig = inspect.signature(func)
    bound_args = {}

    for name, param in sig.parameters.items():
        if name not in list_kwargs:
            continue

        values = list_kwargs[name]
        if not isinstance(values, list):
            raise TypeError(
                f"Expected a list for argument '{name}', got {type(values).__name__}"
            )

        anno = param.annotation

        # Detect if the annotation is a list type
        if get_origin(anno) is list:
            # pass the full list
            bound_args[name] = values
        else:
            # pass only the first element
            if not values:
                raise ValueError(f"No values provided for argument '{name}'")
            bound_args[name] = values[0]

    return func(**bound_args)


def test():
    def f(a: str, b: List[str]) -> List[str]:
        return a, b

    assert run_with_list_arguments(f, {"a": ["hello"], "b": ["world"]}) == (
        "hello",
        ["world"],
    )


if __name__ == "__main__":
    test()
