#!/bin/bash

echo "Installing production dependencies..."
pip install -r requirements/production.txt

echo "🛠 Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
