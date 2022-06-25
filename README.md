# Shelly

## Command Line Parser - Decorator Style

Shelly aims to provide a Python 3 library which provides a simple decorator to parse command line arguments. The following command line argument types are supported:

* Flags: `-v`, ...
* Options: `-f <value>`, ...
* Switches: `--property=<value>`, ...
* Chains: `-x 1 -x 2 -x 3`, ...

You can customize the delimiter for each `Switch` instance as you wish.

## Usage

Here's an example of how to use the Shelly decorator:
```python
from shelly.decorators import shell

@shell()
@shell.option("-f", name="file_name", value_type=str, description="Example file name", required=True)
@shell.switch("--property", name="file_property", value_type=str, description="Property to add to the file", required=False, delimiter=":")
def append_to_file_callback(
    file_name: shell.Option,
    file_property: shell.Switch
):
    with open(file_name.value, "a") as f:
        f.write(file_property.value)


def main():
    shell.parse()


if __name__ == "__main__":
    main()
```

This will append a string to a file. The command line usage would be:
```shell
python script.py -f myfile.txt --property:abcd
```

## Installation

Currently there's no PyPI package available for Shelly, but there will be at some point.

## How to extend the library

Shelly implements a plugin interface which you can use to extend the `shelly.decorator.ShellDecorator` class dynamically.

The following example demonstrates that using a `ListArgument` class which parses arguments of the format `"a,b,c,d"`, giving the result `["a", "b", "c", "d"]`:
```python
# shelly/plugins/list.py

from dataclasses import dataclass
from typing import Type

from shelly.cli import command_line
from shelly.arguments.base import ShellArgumentBase


@dataclass(frozen=True, eq=True, slots=True)
class ListArgument(ShellArgumentBase):
    delimiter = ","

    def _parse(self) -> None:
        self._value.data = command_line[self.value_index].split(self.delimiter)


SHELLY_PLUGIN_TYPE: Type[ListArgument] = ListArgument
SHELLY_PLUGIN_TYPE_NAME: str = "List"
SHELLY_PLUGIN_NAME: str = "list"
```

That's all there is to it. Define a class, define the global variables `SHELLY_PLUGIN_TYPE`, `SHELLY_PLUGIN_TYPE_NAME` and `SHELLY_PLUGIN_NAME` and you're done.

This will result in `shelly.decorator.ShellDecorator` being modified at runtime as follows:

```python
class ShellDecorator:
    __slots__ = ("_callback", "_chains", "_flags", "_options", "_switches", "_list")

    ...
    List: Type[ListArgument] = ListArgument

    def __init__(self) -> None:
        ...
        self._list = dict()

    def list(key: str, **kwargs: dict[str, Any]) -> ShellDecorator):
        return ShellDecorator._parse_value("_list", ListArgument, key, **kwargs)
```

See [`shelly.decorators.ShellDecorator.plug()`](shelly/decorators.py#L193) for implementation details.

## Contribute

If you find any bugs, please, by all means hit me with a pull request! If you want to extend the library, just implement some plugins. You can hit me with a pull request and ask for the plugin being integrated into the main code.

## Known Issues

See the [project issues](https://github.com/thetredev/shelly/issues).
