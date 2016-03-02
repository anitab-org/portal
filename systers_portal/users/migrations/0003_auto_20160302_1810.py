# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0004_auto_20160302_1810'),
        ('users', '0002_auto_20150420_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systersuser',
            name='country',
        ),
        migrations.AddField(
            model_name='systersuser',
            name='city',
            field=models.ForeignKey(default='London', verbose_name=b'City', to='cities_light.City'),
            preserve_default=False,
        ),
    ]
