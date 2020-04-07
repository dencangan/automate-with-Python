import os

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_config_path(config_file):
    return os.path.join(_ROOT, config_file)