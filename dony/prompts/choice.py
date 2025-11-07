from dataclasses import dataclass


@dataclass
class Choice:
    """A choice with optional descriptions for select prompts."""

    value: str
    short_desc: str = ""
    long_desc: str = ""
