# Generated by Django 2.0.1 on 2018-10-14 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netinfo', '0003_links_input_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacts',
            options={'verbose_name_plural': 'contacts'},
        ),
        migrations.AlterModelOptions(
            name='links',
            options={'verbose_name_plural': 'links'},
        ),
        migrations.AlterModelOptions(
            name='sites',
            options={'verbose_name_plural': 'sites'},
        ),
    ]
