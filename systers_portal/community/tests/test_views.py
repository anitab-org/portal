from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.test import TestCase

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


class CommunityLandingViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_get_community_landing_view(self):
        """Test GET request to community landing with and without a page"""
        url = reverse("view_community_landing", kwargs={"slug": "foo"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith("/news/"))

        CommunityPage.objects.create(slug="page", title="Page", order=1,
                                     author=self.systers_user,
                                     community=self.community)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith("/p/page/"))


class CommunityPageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)
        CommunityPage.objects.create(slug="page", title="Page", order=1,
                                     author=self.systers_user,
                                     community=self.community)

    def test_get_community_page_view(self):
        """Test GET request to view a community page"""
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/page.html')
        self.assertEqual(response.context['active_page'], 'page')

        CommunityPage.objects.create(slug="page2", title="Page2", order=2,
                                     author=self.systers_user,
                                     community=self.community)
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page2'})
        response = self.client.get(url)
        self.assertEqual(response.context['active_page'], 'page2')

    def test_join_button_snippet(self):
        """Test the rendering of join button snippet"""
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page'})
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

    def test_community_sidebar_snippet(self):
        """Test the rendering of community sidebar snippet"""
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page'})
        response = self.client.get(url)
        self.assertNotContains(response, "Community Actions")

        User.objects.create_user(username='bar', password='foobar')
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Community Actions")
        self.assertContains(response, "View Community Profile")
        self.assertNotContains(response, "Edit Community Profile")
        self.assertNotContains(response, "Manage Community Users")
        self.assertNotContains(response, "Show Join Requests")

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Community Actions")
        self.assertContains(response, "View Community Profile")
        self.assertContains(response, "Edit Community Profile")
        self.assertContains(response, "Manage Community Users")
        self.assertContains(response, "Show Join Requests")

    def test_page_sidebar_snippet(self):
        """Test the rendering of page actions snippet"""
        url = reverse('view_community_page', kwargs={'slug': 'foo',
                                                     'page_slug': 'page'})
        response = self.client.get(url)
        self.assertNotContains(response, "Page Actions")
        User.objects.create_user(username='bar', password='foobar')
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertNotContains(response, "Page Actions")
        self.assertNotContains(response, "Add page")
        self.assertNotContains(response, "Edit current page")
        self.assertNotContains(response, "Delete current page")

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertContains(response, "Page Actions")
        self.assertContains(response, "Add page")
        self.assertContains(response, "Edit current page")
        self.assertContains(response, "Delete current page")


class AddCommunityPageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_get_add_community_page_view(self):
        """Test GET request to add a new community page"""
        url = reverse("add_community_page", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/add_post.html')

        new_user = User.objects.create_user(username="bar", password="foobar")
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        group = Group.objects.get(name="Foo: Content Manager")
        new_user.groups.add(group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_add_community_page_view(self):
        """Test POST request to add a new community page"""
        url = reverse("add_community_page", kwargs={'slug': 'foo'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data={"slug": "baz"})
        self.assertEqual(response.status_code, 200)

        data = {'slug': 'bar',
                'title': 'Bar',
                'order': 1,
                'content': "Rainbows and ponies"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        page = CommunityPage.objects.get()
        self.assertEqual(page.title, 'Bar')
        self.assertEqual(page.author, self.systers_user)
        self.assertEqual(page.community, self.community)


class EditCommunityPageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)
        self.page = CommunityPage.objects.create(slug="bar", title="Bar",
                                                 order=1,
                                                 author=self.systers_user,
                                                 content="Hi there!",
                                                 community=self.community)

    def test_get_edit_community_page_view(self):
        """Test GET to edit community page"""
        url = reverse('edit_community_page',
                      kwargs={'slug': 'foo', 'page_slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_community_page',
                      kwargs={'slug': 'foo', 'page_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_community_resource_view(self):
        """Test POST to edit community page"""
        url = reverse('edit_community_page',
                      kwargs={'slug': 'foo', 'page_slug': 'foo'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_community_page',
                      kwargs={'slug': 'foo', 'page_slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        data = {'slug': 'another',
                'title': 'Baz',
                'order': 2,
                'content': "Rainbows and ponies"}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith("/p/another/"))


class DeleteCommunityPageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)
        CommunityPage.objects.create(slug="bar", title="Bar", order=1,
                                     author=self.systers_user,
                                     content="Hi there!",
                                     community=self.community)

    def test_get_delete_community_page_view(self):
        """Test GET to confirm deletion of a community page"""
        url = reverse("delete_community_page",
                      kwargs={'slug': 'foo', 'page_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_community_resource_view(self):
        """Test POST to delete a community page"""
        url = reverse("delete_community_page",
                      kwargs={'slug': 'foo', 'page_slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertSequenceEqual(CommunityPage.objects.all(), [])


class CommunityJoinRequestListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_get_community_join_request_list_view(self):
        """Test GET to get the list on not yet approved community join
        requests."""
        url = reverse("view_community_join_request_list",
                      kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<th>1</th>")

        user = User.objects.create_user(username="rainbow", password="foobar")
        systers_user = SystersUser.objects.get(user=user)
        JoinRequest.objects.create(user=systers_user,
                                   community=self.community)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<th>1</th>")
        self.assertContains(response, 'rainbow')


class ApproveCommunityJoinRequestViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_approve_community_join_request_view_redundant(self):
        """Test GET request to approve a community join request for a user
        who is already a member."""
        url = reverse("approve_community_join_request",
                      kwargs={'slug': 'foo', 'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        join_request = JoinRequest.objects.create(user=self.systers_user,
                                                  community=self.community)
        url = reverse("approve_community_join_request",
                      kwargs={'slug': 'foo', 'pk': join_request.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'community/foo/join_requests/')
        for message in response.context['messages']:
            self.assertEqual(message.tags, "info")
            self.assertTrue(
                'foo is already a member of Foo community' in message.message)
        self.assertQuerysetEqual(JoinRequest.objects.all(), [])

    def test_approve_community_join_request_view_new_user(self):
        """Test GET request to approve a community join request and add a new
        member to the community"""
        self.client.login(username='foo', password='foobar')
        user = User.objects.create(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        join_request = JoinRequest.objects.create(user=systers_user,
                                                  community=self.community)
        self.assertFalse(systers_user.is_member(self.community))
        url = reverse("approve_community_join_request",
                      kwargs={'slug': 'foo', 'pk': join_request.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'community/foo/join_requests/')
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'bar successfully became a member of Foo community'
                in message.message)
        self.assertTrue(systers_user.is_member(self.community))
        self.assertTrue(JoinRequest.objects.get().is_approved)

    def test_approve_community_join_request_view_multiple(self):
        """Test GET request to approve multiple community join request from a
        user. This scenario might happen if the join requests are created
        manually from the admin panel."""
        self.client.login(username='foo', password='foobar')
        user = User.objects.create(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        JoinRequest.objects.create(user=systers_user, community=self.community)
        join_request = JoinRequest.objects.create(user=systers_user,
                                                  community=self.community)
        self.assertFalse(systers_user.is_member(self.community))
        url = reverse("approve_community_join_request",
                      kwargs={'slug': 'foo', 'pk': join_request.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'community/foo/join_requests/')
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'bar successfully became a member of Foo community'
                in message.message)
        self.assertTrue(systers_user.is_member(self.community))
        join_requests = JoinRequest.objects.all()
        for join_request in join_requests:
            self.assertTrue(join_request.is_approved)


class RejectCommunityJoinRequestViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_reject_community_join_request_view_redundant(self):
        """Test GET request to try to reject a community join request for a
        user who is already a member. This scenario might happen if the join
        request is created manually from the admin panel."""
        url = reverse("reject_community_join_request",
                      kwargs={'slug': 'foo', 'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        join_request = JoinRequest.objects.create(user=self.systers_user,
                                                  community=self.community)
        url = reverse("reject_community_join_request",
                      kwargs={'slug': 'foo', 'pk': join_request.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'community/foo/join_requests/')
        for message in response.context['messages']:
            self.assertEqual(message.tags, "info")
            self.assertTrue(
                'foo is already a member of Foo community.' in message.message)
        self.assertQuerysetEqual(JoinRequest.objects.all(), [])

    def test_reject_community_join_request_view_multiple(self):
        """Test GET request to reject all community join requests"""
        self.client.login(username='foo', password='foobar')
        user = User.objects.create(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        join_request = JoinRequest.objects.create(user=systers_user,
                                                  community=self.community)
        self.assertFalse(systers_user.is_member(self.community))
        url = reverse("reject_community_join_request",
                      kwargs={'slug': 'foo', 'pk': join_request.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'community/foo/join_requests/')
        for message in response.context['messages']:
            self.assertEqual(message.tags, "info")
            self.assertTrue(
                'bar was successfully rejected to become a member of Foo'
                ' community.' in message.message)
        self.assertFalse(systers_user.is_member(self.community))
        self.assertSequenceEqual(JoinRequest.objects.all(), [])


class RequestJoinCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_request_join_community_view(self):
        """Test GET request to join a community"""
        url = reverse("request_join_community", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        user = User.objects.create_user(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        self.client.login(username="bar", password="foobar")
        nonexistent_url = reverse("request_join_community",
                                  kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(JoinRequest.objects.get())
        self.assertFalse(JoinRequest.objects.get().is_approved)
        self.assertFalse(systers_user.is_member(self.community))
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'You have successfully requested to join Foo community. '
                'In a short while someone will review your request.'
                in message.message)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JoinRequest.objects.all().count(), 1)
        self.assertFalse(JoinRequest.objects.get().is_approved)
        self.assertFalse(systers_user.is_member(self.community))
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You have already requested to join Foo community. Be patient '
                'until someone reviews your request.' in message.message)

        join_request = JoinRequest.objects.get()
        join_request.approve()
        self.community.add_member(systers_user)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JoinRequest.objects.all().count(), 1)
        self.assertTrue(JoinRequest.objects.get().is_approved)
        self.assertTrue(systers_user.is_member(self.community))
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You are already a member of Foo community. No need to '
                'request to join the community.' in message.message)


class CancelCommunityJoinRequestView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_cancel_community_join_request(self):
        """Test GET request to cancel a join request to a community"""
        url = reverse("cancel_community_join_request", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        user = User.objects.create_user(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        self.client.login(username="bar", password="foobar")
        nonexistent_url = reverse("request_join_community",
                                  kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'There is no pending request to join Foo community.'
                in message.message)

        JoinRequest.objects.create(user=systers_user, community=self.community)
        self.assertEqual(JoinRequest.objects.all().count(), 1)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JoinRequest.objects.all().count(), 0)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Your request to join Foo community was canceled.'
                in message.message)

        self.community.add_member(systers_user)
        self.community.save()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You are already a member of Foo community. There are no '
                'pending join requests.' in message.message)


class LeaveCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_leave_community(self):
        """Test GET request to leave a community"""
        url = reverse("leave_community", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username="foo", password="foobar")
        nonexistent_url = reverse("leave_community", kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You are the Foo community admin. If you want to leave the '
                'community, first transfer community ownership to another '
                'user.' in message.message)

        user = User.objects.create_user(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        self.client.login(username="bar", password="foobar")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                "You are not a member of Foo community, hence you can't leave "
                "the community." in message.message)

        self.community.add_member(systers_user)
        self.community.save()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                "You have successfully left Foo community." in message.message)
        self.assertFalse(systers_user.is_member(self.community))
