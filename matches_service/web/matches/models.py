from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField

import architect


@architect.install('partition', type='range', subtype='integer', constraint='240', column='minute_start')
# tutorial -> https://media.readthedocs.org/pdf/architect/latest/architect.pdf
# 1st partition ~ 0:00-4:00
# 2nd partition ~ 4:00-8:00
# 3rd partition ~ 8:00-12:00
# 4th partition ~ 12:00-16:00
# 5th partition ~ 16:00-20:00
# 6th partition ~ 20:00-24:00
# constraint = 240 (minutes) = 4h
class Match(models.Model):
    DISCIPLINES = (
        (0, 'football'),
        (1, 'basketball')
    )
    location = PointField()
    author_id = models.IntegerField()
    # author_nick = models.CharField(null=True) # chyba warto było by dodać to pole
    date = models.DateField()
    minute_start = models.IntegerField(null=True)
    minute_end = models.IntegerField(null=True)
    discipline = models.IntegerField(choices=DISCIPLINES, default=0)
    players = ArrayField(models.IntegerField(), size=100)


class Invite(models.Model):
    inviter = models.IntegerField()
    invitee = models.IntegerField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


