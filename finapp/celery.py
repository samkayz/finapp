from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, signals

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finapp.settings')

app = Celery('finapp')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))