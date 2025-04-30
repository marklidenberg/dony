import subprocess
from textwrap import dedent
from typing import Optional


def shell(
    command: str,
    *,
    capture_output: bool = True,
    text: bool = True,
    exit_on_error: bool = True,
    error_on_unset: bool = True,
    echo_commands: bool = True,
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

    Returns:
        The full command output as a string (or bytes if text=False), or None if capture_output=False.

    Raises:
        subprocess.CalledProcessError: If the command exits with a non-zero status.
    """

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

    # - Dedent and combine

    full_cmd = prefix + dedent(command.strip())

    # - Execute

    proc = subprocess.Popen(
        full_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=text,
    )

    # - Capture output

    buffer = []
    assert proc.stdout is not None
    for line in proc.stdout:
        print(line, end="")
        if capture_output:
            buffer.append(line)
    proc.stdout.close()
    retcode = proc.wait()

    output = "".join(buffer) if capture_output else None

    # - Raise if exit code is non-zero

    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, full_cmd, output=output)

    # - Return output

    return output


def example():
    # Default: set -eux is applied
    print(shell("""echo "{"a": "b"}" """))

# Path("/Users/marklidenberg/Documents/coding/repos/marklidenberg/dony/example/dony"), args={"positional": {}, "keyword": {}}
    print(shell("""uv run python -c 'import dony; import json; from pathlib import Path; import sys; dony.run_dony(dony_dir=Path("/Users/marklidenberg/Documents/coding/repos/marklidenberg/dony/example/dony"), args=...)'"""))
    #
    # # Disable only echoing of commands
    # print(shell("echo 'no x prefix here'", echo_commands=False))
    #
    # try:
    #     shell("""
    #         echo 'this will fail'
    #         false
    #         echo 'won't reach here'
    #     """)
    # except subprocess.CalledProcessError as e:
    #     print("Exited with code", e.returncode)
    #     if e.output is not None:
    #         print("Captured output:\n", e.output)


if __name__ == "__main__":
    example()
