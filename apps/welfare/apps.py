from django.apps import AppConfig

class WelfareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.welfare'

    def ready(self):
        import apps.welfare.signals  # Import signals here