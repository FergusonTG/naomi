from .connection import Connection  # NOQA: F401

from . import config as _config

config = _config._get_config()
