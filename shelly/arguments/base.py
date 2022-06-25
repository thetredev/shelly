from dataclasses import dataclass, field
from typing import Any, Type

from shelly.errors import ShellArgumentError
from shelly.arguments.values import ShellArgumentValue


@dataclass(frozen=True, eq=True, slots=True)
class ShellArgumentBase:
    """Base class used to describe a shell argument and its methods."""

    # The argument key
    # Example: -f
    key: str

    # The argument key indices
    # Example: [1]
    key_indices: list[int]

    # The Python-friendly argument name for key
    # Example: file_name
    name: str = field(default="")

    # The argument description
    # Example: Input file name to process
    description: str = field(default="")

    # Indicates whether the argument should be treated as required
    required: bool = field(default=False)

    # The argument value type known to Python
    # Example: str
    value_type: Type = field(default=None)

    # The argument value
    #  The actual value is encapsulated in class `ShellArgumentValue` as property `data`
    #  to allow for freezing this dataclass and therefore making sure to only access the parsed data.
    # Example: "my_file.txt"
    _value: ShellArgumentValue = field(default_factory=ShellArgumentValue)

    def parse(self) -> None:
        """Try to parse the value using the appropriate subclass. Throws a `ShellArgumentError` exception on failure for a required argument."""
        try:
            self._parse()
        except (IndexError, ValueError):
            if self.required:
                raise ShellArgumentError(f"Could not parse command line argument for required option '{self.key}'")

    def _parse(self) -> None:
        """Overwritten by subclass to perform the actual parsing of the data."""
        raise NotImplementedError("Abstract class!!")

    @property
    def value(self) -> Any:
        """Return the parsed data."""
        return self._value.data

    @property
    def key_index(self) -> int:
        """Return the first key index. Throws a `StopIteration` exception if the key wasn't found in the command line."""
        return next(iter(self.key_indices))
