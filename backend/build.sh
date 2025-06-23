#!/bin/bash

echo "Installing production dependencies..."
pip install -r requirements/production.txt

echo "🛠 Applying database migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput
