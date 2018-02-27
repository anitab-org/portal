from django.apps import apps
from django.test import TestCase
from community.apps import CommunityConfig


class CommunityConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(CommunityConfig.name, 'community')
        self.assertEqual(apps.get_app_config('community').name, 'community')
