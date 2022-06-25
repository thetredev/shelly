from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


class ShellArgumentFlag(ShellArgumentBase):
    def _parse(self) -> None:
        args = [arg for arg in command_line if self._is_flag(arg)]

        self._value.data = sum([
            arg.count(self.__identifier)
            for arg in args
            if all(identifier == self.__identifier for identifier in arg[1:])
        ])

    def _is_flag(self, arg: str):
        if arg.startswith("--"):
            return False

        return self.key == arg or arg.startswith(self.key)

    @property
    def __identifier(self) -> str:
        return self.key[1]
