# def get_celery_app():
#     from celery import Celery

#     app_ = Celery("transcriber", broker="redis://redis:6379/0")

#     # Using a string here means the worker doesn't have to serialize
#     # the configuration object to child processes.
#     # - namespace='CELERY' means all celery-related configuration keys
#     #   should have a `CELERY_` prefix.
#     app_.config_from_object("django.conf:settings", namespace="CELERY")

#     # Load task modules from all registered Django app configs.
#     app_.autodiscover_tasks()

#     return app_


# app = get_celery_app()

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transcriber.settings")

app = Celery("transcriber")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
