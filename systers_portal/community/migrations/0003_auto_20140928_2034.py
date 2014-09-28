# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_communitypage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitypage',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name=b'Content'),
        ),
    ]
