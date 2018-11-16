# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20150227_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='admin',
            field=models.ForeignKey(verbose_name='Community admin', to='users.SystersUser', related_name='community'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='email',
            field=models.EmailField(blank=True, verbose_name='Email', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='Facebook', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='googleplus',
            field=models.URLField(blank=True, verbose_name='Google+', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='mailing_list',
            field=models.EmailField(blank=True, verbose_name='Mailing list', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(null=True, blank=True, verbose_name='Members', to='users.SystersUser', related_name='communities'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='order',
            field=models.IntegerField(unique=True, verbose_name='Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='parent_community',
            field=models.ForeignKey(blank=True, verbose_name='Parent community', to='community.Community', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='twitter',
            field=models.URLField(blank=True, verbose_name='Twitter', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='author',
            field=models.ForeignKey(verbose_name='Author', to='users.SystersUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='community',
            field=models.ForeignKey(verbose_name='Community', to='community.Community'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='Content'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='date_created',
            field=models.DateField(auto_now_add=True, verbose_name='Date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='date_modified',
            field=models.DateField(auto_now=True, verbose_name='Date last modified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='order',
            field=models.IntegerField(unique=True, verbose_name='Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='slug',
            field=models.SlugField(verbose_name='Slug', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='communitypage',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=255),
            preserve_default=True,
        ),
    ]
