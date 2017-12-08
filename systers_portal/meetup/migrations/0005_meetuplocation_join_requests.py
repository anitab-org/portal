# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('meetup', '0004_meetuplocation_sponsors'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetuplocation',
            name='join_requests',
            field=models.ManyToManyField(verbose_name='Join Requests', blank=True, related_name='Join Requests', to='users.SystersUser'),
            preserve_default=True,
        ),
    ]
