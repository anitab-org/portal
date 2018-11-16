# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_auto_20150420_1536'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='communitypage',
            unique_together=set([('community', 'slug'), ('community', 'order')]),
        ),
    ]
