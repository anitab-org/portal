from cities_light.models import City, Country
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.test import TestCase

from community.constants import USER_CONTENT_MANAGER
from community.models import Community, CommunityPage, RequestCommunity
from community.signals import manage_community_groups, remove_community_groups
from membership.models import JoinRequest
from users.models import SystersUser


class RequestCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)

    def test_get_request_community_view(self):
        url = reverse('request_community')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/request_community.html")
        self.assertContains(response, "Request a new community")

    def test_post_request_community_view(self):
        url = reverse('request_community')
        # Test without log in, no data
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)
        # Test with login, invalid data
        self.client.login(username='foo', password='foobar')
        invalid_data = {'name': 'Bar',
                        'slug': 'foo',
                        'order': '1',
                        'user': self.systers_user}
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        # Test with login but valid data
        self.client.login(username='foo', password='foobar')
        valid_data = {'name': 'Bar', 'slug': 'foo', 'order': '1', 'user': self.systers_user,
                      'location': self.location.id, 'is_member': 'Yes', 'email': 'foo@bar.com',
                      'type_community': 'Other',
                      'community_channel': 'Existing Social Media Channels ',
                      'demographic_target_count': 'Foobarbar', 'purpose': 'foopurpose',
                      'is_avail_volunteer': 'Yes', 'count_avail_volunteer': '15',
                      'content_developer': 'foobar', 'selection_criteria': 'foobarbar',
                      'is_real_time': 'foofoobar'
                      }
        response = self.client.post(url, data=valid_data)
        self.assertEqual(response.status_code, 302)
        # Test for showing the user's community requests once requested
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Community requests")
        self.assertContains(response, "Bar")


class EditCommunityRequestViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, location=self.location, is_member='Yes',
            type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_get_edit_community_request_view(self):
        url = reverse('edit_community_request', kwargs={'slug': 'foo'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test once logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'community/edit_community_request.html')
        self.assertContains(response, "Edit Foo")
        # Test if a new user other than requestor accesses the url
        new_user = User.objects.create_user(username='bar', password='foobar')
        SystersUser.objects.get(user=new_user)
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if a superuser accesses the url
        new_user.is_superuser = True
        new_user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test if the url doesn't exist
        nonexistent_url = reverse('edit_community_request',
                                  kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_post_edit_community_request_view(self):
        url = reverse('edit_community_request', kwargs={'slug': 'foo'})
        # Test without logging in,and posting data
        valid_data = {'name': 'Bar', 'slug': 'bar', 'order': '1',
                      'location': self.location.id, 'user': self.systers_user,
                      'is_member': 'Yes', 'email': 'foo@bar.com', 'type_community': 'Other',
                      'community_channel': 'Existing Social Media Channels ',
                      'demographic_target_count': 'Foobarbar', 'purpose': 'foopurpose',
                      'is_avail_volunteer': 'Yes', 'count_avail_volunteer': '15',
                      'content_developer': 'foobar', 'selection_criteria': 'foobarbar',
                      'is_real_time': 'foofoobar'
                      }
        response = self.client.post(url, data=valid_data)
        self.assertEqual(response.status_code, 403)
        # Test with logging in, posting data, redirected to viewing the request
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/bar/view_request/'))
        # Test for non existent url, slug changed to bar.
        response = self.client.post(url, data=valid_data)
        self.assertEqual(response.status_code, 404)
        # Test if a user other than requestor posts the data
        url = reverse('edit_community_request', kwargs={'slug': 'bar'})
        user = User.objects.create_user(username='bar', password='foobar')
        SystersUser.objects.get(user=user)
        self.client.login(username='bar', password='foobar')
        response = self.client.post(url, data=valid_data)
        self.assertEqual(response.status_code, 403)
        # Test if a superuser posts the data
        user.is_superuser = True
        user.save()
        response = self.client.post(url, data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/bar/view_request/'))


class ViewCommunityRequestViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, location=location, is_member='Yes',
            type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_view_community_request_view(self):
        """Test view community profile view"""
        url = reverse('view_community_request', kwargs={'slug': 'foo'})
        # Test for accessing the url without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test for accessing the url after logging in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "community/view_community_request.html")
        self.assertContains(response, "Foo")
        self.assertContains(response, "Edit community request")
        # Approved request cannot be edited
        self.community_request.is_approved = True
        self.community_request.save()
        response = self.client.get(url)
        self.assertNotContains(response, "Edit community request")
        # Test if a user other than requestor accesses the url
        new_user = User.objects.create_user(username='bar', password='foobar')
        SystersUser.objects.get(user=new_user)
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if a superuser accesses the url, approved requests cannot be edited
        new_user.is_superuser = True
        new_user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "community/view_community_request.html")
        self.assertContains(response, "Foo")
        self.assertNotContains(response, "Edit community request")
        # Test if a superuser accesses the url, unapproved requests can be edited
        self.community_request.is_approved = False
        self.community_request.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Foo")
        self.assertContains(response, "Edit community request")
        # Test for non existent url
        nonexistent_url = reverse('view_community_profile',
                                  kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class NewCommunityRequestsListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, location=location, is_member='Yes',
            type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_new_community_requests_list_view(self):
        url = reverse('unapproved_community_requests')
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a superuser
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "community/new_community_requests.html")
        self.assertContains(response, "Foo")
        self.assertSequenceEqual(RequestCommunity.objects.filter(
            is_approved=False), [self.community_request])
        self.assertContains(response, "Requested by")


class RejectRequestCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.password = 'foobar'
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, location=location, is_member='Yes',
            type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_get_reject_request_community_view(self):
        url = reverse('reject_community_request', kwargs={'slug': 'foo'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a superuser
        admin = User.objects.create_superuser(
            username='foo-bar', email='abcd@gmail.com', password=self.password)
        self.admin_systers_user = SystersUser.objects.get(user=admin)
        self.client.login(username='foo-bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "community/confirm_reject_request_community.html")
        # Test for non existent url
        nonexistent_url = reverse('reject_community_request',
                                  kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_post_reject_request_community_view(self):
        url = reverse('reject_community_request', kwargs={'slug': 'foo'})
        # Test without logging in
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # Test if superuser posts
        admin = User.objects.create_superuser(
            username='foo-bar', email='abcd@gmail.com', password=self.password)
        self.admin_systers_user = SystersUser.objects.get(user=admin)
        self.client.login(username='foo-bar', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('community/community_requests'))
        # Test non existent url
        nonexistent_url = reverse(
            "reject_community_request", kwargs={'slug': 'bar'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class ApproveRequestCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.password = 'foobar'
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, location=self.location, is_member='Yes',
            type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_approve_request_community_view_base(self):
        url = reverse('approve_community_request', kwargs={'slug': 'foo'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a superuser
        admin = User.objects.create_superuser(
            username='foo-bar', email='abcd@gmail.com', password=self.password)
        SystersUser.objects.get(user=admin)
        self.client.login(username='foo-bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/foo/'))
        # Test for non existent url
        nonexistent_url = reverse('approve_community_request',
                                  kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_approve_request_community_view_order(self):
        # Test if order of request already exists in Community, redirect to edit page.
        url = reverse('approve_community_request', kwargs={'slug': 'foo'})
        admin = User.objects.create_superuser(
            username='foo-bar', email='abcd@gmail.com', password=self.password)
        admin_systers_user = SystersUser.objects.get(user=admin)
        Community.objects.create(name="FooBarComm", slug="foobar",
                                 order=1, location=self.location, admin=admin_systers_user)
        self.client.login(username='foo-bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/foo/edit_request/'))
        # Test if order is None
        self.community_request.order = None
        self.community_request.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/foo/edit_request/'))

    def test_approve_request_community_view_slug(self):
        """Test if slug already exists in Community, redirect to edit page."""
        url = reverse('approve_community_request', kwargs={'slug': 'foo'})
        admin = User.objects.create_superuser(
            username='foo-bar', email='abcd@gmail.com', password=self.password)
        admin_systers_user = SystersUser.objects.get(user=admin)
        Community.objects.create(name="FooBarComm", slug="foo",
                                 order=2, location=self.location, admin=admin_systers_user)
        self.client.login(username='foo-bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/community/foo/edit_request/'))


class ViewCommunityProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=self.location,
                                                  admin=self.systers_user)

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
                'order': 1,
                'location': self.location.id}
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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
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


class AddCommunityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)

    def test_get_add_community_view(self):
        """Test GET request to add a new community"""
        url = reverse("add_community")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        admin = User.objects.create_superuser(username='foo-bar',
                                              email='abcd@gmail.com', password='foobar')
        self.admin_systers_user = SystersUser.objects.get(user=admin)
        self.client.login(username='foo-bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_add_community_view(self):
        """Test POST request to add a new community"""
        url = reverse("add_community")
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(
            url, data={"slug": "baz", "name": 'FoobarCommunity'})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        data = {'name': 'Bar',
                'slug': 'foo',
                'order': '1',
                'admin': self.systers_user}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

        admin = User.objects.create_superuser(username='foo-bar',
                                              email='abcd@gmail.com', password='foobar')
        self.admin_systers_user = SystersUser.objects.get(user=admin)
        self.client.login(username='foo-bar', password='foobar')
        data = {'name': 'Bar',
                'slug': 'foo',
                'order': '1',
                'location': self.location.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)


class AddCommunityPageViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
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
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
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


class CommunityUsersViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
        CommunityPage.objects.create(slug="bar", title="Bar", order=1,
                                     author=self.systers_user,
                                     content="Hi there!",
                                     community=self.community)

    def test_community_users_view(self):
        """Test GET request to list all community members according to various
        levels of permissions."""
        url = reverse('community_users', kwargs={'slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('community_users', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/users.html")
        self.assertContains(response, '<td><a href="/users/foo/">foo</a></td>')
        self.assertContains(response, 'Permissions')
        self.assertNotContains(response, 'Remove')

        new_user = User.objects.create_user(username='baz', password='foobar')
        new_systers_user = SystersUser.objects.get(user=new_user)
        self.client.login(username='baz', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.community.add_member(new_systers_user)
        self.community.save()
        group = Group.objects.get(name=USER_CONTENT_MANAGER.format("Foo"))
        new_user.groups.add(group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/users.html")
        self.assertContains(response, '<td><a href="/users/baz/">baz</a></td>')
        self.assertContains(response, '<td><a href="/users/foo/">foo</a></td>')
        self.assertContains(response, 'Permissions')
        self.assertContains(response, 'Leave')

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Remove')
        self.assertContains(response, 'Transfer ownership')


class UserPermissionGroupsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_get_user_permissions_groups(self):
        """Test GET request to user permission groups"""
        non_existent_url = reverse('user_permission_groups',
                                   kwargs={'slug': 'bar', 'username': 'bar'})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, 403)

        url = reverse('user_permission_groups', kwargs={'slug': 'foo',
                                                        'username': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        User.objects.create_user(username='bar', password='foobar')
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['form'].fields['groups'].initial, [])

        content_manager_group = Group.objects.get(name="Foo: Content Manager")
        self.systers_user.join_group(content_manager_group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['form'].fields['groups'].initial,
            [content_manager_group.pk])

    def test_post_user_permissions_groups(self):
        """Test POST request to user permission groups"""
        url = reverse('user_permission_groups', kwargs={'slug': 'foo',
                                                        'username': 'foo'})
        self.client.login(username='foo', password='foobar')
        group = Group.objects.get(name="Foo: Content Manager")
        self.assertFalse(self.systers_user.is_group_member(group))
        response = self.client.post(url, data={'groups': [group.pk]})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.systers_user.is_group_member(group))

        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.systers_user.is_group_member(group))


class CommunitySearchViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Test', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Test Country', continent='AS')
        location = City.objects.create(name='Test City', display_name='Test City',
                                       latitude=20, longitude=20,
                                       country=country)
        self.community1 = Community.objects.create(name="Foo", slug="foo",
                                                   order=1, location=location,
                                                   admin=self.systers_user)
        self.community2 = Community.objects.create(name="Bar", slug="bar",
                                                   order=2, location=location,
                                                   admin=self.systers_user)
        self.community3 = Community.objects.create(name="Baz", slug="baz",
                                                   order=3, location=location,
                                                   admin=self.systers_user)

    def test_search_results(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/community_search.html')
        self.assertEqual(len(response.context['communities']), 3)

        response = self.client.get('/community/search/?query=')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/community_search.html')
        self.assertEqual(len(response.context['communities']), 3)
        self.assertContains(response, "Foo")
        self.assertContains(response, "Bar")
        self.assertContains(response, "Baz")

        response = self.client.get('/community/search/?query=B')
        self.assertEqual(len(response.context['communities']), 2)
        self.assertContains(response, "Bar")
        self.assertContains(response, "Baz")
        self.assertNotContains(response, "Foo")

        response = self.client.get('/community/search/?query=Ba')
        self.assertEqual(len(response.context['communities']), 2)
        self.assertContains(response, "Bar")
        self.assertContains(response, "Baz")
        self.assertNotContains(response, "Foo")

        response = self.client.get('/community/search/?query=Bar')
        self.assertEqual(len(response.context['communities']), 1)
        self.assertContains(response, "Bar")
        self.assertNotContains(response, "Baz")
        self.assertNotContains(response, "Foo")

        response = self.client.get('/community/search/?query=F')
        self.assertEqual(len(response.context['communities']), 1)
        self.assertNotContains(response, "Bar")
        self.assertNotContains(response, "Baz")
        self.assertContains(response, "Foo")

        response = self.client.get('/community/search/?query=Foooo')
        self.assertEqual(len(response.context['communities']), 0)
        self.assertNotContains(response, "Bar")
        self.assertNotContains(response, "Baz")
        self.assertNotContains(response, "Foo")
