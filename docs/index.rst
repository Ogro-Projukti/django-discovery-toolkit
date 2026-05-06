Django Discovery Toolkit
========================

**A UDP-based service discovery solution for Django (server + client)**

Use this toolkit when you want machines on an intranet to **find Django hosts by broadcast** instead of hard-coding IPs. The stack has two cooperating pieces:

* **django-udp-discovery** — Django app that runs a UDP listener and answers discovery probes with this host's address.
* **django-udp-discovery-client** — Python client that broadcasts the probe, parses replies, and (optionally) integrates with Django via a management command.

.. note::

   The UDP server package documents **limited support on macOS** upstream; Linux and Windows are the primary environments.

.. toctree::
   :maxdepth: 2
   :caption: Guide

   quickstart
   installation
   architecture
   server
   client
   examples

.. toctree::
   :maxdepth: 2
   :caption: API reference

   reference/index
