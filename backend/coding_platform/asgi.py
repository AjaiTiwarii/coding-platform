"""
ASGI config for coding_platform project.
Exposes the ASGI callable as a module-level variable named 'application'.
Supports both HTTP and WebSocket protocols for real-time features.
"""
import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coding_platform.settings.development')

# Initialize Django ASGI application early to ensure the AppRegistry is populated
django_asgi_app = get_asgi_application()

# WebSocket URL patterns (for future real-time features)
websocket_urlpatterns = [
    # Add WebSocket URL patterns here when implementing real-time features
    # path('ws/submissions/', consumers.SubmissionConsumer.as_asgi()),
    # path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]

# ASGI application with protocol type routing
application = ProtocolTypeRouter({
    # Django's ASGI application handles traditional HTTP requests
    "http": django_asgi_app,
    
    # WebSocket support for real-time features
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
