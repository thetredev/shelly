from shelly.arguments.cli import command_line
from shelly.arguments import ShellArgumentBase


class ShellArgumentFlag(ShellArgumentBase):
    def _parse(self):
        args = [arg for arg in command_line if self._is_flag(arg)]

        self._value.data = sum([
            arg.count(self.identifier)
            for arg in args
            if all(identifier == self.identifier for identifier in arg[1:])
        ])

    def _is_flag(self, arg: str):
        if arg.startswith("--"):
            return False

        return self.key == arg or arg.startswith(self.key)

    @property
    def identifier(self):
        return self.key[1]
