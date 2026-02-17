from tests.data import Base, ComposeBase, Mix


def test_field_not_generated():
    assert not Base.StringField.generated


def test_embedded_dict_not_generated():
    assert not ComposeBase.FirstBase.generated


def test_embedded_dict_field_not_generated():
    assert not ComposeBase.FirstBase.IntField.generated


def test_array_not_generated():
    assert not Mix.ReqFullBaseArray.generated
