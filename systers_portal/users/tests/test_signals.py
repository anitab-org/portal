from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase

from users.models import SystersUser, UserSetting
from users.signals import create_user_settings


class UserSettingsSignalsTestCase(TestCase):
    def setUp(self):
        post_save.connect(create_user_settings, sender=SystersUser,
                          dispatch_uid="create_settings")
        self.password = "foobar"

    def test_settings_signal(self):
        user = User.objects.create_user(username='foo', password=self.password,
                                        email='user@test.com')
        systers_user = SystersUser.objects.get(user=user)
        settings = UserSetting.objects.filter(user=systers_user)
        self.assertEqual(settings.count(), 1)
        self.assertEqual(settings.first().weekly_digest, True)
        self.assertEqual(settings.first().location_change, False)
