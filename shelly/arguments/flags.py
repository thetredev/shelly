from dataclasses import dataclass

from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


@dataclass(frozen=True, eq=True, slots=True)
class ShellArgumentFlag(ShellArgumentBase):
    """Subclass used to implement parsing argument flags."""

    def _parse(self) -> None:
        """Parsing implementation."""
        # Examples:
        #  Key: -v
        #  Command line: -v
        #  Result: 1
        #
        #  Key: -v
        #  Command line: -v -v
        #  Result: 2

        arguments = [argument for argument in command_line if self._is_flag(argument)]

        self._value.data = sum([
            argument.count(self.__identifier) for argument in arguments
            if all(identifier == self.__identifier for identifier in argument[1:])
        ])

    def _is_flag(self, argument: str):
        """Return whether the given argument indicates a flag or not."""
        if argument.startswith("--"):
            return False

        return self.key == argument or argument.startswith(self.key)

    @property
    def __identifier(self) -> str:
        """Return the flag identifier. This will always be the first character of the `key` string."""
        return self.key[1]
