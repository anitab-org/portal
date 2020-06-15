from cities_light.models import Country, City
from django.contrib.auth.models import User
from django.test import TestCase

from blog.forms import (AddNewsForm, EditNewsForm, AddResourceForm,
                        EditResourceForm, TagForm, ResourceTypeForm)
from blog.models import News, Resource, Tag, ResourceType
from community.models import Community
from users.models import SystersUser


class AddNewsFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_add_news_form(self):
        """Test add news form"""
        invalid_data = {'slug': "new"}
        form = AddNewsForm(data=invalid_data, author=self.user,
                           community=self.community)
        self.assertFalse(form.is_valid())

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponies",
                'is_public': 1,
                'is_monitored': 0}
        form = AddNewsForm(data=data, author=self.user,
                           community=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        news = News.objects.get()
        self.assertEqual(news.title, 'Bar')
        self.assertEqual(news.author, self.systers_user)


class EditNewsFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_edit_news_form(self):
        """Test edit news form"""
        incomplete_data = {'title': 'hello'}
        form = EditNewsForm(data=incomplete_data)
        self.assertFalse(form.is_valid())

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponies",
                'is_public': 1,
                'is_monitored': 0}
        news = News.objects.create(slug="baz", title="Foo Bar",
                                   author=self.systers_user,
                                   content="Hi there!",
                                   community=self.community)
        form = EditNewsForm(instance=news, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        news = News.objects.get()
        self.assertEqual(news.slug, 'bar')
        self.assertEqual(news.title, 'Bar')
        self.assertEqual(news.content, 'Rainbows and ponies')


class AddResourceFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_add_resource_form(self):
        """Test add resource form"""
        invalid_data = {'slug': "new"}
        form = AddResourceForm(data=invalid_data, author=self.user,
                               community=self.community)
        self.assertFalse(form.is_valid())

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponies",
                'is_public': 1,
                'is_monitored': 0}
        form = AddResourceForm(data=data, author=self.user,
                               community=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        resource = Resource.objects.get()
        self.assertEqual(resource.title, 'Bar')
        self.assertEqual(resource.author, self.systers_user)


class EditResourceFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_edit_news_form(self):
        """Test edit resource form"""
        incomplete_data = {'title': 'hello'}
        form = EditResourceForm(data=incomplete_data)
        self.assertFalse(form.is_valid())

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponies",
                'is_public': 1,
                'is_monitored': 0}
        resource = Resource.objects.create(slug="baz", title="Foo Bar",
                                           author=self.systers_user,
                                           content="Hi there!",
                                           community=self.community)
        form = EditNewsForm(instance=resource, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        resource = Resource.objects.get()
        self.assertEqual(resource.slug, 'bar')
        self.assertEqual(resource.title, 'Bar')
        self.assertEqual(resource.content, 'Rainbows and ponies')


class TagFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_tag_form(self):
        """Test adding and editing tag form"""
        form = TagForm(data={})
        self.assertFalse(form.is_valid())

        form = TagForm(data={'name': 'foo'})
        self.assertTrue(form.is_valid())
        form.save()
        tag = Tag.objects.get()
        self.assertEqual(tag.name, 'foo')

        form = TagForm(instance=tag, data={'name': 'bar'})
        self.assertTrue(form.is_valid())
        form.save()
        tag = Tag.objects.get()
        self.assertEqual(tag.name, 'bar')


class ResourceTypeFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_resourceType_form(self):
        """Test adding and editing resourceType form"""
        form = ResourceTypeForm(data={})
        self.assertFalse(form.is_valid())

        form = ResourceTypeForm(data={'name': 'foo'})
        self.assertTrue(form.is_valid())
        form.save()
        resourceType = ResourceType.objects.get()
        self.assertEqual(resourceType.name, 'foo')

        form = ResourceTypeForm(instance=resourceType, data={'name': 'bar'})
        self.assertTrue(form.is_valid())
        form.save()
        resourceType = ResourceType.objects.get()
        self.assertEqual(resourceType.name, 'bar')
