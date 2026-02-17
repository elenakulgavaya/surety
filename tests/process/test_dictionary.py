import pytest

from surety.process.dictionary import apply_modifier, dict_predicate


def test_use_function_name_as_repr():
    @dict_predicate
    def filter_dict_function():
        pass

    assert repr(filter_dict_function) == 'filter_dict_function'


def test_use_custom_name_as_repr():
    @dict_predicate(name='test_filter')
    def filter_dict_function():
        pass

    assert repr(filter_dict_function) == 'test_filter'


def test_function_with_name_is_callable():
    @dict_predicate(name='test_f')
    def filter_dict_function():
        return True

    assert filter_dict_function() is True


def test_apply_none_modifier():
    with pytest.raises(ValueError,
                       match='modifier is not dictionary nor callable'):
        apply_modifier({}, None)


def test_apply_list_modifier_is_empty():
    with pytest.raises(ValueError,  match='list modifier is empty'):
        apply_modifier({}, [])


def test_apply_list_modifier_to_not_list():
    with pytest.raises(ValueError,  match=(
            "cannot apply list modifier to <class 'dict'> type")):
        apply_modifier({'a': 1}, ['test'])
