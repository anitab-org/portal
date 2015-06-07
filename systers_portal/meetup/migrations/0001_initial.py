# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0004_auto_20150603_0717'),
        ('users', '0002_auto_20150606_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetupLocation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', unique=True, max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', unique=True, max_length=150)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('email', models.EmailField(verbose_name='Email', max_length=255, blank=True)),
                ('location', models.ForeignKey(to='cities_light.City', verbose_name='Location')),
                ('members', models.ManyToManyField(to='users.SystersUser', verbose_name='Members', related_name='Members', blank=True)),
                ('organizers', models.ManyToManyField(to='users.SystersUser', verbose_name='Organizers', related_name='Organizers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
