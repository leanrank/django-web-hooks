from django.apps import AppConfig


class RestHooksConfig(AppConfig):
    name = "django_rest_webhooks"

    def ready(self):
        try:
            import django_rest_webhooks.signals  # noqa F401
        except ImportError:
            pass
