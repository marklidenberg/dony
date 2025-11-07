# 🍥️ dony

A lightweight Python command runner. A [just](https://github.com/casey/just) alternative.

## How it works

Define your commands in `donyfiles/` in the root of your project.

```python
# donyfiles/hello_world.py

import dony


@dony.command()
def hello_world():
    """Hello, world!"""
    dony.shell('echo "Hello, world!"')


if __name__ == "__main__":
    hello_world()
```

Run commands directly 
- with python: `python donyfiles/<command_name>.py`
- with dony cli: `dony <command_name> [--arg value]`

or just run `dony` command to select from all available commands:

```
                                                                                                                                                                                                                   
  📝 squash                                                                                                                                                                                             
  📝 release                                                                                                                                                                                                        
▌ 📝 hello_world                                                                                                                                                                                                    
  3/3 ─────────────────────────────────────────────────────────────────── 
Select command 👆                                                                                                                                                                                                   
╭───────────────────────────────────────────────────────────────────────╮
│ Prints "Hello, World!"                                                │
╰───────────────────────────────────────────────────────────────────────╯
```

## Quick Start

For MacOS:
```bash

# - Install prerequisites (pipx for global install, fzf and shfmt are optional)

brew install pipx, fzf, shfmt

# - Install dony

pipx install dony

# - Init dony (bootstraps hello-world example)

dony --init

# - Run dony

dony
```

## Commands

```python
import dony
from typing import Optional

@dony.command()
def greet(
    greeting: str = 'Hello',
    name: Optional[str] = None
):
    name = dony.input('What is your name?', provided=name)
    dony.shell(f"echo {greeting}, {name}!")
```

- Use the convenient shell wrapper `dony.shell`
- Use a bundle of useful user interaction functions, like `input`, `confirm` and `press_any_key_to_continue`
- Run commands without arguments – defaults are mandatory


## Use cases
- Build, deploy, release
- DevOps operations
- Testing
- Git management
- Repo chores

## Things to know

- All commands run from the project root (where `donyfiles/` is located)
- Available prompts based on `questionary`:
  - `dony.input`: text entry with optional autocompletions
  - `dony.confirm`: yes/no ([Y/n] or [y/N])
  - `dony.select`: option picker (supports fuzzy matching with fzf)
  - `dony.select_many`: multi-option picker (supports fuzzy matching with fzf)
  - `dony.select_or_input`: option picker + custom input fallback
  - `dony.press_any_key_to_continue`: pause until keypress
  - `dony.path`: filesystem path entry
  - `dony.print`: styled text output
  - `dony.error`: ❌ error message
  - `dony.success`: ✅ success message

### Rich Choice Objects

Selection prompts (`select`, `select_many`, `select_or_input`) support rich `Choice` objects with descriptions:

```python
from dony.prompts.choice import Choice

framework = dony.select(
    "Select a framework",
    choices=[
        Choice("react", "React", "A JavaScript library for building user interfaces"),
        Choice("vue", "Vue.js", "The Progressive JavaScript Framework"),
        Choice("angular", "Angular", "Platform for building mobile and desktop web applications"),
    ],
    fuzzy=True  # Uses fzf with preview pane for long descriptions
)
```

### Shell Command API

The `dony.shell()` function executes shell commands with enhanced features:

```python
dony.shell(
    command: str,
    working_dir: Optional[Union[str, Path]] = None,
    dry_run: bool = False,
    quiet: bool = False,
    capture_output: bool = True,
    abort_on_failure: bool = True,        # Prepends 'set -e'
    abort_on_unset_variable: bool = True, # Prepends 'set -u'
    trace_execution: bool = False,        # Prepends 'set -x'
    show_command: bool = True,
    confirm: bool = False,
) -> Optional[str]
```

## Example

```python
import dony
import re
from typing import Optional

@dony.command()
def squash(
    new_branch: Optional[str] = None,
    target_branch: Optional[str] = None,
    commit_message: Optional[str] = None,
    checkout_to_new_branch: Optional[str] = None,
    remove_merged_branch: Optional[str] = None,
):
  """Squashes current branch to main, checkouts to a new branch"""

  # - Get target branch

  target_branch = dony.input(
    "Enter target branch:",
    default=dony.shell(
      "git branch --list main | grep -q main && echo main || echo master",
      quiet=True,
    ),
    provided=target_branch,
  )

  # - Get github username

  github_username = dony.shell(
    "git config --get user.name",
    quiet=True,
  )

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
""",
  )

  # - Ask user to confirm

  if not dony.confirm("Start squashing?"):
    return

  # - Check if target branch exists

  if not dony.shell(f"git branch --list {target_branch}"):
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
    provided=checkout_to_new_branch,
  )

  # - Check if user wants to remove merged branch

  remove_merged_branch = dony.confirm(
    f"Remove merged branch {merged_branch}?",
    provided=remove_merged_branch,
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

