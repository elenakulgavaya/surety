import copy

from collections.abc import Callable, Mapping, MutableSequence

from surety.process.common import is_callable_with_strict_args


def merge_with_updates(initial_dict, updates, extend_only=False,
                       merge_lists=False):
    """
    Creates copy of initial_dict with updates applied

    **Parameters**

    initial_dict : dictionary used as base for updates
    updates : dictionary with changes to be applied
    extend_only: boolean flag that prohibits to overwrite values, only add new

    **Returns**

    A copy of initial dict with all updates applied

    **Examples**

    initial_dict is None:
      >>> merge_with_updates(None, {2: 2})
      {2: 2}

    Add new value in dict:
      >>> merge_with_updates({1: 1}, {2: 2})
      {1: 1, 2: 2}

    Update value in dict:
      >>> merge_with_updates({1: 1, 2: 2}, {2: 'two', 3: 3} )
      {1: 1, 2: 'two', 3: 3}

    Update value in inner dict:
      >>> merge_with_updates({1: 1, 2: {21: 21}}, {2: {21: 'twenty-one'}})
      {1: 1, 2: {21: 'twenty-one'}}

    Override list:
      >>> merge_with_updates({1: [{2: 2, 3: 3}]}, {1: [{2: 'two'}]})
      {1: [{2: 'two'}]}

    Update value in list:
      >>> merge_with_updates(
      ...   {1: [{2: 2, 3: 3}]}, {1: [{2: 'two'}]},
      ...   merge_lists=True)
      {1: [{2: 'two', 3: 3}]}

    Update value in inner list:
      >>> merge_with_updates(
      ...   {1: {2: [{3: [{4: 4}]}]}},
      ...   {1: {2: [{3: [{4: 'four'}]}]}},
      ...   merge_lists=True)
      {1: {2: [{3: [{4: 'four'}]}]}}

    Extend dict:
      >>> merge_with_updates({1: 1}, {2: 2}, extend_only=True)
      {1: 1, 2: 2}

    Extend list:
      >>> merge_with_updates({1: [2]}, {1: [2, 3]}, merge_lists=True)
      {1: [2, 2, 3]}

    Extend list of dicts:
      >>> merge_with_updates({1: [{2: 2}]}, {1: [{3: 3}]}, merge_lists=True)
      {1: [{2: 2, 3: 3}]}

    Extend empty list with list of dicts:
      >>> merge_with_updates({1: []}, {1: [{2: 2}]}, merge_lists=True)
      {1: [{2: 2}]}

    Extend list of dicts with empty inner dict:
      >>> merge_with_updates({1: [{2: 2}]}, {1: [{}]}, merge_lists=True)
      {1: [{2: 2}, {}]}

    Extend inner dict:
      >>> merge_with_updates({1: 1, 2: {21: 21}}, {2: {22: 22}})
      {1: 1, 2: {21: 21, 22: 22}}

    Overwrite value with dict:
      >>> merge_with_updates({1: 1}, {1: {2: 2}})
      {1: {2: 2}}

    Do not modify initial dict:
      >>> initial_dict = {1: 1, 2: {21: 21}}
      >>> merge_with_updates(initial_dict, {1: 'one', 2: {21: 'two'}})
      {1: 'one', 2: {21: 'two'}}
      >>> print(initial_dict)
      {1: 1, 2: {21: 21}}

    Do not override value in extend mode:
      >>> merge_with_updates({1: 1}, {1: 'one'}, extend_only=True)
      Traceback (most recent call last):
          ...
      ValueError: Can not overwrite "1" value in extend mode

    Do not override inner value in extend mode:
      >>> merge_with_updates({1: {2: 2}}, {1: {2: 0}}, extend_only=True)
      Traceback (most recent call last):
          ...
      ValueError: Can not overwrite "2" value in extend mode

    Do not override list value in extend mode:
      >>> merge_with_updates(
      ...   {1: [{2: 2}]}, {1: [{2: 0}]}, merge_lists=True, extend_only=True)
      Traceback (most recent call last):
          ...
      ValueError: Can not overwrite "2" value in extend mode
    """
    initial_dict = initial_dict or {}
    initial_copy = copy.deepcopy(initial_dict)

    for key, value in updates.items():
        if isinstance(value, Mapping) and isinstance(initial_copy.get(key),
                                                     Mapping):
            initial_copy[key] = merge_with_updates(
                initial_copy.get(key, {}),
                value,
                extend_only=extend_only,
                merge_lists=merge_lists
            )
        elif merge_lists and isinstance(value, list) and isinstance(
                initial_copy.get(key), list):
            if len(initial_copy[key]) == 0 or not isinstance(
                    value[0], Mapping) or value[0] == {}:
                initial_copy[key].extend(value)
            else:
                initial_copy[key][0] = merge_with_updates(
                    initial_copy.get(key, [{}])[0],
                    value[0],
                    extend_only=extend_only,
                    merge_lists=merge_lists
                )
        else:
            if extend_only and key in initial_copy:
                raise ValueError(
                    f'Can not overwrite "{key}" value in extend mode'
                )

            initial_copy[key] = updates[key]

    return initial_copy


def dict_predicate(func=None, name=None):
    class DictPredicate:
        def __init__(self, callable_func):
            self.func = callable_func

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def __repr__(self):
            return name or self.func.__name__

    if func:
        return DictPredicate(func)

    return DictPredicate


def matches_pattern(initial_dict, pattern_dict):
    """
    Checks whether dict matches value/filter pattern

    **Parameters**

    initial_dict : dictionary to verify
    pattern_dict: dictionary pattern to apply for verification. Filter function
    is allowed as value: takes one actual arg and returns True or False.
    Decorate filter functions with @dict_predicate to add names on logging.

    **Returns**

    True/False if the dict matches pattern.

    **Examples**

    Full match:
      >>> matches_pattern({1: 1}, {1: 1})
      True

    Extra value in initial dict:
      >>> matches_pattern({1: 1, 2: 2}, {2: 2})
      True

    Extra value in pattern:
      >>> matches_pattern({1: 1}, {1: 1, 2: 2})
      False

    Inner dict doesn't match filter pattern:
      >>> matches_pattern({1: {2: 2}}, {1: {2: lambda x: x != 2}})
      False

    Inner dict matches filter pattern:
      >>> matches_pattern({1: {2: 2}}, {1: {2: lambda x: x == 2}})
      True
    """
    result = True

    for key, value in pattern_dict.items():
        if result is False or key not in initial_dict:
            return False

        if isinstance(value, Mapping):
            result = matches_pattern(initial_dict[key], value)
        elif is_callable_with_strict_args(value):
            result = value(initial_dict[key])
        else:
            result = value == initial_dict[key]

    return result


def apply_modifier(initial_dict, modifier):
    """
    Returns a copy of an initial dictionary with modified values.

    :param initial_dict: any dictionary to create a copy from and modify
    :param modifier: either a callable that modifies the dictionary or a
    dictionary that contains other modifiers under corresponding keys.
    :return: a copy of the dictionary
    :rtype: dict

    Examples:
      >>> apply_modifier({'a': 7}, lambda _: {})
      {}

      >>> apply_modifier({'b': 7}, {'b': float})
      {'b': 7.0}

      >>> apply_modifier({'c': {'x': 1}, 'd': 2}, {'c': {'x': float}})
      {'c': {'x': 1.0}, 'd': 2}

      >>> apply_modifier({'c': {'x': 1}}, {'d': float})
      {'c': {'x': 1}}

      >>> apply_modifier({'c': {'x': 1}}, {'c': lambda _: 'test'})
      {'c': 'test'}

      >>> apply_modifier({'c': [1, 2, 3]}, {'c': [float]})
      {'c': [1.0, 2.0, 3.0]}

      >>> apply_modifier({'c': []}, {'c': [float]})
      {'c': []}

      >>> apply_modifier(
      ...   {'c': [{'x': [1]}, {'y': 4}]}, {'c': [{'x': [float]}]})
      {'c': [{'x': [1.0]}, {'y': 4}]}

      >>> apply_modifier(
      ...   {'c': [{'x': [1], 'y': 2}]}, {'c': [{'x': [float], 'y': float}]})
      {'c': [{'x': [1.0], 'y': 2.0}]}

    """
    initial_copy = copy.deepcopy(initial_dict)

    if isinstance(modifier, Callable):
        return modifier(initial_copy)

    if isinstance(modifier, MutableSequence):
        if not modifier:
            raise ValueError('list modifier is empty')

        if not isinstance(initial_copy, MutableSequence):
            raise ValueError(
                f'cannot apply list modifier to {type(initial_copy)} type'
            )
        sub_modifier = modifier[0]

        return [apply_modifier(v, sub_modifier) for v in initial_copy]

    if not isinstance(modifier, Mapping):
        raise ValueError('modifier is not dictionary nor callable')

    for key, sub_modifier in modifier.items():
        if key not in initial_copy:
            continue

        initial_copy[key] = apply_modifier(initial_copy[key], sub_modifier)

    return initial_copy

# pylint: disable=line-too-long
def normalize(actual, expected, keys=None):
    """
    Applies same structure as expected, based on id for ordered structures.

    Examples:
      >>> normalize(['c', 'b', 'a'], ['b'])
      ['b', 'c', 'a']

      >>> normalize({'a': [1, 2, 5, 6], 'b': 0}, {'a': [1, 3, 6 ], 'b': None})
      {'a': [1, 6, 2, 5], 'b': 0}

      >>> normalize(
      ...   {'a': {'c': 'test', 'd': ['a', 1]}, 'b': 123},
      ...   {'a': {'d': ['b', 'c', 1]}})
      {'a': {'c': 'test', 'd': [1, 'a']}, 'b': 123}

      >>> normalize(
      ... {'a': [{'id': 1, 'val': 'test'}, {'id': 2, 'val': 'test2'}]},
      ... {'a': [{'id': 2}, {'id': 3}]})
      {'a': [{'id': 2, 'val': 'test2'}, {'id': 1, 'val': 'test'}]}

      >>> normalize(
      ...   {'a': [{'id': 1, 'val': 'test'}, {'id': 2, 'val': 'test2'}]},
      ...   {'a': [{'id': 4, 'val': 'test2'}, {'id': 5, 'val': 'v'}]},
      ...   keys=['fake', 'val'])
      {'a': [{'id': 2, 'val': 'test2'}, {'id': 1, 'val': 'test'}]}

      >>> normalize(
      ...   {'a': [
      ...       {'id': 'b1', 'b': [{'id': 2}, {'id': 1}]},
      ...       {'id': 'b0', 'b': [{'id': 3}, {'id': 4}]}
      ...   ]},
      ...   {'a': [
      ...       {'id': 'b0', 'b': [{'id': 4}]},
      ...       {'id': 'b1', 'b': [{'id': 1}, {'id': 2}]}
      ...   ]})
      {'a': [{'id': 'b0', 'b': [{'id': 4}, {'id': 3}]}, {'id': 'b1', 'b': [{'id': 1}, {'id': 2}]}]}

      >>> normalize(
      ...   [{
      ...       'attempt_number': 0,
      ...       'cost': 280.333,
      ...       'data_source_name':
      ...       '_all_datasources_',
      ...       'data_transferred_bytes': 9046,
      ...       'job_id': '6858248'
      ...   }, {
      ...       'attempt_number': 0,
      ...       'cost': 280.333,
      ...       'data_source_name': 'azure_blob',
      ...       'data_transferred_bytes': 9046,
      ...       'job_id': '6858248'
      ...   }],
      ...   [{
      ...       'attempt_number': 0,
      ...       'cost': 280.333,
      ...       'data_source_name': 'azure_blob',
      ...       'data_transferred_bytes': 9046,
      ...       'job_id': '6858248'
      ...   }, {
      ...       'attempt_number': 0,
      ...       'cost': 280.333,
      ...       'data_source_name': '_all_datasources_',
      ...       'data_transferred_bytes': 9046,
      ...       'job_id': '6858248'
      ...   }],
      ...   keys=['data_source_name', 'cost'])
      [{'attempt_number': 0, 'cost': 280.333, 'data_source_name': 'azure_blob', 'data_transferred_bytes': 9046, 'job_id': '6858248'}, {'attempt_number': 0, 'cost': 280.333, 'data_source_name': '_all_datasources_', 'data_transferred_bytes': 9046, 'job_id': '6858248'}]
    """
    # pylint: enable=line-too-long
    keys = keys or []

    def find_keys(element):
        if not isinstance(element, dict):
            return []

        result = []

        for available_key in keys:
            if available_key in element:
                result.append(available_key)

        return result or ['id']

    def get_index(tar, elem, el_keys=None):
        el_keys = el_keys or ['id']

        def get_combined_key(values_dict):
            return '--'.join(f'{k}::{values_dict.get(k)}' for k in el_keys)

        target = tar
        element = elem

        if isinstance(elem, dict):

            target = [get_combined_key(item) for item in tar]
            element = get_combined_key(elem)

        if element not in target:
            return len(target)

        return target.index(element)

    initial = copy.deepcopy(actual)

    if isinstance(initial, list) and expected is not None:
        element_keys = find_keys(initial[0]) if initial else None
        initial = sorted(
            initial,
            key=lambda x: get_index(expected, x, el_keys=element_keys)
        )
        if len(initial) == len(expected):
            for num, _ in enumerate(initial):
                initial[num] = normalize(
                    initial[num], expected[num], keys=keys
                )

    elif isinstance(initial, dict):
        for key, value in initial.items():
            if expected:
                initial[key] = normalize(value, expected.get(key), keys=keys)

    return initial
