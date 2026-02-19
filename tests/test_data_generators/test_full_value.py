from surety import Array
from tests.data import Mix, Optional


def test_required_full_value():
    assert Mix().ReqBase.full_value


def test_required_embedded_field_full_value():
    assert Mix().ReqBase.StringField.full_value


def test_optional_no_full_value():
    assert Mix().OptBase.full_value is None


def test_optional_embedded_field_no_full_value():
    assert Mix().OptBase.IntField.full_value is None


def test_array_full_value():
    assert Mix().ReqTypeArray.full_value


def test_set_full_value():
    assert Mix().ReqTypeSet.full_value


def test_optional_array_no_full_value():
    assert Mix().OptBaseArray.full_value == []


def test_optional_set_no_full_value():
    assert Mix().OptTypeSet.full_value == []


def test_optional_field_in_array_no_full_value():
    assert Array(Optional)[0].OptString.full_value is None


def test_required_dict_with_optional_fields_full_value():
    assert Mix().ReqOptional.full_value == {
        Mix.ReqOptional.OptInt.name: None,
        Mix.ReqOptional.OptString.name: None,
    }
