import contextlib

from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentSwitch(ShellArgumentBase):
    delimiter: str = "="

    def _parse(self) -> None:
        with contextlib.suppress(StopIteration):
            arg_value = command_line[self.key_index]
            self._value.data = self.value_type(arg_value.split(self.delimiter)[1])
