from shelly.arguments import ShellArgument


# Custom type to show how one could use it to directly transform a raw string from the command line
class TwiceType(int):
    def __new__(cls, raw_value: str):
        i = int.__new__(cls, raw_value)
        return i * 2


# Not the most pythonic way to decorate a function, but it's the closest I could get to a fluent API
# Any suggestions are very welcome!
@ShellArgument()
@ShellArgument.option("-f", name="file_name", value_type=str, description="File name", required=True)
@ShellArgument.option("-t", name="twice", value_type=TwiceType, description="Twice", required=True)
@ShellArgument.switch("--hash", name="hash_value", value_type=str, description="Hash value", required=False)
@ShellArgument.flag("-v", name="verbosity_level", description="Verbosity level", required=False)
def example(file_name: str, twice: TwiceType, hash_value: str, verbosity_level: int):
    print("file name:", file_name)
    print("twice:", twice)
    print("hash value:", hash_value)
    print("verbosity_level", verbosity_level)


# This has to be called from the program itself... possible to remove?
ShellArgument.fire_all()
