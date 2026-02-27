Field Types
===========

Surety provides built-in field types for common data. All types inherit from
``Field`` and are imported from the top-level ``surety`` package. Use these
types to define schemas (``Dictionary`` subclasses).

Bool
----

Generates a random boolean value.

.. code-block:: python

   from surety import Bool

   class FeatureFlag(Dictionary):
       Enabled = Bool(name='enabled')
       Visible = Bool(name='visible')

Int
---

Generates a random integer within configurable bounds.

.. code-block:: python

   from surety import Int

   class Pagination(Dictionary):
       Page = Int(name='page', min_val=1, max_val=500)
       PerPage = Int(name='per_page', min_val=10, max_val=100)

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``min_val``
     - ``0``
     - Minimum value (inclusive).
   * - ``max_val``
     - ``9999``
     - Maximum value (inclusive).

Float
-----

Generates a random float with control over integer and fractional digit lengths.

.. code-block:: python

   from surety import Float

   class Measurement(Dictionary):
       Temperature = Float(name='temperature', i_len=2, f_len=1,
                           min_val=-40, max_val=60)
       WeightKg = Float(name='weight_kg', f_len=3, positive=True)

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``i_len``
     - ``None``
     - Max digits in the integer part.
   * - ``f_len``
     - ``None``
     - Max digits in the fractional part.
   * - ``min_val``
     - ``None``
     - Minimum value.
   * - ``max_val``
     - ``None``
     - Maximum value.
   * - ``positive``
     - ``None``
     - If ``True``, only positive values are generated.

Decimal and StringDecimal
-------------------------

``Decimal`` works like ``Float`` but returns a ``decimal.Decimal`` value — ideal
for money or precision-sensitive fields.

``StringDecimal`` formats the decimal as a string with fixed fractional digits
(e.g. ``"14.50"``).

.. code-block:: python

   from surety import Decimal, StringDecimal

   class InvoiceLine(Dictionary):
       Amount = Decimal(name='amount', i_len=4, f_len=2, positive=True)
       FormattedAmount = StringDecimal(name='formatted_amount', f_len=2)

``Decimal`` provides a static helper to wrap existing values:

.. code-block:: python

   Field = Decimal.from_value("29.95")
   print(field.value)  # Decimal('29.95')

String
------

Generates a random string. When the field ``name`` matches a Faker provider
method (e.g. ``email``, ``city``, ``phone_number``), realistic data is produced
automatically.

.. code-block:: python

   from surety import String

   class Contact(Dictionary):
       Email = String(name='email')              # Faker-generated email
       City = String(name='city')                # Faker-generated city
       Nickname = String(name='nickname', min_len=3, max_len=20)

Use ``fake_as`` to explicitly select a Faker provider regardless of the field
name:

.. code-block:: python

   class Profile(Dictionary):
       Handle = String(name='handle', fake_as='user_name')
       Bio = String(name='bio', fake_as='sentence', max_len=200)

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``min_len``
     - ``1``
     - Minimum string length.
   * - ``max_len``
     - ``None``
     - Maximum string length (truncated if exceeded).
   * - ``fake_as``
     - ``None``
     - Faker provider method name. Falls back to ``name`` if not set.

Uuid
----

Generates a UUID v4 string.

.. code-block:: python

   from surety import Uuid

   class Session(Dictionary):
       SessionId = Uuid(name='session_id')
       TraceId = Uuid(name='trace_id')

DateTime
--------

Generates a random UTC datetime. The output format is configurable.

.. code-block:: python

   from surety import DateTime
   from surety.sdk.dates import Pattern

   class Event(Dictionary):
       CreatedAt = DateTime(name='created_at')
       DateOnly = DateTime(name='date_only', date_format=Pattern.DATE)

Available format patterns:

.. code-block:: python

   Pattern.DATE                                # '%Y-%m-%d'
   Pattern.TIME                                # '%H:%M:%S'
   Pattern.DATETIME                            # '%Y-%m-%d %H:%M:%S'
   Pattern.DATETIME_DELIM_T                    # '%Y-%m-%dT%H:%M:%S'
   Pattern.DATETIME_DELIM_T_WITH_ZONE          # '%Y-%m-%dT%H:%M:%SZ'
   Pattern.DATETIME_DELIM_T_WITH_ZONE_PRECISED # '%Y-%m-%dT%H:%M:%S.%fZ'

DateTime fields support timezone conversion:

.. code-block:: python

   event = Event()
   est_value = event.CreatedAt.to_format(
       Pattern.DATETIME_DELIM_T_WITH_ZONE, new_tz='US/Eastern'
   )

Raw
---

Generates an unstructured dictionary of random string key-value pairs. Useful
for metadata or freeform fields.

.. code-block:: python

   from surety import Raw

   class Audit(Dictionary):
       Metadata = Raw(name='metadata')

Calling ``with_values`` on a ``Raw`` field that already has a value **merges**
the new values into the existing dictionary rather than replacing it.

Enum
----

Subclass ``Enum`` and define class-level attributes for each allowed value:

.. code-block:: python

   from surety import Enum

   class OrderStatus(Enum):
       Pending = 'pending'
       Confirmed = 'confirmed'
       Shipped = 'shipped'
       Delivered = 'delivered'
       Cancelled = 'cancelled'

   class Order(Dictionary):
       Status = OrderStatus(name='status')

   # Exclude specific values during generation
   class ActiveOrder(Dictionary):
       Status = OrderStatus(name='status', exclude=(OrderStatus.Cancelled,))

Use ``to_list()`` to get all possible values:

.. code-block:: python

   OrderStatus.to_list()
   # ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

   OrderStatus.to_list(exclude=('OrderStatus.Cancelled',))
   # ['pending', 'confirmed', 'shipped', 'delivered']

Faker Providers
---------------

The ``String`` field auto-detects Faker providers by ``name`` or ``fake_as``.
Common providers:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Provider
     - Example Output
   * - ``name``
     - ``'Margaret Johnson'``
   * - ``first_name``
     - ``'Elena'``
   * - ``last_name``
     - ``'Williams'``
   * - ``email``
     - ``'j.smith@example.com'``
   * - ``company_email``
     - ``'mwilson@acme.org'``
   * - ``phone_number``
     - ``'+1-555-0123'``
   * - ``address``
     - ``'456 Oak Avenue, Suite 7'``
   * - ``city``
     - ``'Portland'``
   * - ``state``
     - ``'Oregon'``
   * - ``state_abbr``
     - ``'OR'``
   * - ``zipcode``
     - ``'97201'``
   * - ``country``
     - ``'United States'``
   * - ``url``
     - ``'https://example.com'``
   * - ``user_name``
     - ``'jsmith42'``
   * - ``credit_card_number``
     - ``'4111111111111111'``
   * - ``sentence``
     - ``'The quick brown fox jumps.'``
   * - ``date``
     - ``'2024-08-15'``

See the full list of 80+ providers in ``surety.sdk.fakeable.Fakeable``.
