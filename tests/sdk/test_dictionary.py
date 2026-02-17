import json

import pytest

from surety.sdk import Array, Dictionary, String


def test_dictionary_no_generate_value():
    assert Dictionary().generate_value() is None


def test_dictionary_with_values_with_field():
    class TempDict(Dictionary):
        First = String(name='first')
        Second = String(name='second')

    temp_dict = TempDict().with_values({
        TempDict.First: 'first_val',
        TempDict.Second: 'second_val'
    })
    assert temp_dict.value == {'first': 'first_val', 'second': 'second_val'}


def test_dictionary_with_values_no_field():
    class TempDict(Dictionary):
        First = String(name='first')

    with pytest.raises(AttributeError, match='No attribute with name second'):
        TempDict().with_values({'second': 'second_val'})


def test_dictionary_with_values_skip_nones():
    class TempDict(Dictionary):
        First = String(name='first', default='First')
        Second = String(name='second')

    temp_dict = TempDict().with_values({
        TempDict.First.name: None,
        TempDict.Second.name: 'second_val'
    })
    assert temp_dict.value == {'first': 'First', 'second': 'second_val'}


def test_dictionary_with_values_set_to_field():
    class TempDict(Dictionary):
        First = String(name='first')

    temp_dict = TempDict().with_values({
        TempDict.First.name: String(default='test'),
    })
    assert temp_dict.value == {'first': 'test'}


def test_dictionary_set_with_json():
    class TempDict(Dictionary):
        First = String(name='first')

    class OuterDict(Dictionary):
        Dict = TempDict(name='dict')

    outer_dict = OuterDict().with_values({
        OuterDict.Dict.name: json.dumps({TempDict.First.name: 'test'})
    })
    assert outer_dict.value == {'dict': {'first': 'test'}}


def test_dictionary_set_with_bytes():
    class TempDict(Dictionary):
        First = String(name='first')

    class OuterDict(Dictionary):
        Dict = TempDict(name='dict')

    outer_dict = OuterDict().with_values({
        OuterDict.Dict.name: json.dumps({
            TempDict.First.name: 'test1'
        }).encode('utf-8')
    })
    assert outer_dict.value == {'dict': {'first': 'test1'}}


def test_dictionary_set_with_string():
    class TempDict(Dictionary):
        First = String(name='first')

    class OuterDict(Dictionary):
        Dict = TempDict(name='dict')

    with pytest.raises(AttributeError, match='Assigning entity to primitive'):
        OuterDict().with_values({OuterDict.Dict.name: 'test'})


def test_dictionary_of_arrays():
    class TempDict(Dictionary):
        Array = Array(String, name='arr')

    temp_dict = TempDict().with_values({
        TempDict.Array.name: [
            String(default='test'),
            String(default='test2')
        ]
    })
    assert temp_dict.value == {'arr': ['test', 'test2']}
