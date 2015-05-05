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
            field=models.URLField(blank=True, verbose_name='Blog', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systersuser',
            name='country',
            field=django_countries.fields.CountryField(null=True, blank=True, verbose_name='Country', max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systersuser',
            name='homepage_url',
            field=models.URLField(blank=True, verbose_name='Homepage', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systersuser',
            name='profile_picture',
            field=models.ImageField(null=True, blank=True, verbose_name='Profile picture', upload_to='users/pictures/'),
            preserve_default=True,
        ),
    ]
