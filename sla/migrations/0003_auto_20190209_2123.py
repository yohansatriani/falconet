# Generated by Django 2.0.9 on 2019-02-09 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sla', '0002_auto_20190207_2251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='troubles',
            old_name='link_id',
            new_name='link',
        ),
    ]
