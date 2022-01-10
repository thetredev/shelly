from shelly.arguments.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentOption(ShellArgumentBase):
    def _parse(self):
        arg_index = self.key_index + 1
        self._value.data = self.value_type(command_line[arg_index])
