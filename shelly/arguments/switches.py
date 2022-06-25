import contextlib

from shelly.arguments.base import ShellArgumentBase
from shelly.arguments.cli import command_line


class ShellArgumentSwitch(ShellArgumentBase):
    delimiter: str = "="

    def _parse(self) -> None:
        with contextlib.suppress(StopIteration):
            arg_value = command_line[self.key_index]
            self._value.data = self.value_type(arg_value.split(self.delimiter)[1])
