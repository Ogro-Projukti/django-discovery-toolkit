Quickstart: working in five minutes
===================================

This page answers: **how do I get discovery working end-to-end with minimal wiring?**

You need two machines **on the same broadcast domain** (typical LAN / same Wi‑Fi), or run server and client on one host for smoke testing.

Install both packages
---------------------

From the monorepo root (this repository):

.. code-block:: bash

   pip install ./packages/django-udp-discovery ./packages/django-udp-discovery-client[network,django]


For published wheels (when installed from PyPI), use:

.. code-block:: bash

   pip install django-udp-discovery "django-udp-discovery-client[network,django]"

``[network]`` pulls helpers so the client can enumerate interfaces and broadcast on each (**required** for ``discover()`` in normal use). ``[django]`` enables ``python manage.py discover_servers``.

Minimal server (Django)
-----------------------

#. Create a Django project if you don't have one, then edit ``INSTALLED_APPS``:

   .. code-block:: python

      INSTALLED_APPS = [
          # ... default Django apps ...
          "django_udp_discovery",
      ]

#. Use defaults (port **9999**, message **DISCOVER_SERVER**, response prefix **SERVER_IP:**) or override in ``settings.py`` — see :doc:`server`.

#. Run Django:

   .. code-block:: bash

      python manage.py runserver 0.0.0.0:8000

When Django loads, ``django_udp_discovery`` starts a **daemon UDP thread** (unless you are in tests). It binds ``0.0.0.0:DISCOVERY_PORT`` and waits for an **exact** UDP payload match.

Minimal client (Python)
-----------------------

On another terminal or host:

.. code-block:: python

   from discovery_client import discover_one

   server = discover_one()
   if server:
       print(f"Discovered: {server.ip}:{server.port}")
   else:
       print("No server seen before timeout")

The listener responds with ``SERVER_IP:<ipv4>`` only (no ``:port`` in the payload). The client therefore **assumes HTTP port 8000** when the response omits a port — matching the common ``runserver`` case. If you need another port, extend the protocol or point clients at the right service manually.

Optional: discover from Django
------------------------------

#. Add ``"discovery_client_django"`` to ``INSTALLED_APPS`` (can be the same project as the server **or** a separate Django project).

#. Run:

   .. code-block:: bash

      python manage.py discover_servers --verbose


Expected result
---------------

* **Success:** ``discover_one()`` returns a ``DiscoveryResult`` whose ``ip`` is the server's detected LAN address; suggested URL for default dev server is ``http://<ip>:8000``.
* **Empty list / None:** firewall blocking UDP **9999**, server not running, different VLAN / broadcast domain, or missing ``[network]`` extras so interface enumeration fails (check logs for ``django_udp_discovery_client``).

Next: :doc:`installation`, :doc:`architecture`, :doc:`client` (limitations).
