import os
import re
from subprocess import CalledProcessError

import dony
from dony.shell import DonyShellError


@dony.command()
def merge_to_main():
    # - Validate git status

    try:
        dony.shell("""
                
    """)
    except DonyShellError:
        return

    # - Get current branch

    original_branch = dony.shell(
        "git branch --show-current",
        quiet=True,
    )

    # - New branch - current date and time

    new_branch = f"workflow_{dony.shell('date +%Y%m%d_%H%M%S', quiet=True)}"

    # - Get commit message

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

        git diff --cached --name-only | grep -q . && git stash merge_to_main-{new_branch}
        git checkout main
        git pull

        # - Merge

        git merge --squash {original_branch}
        git commit -m "{commit_message}"
        git push 

        # - Remove current branch

        git branch -D {original_branch}

        # - Create new branch

        git checkout -b {new_branch}
        git push --set-upstream origin {new_branch}
    """,
    )


if __name__ == "__main__":
    merge_to_main()
