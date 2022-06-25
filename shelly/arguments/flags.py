from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


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

        args = [arg for arg in command_line if self._is_flag(arg)]

        self._value.data = sum([
            arg.count(self.__identifier) for arg in args
            if all(identifier == self.__identifier for identifier in arg[1:])
        ])

    def _is_flag(self, arg: str):
        """Return whether the given argument indicates a flag or not."""
        if arg.startswith("--"):
            return False

        return self.key == arg or arg.startswith(self.key)

    @property
    def __identifier(self) -> str:
        """Return the flag identifier. This will always be the first character of the `key` string."""
        return self.key[1]
