from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal
from django.dispatch import receiver
from django.test.signals import setting_changed

from django_rest_webhooks.utils import distill_model_event

hook_event = Signal(providing_args=["action", "instance"])
raw_hook_event = Signal(providing_args=["event_name", "payload", "user"])
hook_sent_event = Signal(providing_args=["payload", "instance", "hook"])


def get_model_label(instance):
    if instance is None:
        return None
    opts = instance._meta.concrete_model._meta
    try:
        return opts.label
    except AttributeError:
        return ".".join([opts.app_label, opts.object_name])


@receiver(post_save, dispatch_uid="instance-saved-hook")
def model_saved(sender, instance, created, raw, using, **kwargs):
    """
    Automatically triggers "created" and "updated" actions.
    """
    model_label = get_model_label(instance)
    action = "created" if created else "updated"
    distill_model_event(instance, model_label, action)


@receiver(post_delete, dispatch_uid="instance-deleted-hook")
def model_deleted(sender, instance, using, **kwargs):
    """
    Automatically triggers "deleted" actions.
    """
    model_label = get_model_label(instance)
    distill_model_event(instance, model_label, "deleted")


@receiver(hook_event, dispatch_uid="instance-custom-hook")
def custom_action(sender, action, instance, user=None, **kwargs):
    """
    Manually trigger a custom action (or even a standard action).
    """
    model_label = get_model_label(instance)
    distill_model_event(instance, model_label, action, user_override=user)


@receiver(raw_hook_event, dispatch_uid="raw-custom-hook")
def raw_custom_event(
    sender,
    event_name,
    payload,
    user,
    send_hook_meta=True,
    instance=None,
    trust_event_name=False,
    **kwargs
):
    """
    Give a full payload
    """
    model_label = get_model_label(instance)

    new_payload = payload

    if send_hook_meta:
        new_payload = lambda hook, instance: {"hook": hook.dict(), "data": payload}

    distill_model_event(
        instance,
        model_label,
        None,
        user_override=user,
        event_name=event_name,
        trust_event_name=trust_event_name,
        payload_override=new_payload,
    )


@receiver(setting_changed)
def handle_hook_events_change(sender, setting, *args, **kwargs):
    from django_rest_webhooks.config import reset_event_actions_config

    if setting == "HOOK_EVENTS":
        reset_event_actions_config()
