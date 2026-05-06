Server package: django-udp-discovery
====================================

Role
----

``django-udp-discovery`` is a Django application that listens for a **specific UDP probe** on a configurable port and answers with **this server's IPv4**, so intranet clients can locate the machine without DHCP tricks or MDNS.

Installation
------------

.. code-block:: bash

   pip install django-udp-discovery


Enable automatic listener
-------------------------

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "django_udp_discovery",
   ]

Startup happens in ``UdpDiscoveryConfig.ready()`` — a **daemon thread** runs the UDP loop while Django is up. Automatic start is skipped during tests.

Configuration (Django settings)
-------------------------------

Backed by ``django_udp_discovery.conf.settings``, which reads Django settings first, then these defaults:

``DISCOVERY_PORT`` (default ``9999``)
   UDP bind port on all interfaces (``0.0.0.0``).

``DISCOVERY_MESSAGE`` (default ``DISCOVER_SERVER``)
   Payload clients must send **exactly** (UTF-8 bytes) for a reply.

``RESPONSE_PREFIX`` (default ``SERVER_IP:``)
   Prepended before the dotted-quad in the UDP reply body.

``DISCOVERY_TIMEOUT`` (default ``0.5``)
   Documented for integrators/clients; the listener receive loop timing is governed by socket timeout and ``recvfrom``.

``DISCOVERY_BUFFER_SIZE`` (default ``1024``)
   ``recvfrom`` buffer size.

``ENABLE_LOGGING`` (default ``True``)
   Enables verbose logs from ``django_udp_discovery``.

Override any key in ``settings.py`` as needed **on both peers** if you change message/port/prefix so clients stay in sync.

Protocol implementation details
-------------------------------

#. Listener decodes expectations from settings once per worker start (`listener.py`): ``discovery_message = settings.DISCOVERY_MESSAGE.encode('utf-8')``, likewise ``response_prefix``.
#. Comparison is **byte equality**: ``if data == discovery_message``.
#. Reply is ``sendto(response_prefix + server_ip.encode('utf-8'), client_address)`` — **there is no ``:HTTP_PORT`` appended** by stock server.

Public Python API (package ``__init__``)
----------------------------------------

Re-exported from ``django_udp_discovery.listener``:

* ``start_udp_service()`` → ``bool`` — idempotent start; returns ``False`` if already running / thread died during bind.
* ``stop_udp_service()`` → ``bool`` — graceful stop; waits up to ~2 seconds for thread join.
* ``is_running()`` → ``bool`` — checks flag **and** thread liveness.

Re-exported utilities from ``utility``:

* ``get_server_ip()``, ``format_duration`` (management command UX), ``is_port_in_use``, ``validate_port``, ``is_port_error``.

Management command: ``start_discovery``
---------------------------------------

Provides operator-friendly diagnostics and optional timed runs::

   python manage.py start_discovery
   python manage.py start_discovery --duration 120

The command wraps the same listener functions, prints configuration, handles port conflict retries, and supports Ctrl+C cleanup.

Platform note
-------------

The upstream server README states **macOS is not a supported target** for this package; plan for **Windows or Linux** in production.

Further reading: :doc:`reference/server_modules`.
