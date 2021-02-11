from django.apps import AppConfig


class RestHooksConfig(AppConfig):
    name = "django_web_hooks"

    def ready(self):
        import django_web_hooks.signals
