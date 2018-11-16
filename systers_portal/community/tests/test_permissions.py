from django.test import TestCase

from community.constants import (CONTENT_CONTRIBUTOR, CONTENT_MANAGER,
                                 USER_CONTENT_MANAGER, COMMUNITY_ADMIN)
from community.permissions import (content_contributor_permissions,
                                   content_manager_permissions,
                                   user_content_manager_permissions,
                                   community_admin_permissions,
                                   group_permissions, groups_templates)


class PermissionsTestCase(TestCase):
    def test_content_contributor_permissions(self):
        """Test content contributor list of permissions"""
        permissions = [
            "add_tag",
            "change_tag",
            "add_resourcetype",
            "change_resourcetype",
            "add_community_news",
            "change_community_news",
            "add_community_resource",
            "change_community_resource",
        ]
        self.assertCountEqual(content_contributor_permissions, permissions)

    def test_content_manager_permissions(self):
        """Test content manager list of permissions"""
        permissions = [
            "add_tag",
            "change_tag",
            "add_resourcetype",
            "change_resourcetype",
            "add_community_news",
            "change_community_news",
            "add_community_resource",
            "change_community_resource",
            "delete_tag",
            "delete_resourcetype",
            "delete_community_news",
            "delete_community_resource",
            "add_community_page",
            "change_community_page",
            "delete_community_page",
            "approve_community_comment",
            "delete_community_comment",
        ]
        self.assertCountEqual(content_manager_permissions, permissions)

    def test_user_content_manager_permissions(self):
        """Test user and content manager list of permissions"""
        permissions = [
            "add_tag",
            "change_tag",
            "add_resourcetype",
            "change_resourcetype",
            "add_community_news",
            "change_community_news",
            "add_community_resource",
            "change_community_resource",
            "delete_tag",
            "delete_resourcetype",
            "delete_community_news",
            "delete_community_resource",
            "add_community_page",
            "change_community_page",
            "delete_community_page",
            "approve_community_comment",
            "delete_community_comment",
            "add_community_systersuser",
            "change_community_systersuser",
            "delete_community_systersuser",
            "approve_community_joinrequest"
        ]
        self.assertCountEqual(user_content_manager_permissions, permissions)

    def test_community_admin_permissions(self):
        """Test community admin list of permissions"""
        permissions = [
            "add_tag",
            "change_tag",
            "add_resourcetype",
            "change_resourcetype",
            "add_community_news",
            "change_community_news",
            "add_community_resource",
            "change_community_resource",
            "delete_tag",
            "delete_resourcetype",
            "delete_community_news",
            "delete_community_resource",
            "add_community_page",
            "change_community_page",
            "delete_community_page",
            "approve_community_comment",
            "delete_community_comment",
            "add_community_systersuser",
            "change_community_systersuser",
            "delete_community_systersuser",
            "approve_community_joinrequest",
            "change_community",
            "add_community",
        ]
        self.assertCountEqual(community_admin_permissions, permissions)

    def test_group_permissions(self):
        """Test group permissions keys"""
        self.assertTrue("content_contributor" in group_permissions)
        self.assertTrue("content_manager" in group_permissions)
        self.assertTrue("user_content_manager" in group_permissions)
        self.assertTrue("community_admin" in group_permissions)

    def test_group_templates(self):
        """Test group templates values"""
        self.assertEqual(groups_templates["content_contributor"],
                         CONTENT_CONTRIBUTOR)
        self.assertEqual(groups_templates["content_manager"], CONTENT_MANAGER)
        self.assertEqual(groups_templates["user_content_manager"],
                         USER_CONTENT_MANAGER)
        self.assertEqual(groups_templates["community_admin"], COMMUNITY_ADMIN)
