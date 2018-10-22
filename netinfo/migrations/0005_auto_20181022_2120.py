# Generated by Django 2.0.1 on 2018-10-22 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netinfo', '0004_auto_20181014_1151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sites',
            old_name='address',
            new_name='location',
        ),
        migrations.AddField(
            model_name='sites',
            name='tagline',
            field=models.CharField(default='', max_length=500),
        ),
    ]
