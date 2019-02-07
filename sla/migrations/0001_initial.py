# Generated by Django 2.0.9 on 2019-02-02 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('netinfo', '0014_auto_20190121_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='troubles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cause_type', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('end_time', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
                ('description', models.CharField(default='', max_length=1000)),
                ('isp_ticket', models.CharField(max_length=50)),
                ('link_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netinfo.links')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'troubles',
            },
        ),
    ]