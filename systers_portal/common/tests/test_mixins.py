from cities_light.models import Country, City
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, RequestFactory
from django.views.generic import TemplateView

from common.mixins import UserDetailsMixin
from community.models import Community
from users.models import SystersUser


class UserDetailsMixinTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_get_context_data_no_community(self):
        """Test mixin with no community set"""
        class DummyView(UserDetailsMixin, TemplateView):
            template_name = "dummy"

        request = self.factory.get("/dummy/")
        request.user = self.user
        view = DummyView.as_view()
        self.assertRaises(ImproperlyConfigured, view, request)

    def test_get_context_data_no_user(self):
        """Test mixin for anonymous user"""
        class DummyView(UserDetailsMixin, TemplateView):
            template_name = "dummy"

        request = self.factory.get("/dummy/")
        request.user = AnonymousUser
        view = DummyView.as_view()
        response = view(request)
        context = response.context_data
        self.assertEqual(context.get('is_member'), None)
        self.assertEqual(context.get('join_request'), None)

    def test_get_context_data_member(self):
        """Test mixin for a user that is member of community"""
        class DummyView(UserDetailsMixin, TemplateView):
            template_name = "dummy"
            community = Community.objects.get()

        request = self.factory.get('/dummy/')
        request.user = self.user
        view = DummyView.as_view()
        response = view(request)
        context = response.context_data
        self.assertTrue(context.get('is_member'))
        self.assertEqual(context.get('join_request'), None)
