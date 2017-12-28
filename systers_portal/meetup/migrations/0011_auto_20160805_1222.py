# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0010_auto_20160804_1152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetuplocation',
            options={'permissions': (('add_meetup_location_member', 'Add meetup location member'), ('delete_meetup_location_member', 'Delete meetup location member'), ('add_meetup_location_organizer', 'Add meetup location organizer'), ('delete_meetup_location_organizer', 'Delete meetup location organizer'), ('approve_meetup_location_joinrequest', 'Approve meetup location join request'), ('reject_meetup_location_joinrequest', 'Reject meetup location join request'), ('approve_meetup_comment', 'Approve comment for a meetup'), ('reject_meetup_comment', 'Reject comment for a meetup'), ('add_meetup_rsvp', 'RSVP for a meetup'), ('approve_support_request', 'Approve support request'), ('reject_support_request', 'Reject support request'), ('add_support_request_comment', 'Add comment for a support request'), ('edit_support_request_comment', 'Edit comment for a support request'), ('delete_support_request_comment', 'Delete comment for a support request'), ('approve_support_request_comment', 'Approve comment for a support request'), ('reject_support_request_comment', 'Reject comment for a support request'))},
        ),
    ]
