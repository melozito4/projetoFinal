from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'  # ou o nome correto da tua app

    def ready(self):
        import core.signals  # importa o signals.py
