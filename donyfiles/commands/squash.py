import re
import dony

__NAME__ = "squash:0.1.0"


@dony.command()
def squash(
    new_branch: str = None,
    commit_message: str = None,
    checkout_to_new_branch: str = None,
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

            # - Create new branch

            git checkout -b {new_branch}
            git push --set-upstream origin {new_branch}
        """,
        )


if __name__ == "__main__":
    squash()
