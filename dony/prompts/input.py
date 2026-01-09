import asyncio

import questionary
from prompt_toolkit.styles import Style


async def input(
    message: str,
    default: str = "",
    allow_empty: bool = False,
    multiline: bool = False,
) -> str:
    # - Run input prompt

    while True:
        # - Ask

        result = await questionary.text(
            message,
            default=default,
            qmark="•",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
            multiline=multiline,
        ).ask_async()

        # - Raise KeyboardInterrupt if no result

        if result is None:
            raise KeyboardInterrupt

        # - Return result

        if allow_empty or result:
            return result


async def example():
    print(await input(message="What is your name?"))


if __name__ == "__main__":
    asyncio.run(example())
