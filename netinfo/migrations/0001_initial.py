# Generated by Django 2.0.3 on 2018-09-25 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contacts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(default='', max_length=10)),
                ('contact_value', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='links',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ipadd1', models.CharField(default='0.0.0.0/0', max_length=19)),
                ('ipadd2', models.CharField(default='0.0.0.0/0', max_length=19)),
                ('isp', models.CharField(default='unknown', max_length=20)),
                ('bandwidth', models.PositiveIntegerField(default=0)),
                ('media', models.CharField(default='unknown', max_length=20)),
                ('services', models.CharField(default='unknown', max_length=10)),
                ('status', models.BooleanField(default=1, max_length=1)),
                ('ipadd_others', models.CharField(max_length=19, null=True)),
                ('vrf_name', models.CharField(max_length=100, null=True)),
                ('links_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sites',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('ipadd', models.CharField(default='0.0.0.0/0', max_length=100)),
                ('site_code', models.CharField(default='', max_length=3)),
                ('area_code', models.CharField(default='', max_length=3)),
                ('address', models.CharField(default='', max_length=300)),
                ('city', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='links',
            name='sites1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites1', to='netinfo.sites'),
        ),
        migrations.AddField(
            model_name='links',
            name='sites2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites2', to='netinfo.sites'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='sites',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netinfo.sites'),
        ),
    ]
