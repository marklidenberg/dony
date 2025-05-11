#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from textwrap import dedent

from dony import shell
from dony.get_dony_path import get_donyfiles_path
from dony.parse_unknown_args import parse_unknown_args


def main():
    # - Parse any input arguments (unknown for now)

    args = parse_unknown_args(sys.argv)

    # - Run version command

    if args["keyword"]:
        first_key, first_value = next(iter(args["keyword"].items()))

        if first_key == "version":
            assert first_value == [True]
            assert len(args["keyword"]) == 1, "version command takes no arguments"
            from dony import __version__

            print(f"dony version {__version__}")
            sys.exit(0)

        # - Run help command

        if first_key == "help":
            assert first_value == [True]
            assert len(args["keyword"]) == 1, "help command takes no arguments"
            print(
                dedent("""
                        dony: dony [OPTIONS] COMMAND [ARGS]
                
                        Options:
                          --version       Show version information and exit
                          --help          Show this help message and exit
                        
                        Commands:
                          my_command      Default operation
                        
                        Example:
                          dony my_command --arg_key arg_value
                       """)
            )
            sys.exit(0)

        # - Run 'init command'

        if first_key == "init":
            assert first_value == [True]
            assert len(args["keyword"]) == 1, "init command takes no arguments"

            # - Create donyfiles dir if it does not exist

            if not (Path.cwd() / "donyfiles").exists():
                os.mkdir(Path.cwd() / "donyfiles")

            # - Os into dony dir

            os.chdir(Path.cwd() / "donyfiles")

            # - Run uv init

            shell(
                'uv init --name dony-commands --description "dony environment"',
                working_directory=None,
            )

            # - Create environment

            shell(
                "uv sync",
                working_directory=None,
            )

            # - Add packages

            shell(
                """uv add dony""",
                working_directory=None,
            )

            # - Remove hello.py file

            os.remove("main.py")

            # - Create .gitignore file allowing uv files

            with open(".gitignore", "w") as f:
                f.write(
                    dedent("""
                            !.gitignore
                            !uv.lock
                            !pyproject.toml
                            !.python-version
                            !README.md
                            .venv
                    """).strip()
                )

            # - Create hello world example

            os.makedirs("commands/", exist_ok=True)

            with open("commands/hello_world.py", "w") as f:
                f.write(
                    dedent("""
                            import dony
                            
                            @dony.command()
                            def hello_world(name: str = "John"):
                                print(f"Hello, {name}!")
                            
                            """)
                )

            # - Add files to git

            shell(
                "git add .",
                working_directory=None,
            )

            sys.exit(0)

    # - Get dony dir

    root = Path.cwd()
    try:
        dony_path = get_donyfiles_path(root)

    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        if len(args["positional"]) > 1:
            if args["positional"][1] == "help":
                print("Did you mean `dony --help`?")
            if args["positional"][1] == "init":
                print("Did you mean `dony --init`?")
            if args["positional"][1] == "version":
                print("Did you mean `dony --version`?")
        sys.exit(1)

    # - Run run_dony in local uv environment. Remove dony from the local directory as it shadows the dony module

    shell(
        """
        uv run --no-active python -c "import sys; sys.path.pop(0); import dony; from pathlib import Path; import sys; dony.run_dony(donyfiles_path=Path({}), args={})"

        """.format(
            # dony_dir / ".venv/bin/python",
            ('"' + str(dony_path) + '"').replace('"', '\\"'),
            json.dumps(args).replace('"', '\\"'),
        ),
        print_command=False,
        working_directory=dony_path,
    )


def example():
    import os

    import sys

    sys.argv = ["dony"]

    # os.chdir("../example/")
    os.chdir("/Users/marklidenberg/Documents/coding/repos/marklidenberg/jprint2")
    main()


if __name__ == "__main__":
    # main()
    example()
