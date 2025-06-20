# Main package initialization for coding_platform
# This file makes coding_platform a Python package

from .celery import app as celery_app

__all__ = ('celery_app',)
