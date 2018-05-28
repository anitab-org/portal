from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from meetup.models import (Meetup, MeetupLocation, RequestMeetupLocation)
from django.contrib.auth.models import User
from django.utils import timezone
from cities_light.models import City, Country
from users.models import SystersUser
from django.conf import settings
from django.contrib.auth import (SESSION_KEY, BACKEND_SESSION_KEY,
                                 HASH_SESSION_KEY)
from django.contrib.sessions.backends.db import SessionStore
from allauth.account.models import EmailAddress
import json
from os import getcwd

browsers = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome,
}


class SeleniumTestCase(StaticLiveServerTestCase):
    """
    A base test case for selenium, providing different helper methods.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = browsers['firefox']()
        cls.browser.implicitly_wait(0)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(
            name='Foo', display_name='Foo', country=country)
        with open('{}{}'.format(getcwd(),
                  '/systers_portal/common/tests/selenium/credentials.json')
                  ) as json_data:
            credentials = json.load(json_data)
        self.user = User()
        self.user.username = credentials['username']
        self.user.set_password(credentials['password'])
        self.user.save()
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers",
            slug="foo",
            location=self.location,
            description="It's a test location",
            sponsors="BarBaz",
            leader=self.systers_user)
        self.meetup_location_request = RequestMeetupLocation.objects.create(
            name="Bar Systers",
            slug="bar",
            location=self.location,
            description="This is a test meetup location request",
            user=self.systers_user)
        self.meetup = Meetup.objects.create(
            title="Test Meetup",
            slug="baz",
            date=timezone.now().date(),
            time=timezone.now().time(),
            venue="FooBar colony",
            description="This is a testing meetup.",
            meetup_location=self.meetup_location,
            created_by=self.systers_user)

    def create_session_cookie(self):
        """Create a pre-authenticated authenticated cookie using user credentials"""
        session = SessionStore()
        session[SESSION_KEY] = self.user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = self.user.get_session_auth_hash()
        session.save()

        # Finally, create the cookie dictionary
        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'secure': False,
            'path': '/',
        }
        return cookie

    def verify_user(self):
        """Verify instance user account using django-allauth constructs"""
        account_emailaddresse = EmailAddress()
        account_emailaddresse.email = 'foo@systers.org'
        account_emailaddresse.verified = True
        account_emailaddresse.user_id = self.user.id
        account_emailaddresse.save()

    def make_admin(self):
        self.user.is_superuser = True
        self.user.save()
        self.verify_user()
