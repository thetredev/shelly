from typing import Iterable
from typing import Type

from shelly.arguments.base import ShellArgumentBase
from shelly.arguments.cli import command_line
from shelly.arguments.errors import ShellArgumentError

from shelly.arguments.options import ShellArgumentOption
from shelly.arguments.switches import ShellArgumentSwitch
from shelly.arguments.flags import ShellArgumentFlag


class ShellArgument(object):
    instances: list = list()

    def __init__(self) -> None:
        super().__init__()

        self.callback = None

        self.options: Iterable[ShellArgumentOption] = dict()
        self.switches: Iterable[ShellArgumentSwitch] = dict()
        self.flags: Iterable[ShellArgumentFlag] = dict()

    def __call__(self, callback):
        self.callback = callback

    @staticmethod
    def _find_key_index(key):
        for i, arg in enumerate(command_line):
            if key in arg:
                return i

        raise ValueError()

    def _parse_instance(self, instance_type: Type, key, **kwargs: dict):
        parsed_instance = None
        required = kwargs.get("required", False)

        try:
            key_index = self._find_key_index(key)
            parsed_instance = instance_type(key, key_index, **kwargs)
        except ValueError:
            if required:
                raise ShellArgumentError(f"Could not parse required command line option '{key}'")
        except ShellArgumentError as error:
            raise error

        return parsed_instance

    def _parse_value(self, instance_container: dict, instance_type: Type, key: str, **kwargs: dict):
        parsed_instance = self._parse_instance(instance_type, key, **kwargs)

        if parsed_instance is not None:
            instance_container[key] = parsed_instance

        return self

    def option(self, key: str, **kwargs: dict):
        return self._parse_value(self.options, ShellArgumentOption, key, **kwargs)

    def switch(self, key: str, **kwargs: dict):
        return self._parse_value(self.switches, ShellArgumentSwitch, key, **kwargs)

    def flag(self, key: str, **kwargs: dict):
        return self._parse_value(self.flags, ShellArgumentFlag, key, **kwargs)

    def parse(self):
        self.parse_arguments(self.options.values())
        self.parse_arguments(self.switches.values())
        self.parse_arguments(self.flags.values())

        if self.options or self.switches or self.flags:
            self.instances.append(self)

        return self

    @staticmethod
    def parse_command_line():
        for instance in ShellArgument.instances:
            instance.callback(**{
                    option.name: option.value for option in instance.options.values()
                } | {
                    switch.name: switch.value for switch in instance.switches.values()
                } | {
                    flag.name: flag.value for flag in instance.flags.values()
                }
            )

    @staticmethod
    def parse_arguments(instance: Iterable[ShellArgumentBase]):
        for argument in instance:
            argument.parse()
