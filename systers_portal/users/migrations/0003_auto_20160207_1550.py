# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150420_1504'),
        ('cities_light', '0004_auto_20160207_1542'),
    ]

    operations = [


        migrations.RemoveField(
                model_name='systersuser',
                name='country',
            ),

        migrations.AddField(
            model_name='systersuser',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='cities_light.Country', null=True),
            preserve_default=True,
        ),
    ]

