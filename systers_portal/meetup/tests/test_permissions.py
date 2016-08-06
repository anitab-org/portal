from django.test import TestCase

from meetup.constants import (MEMBER, ORGANIZER)
from meetup.permissions import (member_permissions, organizer_permissions,
                                group_permissions, groups_templates)


class PermissionsTestCase(TestCase):
    def test_member_permissions(self):
        """Test member list of permissions"""
        permissions = [
            "change_meetup",
            "change_meetuplocation",
            "add_meetup_rsvp",
            "add_supportrequest",
            "change_supportrequest",
            "delete_supportrequest"
        ]
        self.assertCountEqual(member_permissions, permissions)

    def test_organizer_permissions(self):
        """Test organizer list of permissions"""
        permissions = [
            "change_meetup",
            "change_meetuplocation",
            "add_meetup_rsvp",
            "add_supportrequest",
            "change_supportrequest",
            "delete_supportrequest",
            "add_meetup",
            "delete_meetup",
            "add_meetuplocation",
            "delete_meetuplocation",
            "add_meetup_location_member",
            "delete_meetup_location_member",
            "add_meetup_location_organizer",
            "delete_meetup_location_organizer",
            "approve_meetup_location_joinrequest",
            "reject_meetup_location_joinrequest",
            "approve_meetup_comment",
            "reject_meetup_comment",
            "approve_support_request",
            "reject_support_request",
            "add_support_request_comment",
            "edit_support_request_comment",
            "delete_support_request_comment",
            "approve_support_request_comment",
            "reject_support_request_comment"
        ]
        self.assertCountEqual(organizer_permissions, permissions)

    def test_group_permissions(self):
        """Test group permissions keys"""
        self.assertTrue("member" in group_permissions)
        self.assertTrue("organizer" in group_permissions)

    def test_group_templates(self):
        """Test group templates values"""
        self.assertEqual(groups_templates["member"], MEMBER)
        self.assertEqual(groups_templates["organizer"], ORGANIZER)
