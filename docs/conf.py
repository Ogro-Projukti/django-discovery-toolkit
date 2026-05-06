# Django Discovery Toolkit — Sphinx configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import os
import sys
from pathlib import Path

_docs_dir = Path(__file__).resolve().parent
_root = _docs_dir.parent

# Installable layouts: django_udp_discovery lives under src/; discovery_client at package root.
sys.path.insert(0, str(_root / "packages" / "django-udp-discovery" / "src"))
sys.path.insert(0, str(_root / "packages" / "django-udp-discovery-client"))
sys.path.insert(0, str(_docs_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings")

import django  # noqa: E402

django.setup()

# -- Project ---------------------------------------------------------------

project = "Django Discovery Toolkit"
copyright = "django-udp-discovery and django-udp-discovery-client contributors"
author = "Ogro-Projukti contributors"

release = version = "1.0.0"

# -- General ---------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

nitpicky = False
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = "sphinx"

language = "en"

# Silence ambiguous cross-import targets (aliases like ``ClientConfig``).
suppress_warnings = ["ref.python"]

python_use_unqualified_type_names = True
autoclass_content = "class"
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True
autodoc_typehints_format = "short"

# -- Intersphinx -----------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "titles_only": False,
}
