# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('meetup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=50, unique=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(verbose_name='Time', blank=True)),
                ('venue', models.TextField(verbose_name='Venue', blank=True)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Update')),
                ('created_by', models.ForeignKey(to='users.SystersUser', verbose_name='Created By', null=True)),
                ('meetup_location', models.ForeignKey(to='meetup.MeetupLocation', verbose_name='Meetup Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
