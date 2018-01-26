# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('meetup', '0012_auto_20160816_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestMeetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=50)),
                ('slug', models.SlugField(verbose_name='Slug', unique=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.TimeField(blank=True, verbose_name='Time')),
                ('venue', models.CharField(blank=True, verbose_name='Venue', max_length=512)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('approved_by', models.ForeignKey(blank=True, to='users.SystersUser', related_name='approvedby', null=True)),
                ('created_by', models.ForeignKey(to='users.SystersUser', null=True, verbose_name='Created By')),
                ('meetup_location', models.ForeignKey(to='meetup.MeetupLocation', verbose_name='Meetup Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='venue',
            field=models.CharField(blank=True, verbose_name='Venue', max_length=512),
            preserve_default=True,
        ),
    ]
