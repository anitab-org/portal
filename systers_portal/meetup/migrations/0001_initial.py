# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('cities_light', '0003_auto_20141120_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetupLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name='Slug')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='Email')),
                ('location', models.ForeignKey(to='cities_light.City', verbose_name='Location')),
                ('members', models.ManyToManyField(to='users.SystersUser', blank=True, verbose_name='Members', related_name='Members')),
                ('organizers', models.ManyToManyField(to='users.SystersUser', verbose_name='Organizers', related_name='Organizers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
