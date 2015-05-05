# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(verbose_name='Author', to='users.SystersUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name='Body'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(verbose_name='Is approved', default=True),
            preserve_default=True,
        ),
    ]
