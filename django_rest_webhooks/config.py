from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

if getattr(django_settings, "HOOK_CUSTOM_MODEL", None) is None:
    django_settings.HOOK_CUSTOM_MODEL = "django_rest_webhooks.Hook"

HOOK_EVENTS = getattr(django_settings, "HOOK_EVENTS", None)
if HOOK_EVENTS is None:
    raise Exception("You need to define settings.HOOK_EVENTS!")

HOOK_EVENT_ACTIONS_CONFIG = None


def get_event_actions_config():
    global HOOK_EVENT_ACTIONS_CONFIG
    if HOOK_EVENT_ACTIONS_CONFIG is None:
        HOOK_EVENT_ACTIONS_CONFIG = {}
        for event_name, auto in HOOK_EVENTS.items():
            if not auto:
                continue
            model_label, action = auto.rsplit(".", 1)
            action_parts = action.rsplit("+", 1)
            action = action_parts[0]
            ignore_user_override = False
            if len(action_parts) == 2:
                ignore_user_override = True

            model_config = HOOK_EVENT_ACTIONS_CONFIG.setdefault(model_label, {})
            if action in model_config:
                raise ImproperlyConfigured(
                    f"settings.HOOK_EVENTS have a duplicate {action} for model {model_label}"
                )
            model_config[action] = (
                event_name,
                ignore_user_override,
            )
    return HOOK_EVENT_ACTIONS_CONFIG


def reset_event_actions_config():
    global HOOK_EVENT_ACTIONS_CONFIG
    global HOOK_EVENTS
    HOOK_EVENT_ACTIONS_CONFIG = None
    HOOK_EVENTS = django_settings.HOOK_EVENTS
