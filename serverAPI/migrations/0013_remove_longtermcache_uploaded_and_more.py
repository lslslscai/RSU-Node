# Generated by Django 4.0.3 on 2022-12-13 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverAPI', '0012_data_longtermcache_data_hash_longtermcache_uploaded_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='longtermcache',
            name='uploaded',
        ),
        migrations.AddField(
            model_name='shorttermcache',
            name='uploaded',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 19, 13, 31, 146766)),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='round_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 19, 13, 31, 146766)),
        ),
    ]
