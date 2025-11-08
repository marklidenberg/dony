from dataclasses import dataclass
from typing import Sequence, Union, Optional, Dict, TypeVar, Generic
import subprocess
import questionary
from questionary import Choice as QuestionaryChoice
from prompt_toolkit.styles import Style


T = TypeVar("T")


@dataclass
class Choice(Generic[T]):
    """A choice with optional descriptions for select prompts."""

    value: T
    display_value: str = ""
    short_desc: str = ""
    long_desc: str = ""

    def __post_init__(self):
        # If display_value is not provided, use str(value)
        if not self.display_value:
            self.display_value = str(self.value)


def select(
    message: str,
    choices: Sequence[Union[str, Choice[T]]],
    default: Optional[str] = None,
    fuzzy: bool = True,
    allow_custom: bool = False,
    custom_choice_text: str = "Custom",
    allow_empty: bool = False,
) -> Union[T, str]:
    """
    Prompt the user to select from a list of choices, each of which can have:
      - a value (the actual value returned)
      - a display value (shown in the list)
      - a short description (shown after the display value)
      - a long description (shown in a right-hand sidebar in fuzzy mode)

    If fuzzy is True, uses fzf with a preview pane for the long descriptions.
    Falls back to questionary if fzf is not available or fuzzy is False.

    Args:
        allow_custom: If True, adds a custom option that prompts for text entry.
        custom_choice_text: The text to display for the custom option (default: "Custom").
    """

    # - Add custom choice if requested

    actual_choices = list(choices)
    if allow_custom:
        actual_choices.append(custom_choice_text)

    # - Run fuzzy select prompt

    if fuzzy:
        try:
            # - Build command

            delimiter = "\t"
            lines = []

            # Map from the displayed first field back to the real value
            display_map: Dict[str, str] = {}

            for choice in actual_choices:
                if isinstance(choice, Choice):
                    value = choice.value
                    display_value = choice.display_value
                    short_desc = choice.short_desc
                    long_desc = choice.long_desc
                else:
                    value = choice
                    display_value = str(choice)
                    short_desc = ""
                    long_desc = ""

                display_map[display_value] = value
                lines.append(
                    f"{display_value}{delimiter}{short_desc}{delimiter}{long_desc}"
                )

            cmd = [
                "fzf",
                "--read0",  # ← treat NUL as item separator
                "--prompt",
                f"{message} 👆",
                "--with-nth",
                "1,2",
                "--delimiter",
                delimiter,
                "--preview",
                "echo {} | cut -f3",
                "--preview-window",
                "down:30%:wrap",
            ]

            # - Run command

            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            output, _ = proc.communicate(input="\0".join(lines))

            if output == "":
                raise KeyboardInterrupt

            # - Parse output

            # fzf returns lines like "disp1<sep>disp2", so split on the delimiter
            picked_display = output.strip().split(delimiter, 1)[0]
            result = display_map[picked_display]

            # - Handle custom input if selected

            if allow_custom and result == custom_choice_text:
                from dony.prompts.input_text import input_text

                return input_text(
                    message=message,
                    allow_empty=allow_empty,
                )

            # - Return if all is good

            return result

        except FileNotFoundError:
            raise FileNotFoundError(
                "fzf is not installed. Install it or set fuzzy=False to use the default prompt."
            )

    # - Fallback to questionary

    q_choices = []

    for choice in actual_choices:
        if isinstance(choice, Choice):
            value = choice.value
            display_value = choice.display_value
            short_desc = choice.short_desc
            long_desc = choice.long_desc
        else:
            value = choice
            display_value = str(choice)
            short_desc = ""
            long_desc = ""

        if long_desc and short_desc:
            # suffix after the short description
            title = f"{display_value} - {short_desc} ({long_desc})"
        elif long_desc and not short_desc:
            # no short_desc, suffix after the display_value
            title = f"{display_value} ({long_desc})"
        elif short_desc:
            title = f"{display_value} - {short_desc}"
        else:
            title = display_value

        q_choices.append(
            QuestionaryChoice(
                title=title,
                value=value,
                checked=value == default,
            )
        )

    # - Run select prompt

    result = questionary.select(
        message=message,
        choices=q_choices,
        default=default,
        qmark="•",
        instruction=" ",
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    ).ask()

    # - Raise KeyboardInterrupt if no result

    if result is None:
        raise KeyboardInterrupt

    # - Handle custom input if selected

    if allow_custom and result == custom_choice_text:
        from dony.prompts.input_text import input_text

        return input_text(
            message=message,
            allow_empty=allow_empty,
        )

    # - Return

    return result


def example():
    selected = select(
        "Give me that path",
        choices=[
            Choice("foo", long_desc="This is the long description for foo."),
            Choice("bar", "second option", "Detailed info about bar goes here."),
            Choice("baz", "third one", "Here's a more in-depth explanation of baz."),
            Choice("qux", long_desc="Qux has no short description, only a long one."),
        ],
        # choices=['foo', 'bar', 'baz', 'qux'],
        fuzzy=False,
        default="foo",
    )
    print(selected)


if __name__ == "__main__":
    example()
