#!/usr/bin/env python

import sys
import django
from django.conf import settings


APP_NAME = "django_rest_webhooks"
comments = "django_comments"

settings.configure(
    DEBUG=True,
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
    USE_TZ=True,
    ROOT_URLCONF="{0}.tests".format(APP_NAME),
    MIDDLEWARE=(
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ),
    SITE_ID=1,
    HOOK_EVENTS={},
    HOOK_THREADING=False,
    INSTALLED_APPS=(
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.admin",
        "django.contrib.sites",
        "django.contrib.messages",
        comments,
        APP_NAME,
    ),
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ],
)

from django.test.utils import get_runner

if hasattr(django, "setup"):
    django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests([APP_NAME])
if failures:
    sys.exit(failures)
