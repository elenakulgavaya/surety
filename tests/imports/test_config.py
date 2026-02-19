import sys
import types
import importlib


def test_config_module_is_registered(monkeypatch):
    fake_module = types.ModuleType('surety_config.config')
    monkeypatch.setitem(sys.modules, 'surety_config.config', fake_module)

    sys.modules.pop('surety.config', None)

    import surety #pylint: disable=import-outside-toplevel
    importlib.reload(surety)

    assert sys.modules['surety.config'] is fake_module


def test_config_module_not_registered_if_missing(monkeypatch):
    monkeypatch.delitem(sys.modules, "surety_config.config", raising=False)
    monkeypatch.delitem(sys.modules, "surety.config", raising=False)
    sys.modules.pop('surety', None)

    import surety #pylint: disable=import-outside-toplevel
    importlib.reload(surety)

    assert 'surety.config' not in sys.modules
