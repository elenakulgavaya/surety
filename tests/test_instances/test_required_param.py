from tests.data import Mix


def test_dict_is_required():
    assert Mix.ReqOptional.required


def test_embedded_dict_is_not_required():
    assert not Mix.OptOptional.OptString.required


def test_embedded_optional_dict_is_required():
    assert Mix.OptBase.IntField.required


def test_array_is_not_required():
    assert not Mix.OptFullBaseArray.required


def test_embedded_array_dict_is_required():
    assert Mix.OptBaseArray.field.StringField.required
