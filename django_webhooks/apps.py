from django.apps import AppConfig


class RestHooksConfig(AppConfig):
    name = "django_webhooks"

    def ready(self):
        import django_webhooks.signals
