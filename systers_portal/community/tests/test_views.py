from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.test import TestCase, Client

from community.models import Community, CommunityPage, JoinRequest
from community.signals import manage_community_groups, remove_community_groups
from users.models import SystersUser


class ViewCommunityProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_view_community_profile_view(self):
        """Test view community profile view"""
        url = reverse('view_community_profile', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/view_profile.html')
        self.assertTemplateUsed(response, 'community/snippets/footer.html')

        nonexistent_url = reverse('view_community_profile',
                                  kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class EditCommunityProfileViewTestCase(TestCase):
    def setUp(self):
        post_save.connect(manage_community_groups, sender=Community,
                          dispatch_uid="manage_groups")
        post_delete.connect(remove_community_groups, sender=Community,
                            dispatch_uid="remove_groups")
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)
        self.client = Client()

    def test_get_edit_community_profile_view(self):
        """Test GET edit community profile"""
        url = reverse('edit_community_profile', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/edit_profile.html')
        self.assertTemplateUsed(response, 'community/snippets/footer.html')
        self.assertContains(response, "/community/foo/profile/")
        self.assertContains(response, "Foo, an Anita Borg Systers Community")

        new_user = User.objects.create_user(username='bar', password='foobar')
        SystersUser.objects.get(user=new_user)
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        new_user.is_superuser = True
        new_user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        nonexistent_url = reverse('edit_community_profile',
                                  kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_post_edit_community_profile_view(self):
        """Test POST edit community profile"""
        url = reverse('edit_community_profile', kwargs={'slug': 'foo'})
        data = {'name': 'Bar',
                'slug': 'bar',
                'order': 1}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/bar/profile/'))

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 404)

        url = reverse('edit_community_profile', kwargs={'slug': 'bar'})
        user = User.objects.create_user(username='bar', password='foobar')
        SystersUser.objects.get(user=user)
        self.client.login(username='bar', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)
        user.is_superuser = True
        user.save()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/bar/profile/'))


class CommunityPageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_join_button_snippet(self):
        """Test the rendering of join button snippet"""
        url = reverse('view_community_main_page', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertNotContains(response, "Join Community")

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Transfer ownership")

        user = User.objects.create_user(username='bar', password='foobar')
        systers_user_bar = SystersUser.objects.get(user=user)
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Join Community")

        self.community.add_member(systers_user_bar)
        self.community.save()
        response = self.client.get(url)
        self.assertContains(response, "Leave Community")

        self.community.remove_member(systers_user_bar)
        self.community.save()
        join_request = JoinRequest.objects.create(user=systers_user_bar,
                                                  community=self.community)
        response = self.client.get(url)
        self.assertContains(response, "Cancel request")

        join_request.is_approved = True
        join_request.save()
        response = self.client.get(url)
        self.assertContains(response, "Join Community")

    def test_actions_sidebar_snippet(self):
        """Test the rendering of actions sidebar snippet"""
        url = reverse('view_community_main_page', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertNotContains(response, "Community Actions")

        User.objects.create_user(username='bar', password='foobar')
        # systers_user_bar = SystersUser.objects.get(user=user)
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Community Actions")
        self.assertContains(response, "View Community Profile")
        self.assertNotContains(response, "Edit Community Profile")
        self.assertNotContains(response, "Manage Community Pages")
        self.assertNotContains(response, "Manage Community Users")
        self.assertNotContains(response, "Show Join Requests")

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Community Actions")
        self.assertContains(response, "View Community Profile")
        self.assertContains(response, "Edit Community Profile")
        self.assertContains(response, "Manage Community Pages")
        self.assertContains(response, "Manage Community Users")
        self.assertContains(response, "Show Join Requests")

    def test_get_view_community_main_page(self):
        """Test GET request to land on community main page, which is in fact
        a community page view"""
        url = reverse('view_community_main_page', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/base.html')
        self.assertEqual(response.context['active_page'], 'news')

        CommunityPage.objects.create(slug="page", title="Page", order=1,
                                     author=self.systers_user,
                                     community=self.community)
        response = self.client.get(url)
        self.assertEqual(response.context['active_page'], 'page')

    def test_get_community_page(self):
        """Test GET request to view a community page"""
        CommunityPage.objects.create(slug="page", title="Page", order=1,
                                     author=self.systers_user,
                                     community=self.community)
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/base.html')
        self.assertEqual(response.context['active_page'], 'page')

        CommunityPage.objects.create(slug="page2", title="Page2", order=2,
                                     author=self.systers_user,
                                     community=self.community)
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page2'})
        response = self.client.get(url)
        self.assertEqual(response.context['active_page'], 'page2')
