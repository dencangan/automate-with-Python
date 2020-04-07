"""
Decorators are wrappers to modify the behaviour of functions and classes. To call decorators, use @decorator.
"""

from time import time
import sys
import warnings


def timer(method):
    """Measure time taken in seconds to run"""

    def timed(*args, **kwargs):
        time_start = time()
        result = method(*args, **kwargs)
        time_end = time()
        print(f"{method.__name__} took {(time_end - time_start):2.2f} seconds.")
        return result

    return timed


def deprecated(name):
    """This is a decorator which can be used to mark functions as deprecated. It will result in a warning being emitted
    when the function is used.

    Parameter
    ---------
        name : str
            To guide user to the latest version
    """

    def wrapper(func):

        def new_func(*args, **kwargs):
            with warnings.catch_warnings():
                warnings.simplefilter("always", category=DeprecationWarning)
                warnings.warn(f"\n***{func.__name__}: This function/class is deprecated. "
                              f"Please refer to new version: {name}***",
                              category=DeprecationWarning)

            return func(*args, **kwargs)

        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        new_func.__dict__.update(func.__dict__)

        return new_func

    return wrapper


# TODO Incomplete
def exception(method):
    """Logs exceptions should any occur during a function's run."""

    def catch(*args, **kwargs):

        try:
            method(*args, **kwargs)
            print("Clear of exceptions!")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"{exc_type} found in {method.__name__} at line {exc_tb.tb_lineno}.\n{e}")

    return catch

