from dataclasses import dataclass

from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


@dataclass(frozen=True, eq=True, slots=True)
class ShellArgumentOption(ShellArgumentBase):
    """Subclass used to implement parsing argument options."""

    def _parse(self):
        """Parsing implementation."""
        # Example:
        #  Key: -x
        #  Command line: -x 70
        #  Result: 70

        self._value.data = self.value_type(command_line[self.value_index])
