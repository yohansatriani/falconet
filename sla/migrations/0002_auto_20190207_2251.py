# Generated by Django 2.0.9 on 2019-02-07 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sla', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='troubles',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='troubles',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
