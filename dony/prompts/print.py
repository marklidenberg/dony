from pprint import pprint
from textwrap import dedent

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def print(
    text: str,
    line_prefix: str = "",
    color_style: str = "ansiblue",  # take colors from prompt_toolkit
):
    # - Dedent text

    text = dedent(text).strip()

    # - Add line prefix if needed

    if line_prefix:
        text = "\n".join([line_prefix + line for line in text.splitlines()])

    # - Print

    return print_formatted_text(
        FormattedText(
            [
                ("class:question", text),
            ]
        ),
        style=questionary.Style(
            [
                ("question", f"fg:{color_style}"),  # the question text
            ]
        ),
    )


def example():
    print("""echo "{"a": "b"}\nfoobar""", line_prefix="│ ")


if __name__ == "__main__":
    example()
