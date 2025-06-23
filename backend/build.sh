#!/usr/bin/env bash

# Fail the build if any command fails
set -o errexit

# Install dependencies (if not already done via requirements)
pip install -r requirements/production.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
