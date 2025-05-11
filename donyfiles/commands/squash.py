import re

import dony


__NAME__ = "squash:0.1.8"


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
