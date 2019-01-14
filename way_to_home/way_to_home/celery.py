"""Celery settings for WayToHome project."""

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_to_home.settings')

CELERY_APP = Celery('WayToHome')

CELERY_APP.config_from_object('django.conf:settings', namespace='CELERY')
CELERY_APP.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
