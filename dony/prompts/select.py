from typing import Sequence, Union, Optional, Tuple
import subprocess
import questionary
from questionary import Choice


from dony import confirm


def select(
    message: str,
    choices: Sequence[Union[str, Tuple[str, str], Tuple[str, str, str]]],
    default: Optional[Union[str, Sequence[str]]] = None,
    multi: bool = False,
    fuzzy: bool = False,
    default_confirm: bool = False,
    provided_answer: str = None,
) -> Union[None, str, Sequence[str]]:
    """
    Prompt the user to select from a list of choices, each of which can have:
      - a display value
      - a short description (shown after the value)
      - a long description (shown in a right-hand sidebar in fuzzy mode)

    If fuzzy is True, uses fzf with a preview pane for the long descriptions.
    Falls back to questionary if fzf is not available or fuzzy is False.
    """

    # - Check if provided answer is set

    if provided_answer is not None:
        if provided_answer not in choices:
            raise ValueError(f"Provided answer '{provided_answer}' is not in choices.")
        return provided_answer

    # - If default is present and default_confirm is True, then ask for confirmation to just use default

    if default is not None and default_confirm:
        # - Ask for confirmation

        if confirm(message + f"\nUse default? [{default}]"):
            return default

    # Helper to unpack a choice tuple or treat a plain string
    def unpack(c):
        if isinstance(c, tuple):
            if len(c) == 3:
                return c  # (value, short_desc, long_desc)
            elif len(c) == 2:
                return (c[0], c[1], "")
            elif len(c) == 1:
                return (c[0], "", "")
        else:
            return (c, "", "")

    if fuzzy:
        try:
            delimiter = "\t"
            lines = []

            # Map from the displayed first field back to the real value
            display_map: dict[str, str] = {}

            for choice in choices:
                value, short_desc, long_desc = unpack(choice)
                display_map[value] = value
                lines.append(f"{value}{delimiter}{short_desc}{delimiter}{long_desc}")

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

            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            output, _ = proc.communicate(input="\0".join(lines))
            if not output:
                raise KeyboardInterrupt

            # fzf returns lines like "disp1<sep>disp2", so split on the delimiter
            picked_disp1 = [
                line.split(delimiter, 1)[0] for line in output.strip().splitlines()
            ]
            results = [display_map[d] for d in picked_disp1]
            return results if multi else results[0]

        except FileNotFoundError:
            pass

    # Fallback to questionary
    q_choices = []

    for choice in choices:
        value, short_desc, long_desc = unpack(choice)

        if long_desc and short_desc:
            # suffix after the short description
            title = f"{value} - {short_desc} (description available)"
        elif long_desc and not short_desc:
            # no short_desc, suffix after the value
            title = f"{value} (description available)"
        elif short_desc:
            title = f"{value} - {short_desc}"
        else:
            title = value

        q_choices.append(
            Choice(
                title=title,
                value=value,
                checked=value in (default or []),
            )
        )

    if multi:
        result = questionary.checkbox(
            message=message,
            choices=q_choices,
            qmark="•",
            instruction="",
        ).ask()

        if result is None:
            raise KeyboardInterrupt

        return result

    result = questionary.select(
        message=message,
        choices=q_choices,
        default=default,
        qmark="•",
        instruction=" ",
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def example():
    selected = select(
        "Give me that path",
        choices=[
            ("foo", "", "This is the long description for foo."),
            ("bar", "second option", "Detailed info about bar goes here."),
            ("baz", "third one", "Here’s a more in-depth explanation of baz."),
            ("qux", "", "Qux has no short description, only a long one."),
        ],
        # choices=['foo', 'bar', 'baz', 'qux'],
        multi=True,
        fuzzy=False,
        default=["foo"],
        default_confirm=True,
    )
    print(selected)


if __name__ == "__main__":
    example()
