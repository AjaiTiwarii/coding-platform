#!/bin/bash
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=coding_platform.settings
celery -A coding_platform worker -l info
