from functools import partial
from typing import Literal

import dony
import fire


async def release(
    version: Literal["patch", "minor", "major"],
    uv_publish_token: str,
):
    """Bump version and publish to PyPI"""

    # - Set up shell with run_from

    shell = partial(
        dony.shell,
        run_from=dony.find_repo_root(__file__),
    )

    # - Assert we are in the main branch

    assert (
        await shell("git branch --show-current") == "main"
    ), "You are not in the main branch"

    # - Select default arguments

    assert version in [
        "patch",
        "minor",
        "major",
    ], "Version must be one of: patch, minor, major"

    # - Exit if there are staged changes

    staged_files = await shell("git diff --cached --name-only")
    assert (
        not staged_files
    ), "There are staged changes. Please commit or unstage them first."

    # - Bump

    await shell(
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

    await shell(
        f"""
        rm -rf dist/* # remove old builds
        uv build
        UV_PUBLISH_TOKEN={uv_publish_token} uv publish
        """
    )


if __name__ == "__main__":
    fire.Fire(release)
