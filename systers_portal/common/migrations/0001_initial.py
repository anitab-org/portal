# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0003_auto_20160207_1550'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name=b'Date created')),
                ('is_approved', models.BooleanField(default=True, verbose_name=b'Is approved')),
                ('body', models.TextField(verbose_name=b'Body')),
                ('object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(verbose_name=b'Author', to='users.SystersUser')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
