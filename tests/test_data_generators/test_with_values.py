import pytest

from surety import Set
from tests.data import (
    AllowedNone, Base, ComposeBase, Mix, Optional, TypeOne, TypeOneArray
)


def test_required_fields_with_values():
    new_value = 'my_new_value'
    entity = Base().with_values({Base.StringField.name: new_value})
    assert entity.StringField.value == new_value


def test_optional_field_with_values_generated():
    entity = Optional().with_values({Optional.OptString.name: 'test_value'})
    assert entity.OptString.generated


def test_optional_field_with_values_new_value():
    new_value = 'optional_string'
    entity = Optional().with_values({Optional.OptString.name: new_value})
    assert entity.OptString.value == new_value


def test_embedded_dict_with_values_dict_generated():
    entity = Mix().with_values({
        Mix.OptBase.name: {Base.StringField.name: 'test_string'},
    })
    assert entity.OptBase.generated


def test_embedded_dict_with_values_field_generated():
    entity = Mix().with_values({
        Mix.OptBase.name: {Base.StringField.name: 'test_val'},
    })
    assert entity.OptBase.StringField.generated



def test_embedded_dict_with_values_new_value():
    new_value = 'embedded_dict_string'
    entity = Mix().with_values({
        Mix.OptBase.name: {Base.StringField.name: new_value}
    })
    assert entity.OptBase.StringField.value == new_value


def test_embedded_dict_with_values_new_dictionary_value():
    new_value = 'new_dict_string'
    entity = Mix().with_values({
        Mix.OptBase.name: {Base.StringField.name: new_value}
    })
    assert entity.OptBase.value[Base.StringField.name] == new_value


def test_array_of_fields_with_values_is_generated():
    entity = Mix().with_values({
        Mix.OptTypeArray.name: ['random_str1', 'random_str2'],
    })
    assert entity.OptTypeArray.generated


def test_set_of_fields_with_values_is_generated():
    entity = Mix().with_values({
        Mix.OptTypeSet.name: {'random_str1', 'random_str2'},
    })
    assert entity.OptTypeSet.generated


def test_array_of_fields_with_values_value():
    new_values = ['str1', 'str2', 'str3']
    entity = Mix().with_values({Mix.OptTypeArray.name: new_values})
    assert entity.OptTypeArray.value == new_values


def test_set_of_fields_with_values_value():
    new_values = {'str1', 'str2', 'str3'}
    entity = Mix().with_values({Mix.OptTypeSet.name: new_values})
    assert entity.OptTypeSet.value == new_values


def test_array_of_fields_with_values_override_value():
    new_values = ['r_str1', 'r_str2', 'r_str3']
    entity = Mix().with_values({Mix.ReqTypeArray.name: new_values})
    assert entity.ReqTypeArray.value == new_values


def test_set_of_fields_with_values_override_value():
    new_values = {'r_str1', 'r_str2', 'r_str3'}
    entity = Mix().with_values({Mix.ReqTypeSet.name: new_values})
    assert entity.ReqTypeSet.value == new_values


def test_array_of_dicts_with_values_is_generated():
    entity = Mix().with_values({Mix.OptBaseArray.name: [
        {Base.StringField.name: 'randoms_name1'},
        {Base.StringField.name: 'randoms_name2'},
    ]})
    assert entity.OptBaseArray.generated


def test_array_of_dicts_with_value_is_generated():
    entity = Mix().with_values({Mix.OptBaseArray.name: [
        {Base.StringField.name: 'name1', Base.IntField.name: 1},
        {Base.StringField.name: 'name2', Base.IntField.name: 2},
    ]})
    assert entity.OptBaseArray.value == [
        {'string_field': 'name1', 'int_field': 1},
        {'string_field': 'name2', 'int_field': 2}
    ]


# --- classmethod tests (Base.with_values instead of Base().with_values) ---

def test_classmethod_generates_required_fields():
    entity = Base.with_values({})
    assert entity.StringField.generated
    assert entity.IntField.generated


def test_classmethod_uses_provided_value():
    new_value = 'provided_value'
    entity = Base.with_values({Base.StringField.name: new_value})
    assert entity.StringField.value == new_value


def test_classmethod_still_generates_non_provided_required_field():
    entity = Base.with_values({Base.StringField.name: 'provided'})
    assert entity.IntField.generated


def test_classmethod_is_full_false_does_not_generate_optional_fields():
    entity = Optional.with_values({})
    assert not entity.OptString.generated
    assert not entity.OptInt.generated


def test_classmethod_is_full_generates_optional_fields():
    entity = Optional.with_values({}, is_full=True)
    assert entity.OptString.generated
    assert entity.OptInt.generated


def test_classmethod_provided_value_overrides_generated():
    new_value = 'overridden'
    entity = Base.with_values({Base.StringField.name: new_value}, is_full=True)
    assert entity.StringField.value == new_value


def test_classmethod_nested_dict_uses_provided_value():
    new_value = 'nested_val'
    entity = ComposeBase.with_values({
        ComposeBase.FirstBase.name: {Base.StringField.name: new_value}
    })
    assert entity.FirstBase.StringField.value == new_value


def test_classmethod_nested_dict_generates_other_required_nested_fields():
    entity = ComposeBase.with_values({
        ComposeBase.FirstBase.name: {Base.StringField.name: 'val'}
    })
    assert entity.FirstBase.IntField.generated


def test_classmethod_nested_optional_dict_not_generated_when_not_full():
    entity = ComposeBase.with_values({})
    assert not entity.OptBase.generated


def test_classmethod_nested_optional_dict_generated_when_full():
    entity = ComposeBase.with_values({}, is_full=True)
    assert entity.OptBase.generated


def test_classmethod_nested_optional_dict_with_values_is_generated():
    entity = ComposeBase.with_values({
        ComposeBase.OptBase.name: {Base.StringField.name: 'val'}
    })
    assert entity.OptBase.generated


def test_classmethod_nested_optional_dict_required_field_generated():
    entity = ComposeBase.with_values({
        ComposeBase.OptBase.name: {Base.StringField.name: 'val'}
    })
    assert entity.OptBase.IntField.generated


def test_classmethod_nested_optional_dict_other_field_generated_when_full():
    entity = ComposeBase.with_values({
        ComposeBase.OptBase.name: {Base.StringField.name: 'val'}
    }, is_full=True)
    assert entity.OptBase.IntField.generated


def test_classmethod_array_value():
    new_values = ['str1', 'str2']
    entity = Mix.with_values({Mix.OptTypeArray.name: new_values})
    assert entity.OptTypeArray.value == new_values


def test_classmethod_allow_none_not_provided_field_value_is_none():
    entity = AllowedNone.with_values({AllowedNone.NoneString.name: 'test'})
    assert entity.NoneInt.value is None


def test_classmethod_nested_allow_none_dict_is_none_when_with_value():
    entity = Mix.with_values({Mix.NoneAllowedNone.name: {AllowedNone.NoneString.name: 'test'}})
    assert entity.NoneAllowedNone.value is {'none_int': None, 'none_str': 'test'}


def test_classmethod_nested_allow_none_dict_is_none_when_not_full():
    entity = Mix.with_values({Mix.ReqOptional.name: {Optional.OptString.name: 'test'}})
    assert entity.NoneAllowedNone.value is None


def test_none_value_in_dict_generates_field():
    entity = Base.with_values({Base.StringField.name: None})
    assert entity.StringField.generated


def test_none_value_in_dict_does_not_prevent_generation():
    entity = Base.with_values({Base.StringField.name: None, Base.IntField.name: 42})
    assert entity.StringField.generated
    assert entity.IntField.value == 42


def test_field_instance_as_value():
    entity = Base.with_values({Base.StringField.name: TypeOne(default='field_val')})
    assert entity.StringField.value == 'field_val'


def test_field_instances_in_array_values():
    new_values = [TypeOne(default='a'), TypeOne(default='b')]
    entity = Mix.with_values({Mix.ReqTypeArray.name: new_values})
    assert entity.ReqTypeArray.value == ['a', 'b']


def test_array_classmethod_with_values():
    result = TypeOneArray.with_values(['a', 'b'])
    assert result.value == ['a', 'b']


def test_set_instance_with_values_wraps_scalars():
    s = Set(TypeOne)
    s.with_values({'x', 'y'})
    assert s.value == {'x', 'y'}


def test_apply_values_with_string_key():
    entity = Base()
    entity.apply_values({Base.StringField.name: 'direct'})
    assert entity.StringField.value == 'direct'


def test_apply_values_with_field_instance_key():
    entity = Base()
    entity.apply_values({Base.StringField: 'by_field'})
    assert entity.StringField.value == 'by_field'


def test_apply_values_none_value_skips_field():
    entity = Base()
    original = entity.StringField.value
    entity.apply_values({Base.StringField.name: None})
    assert entity.StringField.value == original


def test_apply_values_field_with_none_value_skips():
    entity = Base()
    original = entity.StringField.value
    entity.apply_values({Base.StringField.name: TypeOne(name='dummy')})
    assert entity.StringField.value == original


def test_apply_values_dict_value_sets_nested():
    entity = ComposeBase()
    entity.apply_values({ComposeBase.FirstBase.name: {Base.StringField.name: 'nested'}})
    assert entity.FirstBase.StringField.value == 'nested'


def test_apply_values_unknown_key_raises():
    entity = Base()
    with pytest.raises(AttributeError):
        entity.apply_values({'nonexistent_field': 'value'})


def test_classmethod_unknown_key_raises():
    with pytest.raises(AttributeError):
        Base.with_values({'nonexistent_field': 'value'})
