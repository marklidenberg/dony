import asyncio

import questionary
from prompt_toolkit.styles import Style


async def press_any_key(
    message: str = "Press any key to continue...",
) -> None:
    # - Press any key

    result = await questionary.press_any_key_to_continue(
        message=message,
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    ).ask_async()

    # - Raise KeyboardInterrupt if no result

    if result is None:
        raise KeyboardInterrupt


async def example():
    print(await press_any_key())


if __name__ == "__main__":
    asyncio.run(example())
