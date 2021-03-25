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


@shared_task
def hello():
    print("Hello there!")