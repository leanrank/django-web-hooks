import json
from collections import OrderedDict

import django
import requests
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from django_rest_webhooks.signals import hook_sent_event
from django_rest_webhooks.utils import get_module

if getattr(settings, 'HOOK_THREADING', True):
    from django_rest_webhooks.client import Client
    client = Client()
else:
    client = requests.Session()

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class AbstractHook(models.Model):
    """
    Stores a representation of a Hook.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='%(class)ss', on_delete=models.CASCADE)
    event = models.CharField('Event', max_length=64, db_index=True)
    target = models.URLField('Target URL', max_length=255)

    class Meta:
        abstract = True

    def clean(self):
        """ Validation for events. """
        from django_rest_webhooks.config import HOOK_EVENTS
        if self.event not in HOOK_EVENTS.keys():
            raise ValidationError(
                "Invalid hook event {evt}.".format(evt=self.event)
            )

    def dict(self):
        return {
            'id': self.id,
            'event': self.event,
            'target': self.target
        }

    def serialize_hook(self, instance):
        """
        Serialize the object down to Python primitives.

        By default it uses Django's built in serializer.
        """
        if getattr(instance, 'serialize_hook', None) and callable(instance.serialize_hook):
            return instance.serialize_hook(hook=self)
        if getattr(settings, 'HOOK_SERIALIZER', None):
            serializer = get_module(settings.HOOK_SERIALIZER)
            return serializer(instance, hook=self)
        # if no user defined serializers, fallback to the django builtin!
        data = serializers.serialize('python', [instance])[0]
        for k, v in data.items():
            if isinstance(v, OrderedDict):
                data[k] = dict(v)

        if isinstance(data, OrderedDict):
            data = dict(data)

        return {
            'hook': self.dict(),
            'data': data,
        }

    def deliver_hook(self, instance, payload_override=None):
        """
        Deliver the payload to the target URL.

        By default it serializes to JSON and POSTs.

        Args:
            instance: instance that triggered event.
            payload_override: JSON-serializable object or callable that will
                return such object. If callable is used it should accept 2
                arguments: `hook` and `instance`.
        """
        if payload_override is None:
            payload = self.serialize_hook(instance)
        else:
            payload = payload_override

        if callable(payload):
            payload = payload(self, instance)

        if getattr(settings, 'HOOK_DELIVERER', None):
            deliverer = get_module(settings.HOOK_DELIVERER)
            deliverer(self.target, payload, instance=instance, hook=self)
        else:
            client.post(
                url=self.target,
                data=json.dumps(payload, cls=DjangoJSONEncoder),
                headers={'Content-Type': 'application/json'}
            )

        hook_sent_event.send_robust(sender=self.__class__, payload=payload, instance=instance, hook=self)
        return None

    def __unicode__(self):
        return u'{} => {}'.format(self.event, self.target)


class Hook(AbstractHook):
    if django.VERSION >= (1, 7):
        class Meta(AbstractHook.Meta):
            swappable = 'HOOK_CUSTOM_MODEL'




