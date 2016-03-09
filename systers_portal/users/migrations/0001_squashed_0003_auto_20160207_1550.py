# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('users', '0001_initial'), ('users', '0002_auto_20150420_1504'), ('users', '0003_auto_20160207_1550')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystersUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('blog_url', models.URLField(verbose_name='Blog', max_length=255, blank=True)),
                ('homepage_url', models.URLField(verbose_name='Homepage', max_length=255, blank=True)),
                ('profile_picture', models.ImageField(verbose_name='Profile picture', blank=True, null=True, upload_to='users/pictures/')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('country', models.ForeignKey(verbose_name='Country', to='cities_light.Country', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
