# Generated by Django 4.0.3 on 2022-12-11 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverAPI', '0010_shorttermcache_create_round_alter_checkpoint_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='longtermcache',
            name='create_round',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 21, 24, 19, 86651)),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='round_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 21, 24, 19, 86651)),
        ),
    ]
