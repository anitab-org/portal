# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150303_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(to='users.SystersUser', verbose_name='Author'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='community',
            field=models.ForeignKey(to='community.Community', verbose_name='Community'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='Content'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateField(auto_now_add=True, verbose_name='Date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_modified',
            field=models.DateField(verbose_name='Date last modified', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='is_monitored',
            field=models.BooleanField(default=False, verbose_name='Is monitored'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='Is public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(verbose_name='Slug', unique=True, max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='Tags', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='author',
            field=models.ForeignKey(to='users.SystersUser', verbose_name='Author'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='community',
            field=models.ForeignKey(to='community.Community', verbose_name='Community'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='Content'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='date_created',
            field=models.DateField(auto_now_add=True, verbose_name='Date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='date_modified',
            field=models.DateField(verbose_name='Date last modified', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_monitored',
            field=models.BooleanField(default=False, verbose_name='Is monitored'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='Is public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(to='blog.ResourceType', verbose_name='Resource type', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='slug',
            field=models.SlugField(verbose_name='Slug', unique=True, max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='Tags', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=255),
            preserve_default=True,
        ),
    ]
