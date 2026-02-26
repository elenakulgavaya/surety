Processing Utilities
====================

The ``surety.process`` module provides utility functions for working with
dictionaries. These are part of the core ``surety`` package.

Merging Dictionaries
--------------------

``merge_with_updates`` creates a deep copy of a dictionary with updates applied:

.. code-block:: python

   from surety.process.dictionary import merge_with_updates

   base = {'db': {'host': 'localhost', 'port': 5432}, 'debug': False}
   overrides = {'db': {'port': 5433}, 'debug': True}

   result = merge_with_updates(base, overrides)
   # {'db': {'host': 'localhost', 'port': 5433}, 'debug': True}

Use ``extend_only=True`` to prevent overwriting existing values. Raises
``ValueError`` on conflict:

.. code-block:: python

   merge_with_updates(
       {'db': {'host': 'localhost'}},
       {'db': {'port': 5432}},
       extend_only=True
   )
   # {'db': {'host': 'localhost', 'port': 5432}}

Use ``merge_lists=True`` to merge list elements instead of replacing:

.. code-block:: python

   merge_with_updates(
       {'tags': [{'id': 1, 'name': 'alpha'}]},
       {'tags': [{'name': 'beta'}]},
       merge_lists=True
   )
   # {'tags': [{'id': 1, 'name': 'beta'}]}

Pattern Matching
----------------

``matches_pattern`` checks if a dictionary matches a value/filter pattern.
Pattern values can be exact values or callable predicates:

.. code-block:: python

   from surety.process.dictionary import matches_pattern, dict_predicate

   @dict_predicate(name='positive')
   def is_positive(value):
       return value > 0

   matches_pattern(
       {'quantity': 5, 'name': 'Widget'},
       {'quantity': is_positive}
   )
   # True

   matches_pattern(
       {'quantity': -1, 'name': 'Widget'},
       {'quantity': is_positive}
   )
   # False

Extra keys in the initial dictionary are allowed. Extra keys in the pattern
cause the match to fail:

.. code-block:: python

   matches_pattern({1: 1, 2: 2}, {2: 2})    # True — extra key 1 is fine
   matches_pattern({1: 1}, {1: 1, 2: 2})    # False — key 2 not in initial

Applying Modifiers
------------------

``apply_modifier`` transforms dictionary values using callables:

.. code-block:: python

   from surety.process.dictionary import apply_modifier

   data = {'price': 19, 'tags': [1, 2, 3]}

   # Convert price to float
   apply_modifier(data, {'price': float})
   # {'price': 19.0, 'tags': [1, 2, 3]}

   # Apply modifier to all list elements
   apply_modifier(data, {'tags': [float]})
   # {'price': 19, 'tags': [1.0, 2.0, 3.0]}

   # Use a callable for full transformation
   apply_modifier(data, lambda d: {**d, 'currency': 'USD'})
   # {'price': 19, 'tags': [1, 2, 3], 'currency': 'USD'}

Normalizing Order
-----------------

``normalize`` reorders lists in ``actual`` to match the order in ``expected``,
using ``id`` as the default key for matching dict elements:

.. code-block:: python

   from surety.process.dictionary import normalize

   actual = {
       'items': [
           {'id': 'b', 'val': 2},
           {'id': 'a', 'val': 1}
       ]
   }
   expected = {
       'items': [
           {'id': 'a'},
           {'id': 'b'}
       ]
   }

   normalize(actual, expected)
   # {'items': [{'id': 'a', 'val': 1}, {'id': 'b', 'val': 2}]}

Use the ``keys`` parameter when elements don't have an ``id`` field:

.. code-block:: python

   normalize(
       actual=[{'name': 'beta'}, {'name': 'alpha'}],
       expected=[{'name': 'alpha'}, {'name': 'beta'}],
       keys=['name']
   )
   # [{'name': 'alpha'}, {'name': 'beta'}]

Filtering Dictionaries
-----------------------

``filter_dict`` removes entries matching a value or predicate:

.. code-block:: python

   from surety.process.common import filter_dict

   # Filter by value — removes entries equal to the value
   filter_dict(0, {'a': 0, 'b': 42, 'c': 0})
   # {'b': 42}

   # Filter by predicate — keeps entries where predicate returns True
   filter_dict(lambda x: x > 10, {'a': 5, 'b': 42, 'c': 3})
   # {'b': 42}

Works recursively on nested dictionaries:

.. code-block:: python

   filter_dict(0, {'a': {'c': 0, 'd': 42}, 'b': 0})
   # {'a': {'d': 42}}

Excluding None Values
---------------------

``exclude_none_from_kwargs`` removes ``None`` entries from a dictionary:

.. code-block:: python

   from surety.process.common import exclude_none_from_kwargs

   exclude_none_from_kwargs({'a': None, 'b': 1234, 'c': None})
   # {'b': 1234}
