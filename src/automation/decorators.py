"""
Decorators are wrappers to modify the behaviour of functions and classes. To call decorators, use @decorator.
"""

from time import time
import warnings
import functools


def timer(_func=None, *, print_msg=None):
    """
    Allows one to specify print_msg if need be. Useful for timing builtin methods.

    Parameter
    ---------
    print_msg : str
        Information to point user to newest version.
    """
    def decorator_timer(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            time_start = time()
            result = func(*args, **kwargs)
            time_end = time()

            print(f"{func.__name__ if print_msg is None else print_msg} took {(time_end - time_start):2.2f} seconds.")
            return result
        return wrapper_timer

    if _func is None:
        return decorator_timer
    else:
        return decorator_timer(_func)


def deprecated(_func=None, *, print_msg=None):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.

    Parameter
    ---------
    print_msg : str
        Information to point user to newest version.
    """

    def decorator_deprecated(func):

        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            with warnings.catch_warnings():
                if print_msg is None:
                    warnings.warn(f"\nFunction deprecated: {func.__name__}",
                                  category=DeprecationWarning, stacklevel=2)
                else:
                    warnings.warn(f"\nFunction deprecated: {func.__name__}"
                                  f"\n{print_msg}",
                                  category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper_decorator

    if _func is None:
        return decorator_deprecated
    else:
        return decorator_deprecated(_func)


