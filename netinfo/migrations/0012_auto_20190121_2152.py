# Generated by Django 2.0.9 on 2019-01-21 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netinfo', '0011_auto_20190121_2152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devices',
            old_name='placement',
            new_name='location',
        ),
    ]
