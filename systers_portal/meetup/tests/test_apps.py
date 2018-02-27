from django.apps import apps
from django.test import TestCase
from meetup.apps import MeetupConfig


class MeetupConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MeetupConfig.name, 'meetup')
        self.assertEqual(apps.get_app_config('meetup').name, 'meetup')
