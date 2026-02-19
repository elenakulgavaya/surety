import sys
import types
import importlib


def test_config_module_is_registered(monkeypatch):
    fake_module = types.ModuleType('surety_diff')
    monkeypatch.setitem(sys.modules, 'surety_diff', fake_module)

    sys.modules.pop('surety.diff', None)

    import surety #pylint: disable=import-outside-toplevel
    importlib.reload(surety)

    assert sys.modules['surety.diff'] is fake_module


def test_config_module_not_registered_if_missing(monkeypatch):
    monkeypatch.delitem(sys.modules, "surety_diff", raising=False)
    monkeypatch.delitem(sys.modules, "surety.diff", raising=False)
    sys.modules.pop('surety', None)

    import surety #pylint: disable=import-outside-toplevel
    importlib.reload(surety)

    assert 'surety.diff' not in sys.modules
