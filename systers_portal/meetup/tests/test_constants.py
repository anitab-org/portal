from django.test import TestCase

from meetup.constants import (MEMBER, ORGANIZER, SUCCESS_MEETUP_MSG, SLUG_ALREADY_EXISTS_MSG,
                              SLUG_ALREADY_EXISTS, OK)


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

    def test_slug_already_exists_constant(self):
        slug_already_exists_constant = SLUG_ALREADY_EXISTS
        self.assertEqual(slug_already_exists_constant, "slug_already_exists")

    def test_ok_constant(self):
        ok_constant = OK
        self.assertEqual(ok_constant, "success")

    def test_slug_already_exists_msg_constant(self):
        slug_already_exists_msg = SLUG_ALREADY_EXISTS_MSG.format(self.bar)
        self.assertEqual(slug_already_exists_msg,
                         "Slug Bar already exists, please choose a different slug.")

    def test_success_meetup_msg_constant(self):
        success_meetup_msg_constant = SUCCESS_MEETUP_MSG
        self.assertEqual(success_meetup_msg_constant, "Meetup sucessfully created!")
