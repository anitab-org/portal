from django.test import TestCase

from meetup.constants import (MEMBER, ORGANIZER, LOCATION_ALREADY_EXISTS_MSG,
                              SLUG_ALREADY_EXISTS_MSG, NAME_ALREADY_EXISTS_MSG,
                              LOCATION_ALREADY_EXISTS, SLUG_ALREADY_EXISTS,
                              NAME_ALREADY_EXISTS, OK, SUCCESS_MSG, ERROR_MSG)


class ConstantsTestCase(TestCase):
    def setUp(self):
        self.bar = "Bar"

    def test_member_constant(self):
        """Test MEMBER constant value"""
        member = MEMBER.format(self.bar)
        self.assertEqual(member, "Bar: Member")

    def test_organizer_constant(self):
        """Test ORGANIZER constant value"""
        organizer = ORGANIZER.format(self.bar)
        self.assertEqual(organizer, "Bar: Organizer")

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

    def test_slug_already_exists_constant(self):
        slug_already_exists_constant = SLUG_ALREADY_EXISTS
        self.assertEqual(slug_already_exists_constant, "slug_already_exists")
