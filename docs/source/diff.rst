Comparison and Validation (surety-diff)
=======================================

The ``surety-diff`` extension provides structured comparison between expected
and actual data.

.. code-block:: bash

   pip install surety-diff

Basic Comparison
----------------

``compare`` checks actual data against expected and raises ``AssertionError``
with a structured diff on mismatch:

.. code-block:: python

   from surety.diff import compare

   compare(
       actual={'item_id': 42, 'name': 'Widget', 'price': 19.99},
       expected={'item_id': 42, 'name': 'Widget', 'price': 19.99}
   )
   # Passes silently

   compare(
       actual={'item_id': 42, 'name': 'Gadget', 'price': 19.99},
       expected={'item_id': 42, 'name': 'Widget', 'price': 19.99}
   )
   # Raises AssertionError with detailed diff

Using Diff Directly
-------------------

The ``Diff`` class can be used for inspection without raising:

.. code-block:: python

   from surety.diff import Diff

   result = Diff(
       expected={'item_id': 42, 'name': 'Widget'},
       actual={'item_id': 42, 'name': 'Gadget'}
   )
   if result:
       print("Differences found:", result)

Diff reports these change types:

- ``TypeChanged`` — value type differs
- ``ValueChanged`` — value differs
- ``DictItemAdded`` — unexpected key present
- ``DictItemRemoved`` — expected key missing
- ``IterableItemAdded`` — extra element in list
- ``IterableItemRemoved`` — missing element in list
- ``RulesViolated`` — comparison rule returned ``False``
- ``RulesUnapplied`` — rule defined but not matched

Comparison Rules
----------------

Rules define custom matching logic for specific fields. A rule is a callable
that takes two arguments (expected, actual) and returns ``True`` if they match.

.. code-block:: python

   from surety.diff import compare, compare_rule

   @compare_rule(name='within_tolerance')
   def within_tolerance(expected, actual):
       return abs(expected - actual) < 0.01

   compare(
       actual={'amount': 99.994},
       expected={'amount': 99.99},
       rules={'amount': within_tolerance}
   )

Rules are passed as a dictionary mapping field names to rule functions:

.. code-block:: python

   compare(
       actual=response_data,
       expected=contract.value,
       rules={
           'order_id': has_some_value,
           'created_at': timestamp_equal_with_delta_3s,
           'total': within_tolerance
       }
   )

Built-in Rules
--------------

Import from ``surety.diff.rules``:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Rule
     - Description
   * - ``has_some_value``
     - Both values are not ``None``.
   * - ``has_new_value``
     - Values are different (changed).
   * - ``is_valid_uuid``
     - Both values are valid UUID format.
   * - ``sorted_lists_equal``
     - Lists contain the same elements regardless of order.
   * - ``equal_with_accuracy_4``
     - Floats match to 4 decimal places.
   * - ``timestamp_equal_with_delta_3s``
     - Timestamps within 3-second tolerance.
   * - ``timestamp_equal_with_delta_5s``
     - Timestamps within 5-second tolerance.
   * - ``timestamp_equal_with_delta_10s``
     - Timestamps within 10-second tolerance.
   * - ``dates_equal_with_delta_3s``
     - Dates within 3-second tolerance.

Example with built-in rules:

.. code-block:: python

   from surety.diff import compare
   from surety.diff.rules import is_valid_uuid, timestamp_equal_with_delta_3s

   compare(
       actual={
           'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
           'created_at': '2025-03-15T10:30:01Z'
       },
       expected={
           'id': '11111111-2222-3333-4444-555555555555',
           'created_at': '2025-03-15T10:30:03Z'
       },
       rules={
           'id': is_valid_uuid,
           'created_at': timestamp_equal_with_delta_3s
       }
   )

Forbidding Unapplied Rules
---------------------------

By default, ``compare`` raises an error if a rule is defined for a field that
doesn't exist in the data (``forbid_unapplied_rules=True``). Set it to
``False`` to allow unused rules:

.. code-block:: python

   compare(
       actual={'name': 'Widget'},
       expected={'name': 'Widget'},
       rules={'missing_field': has_some_value},
       forbid_unapplied_rules=False
   )
