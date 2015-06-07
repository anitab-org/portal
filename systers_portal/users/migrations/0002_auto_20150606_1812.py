# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systersuser',
            name='blog_url',
            field=models.URLField(verbose_name='Blog', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systersuser',
            name='country',
            field=django_countries.fields.CountryField(verbose_name='Country', null=True, max_length=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systersuser',
            name='homepage_url',
            field=models.URLField(verbose_name='Homepage', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systersuser',
            name='profile_picture',
            field=models.ImageField(upload_to='users/pictures/', verbose_name='Profile picture', null=True, blank=True),
            preserve_default=True,
        ),
    ]
