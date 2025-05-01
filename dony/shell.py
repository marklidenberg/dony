from __future__ import annotations

import os.path
import subprocess
import sys
from inspect import currentframe
from pathlib import Path
from textwrap import dedent
from typing import Optional

from dony.prompts.error import error
from dony.get_dony_root import get_dony_root


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
    working_directory: Optional[str, Path] = "DONY_ROOT_PATH",
    quiet: bool = False,
    dry_run: bool = False,
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

    Returns:
        The full command output as a string (or bytes if text=False), or None if capture_output=False.

    Raises:
        subprocess.CalledProcessError: If the command exits with a non-zero status.
    """

    # - Process dry_run

    if dry_run:
        print("Dry run enabled. Would run")
        print(f"{command}")
        return

    # - Convert working_directory to string

    working_directory = str(working_directory)

    # - Find dony root path

    if working_directory == "DONY_ROOT_PATH":
        # - Get origin path: different cases depending on how the command is called

        if os.environ.get("_DONY_PATH"):
            # running command from dony client. This is set right before running the command (run_with_list_arguments call)
            origin_path = os.environ.get("_DONY_PATH")
        elif sys.argv[0].endswith("dony"):
            # run dony client
            origin_path = currentframe().f_back.f_back.f_code.co_filename
        else:
            # run command directly in python file, decorator is present
            origin_path = currentframe().f_back.f_back.f_back.f_code.co_filename

        # - Get dony root path

        working_directory = get_dony_root(origin_path)

    # - If relative - concat working directory with dony root

    if not os.path.isabs(working_directory):
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
    for line in proc.stdout:
        if not quiet:
            print(line, end="")
        if capture_output:
            buffer.append(line)
    proc.stdout.close()
    return_code = proc.wait()

    output = "".join(buffer) if capture_output else None

    # - Raise if exit code is non-zero

    if return_code != 0:
        if "KeyboardInterrupt" in output:
            raise KeyboardInterrupt
        raise DonyShellError("Dony command failed")

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
    except subprocess.CalledProcessError as e:
        print("Exited with code", e.returncode)
        if e.output is not None:
            print("Captured output:\n", e.output)


if __name__ == "__main__":
    example()
