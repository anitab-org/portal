from django.test import TestCase

from community.constants import (CONTENT_CONTRIBUTOR, CONTENT_MANAGER,
                                 USER_CONTENT_MANAGER, COMMUNITY_ADMIN,
                                 DEFAULT_COMMUNITY_ACTIVE_PAGE,
                                 COMMUNITY_PRESENCE_CHOICES, COMMUNITY_TYPES_CHOICES,
                                 COMMUNITY_CHANNEL_CHOICES, YES_NO_CHOICES,
                                 ORDER_NULL_MSG, ORDER_ALREADY_EXISTS_MSG, SLUG_ALREADY_EXISTS_MSG,
                                 ORDER_NULL, SLUG_ALREADY_EXISTS, ORDER_ALREADY_EXISTS, OK,
                                 SUCCESS_MSG)


class ConstantsTestCase(TestCase):
    def setUp(self):
        self.foo = "Foo"
        self.bar = "Bar"

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

    def test_default_active_community_page_constant(self):
        default_active_community_page = 'news'
        self.assertEqual(default_active_community_page,
                         DEFAULT_COMMUNITY_ACTIVE_PAGE)

    def test_community_presence_choices_constant(self):
        """Test community presence field choices """
        community_presence_choices = [
            ('Facebook Page', 'Facebook Page'),
            ('Facebook Group', 'Facebook Group'),
            ('Twitter', 'Twitter'),
            ('Instagram', 'Instagram'),
            ('Other', 'Other')
        ]
        self.assertCountEqual(community_presence_choices,
                              COMMUNITY_PRESENCE_CHOICES)

    def test_community_types_choices_constant(self):
        """Test community types field choices """
        community_types_choices = [
            ('Affinity Group', 'Affinity Group (Latinas in Computing, LGBT, etc'),
            ('Special Interest Group',
             'Special Interest Group (Student Researchers, Systers in Government,'
             'Women in Cyber Security, etc) '),
            ('Email list', 'Email list (using Mailman3)'),
            ('Other', 'Other')
        ]
        self.assertCountEqual(community_types_choices, COMMUNITY_TYPES_CHOICES)

    def test_community_channel_choices_constant(self):
        """Test community channel field choices """
        community_channel_choices = [
            ('Existing Social Media Channels ', 'Existing Social Media Channels '),
            ('Request New Social Media Channels ',
             'Request New Social Media Channels ')
        ]
        self.assertCountEqual(community_channel_choices,
                              COMMUNITY_CHANNEL_CHOICES)

    def test_yes_no_choices_constant(self):
        """Test yes_no choices """
        yes_no_choices = [
            ('Yes', 'Yes'),
            ('No', 'No')
        ]
        self.assertCountEqual(yes_no_choices, YES_NO_CHOICES)

    def test_order_null_msg_constant(self):
        """Test message"""
        order_null_msg = ORDER_NULL_MSG
        self.assertEqual(
            order_null_msg, "Order is not set, Please choose an order.")

    def test_success_msg_constant(self):
        """Test message"""
        success_msg = SUCCESS_MSG
        self.assertEqual(success_msg, "Community created successfully!")

    def test_order_already_exists_msg_constant(self):
        """Test message"""
        order_already_exists_msg = ORDER_ALREADY_EXISTS_MSG.format(
            self.foo, self.bar)
        self.assertEqual(order_already_exists_msg,
                         "Order Foo already exists, please choose an order other than Bar.")

    def test_slug_already_exists_msg_constant(self):
        """Test message"""
        slug_already_exists_msg = SLUG_ALREADY_EXISTS_MSG.format(
            self.foo, self.bar)
        self.assertEqual(slug_already_exists_msg,
                         "Slug Foo already exists, please choose a slug other than Bar.")

    def test_order_null_constant(self):
        order_null_constant = ORDER_NULL
        self.assertEqual(order_null_constant, "order_null")

    def test_slug_already_exists_constant(self):
        slug_already_exists_constant = SLUG_ALREADY_EXISTS
        self.assertEqual(slug_already_exists_constant, "slug_already_exists")

    def test_order_already_exists_constant(self):
        order_already_exists_constant = ORDER_ALREADY_EXISTS
        self.assertEqual(order_already_exists_constant, "order_already_exists")

    def test_ok_constant(self):
        ok_constant = OK
        self.assertEqual(ok_constant, "success")
