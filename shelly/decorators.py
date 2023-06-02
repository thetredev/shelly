from __future__ import annotations

import importlib
from collections.abc import ValuesView
from pathlib import Path
from typing import Any, Callable, Protocol, Type

from shelly.cli import command_line
from shelly.errors import ShellArgumentError, ShellDecoratorPluginError
from shelly.arguments.chains import ShellArgumentChain
from shelly.arguments.flags import ShellArgumentFlag
from shelly.arguments.options import ShellArgumentOption
from shelly.arguments.switches import ShellArgumentSwitch


class ShellArgumentType(Protocol):
    def parse(self) -> None:
        ...


class ShellArgument(Protocol):
    @property
    def name(self) -> str:
        ...


class ShellDecoratorPlugin(Protocol):
    @property
    def SHELLY_PLUGIN_TYPE(self) -> Type:
        ...

    @property
    def SHELLY_PLUGIN_TYPE_NAME(self) -> str:
        ...

    @property
    def SHELLY_PLUGIN_NAME(self) -> str:
        ...


class ShellDecorator:
    """Decorator used to provide a callback with parsed command line argument values."""
    __slots__ = ("_callback", "_chains", "_flags", "_options", "_switches")

    # List to reference instances of this class
    _instances: list[ShellDecorator] = list()

    # Short type aliases
    Chain: Type[ShellArgumentChain] = ShellArgumentChain
    Flag: Type[ShellArgumentFlag] = ShellArgumentFlag
    Option: Type[ShellArgumentOption] = ShellArgumentOption
    Switch: Type[ShellArgumentSwitch] = ShellArgumentSwitch

    def __init__(self) -> None:
        """Constructor: Initialize instance members."""
        # The callback to call after command line arguments have been parsed
        self._callback = None

        # Command line argument type maps
        # { <argument key>: <argument instance> }
        self._chains: dict[str, ShellArgumentChain] = dict()
        self._flags: dict[str, ShellArgumentFlag] = dict()
        self._options: dict[str, ShellArgumentOption] = dict()
        self._switches: dict[str, ShellArgumentSwitch] = dict()

        # Append this instance to the instance list
        self._instances.append(self)

    def __call__(self, callback: Callable[..., None]) -> None:
        """Called when the Python interpreter has scanned a function decorated with this class."""
        # Store the callback for later use if we haven't already
        if callback is not None and self._callback is None:
            self._callback = callback

        # The interpreter scanning stage is most probably not the only time this method gets called,
        # but AFAIK it's the only chance we get to store the callback, which is why we need the if statement above.

        # We should probably call super() on this method, too, but I'm not too sure of that at the moment.

    def _get_parser_instances(self) -> dict:
        """Yield available parser instances."""
        for slot in self.__slots__:
            if slot != "_callback":
                yield getattr(self, slot)

    @staticmethod
    def _parse_instance(instance_container: ValuesView[ShellArgumentType]) -> None:
        """Parse each command line argument in the instance container."""
        for argument in instance_container:
            argument.parse()

    def _parse_all_instances(self) -> None:
        """Parse all command line argument types."""
        parsers = list(self._get_parser_instances())

        for parser in parsers:
            self._parse_instance(parser.values())

        # Render this instance useless and remove it from the instance list
        # if we couldn't find any command line argument relevant for this decorator.
        remove_instance = all(not parser for parser in parsers)

        if remove_instance:
            self._instances.remove(self)

    @staticmethod
    def _find_key_indices(key: str) -> list[int]:
        """Yield key indices in the command line. Throws a `ValueError` if the key wasn't found."""
        key_indices = [i for i, arg in enumerate(command_line) if key in arg]

        if not key_indices:
            raise ValueError(f"Key {key} not found in command line arguments!")

        yield from key_indices

    @staticmethod
    def _parse_value_internal(instance_type: ShellArgumentType, key: str,  **kwargs: dict[str, Any]) -> ShellArgumentType:
        """Try to parse a command line argument value. Raise a `ShellArgumentError` on failure if the argument is required."""
        parsed_instance = None
        required = kwargs.get("required", False)

        try:
            key_indices = ShellDecorator._find_key_indices(key)
            parsed_instance = instance_type(key, list(key_indices), **kwargs)
        except ValueError:
            if required:
                raise ShellArgumentError(f"Could not parse required command line option '{key}'")

            # Store the parsed instance with 0 key indices and value `None`
            # if parsing wasn't successful and the argument is optional
            parsed_instance = instance_type(key, [], **kwargs)

        return parsed_instance

    @staticmethod
    def _last_instance() -> ShellDecorator:
        """Return the last instance of this decorator."""
        return ShellDecorator._instances[-1]

    @staticmethod
    def _parse_value(instance_container: str, instance_type: ShellArgumentType, key: str, **kwargs: dict[str, Any]) -> ShellDecorator:
        """Wrapper around _parse_value_internal() with more focus on storing the parsed instance in the appropriate command line argument type map."""
        parsed_instance = ShellDecorator._parse_value_internal(instance_type, key, **kwargs)
        last_instance = ShellDecorator._last_instance()

        getattr(last_instance, instance_container)[key] = parsed_instance
        return last_instance

    @staticmethod
    def chain(key: str, **kwargs: dict[str, Any]) -> ShellDecorator:
        """Parse command line argument type `ShellArgumentChain`."""
        return ShellDecorator._parse_value("_chains", ShellArgumentChain, key, **kwargs)

    @staticmethod
    def flag(key: str, **kwargs: dict[str, Any]) -> ShellDecorator:
        """Parse command line argument type `ShellArgumentFlag`."""
        return ShellDecorator._parse_value("_flags", ShellArgumentFlag, key, **kwargs)

    @staticmethod
    def option(key: str, **kwargs: dict[str, Any]) -> ShellDecorator:
        """Parse command line argument type `ShellArgumentOption`."""
        return ShellDecorator._parse_value("_options", ShellArgumentOption, key, **kwargs)

    @staticmethod
    def switch(key: str, **kwargs: dict[str, Any]) -> ShellDecorator:
        """Parse command line argument type `ShellArgumentSwitch`."""
        return ShellDecorator._parse_value("_chains", ShellArgumentSwitch, key, **kwargs)

    @staticmethod
    def _format_callback_kwargs_for(instance_container: ValuesView[ShellArgument]) -> dict[str, ShellArgumentType]:
        """Format parsed arguments as keyword arguments."""
        return {
            argument.name: argument for argument in instance_container
        }

    def _fire(self) -> None:
        """Parse the command line arguments and call the callback with the parsed values."""
        self._parse_all_instances()
        kwargs = dict()

        for parser in self._get_parser_instances():
            kwargs.update(self._format_callback_kwargs_for(parser.values()))

        self._callback(**kwargs)

    @staticmethod
    def parse() -> None:
        """Call _fire() on all instances of the instance list."""
        for instance in ShellDecorator._instances:
            instance._fire()

    @staticmethod
    def plug(plugin: ShellDecoratorPlugin):
        """Dynamically extend this class with a decorator plugin."""
        # Get the decorator plugin name
        instance_name = plugin.SHELLY_PLUGIN_NAME

        # Throw an error if the instance name starts with an underscore (_)
        if instance_name.startswith("_"):
            raise ShellDecoratorPluginError("Plugin instance name must not start with an underscore (_)!")

        # Prepend the decorator plugin instance name with an underscore (_)
        instance_name = f"_{instance_name}"

        # Add the instance name to the class's __slots__ attribute
        setattr(ShellDecorator, "__slots__", (*ShellDecorator.__slots__, instance_name))

        # Add the plugin type to the class
        setattr(ShellDecorator, plugin.SHELLY_PLUGIN_TYPE_NAME, plugin.SHELLY_PLUGIN_TYPE)

        # Add the instance to the class (empty dict)
        setattr(ShellDecorator, instance_name, dict())

        # Add the parser method to the class using lambda magic
        setattr(ShellDecorator, plugin.SHELLY_PLUGIN_NAME,
            lambda key, **kwargs: ShellDecorator._parse_value(
                instance_name, plugin.SHELLY_PLUGIN_TYPE, key, **kwargs
            )
        )


# Short type alias
shell = ShellDecorator


# Register plugins
def __register_plugins():
    plugins_path = Path(__file__).parent.joinpath("plugins")

    plugin_list = [
        plugin_file.stem for plugin_file in plugins_path.iterdir()
        if plugin_file.name != "__init__.py" and plugin_file.name.endswith(".py")
    ]

    for plugin_module in plugin_list:
        shell.plug(importlib.import_module(f"shelly.plugins.{plugin_module}"))


__register_plugins()
