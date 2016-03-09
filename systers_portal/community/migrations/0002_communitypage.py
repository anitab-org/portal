# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name=b'Date published')),
                ('date_modified', models.DateField(auto_now=True, verbose_name=b'Date last modified')),
                ('content', models.TextField(verbose_name=b'Content')),
                ('order', models.IntegerField(unique=True, verbose_name=b'Order')),
                ('author', models.ForeignKey(verbose_name=b'Author', to='users.SystersUser')),
                ('community', models.ForeignKey(verbose_name=b'Community', to='community.Community')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
