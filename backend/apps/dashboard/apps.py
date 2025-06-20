from django.apps import AppConfig

class DashboardConfig(AppConfig):
    """
    Configuration for the dashboard app providing analytics and user insights [19][20]
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'Dashboard'
    
    
