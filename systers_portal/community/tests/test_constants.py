from django.test import TestCase

from community.constants import (CONTENT_CONTRIBUTOR, CONTENT_MANAGER,
                                 USER_CONTENT_MANAGER, COMMUNITY_ADMIN)


class ConstantsTestCase(TestCase):
    def setUp(self):
        self.foo = "Foo"

    def test_content_contributor_constant(self):
        """Test CONTENT_CONTRIBUTOR constant value"""
        content_contributor = CONTENT_CONTRIBUTOR.format(self.foo)
        self.assertEqual(content_contributor, "Foo: Content Contributor")

    def test_content_manager_constant(self):
        """Test CONTENT_MANAGER constant value"""
        content_manager = CONTENT_MANAGER.format(self.foo)
        self.assertEqual(content_manager, "Foo: Content Manager")

    def test_user_content_manager_constant(self):
        """Test USER_CONTENT_MANAGER constant value"""
        user_content_manager = USER_CONTENT_MANAGER.format(self.foo)
        self.assertEqual(user_content_manager, "Foo: User and Content Manager")

    def test_community_admin_constant(self):
        """Test COMMUNITY_ADMIN constant value"""
        community_admin = COMMUNITY_ADMIN.format(self.foo)
        self.assertEqual(community_admin, "Foo: Community Admin")
