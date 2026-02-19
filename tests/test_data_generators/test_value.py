from surety import Array
from tests.data import AllowedNone, Mix, Optional


def test_required_value():
    assert Mix().ReqBase.value


def test_required_embedded_field_value():
    assert Mix().ReqBase.StringField.value


def test_optional_no_value():
    assert Mix().OptBase.value is None


def test_optional_embedded_field_no_value():
    assert Mix().OptBase.IntField.value is None


def test_optional_value_in_full():
    assert Mix(is_full=True).OptBase.value


def test_optional_embedded_field_in_full():
    assert Mix(is_full=True).OptBase.IntField.value


def test_array_value():
    assert Mix().ReqTypeArray.value


def test_set_value():
    assert Mix().ReqTypeSet.value


def test_optional_array_no_value():
    assert Mix().OptBaseArray.value is None


def test_optional_set_no_value():
    assert Mix().OptTypeSet.value is None


def test_optional_array_in_full():
    assert Mix(is_full=True).OptBaseArray.value


def test_optional_set_in_full():
    assert Mix(is_full=True).OptTypeSet.value


def test_optional_field_in_array_no_value():
    assert Array(Optional)[0].OptString.value is None


def test_optional_field_in_array_value_in_full():
    assert Array(Optional, is_full=True)[0].OptString.value


def test_required_dict_with_optional_fields():
    assert Mix().ReqOptional.value == {}


def test_allownone_value_in_dict():
    assert AllowedNone().value == {
        AllowedNone.NoneString.name: None,
        AllowedNone.NoneInt.name: None,
    }
