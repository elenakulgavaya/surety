Configuration (surety-config)
=============================

The ``surety-config`` extension provides YAML-based configuration management.

.. code-block:: bash

   pip install surety-config

Setup
-----

Create a ``config.yaml`` file in your project's ``etc/`` directory:

.. code-block:: yaml

   # etc/config.yaml
   App:
     url: "https://staging.acme.internal"
     api_version: "v2"

   MockServer:
     host: "localhost"
     port: 1080

   Database:
     host: "localhost"
     port: 5432
     name: "acme_test"

Optionally, create ``etc/local.yaml`` to override values locally (typically
excluded from version control):

.. code-block:: yaml

   # etc/local.yaml
   App:
     url: "http://localhost:8080"

Local values are merged on top of the base configuration.

Initialization
--------------

.. code-block:: python

   from surety.config import Cfg

   # Default: reads etc/config.yaml + etc/local.yaml
   Cfg.initialize()

   # Or with custom paths
   Cfg.initialize(
       config_file='/path/to/config.yaml',
       local_config='/path/to/local.yaml'
   )

Configuration is loaded lazily on first access if ``initialize()`` has not been
called explicitly.

Accessing Values
----------------

Use attribute access or dictionary-style access:

.. code-block:: python

   # Attribute access
   app_url = Cfg.App.url           # 'https://staging.acme.internal'
   db_host = Cfg.Database.host     # 'localhost'
   db_port = Cfg.Database.port     # 5432

   # Dictionary-style access
   mock_host = Cfg['MockServer']['host']

   # Check key existence
   if 'Database' in Cfg:
       print(Cfg.Database.name)

   # Get with default fallback
   timeout = Cfg.App.get('timeout', 30)

Nested sections are supported and accessed recursively:

.. code-block:: python

   # config.yaml:
   # Services:
   #   PaymentGateway:
   #     url: "https://pay.example.com"
   #     timeout: 10

   Cfg.Services.PaymentGateway.url      # 'https://pay.example.com'
   Cfg.Services.PaymentGateway.timeout   # 10

Setting Values
--------------

Configuration values can be modified at runtime:

.. code-block:: python

   Cfg.App.url = 'http://localhost:9090'
   Cfg.App['timeout'] = 60
