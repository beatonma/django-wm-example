from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from mentions.exceptions import BadConfig

try:
    from celery import Celery

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

    app = Celery("djangowm")
    app.config_from_object("django.conf:settings", namespace="CELERY")
    app.autodiscover_tasks()


except ModuleNotFoundError:
    if getattr(settings, "WEBMENTION_USE_CELERY", None) is True:
        raise BadConfig(
            "Webmentions is configured to use Celery but it is not installed."
        )
