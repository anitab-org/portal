# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0010_auto_20150522_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='communities', to='users.SystersUser', verbose_name='Members'),
        ),
    ]
