# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_joinrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'verbose_name_plural': 'Communities', 'permissions': (('add_community_systersuser', 'Add community Systers User'), ('change_community_systersuser', 'Change community Systers User'), ('delete_community_systersuser', 'Delete community Systers User'), ('add_community_news', 'Add community news'), ('change_community_news', 'Change community news'), ('delete_community_news', 'Delete community news'), ('add_community_resource', 'Add community resource'), ('change_community_resource', 'Change community resource'), ('delete_community_resource', 'Delete community resource'), ('add_community_page', 'Add community page'), ('change_community_page', 'Change community page'), ('delete_community_page', 'Delete community page'), ('approve_community_comment', 'Approve community comment'), ('delete_community_comment', 'Delete community comment'), ('approve_community_joinrequest', 'Approve community join request'))},
        ),
    ]
