"""
WSGI config for coding_platform project.
Exposes the WSGI callable as a module-level variable named 'application'.
Optimized for production deployment with proper error handling.
"""
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coding_platform.settings.production')

try:
    application = get_wsgi_application()
except Exception as e:
    # Log the error and re-raise
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize WSGI application: {e}")
    raise

# Optional: Apply WSGI middleware for production
if os.environ.get('DJANGO_ENV') == 'production':
    # Add any production-specific WSGI middleware here
    pass
