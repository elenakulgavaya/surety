import importlib
import sys

try:
    config = importlib.import_module("surety_config.config")
except ImportError:
    config = None  #pylint: disable=invalid-name


if config:
    sys.modules["surety.config"] = config
