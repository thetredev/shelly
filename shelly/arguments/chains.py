import contextlib

from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentChain(ShellArgumentBase):
    """Subclass used to implement parsing argument chains."""

    def _parse(self) -> None:
        """Parsing implementation."""
        # Example:
        #  Key: -z
        #  Command line: -z 1 -z 2 -z 3
        #  Result: [1, 2, 3]

        with contextlib.suppress(StopIteration):
            self._value.data = [
                self.value_type(command_line[key_index + 1])
                for key_index in self.key_indices
            ]
