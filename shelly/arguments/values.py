from dataclasses import dataclass
from typing import Any


@dataclass(eq=True, slots=True)
class ShellArgumentValue:
    data: Any = None
