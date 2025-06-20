from django.apps import AppConfig

class SubmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.submissions'
    verbose_name = 'Submissions'
    
    def ready(self):
        # Import signal handlers
        import apps.submissions.signals
