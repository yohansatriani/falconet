# Generated by Django 2.0.3 on 2018-09-26 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netinfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='isp_link_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
