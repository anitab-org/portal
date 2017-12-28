# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0011_auto_20160805_1222'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rsvp',
            unique_together=set([('user', 'meetup')]),
        ),
    ]
