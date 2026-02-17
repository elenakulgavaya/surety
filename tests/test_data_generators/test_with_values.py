from tests.data import Base, Mix, Optional


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


def test_embedded_dict_with_values_field_not_affect_other_generated():
    entity = Mix().with_values({
        Mix.OptBase.name: {Base.StringField.name: 'value'},
    })
    assert not entity.OptBase.IntField.generated


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
    assert entity.OptBase.value == {Base.StringField.name: new_value}


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
