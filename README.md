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

Shelly doesn't implement the default Python plugin architecutre, but it does provide the base dataclass `shelly.arguments.base.ShellArgumentBase` which in theory could be inherited from to provide a specialized parser. However, it's very cumbersome at the moment to connect all dependencies afterwards. There's basically no clean way to do this. I'll see what I can do.

## Contribute

As soon as there's a clean plugin infrastructure, there will be a guide on how to contribute. Until then, just file an [issue](https://github.com/thetredev/shelly/issues).

## Known Issues

See the [project issues](https://github.com/thetredev/shelly/issues).
