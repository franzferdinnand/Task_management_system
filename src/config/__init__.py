from __future__ import absolute_import, unicode_literals

# Це гарантує, що Celery буде запускатись разом з Django
from config.celery import app as celery_app

__all__ = ('celery_app',)