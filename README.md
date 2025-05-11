# 🍥️ dony

A lightweight Python command runner with a simple and consistent workflow. A `Justfile` alternative.

## How it works

Define your commands in `donyfiles/` in the root of your project.

```python
import dony

@dony.command()
def hello_world():
    """Prints "Hello, World!" """
    dony.shell('echo "Hello, World!"')
```

Run `dony` to fuzzy-search your commands from anywhere in your project.

```
                                                                                                                                                                                                                   
  📝 squash                                                                                                                                                                                             
  📝 release                                                                                                                                                                                                        
▌ 📝 hello_world                                                                                                                                                                                                    
  3/3 ─────────────────────────────────────────────────────────────────── 
Select command 👆                                                                                                                                                                                                   
╭───────────────────────────────────────────────────────────────────────╮
│ Prints "Hello, World!"                                                │
│                                                                       │
│                                                                       │
╰───────────────────────────────────────────────────────────────────────╯
```

Or call them directly: `dony <command_name> [--arg value]`.

## Quick Start

1. **Install Prerequisites**: Python 3.8+, `pipx` (for installation only, yor may use any other tool you like), optional `fzf` for fuzzy-search and `shfmt` for pretty command outputs.

   For macOS, run 

   ```bash
   brew install pipx
   brew install fzf 
   brew install shfmt
   ```

2. **Install** `dony`:

    ```bash
    pipx install dony
    ```
3. **cd** into your project:

   ```bash
   cd my/project/path
   ```

4. **Create** `donyfiles/` with a sample command and a `uv` environment:

    ```bash
    dony --init
    ```

5. **Add your own commands** under `donyfiles/commands/`.
6. **Use**:

    ```bash
    dony
    ```

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

- Use the convenient shell wrapper `dony.shell`
- Use a bundle of useful user interaction functions, like `input`, `confirm` and `press_any_key_to_continue`
- Run commands without arguments – defaults are mandatory

## Example


```python
import re
import dony


@dony.command()
def squash(
        new_branch: str = None,
        commit_message: str = None,
        checkout_to_new_branch: str = None,
):
    """Squashes current branch to main, checkouts to a new branch"""

    # - Get default branch if not set

    new_branch = new_branch or f"workflow_{dony.shell('date +%Y%m%d_%H%M%S', quiet=True)}"

    # - Get current branch

    original_branch = dony.shell(
        "git branch --show-current",
        quiet=True,
    )

    # - Get commit message from the user

    if not commit_message:
        while True:
            commit_message = dony.input(f"Enter commit message for merging branch {original_branch} to main:")
            if bool(
                    re.match(
                        r"^(?:(?:feat|fix|docs|style|refactor|perf|test|chore|build|ci|revert)(?:\([A-Za-z0-9_-]+\))?(!)?:)\s.+$",
                        commit_message.splitlines()[0],
                    )
            ):
                break
            dony.print("Only conventional commits are allowed, try again")

    # - Check if user wants to checkout to a new branch

    checkout_to_new_branch = dony.confirm(
        f"Checkout to new branch {new_branch}?",
        provided_answer=checkout_to_new_branch,
    )

    # - Do the process

    dony.shell(
        f"""

        # - Make up to date

        git diff --name-only | grep -q . && git stash squash-{new_branch}
        git checkout main
        git pull

        # - Merge

        git merge --squash {original_branch}
        git commit -m "{commit_message}"
        git push 

        # - Remove current branch

        git branch -D {original_branch}
        git push origin --delete {original_branch}
    """
    )

    if checkout_to_new_branch:
        dony.shell(
            f"""
            git checkout -b {new_branch}
            git push --set-upstream origin {new_branch}
        """,
        )


if __name__ == "__main__":
    squash()
```

## Use cases
- Build & Configuration
- Quality & Testing
- Release Management
- Deployment & Operations
- Documentation & Resources
- Git management

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

## Things to know

- All commands run from the project root (where `donyfiles/` is located)
- Available prompts based on `questionary`:
  - `dony.input`: free-text entry
  - `dony.confirm`: yes/no ([Y/n] or [y/N])
  - `dony.select`: option picker (supports multi & fuzzy)
  - `dony.select_or_input`: option picker (supports multi & fuzzy) with the ability to enter a custom value
  - `dony.press_any_key_to_continue`: pause until keypress
  - `dony.path`: filesystem path entry
  - `dony.autocomplete`: suggestion-driven input
  - `dony.print`: styled text output
  - `dony.error`: ❌ error message
  - `dony.success`: ✅ success message
- `dony` enforces files to be named after functions and will rename them automatically when invoked

## License

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)

