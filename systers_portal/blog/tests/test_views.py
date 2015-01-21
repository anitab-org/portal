from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from blog.models import News
from community.models import Community
from users.models import SystersUser


class CommunityNewsListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)
        self.client = Client()

    def test_community_news_list_view_no_news(self):
        """Test GET request to news list with an invalid community slug and
        with a valid community slug, but no news"""
        url = reverse('view_community_news_list', kwargs={'slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('view_community_news_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/news_list.html')

    def test_community_nest_list_view_with_news(self):
        """Test GET request to news list with a single existing community
        news."""
        News.objects.create(slug="bar", title="Bar",
                            author=self.systers_user,
                            content="Hi there!",
                            community=self.community)
        url = reverse('view_community_news_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/news_list.html')
        self.assertContains(response, "Bar")
        self.assertContains(response, "Hi there!")


class CommunityNewsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)
        self.client = Client()

    def test_community_news_view(self):
        """Test GET request to view a single community news"""
        url = reverse('view_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        News.objects.create(slug="bar", title="Bar",
                            author=self.systers_user,
                            content="Hi there!",
                            community=self.community)
        url = reverse('view_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/news.html')
        self.assertContains(response, "Bar")
        self.assertContains(response, "Hi there!")
