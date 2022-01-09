from shelly.arguments import ShellArgument


# Custom type to show how one could use it to directly transform a raw string from the command line
class TwiceType(int):
    def __new__(cls, raw_value: str):
        i = int.__new__(cls, raw_value)
        return i * 2


# Not the most pythonic way to decorate a function, but it's the best way I could come up with
# for a fluent API type scenario
#  Any suggestions are very welcome!
@ShellArgument() \
.option("-f", name="file_name", value_type=str, description="File name", required=True) \
.option("-t", name="twice", value_type=TwiceType, description="Twice", required=True) \
.switch("--hash", name="hash_value", value_type=str, description="Hash value", required=False) \
.flag("-v", name="verbosity_level", description="Verbosity level", required=False) \
.parse()  # I'd like to get rid of this parse() too, as it's currently just a way to tell the interpreter "we're finished configuring"
def example(file_name: str, twice: TwiceType, hash_value: str, verbosity_level: int):
    print(file_name)
    print(twice)
    print(hash_value)
    print(verbosity_level)


#
ShellArgument.parse_command_line()
