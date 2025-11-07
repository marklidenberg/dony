from importlib.metadata import version

try:
    __version__ = version("dony")
except Exception:
    __version__ = "unknown"

from .command import command
from .shell import shell
from .get_git_root import get_git_root
from .prompts.confirm import confirm
from .prompts.input import input
from .prompts.path import path
from .prompts.press_any_key_to_continue import press_any_key_to_continue
from .prompts.choice import Choice
from .prompts.select import select
from .prompts.select_many import select_many
from .prompts.echo import echo
from .prompts.error import error
from .prompts.success import success
from .prompts.select_or_input import select_or_input

__all__ = [
    "__version__",
    "command",
    "shell",
    "get_git_root",
    "confirm",
    "input",
    "path",
    "press_any_key_to_continue",
    "Choice",
    "select",
    "select_many",
    "echo",
    "error",
    "success",
    "select_or_input",
]
