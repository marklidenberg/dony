import importlib.util
import inspect
import os
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from dotenv import load_dotenv

from dony.get_donyfiles_path import get_donyfiles_path
from dony.prompts.error import error
from dony.prompts.select import select
from dony.run_dony.run_with_list_arguments import run_with_list_arguments
from jprint2 import jprint


def run_dony(
    donyfiles_path: Path,
    args: OrderedDict = OrderedDict({}),
):
    """Dony entry point."""

    # - Create __init__.py in donyfiles_path.parent if it doesn't exist

    if not (donyfiles_path.parent / "__init__.py").exists():
        (donyfiles_path.parent / "__init__.py").touch()

    # - Add dony root to path

    sys.path = [str(donyfiles_path.parent)] + sys.path

    # - Find all py files, extract all commands. If there is a file with filename not same as function name - rename it

    while True:
        file_paths = [
            p for p in donyfiles_path.rglob("**/*.py") if not p.name.startswith("_")
        ]
        commands = {}  # {path: command}
        should_repeat = False

        for file_path in file_paths:
            # - Skip file if starts with _ or .venv

            def _is_skipped(part):
                if part.startswith("_"):
                    return True
                if part == ".venv":
                    return True
                return False

            if any(_is_skipped(part) for part in str(file_path.absolute()).split("/")):
                continue

            # - Collect callables with attribute _dony_command == True (decorated with @command)

            def _load_module(path: Path):
                spec = importlib.util.spec_from_file_location(path.stem, path)
                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)
                return module

            cmds = [
                member
                for _, member in inspect.getmembers(
                    _load_module(file_path), inspect.isfunction
                )
                if getattr(member, "_dony_command", False)
                and inspect.getsourcefile(inspect.unwrap(member)) == str(file_path)
            ]

            # - Validate command has _path

            commands[cmds[0]._path] = cmds[0]

        if not should_repeat:
            break

    # - Validate paths are unique

    counter = Counter(cmd._path for cmd in commands.values())
    duplicates = [path for path, count in counter.items() if count > 1]
    if duplicates:
        print(
            f"Duplicate commands: {duplicates}",
            file=sys.stderr,
        )
        sys.exit(1)

    # - Return if no commands found

    if not commands:
        print("No commands found. Exiting...")
        sys.exit(0)

    # - Choose command and parse arguments

    if len(args["positional"]) == 1:  # no command was passed directly
        # - Interactive mode

        try:
            path = select(
                "Select command",
                choices=sorted(
                    [
                        (
                            ("📝 " if command.__doc__ else "️  ") + command._path,
                            "",
                            command.__doc__ or "",
                        )
                        for command in commands.values()
                    ],
                    key=lambda x: ("/" not in x[0], x[0].replace("📝 ", "").strip()),
                    reverse=True,
                ),
                fuzzy=True,
            )
        except KeyboardInterrupt:
            return error("Dony command interrupted")
    else:
        # - Command line mode

        path = args["positional"][1]

        # - Validate command exists

        if path not in commands:
            print(f"Unknown command: {path}", file=sys.stderr)
            print("\nAvailable commands:", file=sys.stderr)
            for cmd_path in sorted(commands.keys()):
                print(f"  {cmd_path}", file=sys.stderr)
            sys.exit(1)

    if not path:
        return

    print(f"️🍥 Running {path} from {donyfiles_path}...")

    # - Load dotenv from dony path and parent

    load_dotenv(dotenv_path=donyfiles_path / ".env")
    load_dotenv(dotenv_path=donyfiles_path.parent / ".env")

    # - Set dony path to env so that shell function can find it

    os.environ["_DONY_PATH"] = str(donyfiles_path)

    # - Run command with passed arguments

    run_with_list_arguments(
        func=commands[
            path.replace("📝 ", "").replace("\ufe0f", "").strip()
        ],  # 0xfe0f is an invisible "display this preceding character in emoji (color) style" character. Not sure why it's sometimes there
        list_kwargs=args["keyword"],
    )


if __name__ == "__main__":
    run_dony(
        donyfiles_path=get_donyfiles_path(),
        # donyfiles_path=Path("/Users/marklidenberg/Documents/coding/repos/deeplay-io/category-store/donyfiles"),
        args=OrderedDict(
            positional=["hello_world"],
            keyword={},
        ),
    )
