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

        self.instances.append(self)

    def __call__(self, callback):
        if callback is not None:
            self.callback = callback

    def parse(self):
        self.parse_arguments(self.options.values())
        self.parse_arguments(self.switches.values())
        self.parse_arguments(self.flags.values())

        if not self.options and not self.switches and not self.flags:
            self.instances.remove(self)

    @staticmethod
    def last_instance():
        return ShellArgument.instances[-1]

    @staticmethod
    def _find_key_index(key):
        for i, arg in enumerate(command_line):
            if key in arg:
                return i

        raise ValueError()

    @staticmethod
    def _parse_value(instance_type: Type, key: str, **kwargs: dict):
        parsed_instance = None
        required = kwargs.get("required", False)

        try:
            key_index = ShellArgument._find_key_index(key)
            parsed_instance = instance_type(key, key_index, **kwargs)
        except ValueError:
            if required:
                raise ShellArgumentError(f"Could not parse required command line option '{key}'")
        except ShellArgumentError as error:
            raise error

        return parsed_instance

    @staticmethod
    def parse_value(instance_container: str, instance_type: Type, key: str, **kwargs: dict):
        parsed_instance = ShellArgument._parse_value(instance_type, key, **kwargs)
        last_instance = ShellArgument.last_instance()

        if parsed_instance is not None:
            getattr(last_instance, instance_container)[key] = parsed_instance

        return last_instance

    @staticmethod
    def option(key: str, **kwargs: dict):
        return ShellArgument.parse_value("options", ShellArgumentOption, key, **kwargs)

    @staticmethod
    def switch(key: str, **kwargs: dict):
        return ShellArgument.parse_value("switches", ShellArgumentSwitch, key, **kwargs)

    @staticmethod
    def flag(key: str, **kwargs: dict):
        return ShellArgument.parse_value("flags", ShellArgumentFlag, key, **kwargs)

    @staticmethod
    def fire():
        for instance in ShellArgument.instances:
            instance.parse()

            kwargs = {
                option.name: option.value for option in instance.options.values()
            } | {
                switch.name: switch.value for switch in instance.switches.values()
            } | {
                flag.name: flag.value for flag in instance.flags.values()
            }

            instance.callback(**kwargs)

    @staticmethod
    def parse_arguments(instance: Iterable[ShellArgumentBase]):
        for argument in instance:
            argument.parse()
