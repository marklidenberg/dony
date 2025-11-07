import dony


@dony.command(working_dir="git_root")
def update_secrets_baseline():
    """Update .secrets.baseline file"""

    dony.shell("uv tool install detect-secrets")
    dony.shell("uvx detect-secrets scan > .secrets.baseline")


if __name__ == "__main__":
    update_secrets_baseline()
