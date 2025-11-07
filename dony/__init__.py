from importlib.metadata import version

try:
    __version__ = version("dony")
except Exception:
    __version__ = "unknown"

from .command import command, RunFrom
from .shell import shell
from .get_git_root import get_git_root, NotFoundError
from .prompts.confirm import confirm
from .prompts.enter import enter
from .prompts.path import path
from .prompts.press_any_key_to_continue import press_any_key_to_continue
from .prompts.choice import Choice
from .prompts.select import select
from .prompts.select_many import select_many
from .prompts.echo import echo
from .prompts.error import error
from .prompts.success import success

__all__ = [
    "__version__",
    "command",
    "RunFrom",
    "shell",
    "get_git_root",
    "NotFoundError",
    "confirm",
    "enter",
    "path",
    "press_any_key_to_continue",
    "Choice",
    "select",
    "select_many",
    "echo",
    "error",
    "success",
]
