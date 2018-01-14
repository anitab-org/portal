# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0004_auto_20180118_2137'),
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('meetup', '0012_auto_20160816_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestMeetupLocation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name of the Meetup Location.(Naming convention for Systers meetup location is City+Systers.e.g.London Systers, Boston Systers.)', unique=True)),
                ('slug', models.SlugField(max_length=150, verbose_name='Slug of the Meetup Location', unique=True)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description of the Meetup Location')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='Email of the Meetup Location if any.')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('is_approved', models.BooleanField(verbose_name='Is this Approved?', default=False)),
                ('approved_by', models.ForeignKey(blank=True, related_name='approvedby', verbose_name='Approved By', to='users.SystersUser', null=True)),
                ('location', models.ForeignKey(verbose_name='Location', to='cities_light.City')),
                ('user', models.ForeignKey(verbose_name='Requested By', related_name='createdby', to='users.SystersUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='venue',
            field=models.CharField(blank=True, max_length=512, verbose_name='Venue'),
            preserve_default=True,
        ),
    ]
