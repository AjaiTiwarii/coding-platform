"""
Celery configuration for coding_platform project.
Handles asynchronous task processing for code execution and background jobs.
"""
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coding_platform.settings.development')

# Create the Celery application
app = Celery('coding_platform')

# Configure Celery using settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

# Optional: Configure periodic tasks
app.conf.beat_schedule = {
    'cleanup-old-submissions': {
        'task': 'apps.submissions.tasks.cleanup_old_submissions',
        'schedule': 60.0 * 60.0 * 24.0,  # Daily
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery configuration"""
    print(f'Request: {self.request!r}')
