# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
        ('users', '0001_squashed_0003_auto_20160207_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name=b'Date published')),
                ('date_modified', models.DateField(auto_now=True, verbose_name=b'Date last modified')),
                ('content', models.TextField(verbose_name=b'Content')),
                ('is_public', models.BooleanField(default=True, verbose_name=b'Is public')),
                ('is_monitored', models.BooleanField(default=False, verbose_name=b'Is monitored')),
                ('author', models.ForeignKey(verbose_name=b'Author', to='users.SystersUser')),
                ('community', models.ForeignKey(verbose_name=b'Community', to='community.Community')),
            ],
            options={
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name=b'Date published')),
                ('date_modified', models.DateField(auto_now=True, verbose_name=b'Date last modified')),
                ('content', models.TextField(verbose_name=b'Content')),
                ('is_public', models.BooleanField(default=True, verbose_name=b'Is public')),
                ('is_monitored', models.BooleanField(default=False, verbose_name=b'Is monitored')),
                ('author', models.ForeignKey(verbose_name=b'Author', to='users.SystersUser')),
                ('community', models.ForeignKey(verbose_name=b'Community', to='community.Community')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(verbose_name=b'Resource type', blank=True, to='blog.ResourceType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', null=True, verbose_name=b'Tags', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', null=True, verbose_name=b'Tags', blank=True),
            preserve_default=True,
        ),
    ]
