from django.contrib.auth.models import User, Group
from django.test import TestCase

from users.models import SystersUser


class SystersUserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()

    def test_create_systers_user(self):
        """Test creation of SystersUser on new User create"""
        self.assertTrue(1, SystersUser.objects.count())
        self.assertEqual(self.systers_user.user,
                         SystersUser.objects.get().user)

        self.systers_user.user.save()
        self.assertTrue(1, SystersUser.objects.count())

    def test_join_group(self):
        """Test SystersUser joining an auth Group"""
        group = Group.objects.create(name="Baz")
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])
        self.systers_user.join_group(group)
        self.assertEqual(self.systers_user.user.groups.get(), group)

    def test_leave_group(self):
        """Test SystersUser leaving an auth Group"""
        group = Group.objects.create(name="Baz")
        self.systers_user.leave_group(group)
        self.systers_user.join_group(group)
        self.assertEqual(self.systers_user.user.groups.get(), group)
        self.systers_user.leave_group(group)
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')

    def test_unicode(self):
        """Test unicode representation of Django User model"""
        self.assertEqual(unicode(self.user), 'foo')
        self.user.first_name = "Foo"
        self.user.save()
        self.assertEqual(unicode(self.user), 'foo')
        self.user.last_name = "Bar"
        self.user.save()
        self.assertEqual(unicode(self.user), 'Foo Bar')
