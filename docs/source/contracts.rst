Contracts
=========

A contract is a Python class that defines the expected structure and semantics
of data. Contracts are explicit, reusable, and transport-agnostic — the same
contract can validate an API response, a database record, or a UI state.

Defining a Contract
-------------------

Inherit from ``Dictionary`` and declare fields as class attributes:

.. code-block:: python

   from surety import Dictionary, String, Int, Bool

   class WidgetContract(Dictionary):
       WidgetId = Int(name='widget_id')
       Name = String(name='name')
       Description = String(name='description', required=False)
       Deprecated = Bool(name='deprecated', required=False)

Each field's ``name`` parameter determines the key in the output dictionary.

Common Field Parameters
-----------------------

Every field type accepts these parameters:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``name``
     - ``None``
     - Key name in the output dictionary.
   * - ``required``
     - ``True``
     - Whether the field is included in partial generation mode.
   * - ``allow_none``
     - ``False``
     - Whether the field value can be ``None``.
   * - ``default``
     - ``None``
     - Static value or callable used instead of auto-generation.

Nested Contracts
----------------

Contracts can nest arbitrarily to model complex data structures:

.. code-block:: python

   from surety import Dictionary, String, Int, Array, Bool
   from surety.sdk.fakeable import Fakeable

   class AddressContract(Dictionary):
       Street = String(name='street', fake_as=Fakeable.StreetAddress)
       City = String(name='city')
       State = String(name='state')
       ZipCode = String(name='zip_code')

   class PaymentMethodContract(Dictionary):
       CardType = String(name='card_type', fake_as=Fakeable.CreditCardProvider)
       LastFour = String(name='last_four', min_len=4, max_len=4)
       IsDefault = Bool(name='is_default')

   class CustomerContract(Dictionary):
       CustomerId = Int(name='customer_id', min_val=1000, max_val=99999)
       Email = String(name='email')
       BillingAddress = AddressContract(name='billing_address')
       ShippingAddress = AddressContract(name='shipping_address')
       PaymentMethods = Array(PaymentMethodContract, name='payment_methods',
                              min_len=1, max_len=3)

.. code-block:: python

   customer = CustomerContract(is_full=True)
   print(customer.value)
   # {
   #     'customer_id': 48271,
   #     'email': 'margaret.jones@example.com',
   #     'billing_address': {
   #         'street': '742 Evergreen Terrace',
   #         'city': 'Springfield',
   #         'state': 'IL',
   #         'zip_code': '62704'
   #     },
   #     'shipping_address': { ... },
   #     'payment_methods': [
   #         {'card_type': 'Visa', 'last_four': '4242', 'is_default': True}
   #     ]
   # }

Array
-----

Wraps a field type to represent a list of elements:

.. code-block:: python

   from surety import Array, Dictionary, String, Int

   class TagContract(Dictionary):
       TagId = Int(name='tag_id')
       Label = String(name='label', max_len=30)

   class ArticleContract(Dictionary):
       Title = String(name='title')
       Tags = Array(TagContract, name='tags', min_len=1, max_len=5)

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``field``
     - (required)
     - The field type (class) for array elements.
   * - ``min_len``
     - ``1``
     - Minimum number of elements generated.
   * - ``max_len``
     - ``1``
     - Maximum number of elements generated.

Arrays support indexing, iteration, length, and appending:

.. code-block:: python

   article = ArticleContract()
   for tag in article.Tags:
       print(tag.Label.value)

   first_tag = article.Tags[0]
   print(len(article.Tags))

Set
---

Works like ``Array`` but produces a set of unique elements:

.. code-block:: python

   from surety import Set, String

   class PermissionSetContract(Dictionary):
       Roles = Set(String, name='roles', min_len=2, max_len=4)

Generation Modes
----------------

Full vs Partial
^^^^^^^^^^^^^^^

By default, ``Dictionary`` uses ``is_full=False`` — only **required** fields are
generated. Use ``is_full=True`` to include optional fields:

.. code-block:: python

   # Partial — only required fields
   partial = WidgetContract()
   print(partial.value)
   # {'widget_id': 7312, 'name': 'RxkPmW'}

   # Full — all fields including optional
   full = WidgetContract(is_full=True)
   print(full.value)
   # {'widget_id': 5094, 'name': 'aQdLnZ', 'description': 'Lorem ipsum', 'deprecated': False}

Nullable Fields
^^^^^^^^^^^^^^^

Fields with ``allow_none=True`` will not be generated in partial mode. In full
mode, they receive a value:

.. code-block:: python

   class NullableContract(Dictionary):
       Primary = String(name='primary')
       Secondary = String(name='secondary', allow_none=True)

   NullableContract().value           # {'primary': '...'}
   NullableContract(is_full=True).value  # {'primary': '...', 'secondary': '...'}

Default Values
^^^^^^^^^^^^^^

Provide a static value or a callable:

.. code-block:: python

   class ConfigContract(Dictionary):
       Version = Int(name='version', default=1)
       Region = String(name='region', default='us-east-1')
       RequestId = String(name='request_id', default=lambda: 'req-0001')

Accessing Values
----------------

.. code-block:: python

   contract = WidgetContract()
   contract.value       # Dict of generated fields only
   contract.full_value  # Dict of all fields, including None for ungenerated

Overriding Values
-----------------

Use ``with_values()`` to set specific fields while keeping the rest
auto-generated:

.. code-block:: python

   customer = CustomerContract().with_values({
       'customer_id': 1,
       'email': 'test@acme.org'
   })

For nested structures, pass nested dictionaries:

.. code-block:: python

   customer = CustomerContract().with_values({
       'billing_address': {'city': 'Portland', 'state': 'OR'}
   })

For array fields, pass a list:

.. code-block:: python

   article = ArticleContract().with_values({
       'tags': [
           {'tag_id': 10, 'label': 'python'},
           {'tag_id': 20, 'label': 'testing'}
       ]
   })

Regenerating
------------

Call ``generate()`` to regenerate all field values:

.. code-block:: python

   contract = CustomerContract()
   first_email = contract.Email.value

   contract.generate()
   second_email = contract.Email.value
   # first_email != second_email

Custom Fields
-------------

Create custom field types by subclassing ``Field`` and implementing
``generate_value()``:

.. code-block:: python

   import random
   from surety import Field

   class HexColor(Field):
       def generate_value(self):
           return '#' + ''.join(random.choices('0123456789abcdef', k=6))

   class VersionString(Field):
       def generate_value(self):
           return f'{random.randint(0, 9)}.{random.randint(0, 99)}.{random.randint(0, 999)}'

   class ThemeContract(Dictionary):
       PrimaryColor = HexColor(name='primary_color')
       ApiVersion = VersionString(name='api_version')
