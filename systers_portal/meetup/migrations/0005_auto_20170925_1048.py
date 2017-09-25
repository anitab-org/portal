# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0004_meetuplocation_sponsors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='venue',
            field=models.CharField(verbose_name='Venue', max_length=512, blank=True),
            preserve_default=True,
        ),
    ]
