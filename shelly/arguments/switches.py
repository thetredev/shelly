import contextlib

from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentSwitch(ShellArgumentBase):
    """Subclass used to implement parsing argument switches."""

    # The default argument value delimiter
    delimiter: str = "="

    def _parse(self) -> None:
        """Parsing implementation."""
        # Example:
        #  Key: --verbosity
        #  Command line: --verbosity=4
        #  Result: 4

        with contextlib.suppress(StopIteration):
            arg_value = command_line[self.key_index]
            self._value.data = self.value_type(arg_value.split(self.delimiter)[1])
