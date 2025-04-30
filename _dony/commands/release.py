import os

from marklidenberg.dony import dony


@dony.command()
def release(
    version: str = lambda: dony.select(
        "Choose version",
        choices=[
            "major",
            "minor",
            "patch",
        ],
    ),
):
    dony.shell("""

                # - Exit if there are staged changes

                git diff --cached --name-only | grep -q . && { echo "There are staged changes. Exiting."; exit 1; }

                # - Exit if there are unpulled commits

                git fetch origin && git diff --quiet HEAD origin/master ||  { echo "There are some unpulled commits. Exiting."; exit 1; }

                # - Bump and

                get new version

                cd ${0%/*}/..
                pwd
                echo $PWD
                # # poetry version major
                # VERSION=0.1.0
                # # 
                # # # - Commit, tag and push
                # # 
                # git add pyproject.toml
                # git commit --mesdony "chore: release-$VERSION"
                # git tag --annotate "release-$VERSION" --mesdony "chore: release-$VERSION" HEAD
                # git push
                # git push origin "release-$VERSION" # push tag to origin
            """)


if __name__ == "__main__":
    release()
