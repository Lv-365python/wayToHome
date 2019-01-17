"""Celery settings for WayToHome project."""

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'way_to_home.settings')

CELERY_APP = Celery('WayToHome', include=['utils.tasks'])
CELERY_APP.config_from_object('django.conf:settings', namespace='CELERY')
