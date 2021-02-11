from django.apps import AppConfig


class RestHooksConfig(AppConfig):
    name = "django_rest_webhooks"

    def ready(self):
        import django_rest_webhooks.signals
