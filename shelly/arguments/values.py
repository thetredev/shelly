from typing import Any


class ShellArgumentValue:
    __slots__ = ("data",)

    def __init__(self) -> None:
        self.data: Any = None
