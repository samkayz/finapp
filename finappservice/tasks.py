from __future__ import absolute_import, unicode_literals 
from celery.schedules import crontab
from celery import shared_task
from celery.task import periodic_task
from .models import *
import string
import random
import datetime
import time
from datetime import timedelta
import os


@periodic_task(run_every=timedelta(seconds=1000))
def hello():
    print("Welcome to Celery")
    pass