Architecture: how the server and client work together
======================================================

Overview
--------

.. code-block:: text

   ┌─────────────────────────────┐         UDP broadcast / per-if broadcast
   │  Client (any Python host)   │──────────────────────────────────────────►
   │  discovery_client         │   DISCOVER_SERVER (configurable) to :9999
   └──────────────┬────────────┘
                  │
                  │  Responses: SERVER_IP:<ipv4>   (optional :port not sent by stock server)
                  ▼
   ┌─────────────────────────────┐
   │  Django + django-udp-       │
   │  discovery listener thread  │
   │  binds 0.0.0.0:DISCOVERY_   │
   │  PORT                       │
   └─────────────────────────────┘

Lifecycle (server)
------------------

``django_udp_discovery.apps.UdpDiscoveryConfig.ready()`` runs when Django loads. Unless the runtime looks like tests (``test`` in ``sys.argv``, ``pytest`` imported, or ``TESTING`` setting), it:

#. Registers ``atexit`` cleanup to call ``stop_udp_service``.
#. Calls ``start_udp_service()`` once if not already running.

The UDP listener logic lives in the ``django_udp_discovery.listener`` module:

#. Binds UDP to ``("0.0.0.0", DISCOVERY_PORT)``.
#. Reads datagrams up to ``DISCOVERY_BUFFER_SIZE``.
#. If payload **equals** ``DISCOVERY_MESSAGE`` encoded as UTF-8, replies with ``RESPONSE_PREFIX`` + ``get_server_ip()`` (UTF-8), unicast back to ``client_address``.
#. Uses a socket timeout loop so shutdown can observe ``_running``.

``get_server_ip()`` opens a ephemeral UDP socket, ``connect()``\ s toward ``8.8.8.8:80``, reads ``getsockname()[0]`` — a common LAN detection trick — and falls back to ``127.0.0.1``.

Discovery flow (client)
-----------------------

Public entry points: ``discovery_client.discover`` and ``discover_one``. ``discover()`` calls ``discover_servers_multi_interface``:

#. **Select IPv4 interfaces** via ``discovery_client.network.select_interfaces``, honoring whitelist/blacklist on ``ClientConfig``.
#. For each interface, derive a **broadcast address** (from OS data or computed from IP + netmask).
#. Open one UDP socket (broadcast enabled, receive timeout = ``ClientConfig.timeout``).
#. Send the discovery payload to **each** broadcast address.
#. Loop ``recvuntil`` timeouts, parse frames that start with ``response_prefix`` into ``DiscoveryResult``, dedupe by ``(ip, port)``.
#. If UDP body has no trailing ``:<port>``, client defaults port to **8000** (documented assumption).

Single-broadcast helpers exist (``discover_servers_single_broadcast`` toward ``255.255.255.255``); the high-level ``discover()`` prefers multi-interface operation.

Operational limits (real constraints from code)
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Topic
     - Behaviour
   * - IP version
     - **IPv4 only** (`AF_INET`, dotted-quad parsing).
   * - Transport / scope
     - **UDP broadcast** per interface; **no multicast**, no generalized cross‑router discovery.
   * - Blocking API
     - ``discover()`` blocks until socket timeout completes; **no asyncio** shim in-tree.
   * - Retries / subnet scan flags
     - ``ClientConfig.retries`` and ``enable_subnet_scan`` exist but are **unused** in the discovery path today.
   * - Segmented corporate LANs
     - Heuristic warns when broadcasts likely stay inside a ``/24`` while supernet suggests many segments — see ``detect_segmented_network`` when no servers appear.

See :doc:`reference/index` for generated API pages.
