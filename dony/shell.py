from __future__ import annotations

import os.path
import subprocess
import sys
from inspect import currentframe
from pathlib import Path
from textwrap import dedent
from typing import Optional, Union

from dony.prompts.error import error as dony_error
from dony.prompts.print import print as dony_print
from dony.prompts.confirm import confirm as dony_confirm


class DonyShellError(Exception):
    pass


def shell(
    command: str,
    *,
    capture_output: bool = True,
    text: bool = True,
    exit_on_error: bool = True,
    error_on_unset: bool = True,
    echo_commands: bool = False,
    working_dir: Optional[Union[str, Path]] = None,
    quiet: bool = False,
    dry_run: bool = False,
    raise_on_error: bool = True,
    print_command: bool = True,
    confirm: bool = False,
) -> Optional[str]:
    """
    Execute a shell command, streaming its output to stdout as it runs,
    and automatically applying 'set -e', 'set -u' and/or 'set -x' as requested.

    Args:
        command: The command line string to execute.
        capture_output: Captures and returns the full combined stdout+stderr;
                        if False, prints only and returns None.
        text: Treats stdout/stderr as text (str); if False, returns bytes.
        exit_on_error: Prepends 'set -e' (exit on any error).
        error_on_unset: Prepends 'set -u' (error on unset variables).
        echo_commands: Prepends 'set -x' (echo commands before executing).
        working_dir: Changes the working directory before executing the command.
        quiet: Suppresses output.
        dry_run: Prints the command without executing it.
        raise_on_error: Raises an exception if the command exits with a non-zero status.
        print_command: Prints the command before executing it.
        confirm: Asks for confirmation before executing the command.

    Returns:
        The full command output as a string (or bytes if text=False), or None if capture_output=False.

    Raises:
        subprocess.CalledProcessError: If the command exits with a non-zero status.
    """

    # - Get formatted command if needed

    if print_command or dry_run:
        # if is required to avoid recursion
        try:
            formatted_command = shell(
                f"""
                    shfmt << 'EOF'
                    {command}
                """,
                quiet=True,
                print_command=False,
            )
        except Exception:
            formatted_command = command
    else:
        formatted_command = command

    # - Process dry_run

    if dry_run:
        dony_print(
            "🐚 Dry run\n" + formatted_command,
            color_style="ansipurple",
        )

        # - Copy to clipboard if possible

        try:
            import pyperclip

            pyperclip.copy(formatted_command)
        except:
            # todo later: specify exception types
            pass

        return ""

    # - Print command

    if print_command and not quiet or confirm:
        dony_print(
            "🐚\n" + formatted_command,
            color_style="ansipurple",
        )

    if confirm:
        if not dony_confirm(
            "Are you sure you want to run the above command?",
        ):
            return dony_error("Aborted")

    # - Convert working_dir to string

    if isinstance(working_dir, Path):
        working_dir = str(working_dir)

    # - Build the `set` prefix from the enabled flags

    flags = "".join(
        flag
        for flag, enabled in (
            ("e", exit_on_error),
            ("u", error_on_unset),
            ("x", echo_commands),
        )
        if enabled
    )
    prefix = f"set -{flags}; " if flags else ""

    # - Dedent and combine the command

    full_cmd = prefix + dedent(command.strip())

    # - Execute with optional working directory

    proc = subprocess.Popen(
        full_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=text,
        cwd=working_dir,
    )

    # - Capture output

    buffer = []
    assert proc.stdout is not None
    while True:
        try:
            for line in proc.stdout:
                if not quiet:
                    print(line, end="")
                if capture_output:
                    buffer.append(line)
            break
        except UnicodeDecodeError:
            dony_error("Error decoding output. Skipping the line")

    proc.stdout.close()
    return_code = proc.wait()

    output = "".join(buffer) if capture_output else None

    # - Raise if exit code is non-zero

    if return_code != 0 and raise_on_error:
        if "KeyboardInterrupt" in output:
            raise KeyboardInterrupt
        raise DonyShellError("Dony command failed")

    # - Print closing message

    if print_command and not quiet:
        dony_print(
            "—" * 80,
            color_style="ansipurple",
        )

    # - Return output

    return output.strip()


def example():
    # Default: set -eux is applied

    # - Run echo command

    print(shell('echo "{"a": "b"}"'))

    # - Disable only echoing of commands

    print(
        shell(
            'echo "no x prefix here"',
            echo_commands=False,
        )
    )

    # - Run in a different directory

    output = shell("ls", working_dir="/tmp")
    print("Contents of /tmp:", output)

    try:
        shell('echo "this will fail" && false')
        raise Exception("Should have failed")
    except DonyShellError:
        pass


if __name__ == "__main__":
    example()
