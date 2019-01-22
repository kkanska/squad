from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField


class Match(models.Model):
    DISCIPLINES = (
        (0, 'football'),
        (1, 'basketball'),
    )
    location = PointField()
    author_id = models.IntegerField()
    date = models.DateField()
    discipline = models.IntegerField(choices=DISCIPLINES, default=0)
    players = ArrayField(models.IntegerField(), size=12)


class Invite(models.Model):
    inviter = models.IntegerField()
    invitee = models.IntegerField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


