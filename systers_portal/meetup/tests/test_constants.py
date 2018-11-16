from django.test import TestCase

from meetup.constants import (COMMUNITY_MEMBER, COMMUNITY_MODERATOR, LOCATION_ALREADY_EXISTS_MSG,
                              SLUG_ALREADY_EXISTS_MSG, NAME_ALREADY_EXISTS_MSG,
                              LOCATION_ALREADY_EXISTS, SLUG_ALREADY_EXISTS,
                              NAME_ALREADY_EXISTS, OK, SUCCESS_MSG,
                              SUCCESS_MEETUP_MSG, ERROR_MSG)


class ConstantsTestCase(TestCase):
    def setUp(self):
        self.bar = "Bar"

    def test_community_member_constant(self):
        """Test COMMUNITY_MEMBER constant value"""
        member = COMMUNITY_MEMBER.format(self.bar)
        self.assertEqual(member, "Bar: Community Member")

    def test_community_moderator_constant(self):
        """Test COMMUNITY_MODERATOR constant value"""
        moderator = COMMUNITY_MODERATOR.format(self.bar)
        self.assertEqual(moderator, "Bar: Community Moderator")

    def test_location_already_exists_msg_constant(self):
        location_already_exists_msg = LOCATION_ALREADY_EXISTS_MSG.format(
            self.bar)
        self.assertEqual(location_already_exists_msg,
                         "A Meetup Location at this location Bar exists.")

    def test_slug_already_exists_msg_constant(self):
        slug_already_exists_msg = SLUG_ALREADY_EXISTS_MSG.format(self.bar)
        self.assertEqual(slug_already_exists_msg,
                         "Slug Bar already exists, please choose a different slug.")

    def test_name_already_exists_msg_constant(self):
        name_already_exists_msg = NAME_ALREADY_EXISTS_MSG.format(self.bar)
        self.assertEqual(name_already_exists_msg,
                         "Name Bar already exists, please choose a different name.")

    def test_success_msg_constant(self):
        success_msg = SUCCESS_MSG
        self.assertEqual(success_msg, "Meetup Location created successfully!")

    def test_error_msg_constant(self):
        error_msg = ERROR_MSG
        self.assertEqual(error_msg, "Something went wrong. Please try again")

    def test_slug_already_exists_constant(self):
        slug_already_exists_constant = SLUG_ALREADY_EXISTS
        self.assertEqual(slug_already_exists_constant, "slug_already_exists")

    def test_ok_constant(self):
        ok_constant = OK
        self.assertEqual(ok_constant, "success")

    def test_location_already_exists_constant(self):
        location_already_exists_constant = LOCATION_ALREADY_EXISTS
        self.assertEqual(location_already_exists_constant,
                         "location_already_exists")

    def test_name_already_exists_constant(self):
        name_already_exists_constant = NAME_ALREADY_EXISTS
        self.assertEqual(name_already_exists_constant, "name_already_exists")

    def test_success_meetup_msg_constant(self):
        success_meetup_msg_constant = SUCCESS_MEETUP_MSG
        self.assertEqual(success_meetup_msg_constant, "Meetup sucessfully created!")
