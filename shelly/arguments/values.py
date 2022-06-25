from dataclasses import dataclass
from typing import Any


@dataclass(eq=True, slots=True)
class ShellArgumentValue:
    """Class used to encapsulate parsed command line data."""
    data: Any = None
