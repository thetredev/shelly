from shelly.arguments import ShellArgument

from shelly.arguments.chains import ShellArgumentChain
from shelly.arguments.flags import ShellArgumentFlag
from shelly.arguments.options import ShellArgumentOption
from shelly.arguments.switches import ShellArgumentSwitch



# Custom type to show how one could use it to directly transform a raw string from the command line
class DoubleInt(int):
    def __new__(cls, raw_value: str):
        i = int.__new__(cls, raw_value)
        return i * 2


# Not the most pythonic way to decorate a function, but it's the closest I could get to a fluent API
# Any suggestions are very welcome!
@ShellArgument()
@ShellArgument.option("-f", name="file_name", value_type=str, description="Example file name", required=True)
@ShellArgument.option("-t", name="double_int", value_type=DoubleInt, description="Double the integer input", required=True)
@ShellArgument.switch("--hash", name="hash_value", value_type=str, description="Example hash value", required=False)
@ShellArgument.flag("-v", name="verbosity_level", description="Verbosity level", required=False)
@ShellArgument.chain("-z", name="chain_example", value_type=int, description="Chain example", required=True)
def example(
    file_name: ShellArgumentOption,
    double_int: ShellArgumentOption,
    hash_value: ShellArgumentSwitch,
    verbosity_level: ShellArgumentFlag,
    chain_example: ShellArgumentChain
):
    print(file_name.description, file_name.value)
    print(double_int.description, double_int.value)
    print(hash_value.description, hash_value.value)
    print(verbosity_level.description, verbosity_level.value)
    print(chain_example.description, chain_example.value)


# This has to be called from the program itself... possible to remove?
ShellArgument.fire_all()
