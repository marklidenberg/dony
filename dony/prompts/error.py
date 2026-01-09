import asyncio

import questionary
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


async def error(
    message: str,
    prefix: str = "✕ ",
) -> None:
    return print_formatted_text(
        FormattedText(
            [
                ("class:question", prefix + message),
            ]
        ),
        style=questionary.Style(
            [
                ("question", "fg:ansired"),  # the question text
                ("question", "bold"),  # the question text
            ]
        ),
    )


async def example():
    await error("Failed to do something important")


if __name__ == "__main__":
    asyncio.run(example())
