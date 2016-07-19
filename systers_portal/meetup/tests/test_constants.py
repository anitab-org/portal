from django.test import TestCase

from meetup.constants import (MEMBER, ORGANIZER)


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
