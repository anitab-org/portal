from django.test import TestCase
from django.contrib.auth.models import User

from users.models import SystersUser


class SystersUserTestCase(TestCase):
    def test_create_systers_user(self):
        """Test creation of SystersUser on new User create
        """
        user = User.objects.create_user(username="foo", email="foo@mail.org",
                                        password="foobar")
        self.assertTrue(1, SystersUser.objects.count())
        self.assertEqual(user, SystersUser.objects.get().user)

        user.save()
        self.assertTrue(1, SystersUser.objects.count())
