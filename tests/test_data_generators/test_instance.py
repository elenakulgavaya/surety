from tests.data import Base, ComposeBase, Mix


base = Base()
compose_base = ComposeBase()
mix = Mix()
mix_full = Mix(is_full=True)


def test_generated_field():
    assert id(base.StringField.value) != id(
        compose_base.FirstBase.StringField.value)


def test_generated_embedded_field():
    assert id(base.StringField.value) != id(
        compose_base.FirstBase.StringField.value)


def test_generated_array():
    assert mix.ReqBaseArray.value != mix_full.ReqFullBaseArray.value


def test_array_contract():
    assert id(mix.ReqTypeArray.field.value) != id(mix.ReqTypeArray[0].value)


def test_set_contract():
    assert id(mix.ReqTypeSet.field.value) != id(mix.ReqTypeSet[0].value)
