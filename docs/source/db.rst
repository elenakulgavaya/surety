Database Testing (surety-db)
============================

The ``surety-db`` extension provides database interaction with contract
validation, supporting multiple database engines.

.. code-block:: bash

   pip install surety-db

Supported Databases
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Client Class
     - Database
   * - ``PostgresqlDBClient``
     - PostgreSQL
   * - ``MysqlDBClient``
     - MySQL / MariaDB
   * - ``SqliteDBClient``
     - SQLite (file-based)
   * - ``CassandraDBClient``
     - Apache Cassandra

Defining Database Models
------------------------

Database models extend ``Dictionary`` through ``DbModel`` and bind to
SQLAlchemy table models:

.. code-block:: python

   from surety.db import DbModel
   from surety import String, Int, Bool
   from surety.db.types import DbTimestamp, DbUuid

   class WarehouseModel(DbModel):
       __model__ = WarehouseTable  # SQLAlchemy model

       WarehouseId = DbUuid(name='id')
       Name = String(name='name')
       Capacity = Int(name='capacity', min_val=100, max_val=10000)
       Active = Bool(name='active')
       CreatedAt = DbTimestamp(name='created_at')

Database Types
--------------

``surety-db`` provides field types tailored for database columns:

- ``DbUuid`` — UUID field that returns string representation
- ``DbTimestamp`` — current timestamp with format and timezone conversion
- ``DbBool`` — boolean as integer (MySQL)
- ``DBJsonDict`` — JSON dictionary with serialization for ``to_db()``
- ``DbJsonArray`` — JSON array with serialization for ``to_db()``

Setting Up a Client
-------------------

Use ``DbClient`` to create a singleton database client:

.. code-block:: python

   from surety.db import Database, DbClient, PostgresqlDBClient

   db_client = DbClient('warehouse_db', PostgresqlDBClient(
       host='localhost', port=5432, user='testuser',
       password='testpass', db='warehouse_test'
   ))

   db = Database('warehouse_db', db_client)

CRUD Operations
---------------

.. code-block:: python

   # Insert a record
   warehouse = WarehouseModel()
   db.insert(warehouse)

   # Batch insert
   warehouses = [WarehouseModel() for _ in range(5)]
   db.insert_records(warehouses)

   # Query records
   records = db.get_records(
       WarehouseModel,
       active=True
   )

   # Get a single record
   record = db.get_record(
       WarehouseModel,
       name='Main Depot'
   )

   # Update records
   db.update(
       WarehouseModel,
       {'capacity': 5000},
       WarehouseTable.name == 'Main Depot'
   )

   # Delete records
   db.delete(WarehouseModel, active=False)

   # Cascade delete
   db.cascade_delete(WarehouseModel)

Verifying Records
-----------------

Compare database records against contract instances:

.. code-block:: python

   from surety.db import Database

   # Verify a single record
   Database.verify_record(
       actual=records[0],
       expected=warehouse
   )

   # Verify multiple records
   Database.verify_records(
       actual=records,
       expected=warehouses
   )

   # Verify no record exists
   db.verify_no_record(
       WarehouseModel,
       warehouse_id='non-existent-id'
   )

   # Verify no record with wait (for async operations)
   db.verify_no_record_with_wait(
       WarehouseModel,
       warehouse_id='non-existent-id'
   )

Verification supports comparison rules:

.. code-block:: python

   from surety.diff.rules import has_some_value

   Database.verify_record(
       actual=records[0],
       expected=warehouse,
       rules={WarehouseModel.CreatedAt.name: has_some_value}
   )

No-DB Mode
----------

For unit tests that don't require a real database connection:

.. code-block:: python

   db.enable_no_db_mode()

   # Database operations are skipped silently
   db.insert(warehouse)

   db.reset_mode()  # Re-enable actual database calls

SQLite
------

SQLite client supports context manager usage:

.. code-block:: python

   from surety.db import SqliteDBClient

   with SqliteDBClient('/tmp/test.db') as client:
       client.write_data('INSERT INTO items (name) VALUES (?)', 'Widget')
       rows = client.read_data('SELECT * FROM items')

Executing Raw SQL
-----------------

PostgreSQL and MySQL clients support raw SQL execution:

.. code-block:: python

   db_client.execute('SELECT COUNT(*) FROM warehouses WHERE active = %s', True)
