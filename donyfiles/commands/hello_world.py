import os
from subprocess import CalledProcessError

import dony


@dony.command()
def hello_world():
    """Hello, world!"""
    dony.shell('echo "Hello, world!"')


if __name__ == "__main__":
    hello_world()
