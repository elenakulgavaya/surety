from tests.data import Mix


def test_dict_name():
    assert Mix.ReqBase.name == 'req_base'


def test_embedded_dict_name():
    assert Mix.ReqOptional.OptString.name == 'opt_string'


def test_array_name():
    assert Mix.OptBaseArray.name == 'opt_base_array'


def test_embedded_array_dict_name():
    assert Mix.OptBaseArray.field.StringField.name == 'string_field'
