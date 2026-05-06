Examples
========

The snippets below mirror how the packages are meant to be used together. Adjust hostnames, ports, and settings for your environment.

Plain Python service locator
----------------------------

.. code-block:: python

   import logging
   from discovery_client import discover, load_config

   logging.basicConfig(level=logging.INFO)

   cfg = load_config(timeout=3.0, discovery_port=9999)
   for hit in discover(config=cfg):
       print(hit.ip, hit.port, hit.raw_response)

First server only
-----------------

.. code-block:: python

   from discovery_client import discover_one

   node = discover_one()
   if node:
       base = f"http://{node.ip}:{node.port}"
       print("Try:", base)

Interface-scoped discovery
--------------------------

.. code-block:: python

   from discovery_client import ClientConfig, discover

   cfg = ClientConfig(
       timeout=5.0,
       interfaces_whitelist=["Ethernet", "Wi-Fi"],  # exact OS names
   )
   print(discover(config=cfg))

.. note::

   Names differ by OS (e.g. ``en0`` on macOS, ``eth0`` on Linux). Use ``scripts/sanity_check.py`` in the client package while developing to print candidates.

Django server + auto listener
-----------------------------

``settings.py``:

.. code-block:: python

   INSTALLED_APPS = [
       "django.contrib.admin",
       "django.contrib.auth",
       "django.contrib.contenttypes",
       "django.contrib.sessions",
       "django.contrib.messages",
       "django.contrib.staticfiles",
       "django_udp_discovery",
   ]

Run:

.. code-block:: bash

   python manage.py runserver 0.0.0.0:8000

Separate Django “probe” project
-------------------------------

``settings.py``:

.. code-block:: python

   INSTALLED_APPS = [
       "django.contrib.contenttypes",
       "discovery_client_django",
   ]

.. code-block:: bash

   python manage.py discover_servers --timeout 10 --verbose

Operator restart with diagnostics
---------------------------------

On the Django server:

.. code-block:: bash

   python manage.py start_discovery --duration 300

Shows effective ``DISCOVERY_PORT``, message strings, logging state, then tears down cleanly after five minutes unless interrupted.
