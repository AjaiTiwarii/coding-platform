"""
Main URL Configuration for Coding Platform.
Includes all app-specific URL patterns and API endpoints.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.http import JsonResponse
from django.urls import path, include

# Define api_root
def api_root(request):
    return JsonResponse({
        "auth": "/api/auth/",
        "problems": "/api/problems/",
        "submissions": "/api/submissions/",
        "dashboard": "/api/dashboard/"
    })

# 👇 Define your API URL patterns
api_urlpatterns = [
    path('', api_root),  # Changed from 'api/' to '' because this is under /api/
    path('auth/', include('apps.authentication.urls')),
    path('problems/', include('apps.problems.urls')),
    path('submissions/', include('apps.submissions.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]


urlpatterns = [
    # Admin interface
    path(getattr(settings, 'ADMIN_URL', 'admin/'), admin.site.urls),
    
    # API endpoints
    path('api/', include(api_urlpatterns)),
    
    # Health check endpoint
    path('health/', include('health_check.urls')),
    
    # Redirect root to API documentation or frontend
    path('', RedirectView.as_view(url='/api/', permanent=False)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Debug toolbar URLs (development only)
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Custom error handlers
handler400 = 'utils.views.bad_request'
handler403 = 'utils.views.permission_denied'
handler404 = 'utils.views.page_not_found'
handler500 = 'utils.views.server_error'

# Admin site customization
admin.site.site_header = "CodeMaster Administration"
admin.site.site_title = "CodeMaster Admin"
admin.site.index_title = "Welcome to CodeMaster Administration"
