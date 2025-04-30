#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from textwrap import dedent

from dony import shell
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
                        Udony: dony [OPTIONS] COMMAND [ARGS]
                
                        Options:
                          --version       Show version information and exit
                          --help          Show this help mesdony and exit
                        
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

            # - Create dony dir if it does not exist

            if not (Path.cwd() / "dony").exists():
                os.mkdir(Path.cwd() / "dony")

            # - Os into dony dir

            os.chdir(Path.cwd() / "dony")

            # - Run uv init

            shell('uv init  --description "dony environment"')

            # - Create environment

            shell("uv sync")

            # - Add packages

            shell("""uv add dony""")

            # - Remove hello.py file

            os.remove("hello.py")

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
                    """)
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

            sys.exit(0)

    # - Get dony dir

    root = Path.cwd()
    try:

        def _get_dony_dir(root: Path) -> Path:
            current_path = Path(root)

            while True:
                candidates = [
                    (current_path / "_dony"),  # for this exact project, since dony directory is already used
                    (current_path / "dony"),
                ]

                for candidate in candidates:
                    if candidate.exists():
                        return candidate

                current_path = current_path.parent
                if current_path == current_path.parent:
                    raise FileNotFoundError("Could not find 'dony' folder")

        dony_dir = _get_dony_dir(root)

    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # - Cd into dony dir

    print("⚙️ dony called from ", dony_dir)

    os.chdir(dony_dir)

    # - Run run_dony in local uv environment. Remove dony from the local directory as it shadows the dony module

    shell(
        """
    uv run python -c "import sys; sys.path.pop(0); import dony; import json; from pathlib import Path; import sys; dony.run_dony(dony_dir=Path({}), args={})"

        """.format(
            # dony_dir / ".venv/bin/python",
            ('"' + str(dony_dir) + '"').replace('"', '\\"'),
            json.dumps(args).replace('"', '\\"'),
        ),
        echo_commands=False,
        working_directory=os.path.dirname(dony_dir),  # start from the root of the project
    )


def example():
    import os

    import sys

    sys.argv = ["dony"]

    os.chdir("../example/")
    main()


if __name__ == "__main__":
    # main()
    example()
