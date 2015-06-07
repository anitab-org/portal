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
            field=models.ForeignKey(to='users.SystersUser', verbose_name='Author'),
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
            field=models.BooleanField(default=True, verbose_name='Is approved'),
            preserve_default=True,
        ),
    ]
