# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0003_rsvp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='venue',
            field=models.CharField(max_length=512, verbose_name=b'Venue', blank=True),
            preserve_default=True,
        ),
    ]
