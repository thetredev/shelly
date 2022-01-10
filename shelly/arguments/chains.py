from shelly.arguments.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentChain(ShellArgumentBase):
    def _parse(self):
        self._value.data = [
            self.value_type(command_line[key_index + 1]) for key_index in self.key_indices
        ]
