from django.apps import AppConfig


class RestHooksConfig(AppConfig):
    name = 'rest_hooks'

    def ready(self):
        import rest_hooks.signals
