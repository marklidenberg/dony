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

Run `dony` to select and run a command:

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
3. **Add your own commands** under `<your_project>/donyfiles/`, or run `dony --init` to bootstrap a `hello_world` example.
4. **Use from anywhere in your project**:

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


## Use cases
- Build & Configuration
- Quality & Testing
- Release Management
- Deployment & Operations
- Documentation & Resources
- Git management

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


## Example

```python
import re
import dony

@dony.command()
def squash(
    new_branch: str = None,
    target_branch: str = None,
    commit_message: str = None,
    checkout_to_new_branch: str = None,
    remove_merged_branch: str = None,
):
    """Squashes current branch to main, checkouts to a new branch"""

    # - Get target branch

    target_branch = target_branch or dony.input(
        "Enter target branch:",
        default=dony.shell(
            "git branch --list main | grep -q main && echo main || echo master",
            quiet=True,
        ),
    )

    # - Get github username

    github_username = dony.shell("git config --get user.name", quiet=True)

    # - Get default branch if not set

    new_branch = new_branch or f"{github_username}-flow"

    # - Get current branch

    merged_branch = dony.shell(
        "git branch --show-current",
        quiet=True,
    )

    # - Merge with target branch first

    dony.shell(
        f"""

        # push if there are unpushed commits
        git diff --name-only | grep -q . && git push
        
        git fetch origin
        git checkout {target_branch}
        git pull
        git checkout {merged_branch}

        git merge {target_branch}
        
        if ! git diff-index --quiet HEAD --; then

          # try to commit twice, in case of formatting errors that are fixed by the first commit
          git commit -m "Merge with target branch" || git commit -m "Merge with target branch"
          git push
        else
          echo "Nothing merged – no commit made."
        fi
        """,
    )

    # - Do git diff

    dony.shell(
        f"""
        root=$(git rev-parse --show-toplevel)
        
        git diff {target_branch} --name-only -z \
        | while IFS= read -r -d '' file; do
            full="$root/$file"
            printf '\033[1;35m%s\033[0m\n' "$full"
            git --no-pager diff --color=always {target_branch} -- "$file" \
              | sed $'s/^/\t/'
            printf '\n'
          done
"""
    )

    # Ask user to confirm

    dony.confirm("Start squashing?")

    # - Check if target branch exists

    if (
        dony.shell(
            f"""
        git branch --list {target_branch}
    """
        )
        == ""
    ):
        return dony.error(f"Target branch {target_branch} does not exist")

    # - Get commit message from the user

    if not commit_message:
        while True:
            commit_message = dony.input(
                f"Enter commit message for merging branch {merged_branch} to {target_branch}:"
            )
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

    # - Check if user wants to remove merged branch

    remove_merged_branch = dony.confirm(
        f"Remove merged branch {merged_branch}?",
        provided_answer=remove_merged_branch,
    )

    # - Do the process

    dony.shell(
        f"""

        # - Make up to date

        git diff --name-only | grep -q . && git stash push -m "squash-{merged_branch}"
        git checkout {target_branch}

        # - Set upstream if needed

        if ! git ls-remote --heads --exit-code origin "{target_branch}" >/dev/null; then
            git push --set-upstream origin {target_branch} --force
        fi

        # - Pull target branch

        git pull

        # - Merge

        git merge --squash {merged_branch}
        
        # try to commit twice, in case of formatting errors that are fixed by the first commit
        git commit -m "{commit_message}" || git commit -m "{commit_message}"
        git push 

        # - Remove merged branch

        if {str(remove_merged_branch).lower()}; then
            git branch -D {merged_branch}
            git push origin --delete {merged_branch}
        fi

        # - Create new branch

        if {str(checkout_to_new_branch).lower()}; then
            git checkout -b {new_branch}
            git push --set-upstream origin {new_branch}
        fi
    """,
    )


if __name__ == "__main__":
    squash()
```

## License

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)

