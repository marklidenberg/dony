from importlib.metadata import version

try:
    __version__ = version("dony")
except Exception:
    __version__ = "unknown"

from .command import command
from .shell import shell
from .find_git_root import find_git_root
from .prompts.confirm import confirm
from .prompts.input import input
from .prompts.press_any_key import press_any_key
from .prompts.select import Choice, select
from .prompts.select_many import select_many
from .prompts.echo import echo
from .prompts.error import error
from .prompts.success import success

__all__ = [
    "__version__",
    "command",
    "shell",
    "find_git_root",
    "confirm",
    "input",
    "press_any_key",
    "Choice",
    "select",
    "select_many",
    "echo",
    "error",
    "success",
]
