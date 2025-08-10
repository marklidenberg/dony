import os
from typing import Optional

import dony

__NAME__ = "release:0.1.1"


@dony.command()
def release(
    version: Optional[str] = None,
    uv_publish_token: Optional[str] = None,
):
    """Bump version and publish to PyPI"""

    # - Get main branch

    main_branch = dony.shell(
        "git branch --list main | grep -q main && echo main || echo master",
        quiet=True,
    )

    # - Select default arguments

    version = dony.select(
        "Choose version",
        choices=[
            "patch",
            "minor",
            "major",
        ],
        provided=version,
    )

    uv_publish_token = dony.input(
        "Enter UV publish token (usually a PyPI token)",
        default=os.getenv("UV_PUBLISH_TOKEN", ""),
        provided=uv_publish_token,
    )

    # - Get current branch

    original_branch = dony.shell(
        "git branch --show-current",
        quiet=True,
    )

    # - Go to main

    dony.shell(f"""

                # - Exit if there are staged changes

                git diff --cached --name-only | grep -q . && git stash

                # - Go to main

                git checkout {main_branch}

                # - Git pull

                git pull
    """)

    # - Bump

    dony.shell(
        f"""

            # - Bump

            VERSION=$(uv version --bump {version} --short)
            echo $VERSION

            # - Commit, tag and push

            git add pyproject.toml
            git commit --message "chore: release-$VERSION"
            git tag --annotate "release-$VERSION" --message "chore: release-$VERSION" HEAD
            git push
            git push origin "release-$VERSION" # push tag to origin,
            """
    )

    # - Build and publish

    dony.shell(
        f"""
        rm -rf dist/* # remove old builds
        uv build
        UV_PUBLISH_TOKEN={uv_publish_token} uv publish
        """
    )

    # - Go back to original branch

    dony.shell(
        f"""
        git checkout {original_branch}
        git merge --no-edit {main_branch} && git push
        """
    )


if __name__ == "__main__":
    release()
