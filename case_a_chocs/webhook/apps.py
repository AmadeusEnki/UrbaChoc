from django.apps import AppConfig

class WebhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webhook'

    def ready(self):
        # Assurez-vous que l'application est prête à recevoir les signaux
        import webhook.signals