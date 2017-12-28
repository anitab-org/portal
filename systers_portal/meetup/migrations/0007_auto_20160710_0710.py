# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0006_auto_20160622_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetuplocation',
            options={'permissions': (('add_meetup_location_member', 'Add meetup location member'), ('delete_meetup_location_member', 'Delete meetup location member'), ('add_meetup_location_organizer', 'Add meetup location organizer'), ('delete_meetup_location_organizer', 'Delete meetup location organizer'), ('approve_meetup_location_joinrequest', 'Approve meetup location join request'), ('reject_meetup_location_joinrequest', 'Reject meetup location join request'))},
        ),
    ]
