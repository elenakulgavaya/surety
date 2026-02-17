from tests.data import Base, ComposeBase, Mix


def test_field_no_value():
    assert Base.StringField.value is None


def test_embedded_dict_no_value():
    assert ComposeBase.FirstBase.value is None


def test_embedded_dict_field_no_value():
    assert ComposeBase.FirstBase.IntField.value is None


def test_array_no_value():
    assert Mix.ReqFullBaseArray.value is None
