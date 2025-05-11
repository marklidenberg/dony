import os

import dony


@dony.command()
def release(
    version: str = None,
    uv_publish_token: str = None,
):
    """Bump version and publish to PyPI"""

    # - Select default arguments

    version = version or dony.select(
        "Choose version",
        choices=[
            "patch",
            "minor",
            "major",
        ],
    )

    uv_publish_token = uv_publish_token or dony.input(
        "Enter UV publish token (usually a PyPI token)",
        default=os.getenv("UV_PUBLISH_TOKEN", ""),
    )

    # - Get current branch

    original_branch = dony.shell(
        "git branch --show-current",
        quiet=True,
    )

    # - Go to main

    dony.shell("""

                # - Exit if there are staged changes

                git diff --cached --name-only | grep -q . && git stash

                # - Go to main

                git checkout main

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
        uv build
        UV_PUBLISH_TOKEN={uv_publish_token} uv publish
        """
    )

    # - Go back to original branch

    dony.shell(
        f"""
        git checkout {original_branch}
        git merge --no-edit {original_branch} && git push
        """
    )


if __name__ == "__main__":
    release()
