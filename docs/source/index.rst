Surety
======

**Contract-driven testing for Python.**

Surety makes contract-based testing simple and readable.

Surety replaces scattered assertions with explicit **contracts** — Python
classes that define expected data structures, generate fake data, and validate
real responses deterministically.

Contracts are transport-agnostic: the same contract validates an HTTP API
response, a database record, or a UI state object.

.. code-block:: python

   from surety import Dictionary, String, Int

   class ProductContract(Dictionary):
       ProductId = Int(name='product_id', min_val=1, max_val=99999)
       Title = String(name='title', max_len=100)
       Sku = String(name='sku', max_len=12)

   product = ProductContract()
   print(product.value)
   # {'product_id': 4821, 'title': 'Ergonomic Steel Chair', 'sku': 'xK9mPq'}

Three Layers
------------

.. list-table::
   :widths: 30 30 40

   * - **Contracts**
     - ``surety``
     - Define expectations
   * - **Execution Layers**
     - ``surety-api``, ``surety-db``
     - Perform interactions
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
   db
   config

.. toctree::
   :caption: Reference
   :hidden:

   utilities
