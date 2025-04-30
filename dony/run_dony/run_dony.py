import importlib.util
import inspect
import os
import sys
from collections import Counter, OrderedDict
from pathlib import Path

from dony import select
from dony.run_dony.run_with_list_arguments import run_with_list_arguments


def run_dony(
    dony_dir: Path,
    args: OrderedDict,
):
    # - Find all py files, extract all commands. If there is a file with filename not same as function name - rename it

    while True:
        file_paths = [p for p in dony_dir.rglob("commands/*.py") if not p.name.startswith("_")]
        commands = {}  # {path: command}
        should_repeat = False

        for file_path in file_paths:
            # - Skip file if starts with _

            def _is_skipped(part):
                if part.startswith("_"):
                    return True
                if part == ".venv":
                    return True
                return False

            if any(_is_skipped(part) for part in str(file_path.absolute()).split("/")):
                continue

            # - Collect callables with attribute _dony_command == True

            def _load_module(path: Path):
                spec = importlib.util.spec_from_file_location(path.stem, path)
                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)
                return module

            cmds = [
                member
                for _, member in inspect.getmembers(_load_module(file_path), inspect.isfunction)
                if getattr(member, "_dony_command", False)
            ]

            # - Validate exactly one command in a file

            if len(cmds) != 1:
                print(f"{file_path}: expected exactly one @command, found {len(cmds)}", file=sys.stderr)
                sys.exit(1)

            # - Rename file if it's name not the same as the function

            if file_path.stem != cmds[0].__name__:
                # - Repeat the cycle again since we will rename some files

                should_repeat = True

                # - Rename file

                os.rename(file_path, file_path.with_name(cmds[0].__name__ + ".py"))

                # - Git add if possible

                try:
                    os.system(f"git add {file_path.with_name(cmds[0].__name__ + '.py')}")
                except:
                    print(f"failed to add file to git: {file_path.with_name(cmds[0].__name__ + '.py')}")

            # - Validate command has _path

            commands[cmds[0]._path] = cmds[0]

        if not should_repeat:
            break

    # - Validate paths are unique

    counter = Counter(cmd._path for cmd in commands.values())
    duplicates = [path for path, count in counter.items() if count > 1]
    if duplicates:
        print(f"Duplicate commands: {duplicates}", file=sys.stderr)
        sys.exit(1)

    # - Return if no commands found

    if not commands:
        print("No commands found. Exiting...")
        sys.exit(0)

    # - Choose command and parse arguments

    if len(args["positional"]) == 1:  # no command was passed directly
        # - Interactive mode

        path = select(
            "Select command",
            choices=[command._path for command in commands.values()],
        )
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

    print("️⚙️ Running", path + "...")

    # - Run command with passed arguments

    run_with_list_arguments(
        func=commands[path],
        list_kwargs=args["keyword"],
    )


if __name__ == "__main__":
    run_dony(
        dony_dir=Path("../../example/dony"),
        args=OrderedDict(positional=["hello_world"], keyword={"name": ["Mark"]}),
    )

    # import json
    #
    # run_dony(
    #     dony_dir=Path("../../example/dony"),
    #     args=json.loads('{"positional": ["hello_world"], "keyword": {"name": ["Mark"]}}'),
    # )
