# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_auto_20150208_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='community_admin',
            new_name='admin',
        ),
    ]
