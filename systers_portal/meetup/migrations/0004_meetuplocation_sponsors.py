# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0003_rsvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetuplocation',
            name='sponsors',
            field=ckeditor.fields.RichTextField(verbose_name='Sponsors', blank=True),
            preserve_default=True,
        ),
    ]
