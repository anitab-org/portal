# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('community', '0006_auto_20150208_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('approved_by', models.ForeignKey(related_name='approved_by', blank=True, to='users.SystersUser', null=True)),
                ('community', models.ForeignKey(to='community.Community')),
                ('user', models.ForeignKey(related_name='created_by', to='users.SystersUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
