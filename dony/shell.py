from __future__ import annotations

import os.path
import subprocess
import sys
from inspect import currentframe
from pathlib import Path
from textwrap import dedent
from typing import Optional, Union

from dony.prompts.error import error as dony_error
from dony.prompts.echo import echo as dony_print
from dony.prompts.confirm import confirm as dony_confirm


def shell(
    command: str,
    *,
    working_dir: Optional[Union[str, Path]] = None,
    dry_run: bool = False,
    quiet: bool = False,
    capture_output: bool = True,
    abort_on_failure: bool = True,
    abort_on_unset_variable: bool = True,
    trace_execution: bool = False,
    show_command: bool = True,
    confirm: bool = False,
) -> str:
    """
    Execute a shell command, streaming its output to stdout as it runs,
    and automatically applying 'set -e', 'set -u' and/or 'set -x' as requested.

    Args:
        command: The command line string to execute.
        working_dir: Changes the working directory before executing the command.
        dry_run: Prints the command without executing it.
        quiet: Suppresses output.
        capture_output: Captures and returns the full combined stdout+stderr;
                        if False, prints only and returns None.
        abort_on_failure: Prepends 'set -e' (aborts on first command error).
        abort_on_unset_variable: Prepends 'set -u' (aborts on unset variable).
        trace_execution: Prepends 'set -x' (traces command execution at shell level).
        show_command: Shows the formatted command before executing it.
        confirm: Asks for confirmation before executing the command.

    Returns:
        The full command output as a string (or bytes if text=False), or None if capture_output=False.

    Raises:
        RuntimeError: If the command exits with a non-zero status.
        KeyboardInterrupt: If the command is interrupted by the user.
    """

    # - Get formatted command if needed

    if show_command or dry_run:
        # if is required to avoid recursion
        try:
            formatted_command = shell(
                f"""
                    shfmt << 'EOF'
                    {command}
                """,
                quiet=True,
                show_command=False,
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
        except Exception:
            # todo later: specify exception types
            pass

        return ""

    # - Print command

    if (show_command and not quiet) or confirm:
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
            ("e", abort_on_failure),
            ("u", abort_on_unset_variable),
            ("x", trace_execution),
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
        text=True,
        cwd=working_dir,
    )

    # - Capture output

    buffer = []
    if proc.stdout is None:
        raise RuntimeError("Process stdout is unexpectedly None")
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

    output = "".join(buffer) if capture_output else ""

    # - Raise if exit code is non-zero

    if return_code != 0:
        if output and "KeyboardInterrupt" in output:
            raise KeyboardInterrupt
        raise RuntimeError("Dony command failed")

    # - Print closing message

    if show_command and not quiet:
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

    # - Disable only tracing of commands

    print(
        shell(
            'echo "no x prefix here"',
            trace_execution=False,
        )
    )

    # - Run in a different directory

    output = shell("ls", working_dir="/tmp")
    print("Contents of /tmp:", output)

    try:
        shell('echo "this will fail" && false')
        raise Exception("Should have failed")
    except RuntimeError:
        pass


if __name__ == "__main__":
    example()
