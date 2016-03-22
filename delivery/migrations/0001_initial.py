# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_address', models.CharField(max_length=100)),
                ('from_address', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('html', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to_address', models.CharField(max_length=100)),
                ('from_address', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('html', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attempted', models.DateTimeField(auto_now_add=True)),
                ('is_success', models.BooleanField(default=True)),
                ('log_message', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
