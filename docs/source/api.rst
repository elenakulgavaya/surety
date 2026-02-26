API Testing (surety-api)
========================

The ``surety-api`` extension provides HTTP API interaction, schema-based
mocking, and request verification.

.. code-block:: bash

   pip install surety-api

Defining API Schemas
--------------------

An API schema binds contracts to an HTTP endpoint:

.. code-block:: python

   from surety.api import ApiMethod, HttpMethod
   from surety import Dictionary, String, Int

   class CreateOrderRequest(Dictionary):
       ProductId = Int(name='product_id')
       Quality = Int(name='quantity', min_val=1, max_val=100)

   class OrderResponse(Dictionary):
       OrderId = Int(name='order_id')
       Status = String(name='status', default='pending')
       Total = String(name='total')

   class CreateOrder(ApiMethod):
       method = HttpMethod.POST
       url = '/api/v2/orders'
       req_body = CreateOrderRequest
       resp_body = OrderResponse

Available HTTP methods: ``POST``, ``GET``, ``HEAD``, ``PATCH``, ``DELETE``,
``PUT``, ``TRACE``, ``OPTIONS``.

Path Parameters
---------------

Use curly braces in the URL and pass ``path_params``:

.. code-block:: python

   class GetOrder(ApiMethod):
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

Use ``reply()`` directly on an ``ApiMethod`` schema:

.. code-block:: python

   schema = CreateOrder()
   schema.reply(
       body=CreateOrderRequestBody(),
       status=201
   )

Verifying API Calls
-------------------

Assert that a mocked endpoint received the expected request:

.. code-block:: python

   schema = CreateOrder()
   schema.reply(status=201)

   # ... test logic that triggers the API call ...

   schema.verify_called(
       expected=CreateOrderResponse()
   )

Verification supports comparison rules:

.. code-block:: python

   from surety.diff.rules import has_some_value

   schema.verify_called(
       expected=CreateOrderResponse(),
       rules={CreateOrderResponse.Id.name: has_some_value}
   )
