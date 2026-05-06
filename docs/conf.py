# Django Discovery Toolkit — Sphinx configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import os
import re
import sys
import logging
from pathlib import Path
from typing import Any

# Google-style "Attributes:" blocks duplicate Napoleon output for dataclasses and
# some Django model/config classes when both are present (common on PyPI wheels).
_ATTR_BLOCK = re.compile(
    r"(?ms)^Attributes:\s*\n(?:^[ \t].*\n)+",
)

_docs_dir = Path(__file__).resolve().parent

# ``django_udp_discovery`` / ``discovery_client`` come from installed wheels (PyPI or venv).
sys.path.insert(0, str(_docs_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings")

import django  # noqa: E402

django.setup()

# -- Project ---------------------------------------------------------------

project = "Django Discovery Toolkit"
copyright = "django-udp-discovery and django-udp-discovery-client contributors"
author = "Ogro-Projukti contributors"

def _doc_version() -> str:
    """PyPI versions shown in the sidebar when packages are installed."""
    try:
        from importlib.metadata import PackageNotFoundError, version as pkg_version

        s = pkg_version("django-udp-discovery")
        c = pkg_version("django-udp-discovery-client")
        return f"server {s}, client {c}"
    except PackageNotFoundError:
        return "dev"


release = version = _doc_version()

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

suppress_warnings = [
    "ref.python",
    "docutils",
]

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


def _strip_duplicate_attribute_docstrings(
    app: Any,
    what: str,
    name: str,
    obj: object,
    options: dict,
    lines: list[str],
) -> None:
    if what != "class" or not lines:
        return
    text = "\n".join(lines)
    new = _ATTR_BLOCK.sub("\n", text)
    if new != text:
        lines[:] = new.split("\n")


class _DropDuplicatePythonObjectWarnings(logging.Filter):
    """PyPI wheels may register the same dataclass field twice for autodoc."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003 — logging API
        try:
            text = record.getMessage()
        except Exception:
            return True
        if "duplicate object description of" in text and ":no-index:" in text:
            return False
        return True


def setup(app: Any) -> None:
    app.connect(
        "autodoc-process-docstring",
        _strip_duplicate_attribute_docstrings,
    )
    # ``suppress_warnings`` only matches typed Sphinx warnings; python domain duplicates
    # still use stdlib logging without ``type=``.
    for _name in (
        "sphinx.domains.python",
        "sphinx",
    ):
        _log = logging.getLogger(_name)
        _log.addFilter(_DropDuplicatePythonObjectWarnings())
