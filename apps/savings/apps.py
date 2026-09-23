from django.apps import AppConfig

class SavingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.savings'  # <-- CHANGE THIS TO 'apps.savings'

    def ready(self):
        # Change this to 'apps.savings.signals'
        import apps.savings.signals  