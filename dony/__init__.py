from importlib.metadata import version

try:
    __version__ = version("dony")
except Exception:
    __version__ = "unknown"

from .command import command
from .shell import shell
from .prompts.autocomplete import autocomplete
from .prompts.confirm import confirm
from .prompts.input import input
from .prompts.path import path
from .prompts.press_any_key_to_continue import press_any_key_to_continue
from .prompts.select import select
from .prompts.print import print
from .prompts.error import error
from .run_dony.run_dony import run_dony
from .prompts.success import success
from .prompts.select_or_input import select_or_input
