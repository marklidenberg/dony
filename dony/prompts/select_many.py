import asyncio
from typing import List, Sequence, Union, Optional, Dict, TypeVar

import questionary
from questionary import Choice as QuestionaryChoice
from prompt_toolkit.styles import Style

from dony.prompts.select import Choice


T = TypeVar("T")


async def select_many(
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
                default_positions = []  # 1-indexed positions of default items

                # Map from the displayed first field back to the real value
                display_map: Dict[str, Union[T, str]] = {}

                # Build set of default values for pre-selection
                default_set: set[str] = set(default or [])

                for idx, choice in enumerate(choices):
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
                    line = (
                        f"{display_value}{delimiter}{short_desc}{delimiter}{long_desc}"
                    )
                    lines.append(line)

                    # Track positions of default items (1-indexed for fzf)
                    is_default = value in default_set or display_value in default_set
                    if is_default:
                        default_positions.append(idx + 1)

                cmd = [
                    "fzf",
                    "--read0",  # ← treat NUL as item separator
                    "--sync",  # wait for input to complete before starting
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

                # Pre-select default items using pos() to jump to each position
                if default_positions:
                    # Build actions: pos(n)+select for each default position
                    actions = "+".join(
                        [f"pos({pos})+select" for pos in default_positions]
                    )
                    cmd.extend(["--bind", f"start:{actions}"])

                # - Run command

                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                stdout, _ = await proc.communicate(input="\0".join(lines).encode())
                output = stdout.decode()

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

        result = await questionary.checkbox(
            message=message,
            choices=q_choices,
            qmark="•",
            instruction="",
            style=Style(
                [
                    ("question", "fg:ansiblue"),  # the question text
                ]
            ),
        ).ask_async()

        # - Raise if KeyboardInterrupt

        if result is None:
            raise KeyboardInterrupt

        # - Repeat if not allow_empty_selection and no result

        if not result and not allow_empty_selection:
            # try again
            continue

        # - Return if all is good

        return result


async def example():
    selected = await select_many(
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
        fuzzy=True,
        # default=["foo", "baz"],
    )
    print(selected)


if __name__ == "__main__":
    asyncio.run(example())
