from tests.data import Mix


def test_dict_is_not_allowed_none():
    assert not Mix.NotNoneAllowedNone.allow_none


def test_embedded_dict_is_allowed_none():
    assert Mix.NoneAllowedNone.allow_none


def test_embedded_in_dict_is_allowed_none():
    assert Mix.NoneAllowedNone.NoneString.allow_none


def test_array_none_is_allowed():
    assert Mix.NoneTypeArray.allow_none


def test_embedded_array_none_is_allowed():
    assert Mix.NoneTypeArray.field.NoneInt.allow_none
