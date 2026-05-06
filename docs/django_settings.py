"""
Minimal Django settings for Sphinx ``autodoc`` imports (``django-udp-discovery``).
Not used by runtime deployments.
"""

SECRET_KEY = "sphinx-documentation-build-only"
DEBUG = False
ALLOWED_HOSTS = ["localhost"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_udp_discovery",
    "discovery_client_django",
]
MIDDLEWARE = []
ROOT_URLCONF = "django_urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
LANGUAGE_CODE = "en-us"
