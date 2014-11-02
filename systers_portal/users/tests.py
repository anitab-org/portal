from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from community.models import Community, JoinRequest
from users.forms import UserForm, SystersUserForm
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


class UserViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.client = Client()

    def test_user_view(self):
        """Test UserView as a logged-in user"""
        user_url = reverse('user', kwargs={
            'username': self.systers_user.user.username})
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 200)
        nonexistent_user_url = reverse('user', kwargs={'username': 'bar'})
        response = self.client.get(nonexistent_user_url)
        self.assertEqual(response.status_code, 404)

    def test_user_profile_panel(self):
        """Test profile panel from UserView"""
        self.client.login(username='foo', password='foobar')
        user_url = reverse('user', kwargs={
            'username': self.systers_user.user.username})
        response = self.client.get(user_url)
        self.assertContains(response, 'Edit profile')
        self.assertTemplateUsed(response, 'users/view_profile.html')
        self.assertTemplateUsed(response, 'users/snippets/profile.html')

        new_user = User.objects.create_user(username='bar', password='foobar')
        new_user_url = reverse('user', kwargs={'username': new_user.username})
        response = self.client.get(new_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit profile')

    def test_user_panel_membership(self):
        """Test membership panel from UserView"""
        self.client.login(username='foo', password='foobar')
        user_url = reverse('user', kwargs={
            'username': self.systers_user.user.username})
        response = self.client.get(user_url)
        self.assertContains(response,
                            "Looks like you are member of no community.")
        self.assertTemplateUsed(response, 'users/view_profile.html')
        self.assertTemplateUsed(response, 'users/snippets/membership.html')

        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=self.systers_user)
        community.add_member(self.systers_user)
        community.save()
        response = self.client.get(user_url)
        self.assertContains(response, "Transfer ownership")
        new_user = User.objects.create_user(username='bar', password='foobar')
        new_systers_user = SystersUser.objects.get(user=new_user)
        new_comm = Community.objects.create(name="Bar", slug="bar",
                                            order=2,
                                            community_admin=new_systers_user)
        new_comm.add_member(self.systers_user)
        new_comm.save()
        response = self.client.get(user_url)
        self.assertContains(response, "Leave")
        new_comm.remove_member(self.systers_user)
        new_comm.save()
        JoinRequest.objects.create(user=self.systers_user, community=new_comm)
        response = self.client.get(user_url)
        self.assertContains(response, "Cancel request")

        new_user_url = reverse('user', kwargs={'username': new_user.username})
        response = self.client.get(new_user_url)
        self.assertNotContains(response, 'Transfer ownership')

    def test_user_panel_permissions(self):
        """Test permissions panel from UserView"""
        self.client.login(username='foo', password='foobar')
        user_url = reverse('user', kwargs={
            'username': self.systers_user.user.username})
        response = self.client.get(user_url)
        self.assertContains(response, "Looks like you have no permissions.")
        self.assertTemplateUsed(response, 'users/view_profile.html')
        self.assertTemplateUsed(response, 'users/snippets/permissions.html')
        group = Group.objects.create(name="Bar")
        self.systers_user.user.groups.add(group)
        response = self.client.get(user_url)
        self.assertContains(response, "Bar")


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.client = Client()

    def test_get_user_profile_view(self):
        """Test GET user profile"""
        # Get profile as non logged-in user
        profile_url = reverse('user_profile', kwargs={'username': 'foo'})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 403)
        # Get your own profile as a logged-in user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        # Get view profile of nonexistent profile
        bar_profile_url = reverse('user_profile', kwargs={'username': 'bar'})
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 404)
        # Get view profile of other user
        user = User.objects.create_user(username='bar', password='foobar')
        systersuser = SystersUser.objects.get(user=user)
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 403)
        # Get view profile as superusers
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 200)
        # Get view profile of other user having the necessary permissions
        self.user.is_superuser = True
        self.user.save()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=self.systers_user)
        community.add_member(systersuser)
        community.save()
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_post_user_profile_view(self):
        """Test POST user profile"""
        self.client.login(username='foo', password='foobar')
        profile_url = reverse('user_profile', kwargs={'username': 'foo'})
        response = self.client.post(profile_url, data={'first_name': 'Foo'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/users/foo/'))
        user = User.objects.get(username='foo')
        self.assertEqual(user.first_name, 'Foo')

        bar_profile_url = reverse('user_profile', kwargs={'username': 'bar'})
        response = self.client.post(bar_profile_url, data={})
        self.assertEqual(response.status_code, 404)

        self.user.is_superuser = True
        self.user.save()
        user = User.objects.create_user(username='bar', password='foobar')
        SystersUser.objects.get(user=user)
        response = self.client.post(bar_profile_url,
                                    data={'first_name': 'Bar'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/users/bar/'))
        user = User.objects.get(username='bar')
        self.assertEqual(user.first_name, 'Bar')

    def test_user_profile_view_templates(self):
        """Test the usage of templates and content in UserProfileView"""
        profile_url = reverse('user_profile', kwargs={'username': 'foo'})
        self.client.login(username='foo', password='foobar')
        response = self.client.get(profile_url)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
        self.assertContains(response, "Edit my profile")
        self.assertContains(response, "/users/foo/")

        self.user.is_superuser = True
        self.user.save()
        User.objects.create_user(username='bar', password='foobar')
        bar_profile_url = reverse('user_profile', kwargs={'username': 'bar'})
        response = self.client.get(bar_profile_url)
        self.assertContains(response, "Edit profile of bar")
        self.assertContains(response, "/users/bar/")


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


class UserFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()

    def test_user_form(self):
        """Test the combined User and SystersUser form"""
        form = UserForm(instance=self.user)
        self.assertEqual(type(form.systers_user_form), SystersUserForm)
        data = {'first_name': 'Foo',
                'last_name': 'Bar',
                'blog_url': 'http://example.com/'}
        form = UserForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.first_name, 'Foo')
        self.assertEqual(self.user.last_name, 'Bar')
        systers_user = SystersUser.objects.get()
        self.assertEqual(systers_user.blog_url, 'http://example.com/')
