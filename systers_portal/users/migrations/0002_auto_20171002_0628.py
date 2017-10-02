# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systersuser',
            name='country',
            field=django_countries.fields.CountryField(blank=True, null=True, verbose_name='Country', max_length=2),
            preserve_default=True,
        ),
    ]
