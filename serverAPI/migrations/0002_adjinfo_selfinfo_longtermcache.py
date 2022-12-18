# Generated by Django 4.0.3 on 2022-12-04 12:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodeIP', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'adj_info',
            },
        ),
        migrations.CreateModel(
            name='SelfInfo',
            fields=[
                ('reg_time', models.DateTimeField()),
                ('address', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('private_key', models.CharField(max_length=256)),
                ('loc_x', models.IntegerField()),
                ('loc_y', models.IntegerField()),
                ('chain_id', models.CharField(max_length=256)),
                ('current_round', models.PositiveIntegerField()),
                ('bc_port', models.CharField(max_length=5)),
                ('last_updated', models.DateTimeField()),
                ('node_status', models.BooleanField(default=True)),
                ('data_status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'self_info',
            },
        ),
        migrations.CreateModel(
            name='LongTermCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('upload_round', models.PositiveIntegerField()),
                ('loc_x', models.FloatField()),
                ('loc_y', models.FloatField()),
                ('type', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('content', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'long_term_cache',
                'unique_together': {('create_time', 'loc_x', 'loc_y', 'type')},
            },
        ),
    ]