from dataclasses import dataclass
from typing import Any


@dataclass
class Choice:
    """A choice with optional descriptions for select prompts."""

    value: Any
    display_value: str = ""
    short_desc: str = ""
    long_desc: str = ""

    def __post_init__(self):
        # If display_value is not provided, use str(value)
        if not self.display_value:
            self.display_value = str(self.value)
