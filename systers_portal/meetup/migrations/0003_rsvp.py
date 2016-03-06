# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('meetup', '0002_meetup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('coming', models.BooleanField(default=True)),
                ('plus_one', models.BooleanField(default=False)),
                ('meetup', models.ForeignKey(to='meetup.Meetup', verbose_name='Meetup')),
                ('user', models.ForeignKey(to='users.SystersUser', verbose_name='User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
