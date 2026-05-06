Installation and setup
=======================

Packages and repositories
-------------------------

This toolkit ships as **two separate PyPI packages**, each with its **own GitHub repository**:

.. list-table::
   :widths: 28 72
   :header-rows: 1

   * - Role
     - Links
   * - **Server**
     -
       `django-udp-discovery on PyPI <https://pypi.org/project/django-udp-discovery/>`__ ·
       `django-udp-discovery source <https://github.com/Ogro-Projukti/django-udp-discovery>`__
   * - **Client**
     -
       `django-udp-discovery-client on PyPI <https://pypi.org/project/django-udp-discovery-client/>`__ ·
       `django-udp-discovery-client source <https://github.com/Ogro-Projukti/django-udp-discovery-client>`__

You normally install **both** packages into the environments that need them (server Django app + any discoverer scripts or Django projects).

Requirements
------------

* **Python**: ``django-udp-discovery`` supports Python **3.7+**; the client targets **3.8+**. Prefer **3.8+** for both together.
* **Django**: required on **servers** (``django-udp-discovery``). Optional on **clients** except for ``python manage.py discover_servers``, which needs Django and ``discovery_client_django``.
* **Network extras (client)**: Broad discovery relies on ``netifaces`` *or* **ifaddr** (see ``pip install django-udp-discovery-client[network]``). Without either, ``discover()`` logs an ``ImportError`` and returns ``[]``.
* **Server platform**: upstream documents **Linux and Windows**; **macOS is not supported** for ``django-udp-discovery``.

Install from PyPI (recommended)
-------------------------------

Latest published releases:

.. code-block:: bash

   pip install django-udp-discovery
   pip install "django-udp-discovery-client[network,django]"

The client line enables interface enumeration (**``network``**) and Django integration (**``django``**) for the ``discover_servers`` command.

Install from each Git clone
---------------------------

Pick the repo you need, clone it, install from its root (editable optional).

.. rubric:: Server

.. code-block:: bash

   git clone https://github.com/Ogro-Projukti/django-udp-discovery.git
   cd django-udp-discovery
   pip install .

``django-udp-discovery`` sources live under ``src/django_udp_discovery``; Hatch builds that layout automatically.

.. rubric:: Client

.. code-block:: bash

   git clone https://github.com/Ogro-Projukti/django-udp-discovery-client.git
   cd django-udp-discovery-client
   pip install .
   pip install ".[network]"
   pip install ".[django]"          # optional, for ``discover_servers``

Use ``"[all]"`` if you prefer one command for extras.

Build these docs locally (toolkit repository only)
--------------------------------------------------

This repo can hold **documentation only**. It does **not** vendor the libraries; Sphinx imports them after you install from PyPI (same set Read the Docs uses):

.. code-block:: bash

   pip install -r docs/requirements.txt

That installs Sphinx, ``django-udp-discovery``, ``django-udp-discovery-client[django]``, ``ifaddr`` (lightweight imports for ``autodoc``), and the HTML theme. Then:

.. code-block:: bash

   python -m sphinx -b html docs docs/_build/html

If you keep a local ``packages/`` directory for reading upstream source, list it in ``.gitignore`` and do not rely on it for builds.

Django settings checklist
-------------------------

Server project
~~~~~~~~~~~~~~

Add the app and run Django:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "django_udp_discovery",
   ]

Optional tuning (see :doc:`server`):

.. code-block:: python

   DISCOVERY_PORT = 9999
   DISCOVERY_MESSAGE = "DISCOVER_SERVER"
   RESPONSE_PREFIX = "SERVER_IP:"
   ENABLE_LOGGING = True

Server debugging and console logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ENABLE_LOGGING`` toggles informational output inside ``django_udp_discovery``, but Django still needs a **`LOGGING`** configuration before records reach handlers. The snippet below matches the **`django-udp-discovery` package README** (``Debugging and Console Logging``): add it, or merge the ``loggers`` entry, into your ``settings.py``.

See also `Logging <https://docs.djangoproject.com/en/stable/topics/logging/>`_ in the Django documentation.

.. note::

   This subsection mirrors upstream server docs: `Debugging and Console Logging
   <https://github.com/Ogro-Projukti/django-udp-discovery#debugging-and-console-logging>`_ in the django-udp-discovery repository.

.. code-block:: python

   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {message}',
               'style': '{',
           },
           'simple': {
               'format': '{levelname} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
               'formatter': 'simple',
           },
       },
       'loggers': {
           'django_udp_discovery': {
               'handlers': ['console'],
               'level': 'DEBUG' if DEBUG else 'INFO',
               'propagate': False,
           },
       },
   }

With this in place you should see, on the console, details such as:

* listener startup / shutdown events
* discovery UDP requests received at the probe port
* successful replies emitted back to callers
* port binding conflicts and unexpected socket faults
* other state transitions emitted by ``django_udp_discovery``

The ``DEBUG`` versus ``INFO`` split follows Django’s ``DEBUG`` flag (`DEBUG=False` collapses chatter to informational messages only).

Client-only Django project (management command)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "discovery_client_django",
   ]

Core Python discovery does **not** require Django. Client logging mirrors the standalone package README: configure the **`django_udp_discovery_client`** logger if you integrate it into Django’s ``LOGGING`` tree.

Firewalls and ports
-------------------

* UDP **incoming** on the server must reach the Django process (default **9999**).
* Answers are sent **directly back** to the sender’s socket; firewall rules must allow that return traffic.
* Discovery does **not** expose HTTPS/HTTP ports; clients still need the real app port afterward (often **8000**, see protocol notes in :doc:`quickstart`).

Verifying
---------

* **Server**: run Django; confirm UDP starts without binding errors logged by ``django_udp_discovery``.
* **Client**: ``python -c "from discovery_client import discover; print(discover())"`` or ``python manage.py discover_servers``.

See :doc:`quickstart` for the shortest end-to-end path.
