# Django Discovery Toolkit

Unified Sphinx documentation for the **django-udp-discovery** server package and **django-udp-discovery-client**, a UDP broadcast discovery stack for Django on intranet-style networks.

| Component | Repository | Package |
|-----------|------------|---------|
| Server | [django-udp-discovery](https://github.com/Ogro-Projukti/django-udp-discovery) | [`django-udp-discovery`](https://pypi.org/project/django-udp-discovery/) |
| Client | [django-udp-discovery-client](https://github.com/Ogro-Projukti/django-udp-discovery-client) | [`django-udp-discovery-client`](https://pypi.org/project/django-udp-discovery-client/) |

This repository contains **only documentation and tooling** (`docs/`, `.readthedocs.yaml`). The libraries are consumed from PyPI when building docs (see [`docs/requirements.txt`](docs/requirements.txt)).

## Build locally

```bash
pip install -r docs/requirements.txt
python -m sphinx -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser.

## Read the Docs

Configure the project with **Configuration file**: `.readthedocs.yaml` at the repo root.

## Contributing

Improvements to the prose, examples, and API layout should happen here. Fixes to behavior or library docstrings belong in the respective **server** or **client** repositories.
