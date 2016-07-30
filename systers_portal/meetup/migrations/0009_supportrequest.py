# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('meetup', '0008_auto_20160710_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('meetup', models.ForeignKey(verbose_name='Meetup', to='meetup.Meetup')),
                ('volunteer', models.ForeignKey(verbose_name='Volunteer', to='users.SystersUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
