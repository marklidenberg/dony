import questionary
from prompt_toolkit.styles import Style


def press_any_key(
    message: str = "Press any key to continue...",
) -> None:
    # - Press any key

    result = questionary.press_any_key_to_continue(
        message=message,
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    ).ask()

    # - Raise KeyboardInterrupt if no result

    if result is None:
        raise KeyboardInterrupt


def example():
    print(press_any_key())


if __name__ == "__main__":
    example()
