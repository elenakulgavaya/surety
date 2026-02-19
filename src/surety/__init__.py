import importlib
import sys

try:
    config = importlib.import_module('surety_config.config')
except ImportError:
    config = None  #pylint: disable=invalid-name


if config:
    sys.modules['surety.config'] = config


try:
    diff = importlib.import_module('surety_diff')
except ImportError:
    diff = None #pylint: disable=invalid-name

if diff:
    sys.modules['surety.diff'] = diff
