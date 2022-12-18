# Generated by Django 4.0.3 on 2022-12-10 22:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverAPI', '0009_checkpoint_alter_selfinfo_last_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorttermcache',
            name='create_round',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='checkpoint',
            name='result',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 22, 44, 45, 44082)),
        ),
        migrations.AlterField(
            model_name='selfinfo',
            name='round_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 22, 44, 45, 44082)),
        ),
        migrations.AlterUniqueTogether(
            name='checkpoint',
            unique_together={('owner', 'round')},
        ),
    ]
