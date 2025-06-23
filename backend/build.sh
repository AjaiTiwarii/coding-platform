#!/bin/bash

echo "📦 Installing dependencies..."
pip install -r requirements/production.txt

echo "🛠 Applying migrations..."
python3 manage.py migrate

echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput
