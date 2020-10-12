"""Functions to assist in configuring paths and environments in Python."""

import sys
import os


def get_env_values(env_key=None):
    envs = dict(os.environ)

    if env_key is None:
        return envs

    assert env_key in list(envs), f"{env_key} is not an acceptable environment key. Acceptable keys are {list(envs)}"
    value = envs[env_key]
    return value


def append_sys_path(path="../"):
    """
    Function to append package directory to sys path - so a module can be from the command line.

    Parameters
    ----------
    path : str
        Directory path to append sys path to. Can use path hierarchy delimiting characters.
        Defaults to "../" (go up one level).

    Returns
    -------
    Print statement of appended path.

    Notes
    -----
    Same level: ./
    Go up 1 level: ../ - Defaults to this
    Go up 2 levels: ../..
    Go up 3 levels: ../../..
    """

    try:
        package_src = os.path.abspath(os.path.join(__file__, path))
        sys.path.append(package_src)
        print(f"Appended {package_src} to sys.path. Use sys.path to see full list of appended paths.")

    except NameError:
        # NameError will occur if running in interactive console (__file__ not defined)
        print("Appending path by running in interactive console...")
        package_src = os.path.abspath(path)
        assert os.path.exists(package_src) is True, "The path specified does not exist."
        sys.path.append(package_src)
        print(f"Appended {package_src} to sys.path. Use sys.path to see full list of appended paths.")


if __name__ == "__main__":
    append_sys_path()