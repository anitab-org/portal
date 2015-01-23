from django.contrib.auth.models import User
from django.test import TestCase

from blog.forms import NewsForm
from blog.models import News
from community.models import Community
from users.models import SystersUser


class CommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_news_form(self):
        """Test news form"""
        invalid_data = {'slug': "new"}
        form = NewsForm(data=invalid_data, author=self.user,
                        community=self.community)
        self.assertFalse(form.is_valid())

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponnies",
                'is_public': 1,
                'is_monitored': 0}
        form = NewsForm(data=data, author=self.user, community=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        news = News.objects.get()
        self.assertEqual(news.title, 'Bar')
        self.assertEqual(news.author, self.systers_user)
