from cities_light.models import Country, City
from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Tag, ResourceType, News, Resource
from community.models import Community
from users.models import SystersUser


class TagModelTestCase(TestCase):
    def test_str(self):
        """Test Tag object string representation"""
        tag = Tag.objects.create(name="Foo")
        self.assertEqual(str(tag), "Foo")


class ResourceTypeModelTestCase(TestCase):
    def test_str(self):
        """Test ResourceType object string representation"""
        resource_type = ResourceType.objects.create(name="Foo")
        self.assertEqual(str(resource_type), "Foo")


class NewsModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_str(self):
        """Test News object string representation"""
        news = News.objects.create(slug="foonews", title="Bar",
                                   author=self.systers_user,
                                   content="Hi there!",
                                   community=self.community)
        self.assertEqual(str(news), "Bar of Foo Community")


class ResourceModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_unicode(self):
        """Test Resource object string representation"""
        resource = Resource.objects.create(slug="fooresource", title="Bar",
                                           author=self.systers_user,
                                           content="Hi there!",
                                           community=self.community)
        self.assertEqual(str(resource), "Bar of Foo Community")
