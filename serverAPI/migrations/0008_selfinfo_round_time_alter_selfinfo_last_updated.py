# Generated by Django 4.0.3 on 2022-12-08 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverAPI', '0007_longtermcache_owner_shorttermcache_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfinfo',
            name='round_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 19, 42, 25, 691203)),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 19, 42, 25, 691203)),
        ),
    ]
