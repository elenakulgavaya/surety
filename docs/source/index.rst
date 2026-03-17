.. meta::
   :description: Surety is a Python contract-driven testing framework. Define schemas as Python classes, generate realistic test data, and validate API, database, and UI interactions deterministically.
   :keywords: python testing, contract testing, contract-driven testing, test automation, schema validation, api testing, test data generation, surety
   :google-site-verification: kkzPK605few1TEm02D81pw_QzbuKvXapr7pXLks8r7k

Surety — Contract-Driven Testing Framework for Python
======================================================

**Contract-driven testing for Python.**

Surety makes contract-based testing simple and readable.

Surety replaces scattered assertions with explicit **schemas** and
**contracts**. Schemas are Python classes that define expected data structures,
generate fake data, and validate real responses deterministically. Contracts
bind schemas to communication semantics — an API endpoint, a database table,
or an event name.

Schemas are transport-agnostic: the same schema validates an HTTP API
response, a database record, or a UI state object.

.. code-block:: python

   from surety import Dictionary, String, Int

   class Product(Dictionary):
       ProductId = Int(name='product_id', min_val=1, max_val=99999)
       Title = String(name='title', max_len=100)
       Sku = String(name='sku', max_len=12)

   product = Product()
   print(product.value)
   # {'product_id': 4821, 'title': 'Ergonomic Steel Chair', 'sku': 'xK9mPq'}

Three Layers
------------

.. list-table::
   :widths: 30 30 40

   * - **Schemas**
     - ``surety``
     - Define data structures and generate test data
   * - **Contracts & Execution**
     - ``surety-api``, ``surety-db``, ``surety-ui``
     - Bind schemas to endpoints, tables, and pages; perform interactions
   * - **Diff Engine**
     - ``surety-diff``
     - Verify interactions

.. toctree::
   :caption: Getting Started
   :hidden:

   installation
   quickstart

.. toctree::
   :caption: Core
   :hidden:

   philosophy
   contracts
   field_types

.. toctree::
   :caption: Extensions
   :hidden:

   diff
   api
   ui
   db
   config

.. toctree::
   :caption: Reference
   :hidden:

   utilities
