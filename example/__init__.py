import logging

log = logging.getLogger(__name__)

from .celery import app as celery_app

__all__ = [
    "celery_app",
]
