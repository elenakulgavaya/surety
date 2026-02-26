Quick Start
===========

Define a Contract
-----------------

A contract is a Python class that inherits from ``Dictionary``. Fields are
declared as class attributes:

.. code-block:: python

   from surety import Dictionary, String, Int, Bool

   class CustomerContract(Dictionary):
       Id = Int(name='customer_id')
       FirstName = String(name='first_name')
       LastName = String(name='last_name')
       Active = Bool(name='active')

Generate Test Data
------------------

Create an instance to auto-generate realistic fake data for every field:

.. code-block:: python

   customer = CustomerContract()
   print(customer.value)
   # {'customer_id': 7312, 'first_name': 'Margaret', 'last_name': 'Williams', 'active': True}

Override specific values while keeping the rest generated:

.. code-block:: python

   customer = CustomerContract().with_values({
       CustomerContract.Id.name: 1,
       CustomerContract.FirstName.name: 'Jane'
   })
   # customer_id is 1, first_name is 'Jane', last_name and active are auto-generated

Validate Data
-------------

Use ``surety-diff`` to compare actual data against the contract:

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
- :doc:`contracts` — learn about contracts, nesting, and generation modes
- :doc:`field_types` — explore all available field types
- :doc:`diff` — comparison rules and validation
- :doc:`api` — API testing and mocking
- :doc:`db` — database testing
