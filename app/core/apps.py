from django.apps import AppConfig
from django.core.management import call_command

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # Automatically call initapp to avoid manual step
    def ready(self):
        call_command('initapp')
