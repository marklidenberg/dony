import asyncio

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


async def success(
    message: str,
    prefix: str = "✓ ",
) -> None:
    return print_formatted_text(
        FormattedText(
            [
                ("class:qmark", ""),
                ("class:question", prefix + message),
            ]
        ),
        style=questionary.Style(
            [
                ("question", "fg:ansigreen"),  # the question text
                ("question", "bold"),  # the question text
            ]
        ),
    )


async def example():
    await success(message="Success")


if __name__ == "__main__":
    asyncio.run(example())
