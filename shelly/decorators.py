from __future__ import annotations

from collections.abc import ValuesView
from typing import Any, Callable, Protocol, Type

from shelly.cli import command_line
from shelly.errors import ShellArgumentError
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


class ShellArgumentDecorator:
    """Decorator used to provide a callback with parsed command line argument values."""
    __slots__ = ("callback", "chains", "flags", "options", "switches")

    # List to reference instances of this class
    instances: list[ShellArgumentDecorator] = list()

    # Short type aliases
    Chain: Type[ShellArgumentChain] = ShellArgumentChain
    Flag: Type[ShellArgumentFlag] = ShellArgumentFlag
    Option: Type[ShellArgumentOption] = ShellArgumentOption
    Switch: Type[ShellArgumentSwitch] = ShellArgumentSwitch

    def __init__(self) -> None:
        """Constructor: Initialize instance members."""
        # The callback to call after command line arguments have been parsed
        self.callback = None

        # Command line argument type maps
        # { <argument key>: <argument instance> }
        self.chains: dict[str, ShellArgumentChain] = dict()
        self.flags: dict[str, ShellArgumentFlag] = dict()
        self.options: dict[str, ShellArgumentOption] = dict()
        self.switches: dict[str, ShellArgumentSwitch] = dict()

        # Append this instance to the instance list
        self.instances.append(self)

    def __call__(self, callback: Callable[..., None]) -> None:
        """Called when the Python interpreter has scanned a function decorated with this class."""
        # Store the callback for later use if we haven't already
        if callback is not None and self.callback is None:
            self.callback = callback

        # The interpreter scanning stage is most probably not the only time this method gets called,
        # but AFAIK it's the only chance we get to store the callback, which is why we need the if statement above.

        # We should probably call super() on this method, too, but I'm not too sure of that at the moment.

    @staticmethod
    def _parse(instance_container: ValuesView[ShellArgumentType]) -> None:
        """Parse each command line argument in the instance container."""
        for argument in instance_container:
            argument.parse()

    def parse(self) -> None:
        """Parse all command line argument types."""
        self._parse(self.chains.values())
        self._parse(self.flags.values())
        self._parse(self.options.values())
        self._parse(self.switches.values())

        # Render this instance useless and remove it from the instance list
        # if we couldn't find any command line argument relevant for this decorator.
        if not self.flags and not self.options and not self.switches and not self.chains:
            self.instances.remove(self)

    @staticmethod
    def find_key_indices(key: str) -> list[int]:
        """Yield key indices in the command line. Throws a `ValueError` if the key wasn't found."""
        key_indices = [i for i, arg in enumerate(command_line) if key in arg]

        if not key_indices:
            raise ValueError(f"Key {key} not found in command line arguments!")

        yield from key_indices

    @staticmethod
    def _parse_value(instance_type: ShellArgumentType, key: str,  **kwargs: dict[str, Any]) -> ShellArgumentType:
        """Try to parse a command line argument value. Raise a `ShellArgumentError` on failure if the argument is required."""
        parsed_instance = None
        required = kwargs.get("required", False)

        try:
            key_indices = ShellArgumentDecorator.find_key_indices(key)
            parsed_instance = instance_type(key, list(key_indices), **kwargs)
        except ValueError:
            if required:
                raise ShellArgumentError(f"Could not parse required command line option '{key}'")

            # Store the parsed instance with 0 key indices and value `None`
            # if parsing wasn't successful and the argument is optional
            parsed_instance = instance_type(key, [], **kwargs)

        return parsed_instance

    @staticmethod
    def _last_instance() -> ShellArgumentDecorator:
        """Return the last instance of this decorator."""
        return ShellArgumentDecorator.instances[-1]

    @staticmethod
    def parse_value(instance_container: str, instance_type: ShellArgumentType, key: str, **kwargs: dict[str, Any]) -> ShellArgumentDecorator:
        """Wrapper around _parse_value() with more focus on storing the parsed instance in the appropriate command line argument type map."""
        parsed_instance = ShellArgumentDecorator._parse_value(instance_type, key, **kwargs)
        last_instance = ShellArgumentDecorator._last_instance()

        getattr(last_instance, instance_container)[key] = parsed_instance
        return last_instance

    @staticmethod
    def chain(key: str, **kwargs: dict[str, Any]) -> ShellArgumentDecorator:
        """Parse command line argument type `ShellArgumentChain`."""
        return ShellArgumentDecorator.parse_value("chains", ShellArgumentChain, key, **kwargs)

    @staticmethod
    def flag(key: str, **kwargs: dict[str, Any]) -> ShellArgumentDecorator:
        """Parse command line argument type `ShellArgumentFlag`."""
        return ShellArgumentDecorator.parse_value("flags", ShellArgumentFlag, key, **kwargs)

    @staticmethod
    def option(key: str, **kwargs: dict[str, Any]) -> ShellArgumentDecorator:
        """Parse command line argument type `ShellArgumentOption`."""
        return ShellArgumentDecorator.parse_value("options", ShellArgumentOption, key, **kwargs)

    @staticmethod
    def switch(key: str, **kwargs: dict[str, Any]) -> ShellArgumentDecorator:
        """Parse command line argument type `ShellArgumentSwitch`."""
        return ShellArgumentDecorator.parse_value("chains", ShellArgumentSwitch, key, **kwargs)

    @staticmethod
    def _format_callback_kwargs_for(instance_container: ValuesView[ShellArgument]) -> dict[str, ShellArgumentType]:
        """Format parsed arguments as keyword arguments."""
        return {
            argument.name: argument for argument in instance_container
        }

    def fire(self) -> None:
        """Parse the command line arguments and call the callback with the parsed values."""
        self.parse()

        kwargs = self._format_callback_kwargs_for(self.chains.values()) \
            | self._format_callback_kwargs_for(self.flags.values()) \
            | self._format_callback_kwargs_for(self.options.values()) \
            | self._format_callback_kwargs_for(self.switches.values())

        self.callback(**kwargs)

    @staticmethod
    def fire_all() -> None:
        """Call fire() on all instances of the instance list."""
        for instance in ShellArgumentDecorator.instances:
            instance.fire()


# Short type alias
shell = ShellArgumentDecorator
