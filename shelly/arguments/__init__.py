from collections.abc import ValuesView

from shelly.arguments.cli import command_line
from shelly.arguments.errors import ShellArgumentError

from shelly.arguments.flags import ShellArgumentFlag
from shelly.arguments.options import ShellArgumentOption
from shelly.arguments.switches import ShellArgumentSwitch


class ShellArgument(object):
    instances: list = list()

    def __init__(self) -> None:
        super().__init__()

        self.callback = None

        self.flags: dict[str, ShellArgumentFlag] = dict()
        self.options: dict[str, ShellArgumentOption] = dict()
        self.switches: dict[str, ShellArgumentSwitch] = dict()

        self.instances.append(self)

    def __call__(self, callback):
        if callback is not None and self.callback is None:
            self.callback = callback

    @staticmethod
    def _parse(instance_container: ValuesView[ShellArgumentFlag | ShellArgumentOption | ShellArgumentSwitch]):
        for argument in instance_container:
            argument.parse()

    def parse(self):
        self._parse(self.flags.values())
        self._parse(self.options.values())
        self._parse(self.switches.values())

        if not self.flags and not self.options and not self.switches:
            self.instances.remove(self)

    @staticmethod
    def _find_key_index(key: str) -> int:
        for i, arg in enumerate(command_line):
            if key in arg:
                return i

        raise ValueError()

    @staticmethod
    def _parse_value(instance_type: ShellArgumentFlag | ShellArgumentOption | ShellArgumentSwitch, key: str, **kwargs: dict):
        parsed_instance = None
        required = kwargs.get("required", False)

        try:
            key_index = ShellArgument._find_key_index(key)
            parsed_instance = instance_type(key, key_index, **kwargs)
        except ValueError:
            if required:
                raise ShellArgumentError(f"Could not parse required command line option '{key}'")

        return parsed_instance

    @staticmethod
    def _last_instance():
        return ShellArgument.instances[-1]

    @staticmethod
    def parse_value(instance_container: str, instance_type: ShellArgumentFlag | ShellArgumentOption | ShellArgumentSwitch, key: str, **kwargs: dict):
        parsed_instance = ShellArgument._parse_value(instance_type, key, **kwargs)
        last_instance = ShellArgument._last_instance()

        if parsed_instance is not None:
            getattr(last_instance, instance_container)[key] = parsed_instance

        return last_instance

    @staticmethod
    def flag(key: str, **kwargs: dict):
        return ShellArgument.parse_value("flags", ShellArgumentFlag, key, **kwargs)

    @staticmethod
    def option(key: str, **kwargs: dict):
        return ShellArgument.parse_value("options", ShellArgumentOption, key, **kwargs)

    @staticmethod
    def switch(key: str, **kwargs: dict):
        return ShellArgument.parse_value("switches", ShellArgumentSwitch, key, **kwargs)

    @staticmethod
    def _format_callback_kwargs_for(instance_container: ValuesView[ShellArgumentFlag | ShellArgumentOption | ShellArgumentSwitch]):
        return {
            argument.name: argument for argument in instance_container
        }

    def fire(self):
        self.parse()

        kwargs = self._format_callback_kwargs_for(self.flags.values()) \
            | self._format_callback_kwargs_for(self.options.values()) \
            | self._format_callback_kwargs_for(self.switches.values())

        self.callback(**kwargs)

    @staticmethod
    def fire_all():
        for instance in ShellArgument.instances:
            instance.fire()
