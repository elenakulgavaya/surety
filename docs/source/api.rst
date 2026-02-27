API Testing (surety-api)
========================

The ``surety-api`` extension provides API contracts, HTTP interaction,
schema-based mocking, and request verification.

.. code-block:: bash

   pip install surety-api

Defining an API Contract
------------------------

An API contract binds request and response schemas to an HTTP endpoint:

.. code-block:: python

   from surety.api import ApiContract, HttpMethod
   from surety import Dictionary, String, Int

   # Schemas — define data structure
   class CreateOrderRequest(Dictionary):
       ProductId = Int(name='product_id')
       Quantity = Int(name='quantity', min_val=1, max_val=100)

   class OrderResponse(Dictionary):
       OrderId = Int(name='order_id')
       Status = String(name='status', default='pending')
       Total = String(name='total')

   # Contract — binds schemas to an API endpoint
   class CreateOrder(ApiContract):
       method = HttpMethod.POST
       url = '/api/v2/orders'
       req_body = CreateOrderRequest
       resp_body = OrderResponse

The schemas (``CreateOrderRequest``, ``OrderResponse``) define *what the data
looks like*. The contract (``CreateOrder``) defines *where and how the data is
exchanged*.

Available HTTP methods: ``POST``, ``GET``, ``HEAD``, ``PATCH``, ``DELETE``,
``PUT``, ``TRACE``, ``OPTIONS``.

Path Parameters
---------------

Use curly braces in the URL and pass ``path_params``:

.. code-block:: python

   class GetOrder(ApiContract):
       method = HttpMethod.GET
       url = '/api/v2/orders/{order_id}'
       resp_body = OrderResponse

   GetOrder().call(path_params={'order_id': 42})

Making API Calls
----------------

Use ``call()`` to execute HTTP requests:

.. code-block:: python

   CreateOrder().call(
       headers={'Authorization': 'Bearer tk_test_abc123'}
   )

ApiCaller
---------

``ApiCaller`` provides method chaining with built-in verification:

.. code-block:: python

   from surety.api import ApiCaller

   class CreateOrderCaller(ApiCaller):
       schema = CreateOrder

   CreateOrderCaller(
       req_body={'product_id': 501, 'quantity': 3},
       headers={'Authorization': 'Bearer tk_test_abc123'}
   ).request().verify_response(resp_body=OrderResponse().value)

Response verification supports comparison rules and normalization:

.. code-block:: python

   from surety.diff.rules import has_some_value

   caller.verify_response(
       resp_body=OrderResponse().value,
       rules={'order_id': has_some_value},
       normalize=True
   )

Mocking with MockServer
------------------------

Set up mock responses for downstream services:

.. code-block:: python

   from surety.api import MockServer

   mock = MockServer()

   mock.reply(
       method='POST',
       url='/external-api/v1/validate',
       body={'valid': True, 'score': 0.98},
       status=200
   )

   # After the test runs, verify the mock was called
   mock.verify_all_mocks_called()

Additional MockServer methods:

.. code-block:: python

   # Capture requests to a URL
   captured = mock.catch(url='/external-api/v1/validate', timeout=5)

   # Check for unexpected unmocked requests
   unaddressed = mock.get_unaddressed_requests()

   # Wait for all mocks to be called
   mock.wait_for_mocks_to_be_called(timeout_seconds=3)

   # Reset all expectations
   mock.reset()

Schema-based Mocking
---------------------

Use ``reply()`` directly on an API contract to mock its endpoint using the
contract's schemas:

.. code-block:: python

   contract = CreateOrder()
   contract.reply(
       body=CreateOrderRequest(),
       status=201
   )

Verifying API Calls
-------------------

Assert that a mocked endpoint received the expected request:

.. code-block:: python

   contract = CreateOrder()
   contract.reply(status=201)

   # ... test logic that triggers the API call ...

   contract.verify_called(
       expected=OrderResponse()
   )

Verification supports comparison rules:

.. code-block:: python

   from surety.diff.rules import has_some_value

   contract.verify_called(
       expected=OrderResponse(),
       rules={OrderResponse.OrderId.name: has_some_value}
   )
