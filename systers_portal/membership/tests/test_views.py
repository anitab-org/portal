from cities_light.models import Country, City
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase

from community.constants import USER_CONTENT_MANAGER
from community.models import Community
from membership.models import JoinRequest
from users.models import SystersUser


class CommunityJoinRequestListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        self.assertRedirects(response, '/community/foo/join_requests/')
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
        self.assertRedirects(response, '/community/foo/join_requests/')
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
        self.assertRedirects(response, '/community/foo/join_requests/')
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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        self.assertRedirects(response, '/community/foo/join_requests/')
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
        self.assertRedirects(response, '/community/foo/join_requests/')
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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_request_join_community_view(self):
        """Test GET request to join a community"""
        current_url = reverse("view_community_news_list", kwargs={'slug': 'foo'})
        url = reverse("request_join_community", kwargs={'slug': 'foo'})
        response = self.client.get(url, {'current_url': current_url})
        self.assertEqual(response.status_code, 403)

        user = User.objects.create_user(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        self.client.login(username="bar", password="foobar")
        nonexistentnews_url = reverse("view_community_news_list", kwargs={'slug': 'new'})
        nonexistent_url = reverse("request_join_community",
                                  kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_url, {'current_url': nonexistentnews_url})
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url, {'current_url': current_url}, follow=True)
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

        response = self.client.get(url, {'current_url': current_url}, follow=True)
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
        response = self.client.get(url, {'current_url': current_url}, follow=True)
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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_cancel_community_join_request(self):
        """Test GET request to cancel a join request to a community"""
        current_url = reverse("view_community_news_list", kwargs={'slug': 'foo'})
        url = reverse("cancel_community_join_request", kwargs={'slug': 'foo'})
        response = self.client.get(url, {'current_url': current_url})
        self.assertEqual(response.status_code, 403)

        user = User.objects.create_user(username='bar', password='foobar')
        systers_user = SystersUser.objects.get(user=user)
        self.client.login(username="bar", password="foobar")
        nonexistentnews_url = reverse("view_community_news_list", kwargs={'slug': 'new'})
        nonexistent_url = reverse("request_join_community",
                                  kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_url, {'current_url': nonexistentnews_url})
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url, {'current_url': current_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'There is no pending request to join Foo community.'
                in message.message)

        JoinRequest.objects.create(user=systers_user, community=self.community)
        self.assertEqual(JoinRequest.objects.all().count(), 1)
        response = self.client.get(url, {'current_url': current_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JoinRequest.objects.all().count(), 0)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Your request to join Foo community was canceled.'
                in message.message)

        self.community.add_member(systers_user)
        self.community.save()
        response = self.client.get(url, {'current_url': current_url}, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You are already a member of Foo community. There are no '
                'pending join requests.' in message.message)


class LeaveCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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


class TransferOwnershipViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_get_transfer_ownership_view(self):
        """Test GET request to transfer ownership of a community"""
        url = reverse('transfer_ownership', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        User.objects.create_user(username="bar", password="foobar")
        self.client.login(username="bar", password="foobar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        nonexistent_url = reverse("transfer_ownership", kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        self.client.login(username="foo", password="foobar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_transfer_ownership_view(self):
        """Test POST request to transfer ownership of a community"""
        url = reverse('transfer_ownership', kwargs={'slug': 'foo'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        bar_user = User.objects.create_user(username="bar", password="foobar")
        bar_systers_user = SystersUser.objects.get(user=bar_user)
        self.client.login(username="bar", password="foobar")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        nonexistent_url = reverse("transfer_ownership", kwargs={'slug': 'new'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        self.client.login(username="foo", password="foobar")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        response = self.client.post(url, data={'new_admin': 42})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice.")

        self.community.add_member(bar_systers_user)
        self.community.save()

        response = self.client.post(url, follow=True,
                                    data={'new_admin': bar_systers_user.pk},)
        self.assertEqual(response.status_code, 200)
        community = Community.objects.get(name="Foo")
        self.assertEqual(community.admin, bar_systers_user)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                "The new Foo community admin is bar. You no longer have any "
                "admin permissions in this community." in message.message)


class RemoveCommunityMemberViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_remove_community_member_view(self):
        """Test GET request to remove a community member"""
        url = reverse('remove_member',
                      kwargs={'slug': 'foo', 'username': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        admin_url = reverse('remove_member',
                            kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(admin_url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                "foo is the Foo community admin. It is not possible to remove "
                "the admin from community members." in message.message)

        bar_user = User.objects.create_user(username="bar", password="foobar")
        bar_systers_user = SystersUser.objects.get(user=bar_user)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                "bar is not a member of Foo community, hence the user can't "
                "be removed from the community members." in message.message)

        self.community.add_member(bar_systers_user)
        self.community.save()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue("bar is no longer member of Foo community."
                            in message.message)

        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.community.add_member(bar_systers_user)
        self.community.save()
        group = Group.objects.get(name=USER_CONTENT_MANAGER.format("Foo"))
        bar_user.groups.add(group)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue("You have successfully left Foo community."
                            in message.message)
