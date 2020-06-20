from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from cities_light.models import City, Country

from meetup.models import (Meetup, Rsvp, SupportRequest,
                           RequestMeetup)
from users.models import SystersUser


class MeetupBaseTestCase:
    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)


class MeetupTestCase(MeetupBaseTestCase, TestCase):
    def setUp(self):
        super(MeetupTestCase, self).setUp()
        self.meetup = Meetup.objects.create(title="Test Meetup", slug="baz",
                                            date=timezone.now().date(), time=timezone.now().time(),
                                            venue="FooBar colony",
                                            description="This is a testing meetup.",
                                            meetup_location=self.location,
                                            created_by=self.systers_user,
                                            leader=self.systers_user)

    def test_str(self):
        """Test Meetup object str/unicode representation"""
        self.assertEqual(str(self.meetup), "Test Meetup")


class RequestMeetupTestCase(MeetupBaseTestCase, TestCase):
    def setUp(self):
        super(RequestMeetupTestCase, self).setUp()
        self.meetup_request = \
            RequestMeetup.objects.create(title="Test Meetup Request", slug="baz",
                                         date=timezone.now().date(), time=timezone.now().time(),
                                         venue="FooBar colony",
                                         description="This is a testing meetup request.",
                                         meetup_location=self.location,
                                         created_by=self.systers_user)

    def test_str(self):
        """Test Meetup object str/unicode representation"""
        self.assertEqual(str(self.meetup_request), "Test Meetup Request")

    def test_get_verbose_fields(self):
        fields = self.meetup_request.get_verbose_fields()
        self.assertEqual(len(fields), 12)
        self.assertTrue(fields[1], ('Title', 'Test Meetup Request'))


class RsvpTestCase(MeetupBaseTestCase, TestCase):
    def setUp(self):
        super(RsvpTestCase, self).setUp()
        self.meetup = Meetup.objects.create(title="Test Meetup", slug="baz",
                                            date=timezone.now().date(), time=timezone.now().time(),
                                            venue="FooBar colony",
                                            description="This is a testing meetup.",
                                            meetup_location=self.location,
                                            leader=self.systers_user,
                                            created_by=self.systers_user)
        self.rsvp = Rsvp.objects.create(user=self.systers_user, meetup=self.meetup)

    def test_str(self):
        self.assertEqual(str(self.rsvp), "foo RSVP for meetup Test Meetup")


class SupportRequestTestCase(MeetupBaseTestCase, TestCase):
    def setUp(self):
        super(SupportRequestTestCase, self).setUp()
        self.meetup = Meetup.objects.create(title="Test Meetup", slug="baz",
                                            date=timezone.now().date(), time=timezone.now().time(),
                                            venue="FooBar colony",
                                            description="This is a testing meetup.",
                                            meetup_location=self.location,
                                            leader=self.systers_user,
                                            created_by=self.systers_user)
        self.support_request = SupportRequest.objects.create(volunteer=self.systers_user,
                                                             meetup=self.meetup,
                                                             description="Support Request")

    def test_str(self):
        self.assertEqual(str(self.support_request), "foo volunteered for meetup Test Meetup")
