UI Testing (surety-ui)
======================

The ``surety-ui`` extension provides browser-based UI testing with Selenium
for frontend testing in the browser. It offers page objects, reusable UI
element abstractions, client-side storage access, and screenshot comparison.

.. code-block:: bash

   pip install surety-ui

Browser
-------

``Browser`` is a singleton wrapper around a Selenium Chrome WebDriver.
Configuration is read from ``surety-config``:

.. code-block:: yaml

   # etc/config.yaml
   Browser:
     headless: true
     no_sandbox: true        # for CI environments
     # remote_url: "http://selenium-hub:4444"  # optional remote WebDriver
     # devtools: true         # auto-open DevTools
     # exclude_logs_from:     # filter console log noise
     #   - "favicon.ico"

.. code-block:: python

   from surety.ui import Browser

   browser = Browser()
   browser.driver.get('https://example.com')
   browser.close()

Pages
-----

``Page`` provides a base class for page objects. Define ``base_url`` and
``url`` to enable navigation:

.. code-block:: python

   from surety.ui import Browser, Page

   class LoginPage(Page):
       base_url = 'https://staging.example.com'
       url = 'auth/login'

   class UserProfilePage(Page):
       base_url = 'https://staging.example.com'
       url = 'users/{}'

   # Navigate
   LoginPage.open()
   UserProfilePage.open('user-42')

   # Verify current URL
   LoginPage.verify_current_url()

UI Elements
-----------

Surety-ui provides typed element abstractions that wrap Selenium locators.
Elements are declared as class attributes on pages or containers and support
CSS selectors, XPath, ``data-testid`` attributes, and element names:

.. code-block:: python

   from surety.ui import Page, Button, TextInput, Label, Link, Select, Checkbox

   class LoginPage(Page):
       base_url = 'https://staging.example.com'
       url = 'auth/login'

       EmailInput = TextInput(test_id='email-input')
       PasswordInput = TextInput(test_id='password-input')
       SubmitButton = Button(test_id='login-submit')
       ErrorMessage = Label(css='.error-message')

   # Interact with elements
   LoginPage.open()
   LoginPage.EmailInput.input('user@example.com')
   LoginPage.PasswordInput.input('password123')
   LoginPage.SubmitButton.click()

Available element types:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Key Methods
   * - ``Button``
     - ``click()``, ``wait_for_text()``, ``verify_text()``, ``is_disabled``
   * - ``TextInput``
     - ``input()``, ``clear_and_type()``, ``get_value()``, ``set_value()``, ``verify_value()``
   * - ``Label``
     - ``text``, ``wait_for_text()``, ``verify_text()``, ``wait_for_updated()``
   * - ``Link``
     - ``click()``, ``url`` (href attribute)
   * - ``Select``
     - ``select(value=, index=, text=)``, ``all_options``, ``selected_option``
   * - ``Checkbox``
     - ``click()``, ``checked``, ``verify_checked()``
   * - ``Container``
     - Base container for grouping nested elements
   * - ``Table``
     - ``Head``, ``Rows``, ``read_data()``

Element Locators
^^^^^^^^^^^^^^^^

Elements can be located using several strategies. The default and recommended
approach is to pass the element's ``id`` attribute directly as the first
argument:

.. code-block:: python

   Button('submit-btn')               # by id (default, recommended)
   Button(test_id='submit')           # data-testid attribute
   TextInput(css='input.email')       # CSS selector
   Label(xpath='//div[@class="msg"]') # XPath
   TextInput(name='username')         # HTML name attribute

Element Lists
^^^^^^^^^^^^^

Use ``Elements`` (from ``surety.ui.browser``) to work with collections of
elements:

.. code-block:: python

   from surety.ui.browser import Elements
   from surety.ui import Label, Container

   class SearchResults(Page):
       base_url = 'https://staging.example.com'
       url = 'search'

       Items = Elements(css='.result-item', element_class=Label)

   SearchResults.Items.wait_for_items_load(10)
   labels = SearchResults.Items.get_labels()
   SearchResults.Items.click_by_text('First Result')

Tables
^^^^^^

``Table`` and ``TableRow`` provide structured table interaction:

.. code-block:: python

   from surety.ui import Table, Page

   class DataPage(Page):
       base_url = 'https://staging.example.com'
       url = 'data'

       DataTable = Table(test_id='data-table')

   DataPage.open()
   headers, rows = DataPage.DataTable.read_data()

Local Storage
-------------

``LocalStorage`` provides access to the browser's ``window.localStorage``:

.. code-block:: python

   from surety.ui import LocalStorage

   # Set and get items
   LocalStorage.set_item('auth_token', 'tk_test_abc123')
   token = LocalStorage.get_item('auth_token')

   # Remove or clear
   LocalStorage.remove_item('auth_token')
   LocalStorage.clear()

   # Base64-encoded storage (for complex data)
   LocalStorage.set_encoded('user_prefs', {'theme': 'dark', 'lang': 'en'})
   LocalStorage.verify_decoded('user_prefs', {'theme': 'dark', 'lang': 'en'})

   # Verify with comparison rules
   LocalStorage.verify_item('cart', expected={'items': []})

IndexedDB
---------

``IndexedDb`` provides access to the browser's IndexedDB:

.. code-block:: python

   from surety.ui.indexed_db import IndexedDb

   db = IndexedDb('my_app_db')

   # Read all records from a store
   records = db.get_all_records('users')

   # Clear a store
   db.delete_all_records('users')

   # Insert a record
   db.insert_record('users', '{"id": 1, "name": "Test User"}')

Screenshot Comparison
---------------------

Surety-ui supports visual regression testing through screenshot comparison.
Configure the threshold in ``surety-config``:

.. code-block:: yaml

   # etc/config.yaml
   Screenshot:
     compare: true
     threshold: 0.5  # allowed mismatch percentage

Use the ``compare_screenshot`` decorator to enable per-test screenshot
comparison:

.. code-block:: python

   from surety.ui.pytest_addons import compare_screenshot

   @compare_screenshot
   def test_login_page_layout():
       LoginPage.open()
       # Screenshot is taken and compared automatically at test end

Individual elements also support screenshot verification:

.. code-block:: python

   LoginPage.SubmitButton.verify_displayed(height=40, width=120)

Pytest Integration
------------------

Surety-ui provides pytest utilities for automatic screenshot capture on test
failure and console error checking:

.. code-block:: python

   from surety.ui.pytest_addons import (
       save_screenshot_on_failure,
       check_console_errors,
   )

   # Decorator to fail test on browser console errors
   @check_console_errors
   def test_no_js_errors():
       LoginPage.open()
       LoginPage.SubmitButton.click()
