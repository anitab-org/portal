from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

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
        self.assertListEqual(list(self.systers_user.user.groups.all()), [])
        self.systers_user.join_group(group)
        self.assertEqual(self.systers_user.user.groups.get(), group)

    def test_leave_group(self):
        """Test SystersUser leaving an auth Group"""
        group = Group.objects.create(name="Baz")
        self.systers_user.leave_group(group)
        self.systers_user.join_group(group)
        self.assertEqual(self.systers_user.user.groups.get(), group)
        self.systers_user.leave_group(group)
        self.assertListEqual(list(self.systers_user.user.groups.all()), [])


class SystersUserViewsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.client = Client()

    def test_user_profile_view(self):
        """Test UserProfileView as a logged-in user"""
        self.client.login(username='foo', password='foobar')
        profile_url = reverse('user_profile', kwargs={
            'username': self.systers_user.user.username})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit profile')
        self.assertTemplateUsed(response, 'users/view_profile.html')
        self.assertTemplateUsed(response, 'users/snippets/profile.html')
        nonexisten_profile_url = reverse('user_profile', kwargs={
            'username': 'bar'})
        response = self.client.get(nonexisten_profile_url)
        self.assertEqual(response.status_code, 404)

        new_user = User.objects.create_user(username='bar', password='foobar')
        new_user_profile_url = reverse('user_profile', kwargs={
            'username': new_user.username})
        response = self.client.get(new_user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit profile')


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
