# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name=b'Slug')),
                ('order', models.IntegerField(unique=True, verbose_name=b'Order')),
                ('email', models.EmailField(max_length=255, verbose_name=b'Email', blank=True)),
                ('mailing_list', models.EmailField(max_length=255, verbose_name=b'Mailing list', blank=True)),
                ('website', models.URLField(max_length=255, verbose_name=b'Website', blank=True)),
                ('facebook', models.URLField(max_length=255, verbose_name=b'Facebook', blank=True)),
                ('googleplus', models.URLField(max_length=255, verbose_name=b'Google+', blank=True)),
                ('twitter', models.URLField(max_length=255, verbose_name=b'Twitter', blank=True)),
                ('community_admin', models.ForeignKey(related_name=b'community', verbose_name=b'Community admin', to='users.SystersUser')),
                ('members', models.ManyToManyField(related_name=b'communities', null=True, verbose_name=b'Members', to='users.SystersUser', blank=True)),
                ('parent_community', models.ForeignKey(verbose_name=b'Parent community', blank=True, to='community.Community', null=True)),
            ],
            options={
                'verbose_name_plural': 'Communities',
            },
            bases=(models.Model,),
        ),
    ]
