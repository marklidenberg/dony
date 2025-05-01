# 🍥️ dony

A lightweight Python command runner with simple and consistent workflow for managing project 
commands.

A `Justfile` alternative.

## How it works

Define your commands in `donyfiles/` in the root of your project.

```python
# donyfiles/commands/hello_world.py
import dony

@dony.command()
def hello_world(name: str = "John"):
    print(f"Hello, {name}!")	
```

Run `dony` to fuzzy-search your commands from anywhere in your project.

## Commands

Create commands as Python functions
```python
import dony

@dony.command()
def greet(
	greeting: str = 'Hello',
	name: str = None
):
	name = name or dony.input('What is your name?')
	dony.shell(f"echo {greeting}, {name}!")
```

- All parameters must provide defaults to allow invocation with no arguments, and any missing values should be requested via user prompts
- Currently, only str and List[str] parameter types are supported.

## Running commands

Run commands interactively:

```bash
dony
```

Run commands directly:

```bash
dony <command_name> [--arg1 value --arg2 value]
```

## Example


```python
import re
import dony


@dony.command()
def squash_and_migrate(
	new_branch: str = None,
	commit_message: str = None,
):
    """Squashes current branch to main, checkouts to a new branch"""

    # - Get default branch if not set

    new_branch = (
            new_branch or f"workflow_{dony.shell('date +%Y%m%d_%H%M%S', quiet=True)}"
    )

    # - Get current branch

    original_branch = dony.shell(
        "git branch --show-current",
        quiet=True,
    )

    # - Get commit message from the user

    if not commit_message:
        while True:
            commit_message = dony.input(
                f"Enter commit message for merging branch {original_branch} to main:"
            )
            if bool(
                    re.match(
                        r"^(?:(?:feat|fix|docs|style|refactor|perf|test|chore|build|ci|revert)(?:\([A-Za-z0-9_-]+\))?(!)?:)\s.+$",
                        commit_message.splitlines()[0],
                    )
            ):
                break
            dony.print("Only conventional commits are allowed, try again")

    # - Do the process

    dony.shell(
        f"""

        # - Make up to date

        git diff --cached --name-only | grep -q . && git stash squash_and_migrate-{new_branch}
        git checkout main
        git pull

        # - Merge

        git merge --squash {original_branch}
        git commit -m "{commit_message}"
        git push 

        # - Remove current branch

        git branch -D {original_branch}
        git push origin --delete {original_branch}

        # - Create new branch

        git checkout -b {new_branch}
        git push --set-upstream origin {new_branch}
    """,
    )

```

## Use cases:
- Build & Configuration
- Quality & Testing
- Release Management
- Deployment & Operations
- Documentation & Resources
- Git management

## Installation

Ensure you have the following prerequisites:
- Python 3.8 or higher
- `pipx` for isolated installation (`brew install pipx` on macOS)
- `fzf` for fuzzy command selection (`brew install fzf` on macOS)

Then install the package with `pipx`:
```bash
pipx install dony
```

Initialize your project:

```bash
dony --init
```

This creates a `donyfiles/` directory:
- A `commands/` directory containing a sample command
- A dedicated `uv` virtual environment


## donyfiles structure

```text
dony/
... (uv environment) 
├── commands/
│   ├── my_global_command.py # one command per file
│   ├── my-service/         
│   │   ├── service_command.py  # will be displayed as `my-service/service_command`
│   │   └── _helper.py       # private module (ignored)
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto\:marklidenberg@gmail.com)

