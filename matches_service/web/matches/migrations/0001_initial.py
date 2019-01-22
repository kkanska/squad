# Generated by Django 2.0.5 on 2018-06-11 10:58

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('author_id', models.IntegerField()),
                ('date', models.DateField()),
                ('discipline', models.IntegerField(choices=[(0, 'football'), (1, 'basketball')], default=0)),
                ('players', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=12)),
            ],
        ),
    ]