from cities_light.models import Country, City
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.views.generic import TemplateView

from blog.mixins import ResourceTypesMixin
from blog.models import ResourceType
from community.models import Community
from users.models import SystersUser


class ResourceTypesMixinTestCase(TestCase):
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

    def test_get_context_data_empty(self):
        """Test mixin and no resource type objects"""
        class DummyView(ResourceTypesMixin, TemplateView):
            template_name = "dummy"

        request = self.factory.get("/dummy/")
        view = DummyView.as_view()
        response = view(request)
        context = response.context_data
        self.assertSequenceEqual(context.get('resource_types'), [])

    def test_get_context_data(self):
        """Test mixin with 2 resource types"""
        class DummyView(ResourceTypesMixin, TemplateView):
            template_name = "dummy"

        resource_type1 = ResourceType.objects.create(name="foo")
        resource_type2 = ResourceType.objects.create(name="bar")
        request = self.factory.get("/dummy/")
        view = DummyView.as_view()
        response = view(request)
        context = response.context_data
        self.assertCountEqual(context.get('resource_types'),
                              [resource_type1, resource_type2])
