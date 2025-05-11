from __future__ import annotations

import os.path
import subprocess
import sys
from inspect import currentframe
from pathlib import Path
from textwrap import dedent
from typing import Optional

from dony.prompts.error import error
from dony.prompts.print import print as dony_print
from dony.get_dony_root import get_dony_root
import pyperclip


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
    working_directory: Optional[str, Path] = None,
    quiet: bool = False,
    dry_run: bool = False,
    copy_dry_run_to_clipboard: bool = True,
    raise_on_error: bool = True,
    print_command: bool = True,
) -> Optional[str]:
    """
    Execute a shell command, streaming its output to stdout as it runs,
    and automatically applying 'set -e', 'set -u' and/or 'set -x' as requested.

    Args:
        command: The command line string to execute.
        capture_output: If True, captures and returns the full combined stdout+stderr;
                        if False, prints only and returns None.
        text: If True, treats stdout/stderr as text (str); if False, returns bytes.
        exit_on_error: If True, prepend 'set -e' (exit on any error).
        error_on_unset: If True, prepend 'set -u' (error on unset variables).
        echo_commands: If True, prepend 'set -x' (echo commands before executing).
        working_directory: If provided, change the working directory before executing the command.
        quiet: If True, suppresses output.
        dry_run: If True, prints the command without executing it.
        raise_on_error: If True, raises an exception if the command exits with a non-zero status.
        copy_dry_run_to_clipboard: If True, copies the dry run command to the clipboard.
        print_command: If True, prints the command before executing it.

    Returns:
        The full command output as a string (or bytes if text=False), or None if capture_output=False.

    Raises:
        subprocess.CalledProcessError: If the command exits with a non-zero status.
    """

    # - Get formatted command if needed

    if print_command or dry_run:
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
            # line_prefix="    ",
        )

        # - Copy to clipboard

        if copy_dry_run_to_clipboard:
            try:
                pyperclip.copy(formatted_command)
            except:
                error("Failed to copy dry-run to clipboard")

        return ""

    # - Print command

    if print_command and not quiet:
        dony_print(
            "🐚\n" + formatted_command,
            color_style="ansipurple",
            # line_prefix="    ",
        )

    # - Convert working_directory to string

    if isinstance(working_directory, Path):
        working_directory = str(working_directory)

    # - If relative - concat working directory with dony root

    if isinstance(working_directory, str) and not os.path.isabs(working_directory):
        working_directory = get_dony_root() / working_directory

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
        cwd=working_directory,
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
            error("Error decoding output. Skipping the line")

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
    print(shell('echo "{"a": "b"}"'))

    # Disable only echoing of commands
    print(
        shell(
            'echo "no x prefix here"',
            echo_commands=False,
        )
    )

    # Run in a different directory
    output = shell("ls", working_directory="/tmp")
    print("Contents of /tmp:", output)

    try:
        shell('echo "this will fail" && false')
        raise Exception("Should have failed")
    except DonyShellError:
        pass


if __name__ == "__main__":
    example()
