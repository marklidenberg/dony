import itertools

from dony.shell import shell

import itertools
import sys
from collections import OrderedDict


def parse_unknown_args(arg_list: list) -> dict:
    """
    Turn a flat list like
      ['my_command',
       '--simple','simple',
       '--list1','a','b',
       '--list2','c','--list2','d']
    into
      {'positional': ['my_command'],
       'simple':     ['simple'],
       'list1':      ['a','b'],
       'list2':      ['c','d']}
    """
    left_tokens = iter(arg_list)
    result = {
        "positional": [],
        "keyword": OrderedDict(),
    }

    while True:
        # - Get next token

        try:
            token = next(left_tokens)
        except StopIteration:
            break

        # - Raise if short argument, not supported

        if token.startswith("-") and not token.startswith("--"):
            raise ValueError(f"Short arguments are not supported: {token}")

        # - Handle flag

        if token.startswith("--"):
            # - Init values

            values = []

            # - Strip --

            key = token.lstrip("-")  # --simple -> simple

            # - Consume _all_ subsequent non-flag tokens as values

            while True:
                try:
                    next_token = next(left_tokens)
                except StopIteration:
                    break
                if next_token.startswith("--"):
                    # push back this flag for the next iteration
                    left_tokens = itertools.chain([next_token], left_tokens)
                    break
                values.append(next_token)

            # - If no explicit values, treat as a boolean flag

            if not values:
                values = [True]

            # - Add values

            result["keyword"].setdefault(key, []).extend(values)

        else:
            # - Positional argument

            result["positional"].append(token)

    # - Return result

    return result


def example():
    import os

    shell("uv run python parse_unknown_args_example.py positional1 positional2 --simple simple --list1 a b --list2 c --list2 d")


if __name__ == "__main__":
    example()
