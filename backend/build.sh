# backend/build.sh
#!/bin/bash

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🛠 Applying migrations..."
python manage.py migrate
