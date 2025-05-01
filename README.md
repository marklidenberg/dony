# 🍥️ dony

A lightweight Python command runner with simple and consistent workflow for managing project 
commands.

A `Justfile` alternative.

## How it works

Define your commands in `donyfiles/` in the root of your project.

```python
import dony

@dony.command()
def hello_world():
    """Prints "Hello, World!" """
    dony.shell('echo "Hello, World!')
```

Run `dony` to fuzzy-search your commands from anywhere in your project.

```
                                                                                                                                                                                                                   
  📝 squash_and_migrate                                                                                                                                                                                             
  📝 release                                                                                                                                                                                                        
▌ 📝 hello_world                                                                                                                                                                                                    
  3/3 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
Select command 👆                                                                                                                                                                                                   
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Prints "Hello, World!"                                                                                                                                                                                           │
│                                                                                                                                                                                                                  │
│                                                                                                                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Or call them directly: `dony <command_name> [--arg value]`.

## Commands

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

- Use convenient shell wrapper `dony.shell`
- Use a bundle of useful user interaction functions, like `input`, `confirm` and `press_any_key_to_continue`
- Run any command without any arguments - defaults are mandatory

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

    # - Squash and migrate

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

## Use cases
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

Creates a `donyfiles/` folder with a sample command and a `uv` virtual environment.


## donyfiles/

```text
donyfiles/
... (uv environment) 
├── commands/
│   ├── my_command.py # one command per file
│   ├── my-service/         
│   │   ├── service_command.py  # will be displayed as `my-service/service_command`
│   │   └── _helper.py       # non-command file
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto\:marklidenberg@gmail.com)

