from tests.data import Mix


def test_array_is_full_false():
    assert not Mix.OptBaseArray.field.is_full


def test_array_is_full_true():
    assert Mix.OptFullBaseArray.field.is_full
