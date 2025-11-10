from typing import List, Sequence, Union, Optional, Dict, TypeVar
import subprocess
import questionary
from questionary import Choice as QuestionaryChoice
from prompt_toolkit.styles import Style

from dony.prompts.select import Choice


T = TypeVar("T")


def select_many(
    message: str,
    choices: Sequence[Union[str, Choice[T]]],
    default: Optional[Sequence[str]] = None,
    fuzzy: bool = True,
    allow_empty_selection: bool = False,
) -> List[Union[T, str]]:
    """
    Prompt the user to select multiple items from a list of choices, each of which can have:
      - a value (the actual value returned)
      - a display value (shown in the list)
      - a short description (shown after the value)
      - a long description (shown in a right-hand sidebar in fuzzy mode)

    If fuzzy is True, uses fzf with a preview pane for the long descriptions.
    Falls back to questionary if fzf is not available or fuzzy is False.
    """

    # - Run fuzzy select prompt

    if fuzzy:
        while True:
            try:
                # - Build command

                delimiter = "\t"
                lines = []

                # Map from the displayed first field back to the real value
                display_map: Dict[str, Union[T, str]] = {}

                for choice in choices:
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
                    "--multi",
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
                picked_displays = [
                    line.split(delimiter, 1)[0] for line in output.strip().splitlines()
                ]
                results = [display_map[d] for d in picked_displays]

                # - Try again if no results

                if not results and not allow_empty_selection:
                    # try again
                    continue

                # - Return if all is good

                return results

            except FileNotFoundError:
                raise FileNotFoundError(
                    "fzf is not installed. Install it or set fuzzy=False to use the default prompt."
                )

    # - Fallback to questionary

    q_choices = []

    for choice in choices:
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
                checked=value in (default or []),
            )
        )

    # - Run checkbox select prompt

    while True:
        # - Ask

        result = questionary.checkbox(
            message=message,
            choices=q_choices,
            qmark="•",
            instruction="",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
        ).ask()

        # - Raise if KeyboardInterrupt

        if result is None:
            raise KeyboardInterrupt

        # - Repeat if not allow_empty_selection and no result

        if not result and not allow_empty_selection:
            # try again
            continue

        # - Return if all is good

        return result


def example():
    selected = select_many(
        "Select multiple paths",
        choices=[
            Choice(value="foo", long_desc="This is the long description for foo."),
            Choice(
                value="bar",
                display_value="second option",
                short_desc="Detailed info about bar goes here.",
            ),
            Choice(
                value="baz",
                display_value="third one",
                short_desc="Here's a more in-depth explanation of baz.",
            ),
            Choice(
                value="qux", long_desc="Qux has no short description, only a long one."
            ),
        ],
        # choices=['foo', 'bar', 'baz', 'qux'],
        fuzzy=False,
        default=["foo"],
    )
    print(selected)


if __name__ == "__main__":
    example()
