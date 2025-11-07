from pprint import pprint
from textwrap import dedent

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def echo(
    text: str,
    line_prefix: str = "",
    color_style: str = "ansiwhite",  # take colors from prompt_toolkit
    prefix: str = "",
    suffix: str = "",
    bold: bool = False,
) -> None:
    # - Dedent text

    text = dedent(text).strip()

    # - Add line prefix if needed

    if line_prefix:
        text = "\n".join([line_prefix + line for line in text.splitlines()])

    # - Add prefix and suffix

    text = prefix + text + suffix

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
            + [
                ("question", "bold"),
            ]
            if bold
            else [],
        ),
    )


def example():
    echo(
        """echo "{"a": "b"}\nfoobar""",
        line_prefix="│ ",
        bold=False,
    )


if __name__ == "__main__":
    example()
