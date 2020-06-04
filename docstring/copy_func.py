import types


def copy_func(func, name=None):
    """Copy function with a new name.

    :param func: function to copy
    :param name: new name
    :returns: copied function
    """
    return types.FunctionType(func.__code__,
                              func.__globals__, name or func.__name__,
                              func.__defaults__,
                              func.__closure__)
