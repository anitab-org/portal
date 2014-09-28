# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name=b'Content'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name=b'Content'),
        ),
    ]
