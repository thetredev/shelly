from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Type

from shelly.arguments.errors import ShellArgumentError
from shelly.arguments.values import ShellArgumentValueWrapper


@dataclass(frozen=True, eq=True)
class ShellArgumentBase(object):
    key: str
    key_index: int

    name: str = field(default="")
    description: str = field(default="")

    required: bool = field(default=False)

    value_type: Type = field(default=None)
    _value: ShellArgumentValueWrapper = field(default_factory=ShellArgumentValueWrapper)

    def parse(self):
        try:
            self._parse()
        except (IndexError, ValueError):
            if self.required:
                raise ShellArgumentError(f"Could not parse command line argument for required option '{self.key}'")

    def _parse(self):
        raise NotImplementedError("Abstract class!!")

    @property
    def value(self) -> Any:
        return self._value.data
