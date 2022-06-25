from shelly.arguments.base import ShellArgumentBase
from shelly.arguments.cli import command_line


class ShellArgumentChain(ShellArgumentBase):
    def _parse(self) -> None:
        self._value.data = [
            self.value_type(command_line[key_index + 1]) for key_index in self.key_indices
        ]
