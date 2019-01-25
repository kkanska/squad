from __future__ import absolute_import, unicode_literals
import string


from django.contrib.auth.models import User
from matches.models import Match
from django.utils.crypto import get_random_string
from django.contrib.gis.geos import Point

from celery import shared_task
from random import randint
from datetime import datetime as dt

import time

@shared_task
def create_random_matches(matches_number):
  print("SHARED TASK : CREATE RANDOM MATCHES ---------------------------------------------------------------------")
  for i in range(matches_number):
    select_day = float(dt.today().strftime("%d.%m%Y"))
    select_time = float(dt.today().strftime("%H.%M%S"))
    location = Point(select_day, select_time)
    author_id = i
    date = str(dt.today().date())
    discipline = i%2
    players = list(set([randint(1,20) for i in range(10)]))
    time.sleep(3)
    Match.objects.create(location=location, author_id=author_id, date=date, discipline=discipline, players=players)
  return str(matches_number) + ' random matches created with success!'
