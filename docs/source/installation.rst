Installation
============

Requirements
------------

Python 3.7 or later.

Core
----

.. code-block:: bash

   pip install surety

The core package includes schema definitions, field types, data generation,
and processing utilities.

Extensions
----------

Install the extensions you need:

.. code-block:: bash

   pip install surety-diff      # Comparison and validation engine
   pip install surety-api       # HTTP API contracts, interaction, and mocking
   pip install surety-ui        # Browser-based UI testing with Selenium
   pip install surety-db        # Database contracts and interaction layer
   pip install surety-config    # YAML-based configuration management

Versioning
----------

Surety follows Semantic Versioning.
Each extension is versioned independently but remains compatible within major
versions.
