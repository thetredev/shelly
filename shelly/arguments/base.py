from dataclasses import dataclass, field
from typing import Any, Type

from shelly.arguments.errors import ShellArgumentError
from shelly.arguments.values import ShellArgumentValue


@dataclass(frozen=True, eq=True, slots=True)
class ShellArgumentBase:
    key: str
    key_indices: list[int]

    name: str = field(default="")
    description: str = field(default="")

    required: bool = field(default=False)

    value_type: Type = field(default=None)
    _value: ShellArgumentValue = field(default_factory=ShellArgumentValue)

    def parse(self) -> None:
        try:
            self._parse()
        except (IndexError, ValueError):
            if self.required:
                raise ShellArgumentError(f"Could not parse command line argument for required option '{self.key}'")

    def _parse(self) -> None:
        raise NotImplementedError("Abstract class!!")

    @property
    def value(self) -> Any:
        return self._value.data

    @property
    def key_index(self) -> int:
        return next(iter(self.key_indices))
