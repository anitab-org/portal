from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Tag, ResourceType, News, Resource
from community.models import Community
from users.models import SystersUser


class TagModelTestCase(TestCase):
    def test_unicode(self):
        """Test Tag object str/unicode representation"""
        tag = Tag.objects.create(name="Foo")
        self.assertEqual(unicode(tag), "Foo")


class ResourceTypeModelTestCase(TestCase):
    def test_unicode(self):
        """Test ResourceType object str/unicode representation"""
        resource_type = ResourceType.objects.create(name="Foo")
        self.assertEqual(unicode(resource_type), "Foo")


class NewsModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.
                                                  systers_user)

    def test_unicode(self):
        """Test News object str/unicode representation"""
        news = News.objects.create(slug="foonews", title="Bar",
                                   author=self.systers_user,
                                   content="Hi there!",
                                   community=self.community)
        self.assertEqual(unicode(news), "Bar of Foo Community")


class ResourceModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.
                                                  systers_user)

    def test_unicode(self):
        """Test Resource object str/unicode representation"""
        resource = Resource.objects.create(slug="fooresource", title="Bar",
                                           author=self.systers_user,
                                           content="Hi there!",
                                           community=self.community)
        self.assertEqual(unicode(resource), "Bar of Foo Community")
