from __future__ import absolute_import, unicode_literals
from matches.models import Match
from django.contrib.gis.geos import Point
from celery import shared_task


@shared_task
def create_match(match):
	Match.objects.create(
		location=Point(match['point'][0], match['point'][1]),
		author_id=match['author_id'],
		date=match['date'][:10],
		discipline=match['discipline'],
		minute_start=match['minute_start'],
		minute_end=match['minute_end'],
		players=match['squad']
	)