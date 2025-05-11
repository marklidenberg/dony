import re

import dony


@dony.command()
def pipx_install_dot():
    """Installs current branch to pipx"""

    dony.shell("pipx install . --force")


if __name__ == "__main__":
    pipx_install_dot()
