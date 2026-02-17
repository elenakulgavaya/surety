from tests.data import AllowedNone, ComposeOptional, Mix, Optional


def test_generate_field_is_generated():
    entity = Optional()
    entity.OptInt.generate()
    assert entity.OptInt.generated


def test_generate_field_value():
    entity = Optional()
    entity.OptInt.generate()
    assert entity.OptInt.value


def test_generate_field_not_affect_other_generated():
    entity = Optional()
    entity.OptInt.generate()
    assert entity.OptString.generated is False


def test_generated_field_not_affect_other_values():
    entity = Optional()
    entity.OptInt.generate()
    assert entity.OptString.value is None


def test_generate_embedded_field_dictionary_is_generated():
    entity = ComposeOptional()
    entity.OptionalOpt.OptString.generate()
    assert entity.OptionalOpt.generated


def test_generate_embedded_field_dictionary_value():
    entity = ComposeOptional()
    entity.OptionalOpt.OptString.generate()
    assert entity.OptionalOpt.value


def test_generate_embedded_field_is_generated():
    entity = ComposeOptional()
    entity.OptionalOpt.OptString.generate()
    assert entity.OptionalOpt.OptString.generated


def test_generate_embedded_field_value():
    entity = ComposeOptional()
    entity.OptionalOpt.OptString.generate()
    assert entity.OptionalOpt.OptString.value


def test_generate_embedded_field_not_affect_other_is_generated():
    entity = ComposeOptional()
    entity.OptionalOpt.OptString.generate()
    assert entity.OptionalOpt.OptInt.generated is False


def test_generate_embedded_field_not_affect_other_value():
    entity = ComposeOptional()
    entity.OptionalOpt.OptString.generate()
    assert entity.OptionalOpt.OptInt.value is None


def test_generate_dictionary_is_generated():
    entity = Mix()
    entity.OptBase.generate()
    assert entity.OptBase.generated


def test_generated_dictionary_value():
    entity = Mix()
    entity.OptBase.generate()
    assert entity.OptBase.value


def test_generate_optional_dictionary_is_generated():
    entity = Mix()
    entity.OptOptional.generate()
    assert entity.OptOptional.generated


def test_generate_optional_dictionary_value():
    entity = Mix()
    entity.OptOptional.generate()
    assert entity.OptOptional.value == {}


def test_generate_allow_none_value():
    entity = AllowedNone()
    entity.NoneString.generate()
    assert entity.NoneString.generated
