# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20140928_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcetype',
            name='name',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
