# Generated by Django 2.0.9 on 2019-02-07 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netinfo', '0014_auto_20190121_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='input_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='links',
            name='input_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
