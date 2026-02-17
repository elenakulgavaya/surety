from tests.data import Mix


mix = Mix()
mix_full = Mix(is_full=True)


def test_generated_dict_is_required():
    assert mix_full.ReqOptional.required is Mix.ReqOptional.required


def test_generated_embedded_dict_is_required():
    assert (Mix.OptOptional.OptString.required is
            mix.OptOptional.OptString.required)


def test_generated_embedded_optional_dict_is_required():
    assert Mix.OptBase.IntField.required is mix_full.OptBase.IntField.required


def test_generated_array_is_required():
    assert Mix.OptFullBaseArray.required is mix_full.OptFullBaseArray.required


def test_generated_embedded_array_dict_is_required():
    assert (Mix.OptBaseArray.field.StringField.required is
            mix_full.OptBaseArray[0].StringField.required)
