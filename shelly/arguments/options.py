from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentOption(ShellArgumentBase):
    """Subclass used to implement parsing argument options."""

    def _parse(self):
        """Parsing implementation."""
        # Example:
        #  Key: -x
        #  Command line: -x 70
        #  Result: 70

        arg_index = self.key_index + 1
        self._value.data = self.value_type(command_line[arg_index])
