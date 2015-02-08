# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_auto_20141006_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joinrequest',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='joinrequest',
            name='community',
        ),
        migrations.RemoveField(
            model_name='joinrequest',
            name='user',
        ),
        migrations.DeleteModel(
            name='JoinRequest',
        ),
    ]
