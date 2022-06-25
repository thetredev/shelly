from shelly.decorators import shell


# Custom type to show how one could use it to directly transform a raw string from the command line
class DoubleInt(int):
    def __new__(cls, raw_value: str):
        i = int.__new__(cls, raw_value)
        return i * 2


# Not the most pythonic way to decorate a function, but it's the closest I could get to a fluent API
# Any suggestions are very welcome!
@shell()
@shell.option("-f", name="file_name", value_type=str, description="Example file name", required=True)
@shell.option("-t", name="double_int", value_type=DoubleInt, description="Double the integer input", required=True)
@shell.switch("--hash", name="hash_value", value_type=str, description="Example hash value", required=False)
@shell.flag("-v", name="verbosity_level", description="Verbosity level", required=False)
@shell.chain("-z", name="chain_example", value_type=int, description="Chain example", required=True)
def example(
    file_name: shell.Option,
    double_int: shell.Option,
    hash_value: shell.Switch,
    verbosity_level: shell.Flag,
    chain_example: shell.Chain
):
    print(file_name.description, file_name.value)
    print(double_int.description, double_int.value)
    print(hash_value.description, hash_value.value)
    print(verbosity_level.description, verbosity_level.value)
    print(chain_example.description, chain_example.value)


# This has to be called from the program itself... possible to remove?
shell.fire_all()


# Execute as follows:
# python concept.py -f "test.txt" -t 3 -v 5 -z 1 -z 3 -z 6 --hash=35t1251
