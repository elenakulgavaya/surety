import pytest

from surety.process.common import is_callable_with_strict_args


def test_arg_not_callable():
    assert is_callable_with_strict_args('test') is False


def test_single_arg_function():
    assert is_callable_with_strict_args(func=lambda x: x)


def test_multiple_args_function_match():
    assert is_callable_with_strict_args(func=lambda x, y: x + y, args_count=2)


def test_func_as_a_class_property():
    class Temp:
        @staticmethod
        def func(arg):
            return arg

    assert is_callable_with_strict_args(Temp)


def test_class_property_not_a_function():
    class Temp:
        func = None

    with pytest.raises(TypeError):
        is_callable_with_strict_args(Temp)


def test_arg_count_mismatch():
    with pytest.raises(TypeError):
        is_callable_with_strict_args(func=lambda: True)
