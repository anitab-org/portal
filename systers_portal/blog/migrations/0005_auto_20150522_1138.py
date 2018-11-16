# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150420_1504'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='news',
            unique_together=set([('community', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('community', 'slug')]),
        ),
    ]
