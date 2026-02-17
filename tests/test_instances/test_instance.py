from tests.data import Base, ComposeBase, ComposeOptional, Mix, Optional


def test_field():
    assert id(Base.StringField) != id(Optional.OptString)


def test_required_dict():
    assert id(ComposeBase.FirstBase) != id(ComposeBase.SecondBase)


def test_optional_dict():
    assert id(ComposeOptional.FirstOpt) != id(ComposeOptional.OptionalOpt)


def test_embedded():
    assert id(Mix.ReqBase) != id(ComposeBase.FirstBase)


def test_field_array():
    assert id(Mix.OptTypeArray) != id(Mix.OptBaseArray)


def test_field_array_generator():
    assert id(Mix.OptTypeArray.field) != id(Mix.OptBaseArray.field)
