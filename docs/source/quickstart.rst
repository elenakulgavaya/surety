Quick Start
===========

Define a Schema
-----------------

A schema is a Python class that inherits from ``Dictionary``. Fields are
declared as class attributes. Schemas define the shape of data — fields,
types, and constraints:

.. code-block:: python

   from surety import Dictionary, String, Int, Bool

   class Customer(Dictionary):
       Id = Int(name='customer_id')
       FirstName = String(name='first_name')
       LastName = String(name='last_name')
       Active = Bool(name='active')

Generate Test Data
------------------

Create an instance to auto-generate realistic fake data for every field:

.. code-block:: python

   customer = Customer()
   print(customer.value)
   # {'customer_id': 7312, 'first_name': 'Margaret', 'last_name': 'Williams', 'active': True}

Override specific values while keeping the rest generated:

.. code-block:: python

   customer = Customer().with_values({
       Customer.Id.name: 1,
       Customer.FirstName.name: 'Jane'
   })
   # customer_id is 1, first_name is 'Jane', last_name and active are auto-generated

Validate Data
-------------

Use ``surety-diff`` to compare actual data against the schema:

.. code-block:: python

   from surety.diff import compare

   expected = customer.value
   actual = {
       'customer_id': 1,
       'first_name': 'Jane',
       'last_name': 'Williams',
       'active': True
   }

   # Raises AssertionError with a structured diff if values differ
   compare(actual=actual, expected=expected)

Where to Go Next
-----------------

- :doc:`philosophy` — understand the design principles
- :doc:`contracts` — learn about schemas, contracts, nesting, and generation modes
- :doc:`field_types` — explore all available field types
- :doc:`diff` — comparison rules and validation
- :doc:`api` — API contracts and mocking
- :doc:`ui` — browser-based UI testing
- :doc:`db` — database testing
