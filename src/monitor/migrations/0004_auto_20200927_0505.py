# Generated by Django 3.0.5 on 2020-09-26 22:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20200927_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='thermalpoint',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='thermalpoint',
            name='county',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='thermalpoint',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 26, 22, 5, 22, 513056, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='thermalpoint',
            name='nearest_city_distance',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='thermalpoint',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fireobject',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 26, 22, 5, 22, 513464, tzinfo=utc)),
        ),
    ]
