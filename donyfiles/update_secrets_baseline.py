import dony
from dony.command import RunFrom


@dony.command(run_from=RunFrom.GIT_ROOT)
def update_secrets_baseline():
    """Update .secrets.baseline file"""

    dony.shell("uv tool install detect-secrets")
    dony.shell("uvx detect-secrets scan > .secrets.baseline")


if __name__ == "__main__":
    update_secrets_baseline()
