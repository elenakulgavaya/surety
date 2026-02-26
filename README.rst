.. image:: https://raw.githubusercontent.com/elenakulgavaya/surety/main/docs/source/_static/surety.png
    :target: https://surety.readthedocs.io/en/latest/
    :alt: Surety
    :height: 120

------

.. image:: https://img.shields.io/pypi/v/surety.svg
    :target: https://pypi.org/project/surety/
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/surety.svg
    :target: https://pypi.org/project/surety/
    :alt: Python versions


.. image:: https://github.com/elenakulgavaya/surety/actions/workflows/test.yml/badge.svg
    :target: https://github.com/elenakulgavaya/surety/actions?query=workflow%3ATests+branch%3Amain++
    :alt: Tests

.. image:: https://readthedocs.org/projects/surety/badge/?version=latest
    :target: https://surety.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/l/surety.svg
    :target: https://github.com/elenakulgavaya/surety/blob/main/LICENSE
    :alt: License

------

Contract-driven testing for Python.

Surety makes contract-based testing simple and readable.

The ``surety`` framework replaces scattered assertions with explicit
**contracts** — Python classes that define expected data structures, generate
realistic test data, and validate real responses deterministically.


.. code-block:: python

   from surety import Dictionary, String, Int, Bool

   class CustomerContract(Dictionary):
       Id = Int(name='customer_id', min_val=1000, max_val=99999)
       Email = String(name='email')
       FirstName = String(name='first_name')
       Active = Bool(name='active')

   customer = CustomerContract()
   print(customer.value)
   # {'customer_id': 48271, 'email': 'jane.doe@example.com', 'first_name': 'Margaret', 'active': True}


Features
--------

- **Contract-first** — define expected behavior as reusable Python classes, not scattered assertions
- **Data generation** — auto-generate realistic test data using `Faker <https://faker.readthedocs.io/>`_ with 80+ providers
- **Transport-agnostic** — the same contract validates API responses, database records, and UI state
- **Structured diffs** — precise mismatch reporting with custom comparison rules (via ``surety-diff``)
- **API testing** — HTTP interaction, schema-based mocking, and request verification (via ``surety-api``)
- **Database testing** — PostgreSQL, MySQL, SQLite, and Cassandra support (via ``surety-db``)
- **Field types** — ``Bool``, ``Int``, ``Float``, ``Decimal``, ``String``, ``Uuid``, ``DateTime``, ``Enum``, ``Array``, and more
- **Extensible** — create custom field types, comparison rules, and execution adapters
- **Python 3.7+** compatible


Install
-------

.. code-block:: bash

   pip install surety

Optional extensions:

.. code-block:: bash

   pip install surety-diff      # Structured comparison engine
   pip install surety-api       # HTTP API interaction and mocking
   pip install surety-db        # Database interaction layer
   pip install surety-config    # YAML-based configuration


Quick Example
--------------

Define a contract, generate data, and validate:

.. code-block:: python

   from surety import Dictionary, String, Int, Array
   from surety.diff import compare

   # Define contracts
   class AddressContract(Dictionary):
       City = String(name='city')
       ZipCode = String(name='zip_code', fake_as='zipcode')

   class OrderContract(Dictionary):
       Id = Int(name='order_id')
       Status = String(name='status', default='pending')
       ShippingAddress = AddressContract(name='shipping_address')

   # Generate test data
   order = OrderContract()
   print(order.value)
   # {'order_id': 7312, 'status': 'pending', 'shipping_address': {'city': 'Portland', 'zip_code': '97201'}}

   # Validate against actual response
   compare(actual=api_response, expected=order.value)

Override specific values while keeping the rest auto-generated:

.. code-block:: python

   order = OrderContract().with_values({
       Order.Id.name: 1,
       Order.ShippingAddress.name: {AddressContract.City.name: 'Seattle'}
   })

Use comparison rules for dynamic fields:

.. code-block:: python

   from surety.diff import compare
   from surety.diff.rules import has_some_value, timestamp_equal_with_delta_3s

   compare(
       actual=response,
       expected=order.value,
       rules={
           Order.Id.name: has_some_value,
           Order.CreatedAt.name: timestamp_equal_with_delta_3s
       }
   )


Architecture
------------

Surety separates three concerns:

.. list-table::
   :widths: 25 25 50

   * - **Contracts**
     - ``surety``
     - Define expectations and generate test data
   * - **Execution**
     - ``surety-api``, ``surety-db``
     - Perform HTTP and database interactions
   * - **Validation**
     - ``surety-diff``
     - Compare actual data against contracts


Documentation
-------------

Full documentation: https://surety.readthedocs.io/


Issues
------

Report bugs and feature requests at the `issue tracker <https://github.com/elenakulgavaya/surety/issues>`_.


License
-------

MIT License. See `LICENSE <https://github.com/elenakulgavaya/surety/blob/main/LICENSE>`_ for details.

Copyright (c) 2026 Elena Kulgavaya.
