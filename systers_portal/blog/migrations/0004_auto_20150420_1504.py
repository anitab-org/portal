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
            field=models.ForeignKey(verbose_name='Author', to='users.SystersUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='community',
            field=models.ForeignKey(verbose_name='Community', to='community.Community'),
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
            field=models.DateField(auto_now=True, verbose_name='Date last modified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='is_monitored',
            field=models.BooleanField(verbose_name='Is monitored', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='is_public',
            field=models.BooleanField(verbose_name='Is public', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(verbose_name='Slug', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, verbose_name='Tags', to='blog.Tag'),
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
            field=models.ForeignKey(verbose_name='Author', to='users.SystersUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='community',
            field=models.ForeignKey(verbose_name='Community', to='community.Community'),
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
            field=models.DateField(auto_now=True, verbose_name='Date last modified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_monitored',
            field=models.BooleanField(verbose_name='Is monitored', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_public',
            field=models.BooleanField(verbose_name='Is public', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(blank=True, verbose_name='Resource type', to='blog.ResourceType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='slug',
            field=models.SlugField(verbose_name='Slug', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, verbose_name='Tags', to='blog.Tag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=255),
            preserve_default=True,
        ),
    ]
