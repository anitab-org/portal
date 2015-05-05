# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_auto_20150420_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitypage',
            name='order',
            field=models.IntegerField(verbose_name='Order'),
            preserve_default=True,
        ),
    ]
