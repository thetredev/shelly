class ShellArgumentError(ValueError):
    """Class used to distinguish Python errors from shelly errors."""


class ShellDecoratorPluginError(ValueError):
    """Class used to distinguish Python and general shelly errors from shelly plugin errors."""
