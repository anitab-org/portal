# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('cities_light', '0004_auto_20171013_1705'),
        ('meetup', '0012_auto_20160816_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestMeetupLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name of the Meetup Location.(Naming convention for Systers meetup location is City+Systers.e.g.London Systers, Boston Systers.)')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='Slug of the Meetup Location')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description of the Meetup Location')),
                ('email', models.EmailField(max_length=255, verbose_name='Email of the Meetup Location if any.', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is this Approved?')),
                ('approved_by', models.ForeignKey(related_name='approvedby', to='users.SystersUser', blank=True, null=True, verbose_name='Approved By')),
                ('location', models.ForeignKey(to='cities_light.City', verbose_name='Location')),
                ('user', models.ForeignKey(related_name='createdby', to='users.SystersUser', verbose_name='Requested By')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='venue',
            field=models.CharField(max_length=512, verbose_name='Venue', blank=True),
            preserve_default=True,
        ),
    ]
