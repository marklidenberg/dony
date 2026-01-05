import inspect
from functools import wraps


def typer_partial(fn, /, *fixed_args, **fixed_kwargs):
    """
    Partially apply a Typer command function.

    - fixed_args bind to the earliest positional parameters
      (POSITIONAL_ONLY / POSITIONAL_OR_KEYWORD) in order.
    - fixed_kwargs bind by name.
    - Those bound params are removed from the exposed CLI signature
      via wrapper.__signature__ so Typer won't show them.
    """
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    # 1) Bind fixed_args to leading positional-capable params
    fixed_by_name = {}
    arg_i = 0
    for p in params:
        if arg_i >= len(fixed_args):
            break
        if p.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            if p.name in fixed_kwargs:
                raise TypeError(
                    f"Parameter {p.name!r} fixed both positionally and by keyword"
                )
            fixed_by_name[p.name] = fixed_args[arg_i]
            arg_i += 1
        else:
            # hit KEYWORD_ONLY / VAR_POSITIONAL / VAR_KEYWORD before binding all fixed_args
            raise TypeError(
                f"Too many fixed positional args: can't bind {len(fixed_args)} args "
                f"to function {fn.__name__} (stopped at parameter {p.name!r})"
            )
    if arg_i < len(fixed_args):
        raise TypeError(f"Too many fixed positional args for {fn.__name__}")

    # 2) Validate fixed_kwargs exist
    for name in fixed_kwargs:
        if name not in sig.parameters:
            raise TypeError(f"{fn.__name__} has no parameter named {name!r}")

    # Merge fixed name bindings (from positional) + fixed kwargs
    fixed_all = {**fixed_by_name, **fixed_kwargs}

    # 3) Build new signature removing fixed params
    new_params = [p for p in params if p.name not in fixed_all]
    new_sig = sig.replace(parameters=new_params)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Guard against passing hidden params explicitly
        overlap = set(kwargs) & set(fixed_all)
        if overlap:
            raise TypeError(
                f"These parameters are fixed and cannot be passed: {sorted(overlap)}"
            )

        # Bind what Typer provided (positional/keyword) against the NEW signature
        bound = new_sig.bind_partial(*args, **kwargs)

        # Call original: we pass fixed params as keywords (safe, explicit)
        return fn(**{**fixed_all, **bound.arguments})

    wrapper.__signature__ = new_sig  # what Typer will inspect
    return wrapper


def test():
    # Test basic positional binding
    def greet(name, greeting, punctuation="!"):
        return f"{greeting}, {name}{punctuation}"

    partial_greet = typer_partial(greet, "World")
    assert partial_greet("Hello") == "Hello, World!"
    assert partial_greet("Hi", punctuation="?") == "Hi, World?"

    # Test keyword binding
    partial_greet2 = typer_partial(greet, greeting="Hey")
    assert partial_greet2("Alice") == "Hey, Alice!"

    # Test both positional and keyword binding
    partial_greet3 = typer_partial(greet, "Bob", punctuation="...")
    assert partial_greet3("Yo") == "Yo, Bob..."

    # Test signature is updated correctly
    sig = inspect.signature(partial_greet)
    assert "name" not in sig.parameters
    assert "greeting" in sig.parameters
    assert "punctuation" in sig.parameters

    # Test error on duplicate binding
    try:
        typer_partial(greet, "World", name="Alice")
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert "fixed both positionally and by keyword" in str(e)

    # Test error on unknown parameter
    try:
        typer_partial(greet, unknown="value")
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert "has no parameter named" in str(e)

    # Test error on passing fixed param at call time
    try:
        partial_greet("Hello", name="Override")
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert "fixed and cannot be passed" in str(e)

    # Test with keyword-only params
    def func_with_kwonly(a, b, *, c, d="default"):
        return f"{a}-{b}-{c}-{d}"

    partial_kwonly = typer_partial(func_with_kwonly, "A", c="C")
    assert partial_kwonly("B") == "A-B-C-default"
    assert partial_kwonly("B", d="D") == "A-B-C-D"


if __name__ == "__main__":
    test()
