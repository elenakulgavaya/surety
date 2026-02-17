from surety.sdk.array import Array
from tests.data import Base, ComposeBase, Mix, Optional, TypeOne


def test_field_generated():
    assert TypeOne().generated


def test_embedded_field_generated():
    assert Base().IntField.generated


def test_optional_field_not_generated():
    assert not Optional().OptString.generated


def test_optional_field_generated_in_full():
    assert Optional(is_full=True).OptString.generated


def test_dict_generated():
    assert ComposeBase().generated


def test_embedded_dict_generated():
    assert ComposeBase().FirstBase.generated


def test_embedded_optional_dict_not_generated():
    assert not ComposeBase().OptBase.generated


def test_embedded_optional_dict_generated_in_full():
    assert ComposeBase(is_full=True).OptBase.generated


def test_array_generated():
    assert Array(Base).generated


def test_array_dict_generated():
    assert Array(Base)[0].generated


def test_array_embedded_field_generated():
    assert Array(Base)[0].StringField.generated


def test_array_optional_not_generated():
    assert not Array(ComposeBase)[0].OptBase.generated


def test_array_optional_generated_in_full():
    assert Array(ComposeBase, is_full=True)[0].OptBase.generated


def test_optional_array_not_generated():
    assert not Mix().OptFullBaseArray.generated


def test_optional_array_generated_in_full():
    assert Mix(is_full=True).OptFullBaseArray.generated


def test_optional_allownone_not_generated():
    assert not Mix().NotNoneAllowedNone.OptNoneInt.generated


def test_optional_allownone_generated_in_full():
    assert Mix(is_full=True).NotNoneAllowedNone.OptNoneInt.generated
