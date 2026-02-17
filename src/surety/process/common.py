import inspect

from collections.abc import Mapping


def filter_dict(function_or_value, dict_to_filter):
    """
    Filter by value
      >>> filter_dict(123, {'a': 123, 'b': 1234})
      {'b': 1234}

    Filter by value not applicable
      >>> filter_dict(123, {'a': 1234, 'b': 5123})
      {'a': 1234, 'b': 5123}

    Embedded filter by value
      >>> filter_dict(123, {'a': {'c': 123}, 'b': 1234})
      {'b': 1234}

    Embedded with extra by value
      >>> filter_dict(123, {'a': {'c': 123, 'd': 432}, 'b': 1234})
      {'a': {'d': 432}, 'b': 1234}

    Embedded mixed filter
      >>> filter_dict(123, {'a': {'c': 123, 'd': 432}, 'b': 123, 'e': 'test'})
      {'a': {'d': 432}, 'e': 'test'}

    Filter by callable
      >>> filter_dict(lambda x: x % 2 == 0, {'a': 532, 'b': 891})
      {'a': 532}

    Filter by callable not applicable
      >>> filter_dict(lambda x: x % 2 == 0, {'a': 538, 'b': 8})
      {'a': 538, 'b': 8}

    Embedded filter by callable
      >>> filter_dict(lambda x: bool(x), {'a': {'c': False}, 'b': 'test'})
      {'b': 'test'}

    Embedded with extra by callable
      >>> filter_dict(
      ...   lambda x: 'a' in x, {'a': {'c': 'ba', 'd': 'tt'}, 'b': 'd'})
      {'a': {'c': 'ba'}}

    Embedded mixed filter
      >>> filter_dict(
      ...   lambda x: bool(x), {'a': {'c': True, 'd': 0}, 'b': 'test', 'e': []}
      ...   )
      {'a': {'c': True}, 'b': 'test'}

    """
    func = function_or_value

    if not callable(function_or_value):
        def new_func(value):
            return value != function_or_value

        func = new_func

    result = {}

    for key, value in dict_to_filter.items():
        if isinstance(value, Mapping):
            value = filter_dict(func, value)

            if value:
                result[key] = value

        elif func(value):
            result[key] = value

    return result


def exclude_none_from_kwargs(kwargs):
    """
    Remove single None value
      >>> exclude_none_from_kwargs({'a': None, 'b': 1234})
      {'b': 1234}

    Remove multiple None value
      >>> exclude_none_from_kwargs({'a': None, 'b': 1234, 'c': None})
      {'b': 1234}

    Remove all None values
      >>> exclude_none_from_kwargs({'a': None, 'c': None})
      {}

    Do nothing when there is no None value
      >>> exclude_none_from_kwargs({'a': 123, 'b': 1234})
      {'a': 123, 'b': 1234}
    """
    return {k: v for k, v in kwargs.items() if v is not None}


def is_callable_with_strict_args(func, args_count=1):
    if not callable(func):
        return False

    if hasattr(func, 'func'):
        func = func.func

    if not inspect.isfunction(func):
        raise TypeError(f'Expected function, got {type(func)}')

    argspec = inspect.getfullargspec(func)

    if argspec.varkw is None and len(argspec.args) == args_count:
        return True

    raise TypeError(f'Expected callable with {args_count} args. '
                    f'Got: "{func.__name__}" func with {argspec}')
