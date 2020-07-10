from django.test import TestCase

from meetup.constants import (COMMUNITY_MEMBER, COMMUNITY_MODERATOR, COMMUNITY_LEADER)
from meetup.permissions import (community_member_permissions, community_moderator_permissions,
                                community_leader_permissions, group_permissions, groups_templates)


class PermissionsTestCase(TestCase):
    def test_community_member_permissions(self):
        """Test member list of permissions"""
        permissions = [
            "add_meetup_rsvp",
            "add_support_request"
        ]
        self.assertCountEqual(community_member_permissions, permissions)

    def test_community_moderator_permissions(self):
        """Test moderator list of permissions"""
        permissions = [
            "add_meetup_rsvp",
            "add_support_request",
            "add_meetups",
            "change_meetups",
            "delete_meetups",
            "approve_meetup_request",
            "reject_meetup_request",
            "view_meetup_request",
            "approve_support_request",
            "reject_support_request",
            "add_resource",
        ]
        self.assertCountEqual(community_moderator_permissions, permissions)

    def test_community_leader_permissions(self):
        """Test leader list of permissions"""
        permissions = [
            "add_meetup_rsvp",
            "add_support_request",
            "add_meetups",
            "change_meetups",
            "delete_meetups",
            "approve_meetup_request",
            "reject_meetup_request",
            "view_meetup_request",
            "approve_support_request",
            "reject_support_request",
            "add_resource",
        ]
        self.assertCountEqual(community_leader_permissions, permissions)

    def test_group_permissions(self):
        """Test group permissions keys"""
        self.assertTrue("community_member" in group_permissions)
        self.assertTrue("community_moderator" in group_permissions)
        self.assertTrue("community_leader" in group_permissions)

    def test_group_templates(self):
        """Test group templates values"""
        self.assertEqual(groups_templates["community_member"], COMMUNITY_MEMBER)
        self.assertEqual(groups_templates["community_moderator"], COMMUNITY_MODERATOR)
        self.assertEqual(groups_templates["community_leader"], COMMUNITY_LEADER)
