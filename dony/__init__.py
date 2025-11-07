from importlib.metadata import version

try:
    __version__ = version("dony")
except Exception:
    __version__ = "unknown"

from .command import command
from .shell import shell
from .get_git_root import get_git_root
from .prompts.autocomplete import autocomplete
from .prompts.confirm import confirm
from .prompts.input import input
from .prompts.path import path
from .prompts.press_any_key_to_continue import press_any_key_to_continue
from .prompts.select import select, Choice
from .prompts.print import print
from .prompts.error import error
from .prompts.success import success
from .prompts.select_or_input import select_or_input
