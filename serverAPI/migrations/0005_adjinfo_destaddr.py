# Generated by Django 4.0.3 on 2022-12-06 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverAPI', '0004_adjinfo_selfaddr_alter_adjinfo_nodeip'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjinfo',
            name='destAddr',
            field=models.CharField(default='', max_length=255),
        ),
    ]
