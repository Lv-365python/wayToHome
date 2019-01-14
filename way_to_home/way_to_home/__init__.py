"""Initialization module."""

from .celery import CELERY_APP as celery_app

__all__ = ['celery_app']
