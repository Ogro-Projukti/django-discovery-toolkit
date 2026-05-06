Client package: django-udp-discovery-client
===========================================

Role
----

``django-udp-discovery-client`` implements the **UDP broadcast side** of the toolkit: enumerate interfaces, send the discovery payload, collect ``SERVER_IP:`` replies, and present structured ``DiscoveryResult`` objects. **Django is optional**; only ``discovery_client_django`` needs it.

Install paths
-------------

.. code-block:: bash

   pip install ./packages/django-udp-discovery-client        # core only
   pip install "./packages/django-udp-discovery-client[network]"   # recommended
   pip install "./packages/django-udp-discovery-client[all]"     # network + django extras

``[network]`` installs ``netifaces`` / ``ifaddr`` so ``discover()`` can broadcast per interface. Without it, ``discover()`` logs an ``ImportError`` and returns ``[]``.

Public API (``discovery_client``)
---------------------------------

``__all__`` exports:

* ``ClientConfig`` — dataclass with validation + ``from_env``.
* ``load_config(**kwargs)`` — merges defaults, ``DISCOVERY_CLIENT_*`` env vars, then kwargs.
* ``DiscoveryResult`` — ``ip``, ``port``, ``raw_response``, ``extra``.
* ``discover(config=None)`` → ``list[DiscoveryResult]`` — never raises for network errors; returns empty list and logs.
* ``discover_one(config=None)`` → first result or ``None``.

Environment variables (prefix ``DISCOVERY_CLIENT_``)
----------------------------------------------------

``PORT``, ``MESSAGE``, ``RESPONSE_PREFIX``, ``TIMEOUT``, ``RETRIES`` (stored but unused), ``ENABLE_SUBNET_SCAN`` (unused), ``INTERFACES_WHITELIST``, ``INTERFACES_BLACKLIST`` (comma-separated names, case-sensitive).

``discovery_client.network``
----------------------------

Helpers for interface discovery and math:

* ``get_interfaces()``, ``select_interfaces(config)``, ``InterfaceInfo``.
* Netmask / broadcast utilities: ``netmask_to_prefix``, ``broadcast_from_ip_and_mask``, etc.

These power multi-interface broadcast selection and optional diagnostics when **no** servers answer.

Django integration
------------------

Add ``discovery_client_django`` to ``INSTALLED_APPS`` and run::

   python manage.py discover_servers [--timeout ...] [--port ...] [--verbose]

The command builds a ``ClientConfig`` from CLI flags, calls ``discover()``, prints a table, and emits the **segmented network** warning (via ``format_segmented_network_warning``) when applicable and no hosts were found.

Behavioural notes you should know
---------------------------------

* **Default HTTP port in results:** if the server reply is only ``SERVER_IP:x.y.z.w`` (as the stock server sends), the client parser **assumes port 8000** for convenience.
* **IPv4 / broadcast only:** no IPv6; no multicast; broadcasts do not cross arbitrary routers/VLANs.
* **Blocking calls:** plan thread boundaries accordingly.
* **Retries flag:** present in config but **not consumed** by the socket layer today.

Further reading: :doc:`reference/client_modules`.
