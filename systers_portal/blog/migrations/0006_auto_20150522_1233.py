# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150522_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='Tags'),
        ),
    ]
