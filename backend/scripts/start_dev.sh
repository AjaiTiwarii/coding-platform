#!/bin/bash
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=coding_platform.settings
python manage.py runserver 0.0.0.0:8000
