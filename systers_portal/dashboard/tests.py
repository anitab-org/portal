from django.contrib.auth.models import User, Group
from django.test import TestCase

from cms.api import create_page
from cms.models.pagemodel import Page

from dashboard.forms import NewsForm
from dashboard.management import (content_contributor_permissions,
                                  content_manager_permissions,
                                  user_content_manager_permissions,
                                  community_admin_permissions)
from dashboard.models import (SysterUser, Community, News, Resource, Tag,
                              ResourceType, CommunityPage)


class DashboardTestCase(TestCase):

    def setUp(self):
        self.auth_user = User.objects.create(username='foo', password='foobar')
        self.tag = Tag.objects.create(name='dummy_tag')
        self.resource_type = ResourceType.objects.create(
            name='dummy_resource_type')

    def test_user_and_syster_user(self):
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(
            user=self.auth_user,
            blog_url='http://blog_url.com',
            homepage_url='http://homepage_url.com')
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(unicode(systeruser), self.auth_user.username)
        self.assertEqual(systeruser.blog_url,
                         self.auth_user.systeruser.blog_url)
        self.assertEqual(systeruser.blog_url, 'http://blog_url.com')
        self.assertEqual(systeruser.homepage_url, 'http://homepage_url.com')
        second_user = User.objects.create(username='user2', password='user2')
        second_systeruser = SysterUser.objects.create(user=second_user)  # NOQA
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(len(SysterUser.objects.all()), 2)
        second_user.delete()
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)

    def test_community_model(self):
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        community.members.add(systeruser)
        second_user = User.objects.create(username='user2', password='user2')
        second_systeruser = SysterUser.objects.create(
            user=second_user)
        community.members.add(second_systeruser)
        community_members = SysterUser.objects.filter(
            member_of_community=community)
        community_admin = SysterUser.objects.get(community=community)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(community_members), 2)
        self.assertEqual(unicode(community), 'dummy_community')
        self.assertEqual(community.community_admin, systeruser)
        self.assertEqual(community_admin, systeruser)
        self.assertEqual(systeruser in community_members, True)
        self.assertEqual(second_systeruser in community_members, True)

    def test_tag_model(self):
        self.assertEqual(len(Tag.objects.all()), 1)
        tag = Tag.objects.create(name='dummy_tag1')
        self.assertEqual(len(Tag.objects.all()), 2)
        self.assertEqual(unicode(tag), 'dummy_tag1')

    def test_resourcetype_model(self):
        self.assertEqual(len(ResourceType.objects.all()), 1)
        resource = ResourceType.objects.create(name='dummy_resource1')
        self.assertEqual(len(ResourceType.objects.all()), 2)
        self.assertEqual(unicode(resource), 'dummy_resource1')

    def test_news_model(self):
        self.assertQuerysetEqual(News.objects.all(), [])
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        news_article = News.objects.create(title='dummy_article',
                                           community=community,
                                           author=systeruser,
                                           content='dummy news article')
        news_article.tags.add(self.tag)
        news_article_tags = Tag.objects.filter(news=news_article)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(len(News.objects.all()), 1)
        self.assertEqual(unicode(news_article),
                         'dummy_article of dummy_community Community')
        self.assertEqual(news_article.community,
                         community)
        self.assertEqual(news_article.author, systeruser)
        self.assertEqual(news_article.community.community_admin,
                         systeruser)
        self.assertEqual(news_article.author.user, self.auth_user)
        self.assertEqual(news_article_tags[0], self.tag)
        self.assertEqual(news_article.is_public, True)
        self.assertEqual(news_article.community,
                         Community.objects.get(news=news_article))

    def test_resource_model(self):
        self.assertQuerysetEqual(Resource.objects.all(), [])
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        resource = Resource.objects.create(title='dummy_resource',
                                           community=community,
                                           author=systeruser,
                                           content='dummy resource',
                                           resource_type=self.resource_type)
        resource.tags.add(self.tag)
        resource_tags = Tag.objects.filter(resource=resource)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(SysterUser.objects.all()), 1)
        self.assertEqual(len(Resource.objects.all()), 1)
        self.assertEqual(unicode(resource),
                         'dummy_resource of dummy_community Community')
        self.assertEqual(resource.community, community)
        self.assertEqual(resource.author, systeruser)
        self.assertEqual(resource.community.community_admin, systeruser)
        self.assertEqual(resource.author.user, self.auth_user)
        self.assertEqual(resource_tags[0], self.tag)
        self.assertEqual(resource.resource_type, self.resource_type)
        self.assertEqual(resource.is_public, True)
        self.assertEqual(resource.community,
                         Community.objects.get(resource=resource))
        resource.is_public = False
        self.assertEqual(resource.is_public, False)

    def test_CommunityPage_model(self):
        self.assertQuerysetEqual(CommunityPage.objects.all(), [])
        self.assertQuerysetEqual(Community.objects.all(), [])
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name='dummy_community',
                                             community_admin=systeruser)
        about_dummy_community = create_page('About',
                                            'page_template.html',
                                            'en-us')
        about_page_for_dummy_community = CommunityPage.objects.create(
            title='About',
            page=about_dummy_community,
            community=community)
        self.assertEqual(len(Community.objects.all()), 1)
        self.assertEqual(len(Page.objects.all()), 1)
        self.assertEqual(len(CommunityPage.objects.all()), 1)
        self.assertEqual(len(Page.objects.all()), 1)
        self.assertEqual(unicode(about_page_for_dummy_community),
                         'About of dummy_community Community')
        self.assertEqual(about_page_for_dummy_community.page,
                         about_dummy_community)
        self.assertEqual(about_page_for_dummy_community.community, community)
        faq_dummy_community = create_page('faq', 'page_template.html', 'en-us')
        self.assertEqual(len(Page.objects.all()), 2)
        faq_page_for_dummy_community = CommunityPage.objects.create(
            title='FAQ',
            page=faq_dummy_community,
            community=community)
        self.assertEqual(faq_page_for_dummy_community.page,
                         faq_dummy_community)
        self.assertEqual(faq_page_for_dummy_community.community, community)
        second_community = Community.objects.create(
            name='second_dummy_community',
            community_admin=systeruser,
            slug='second_community',)
        about_second_dummy_community = create_page('About',
                                                   'page_template.html',
                                                   'en-us')
        about_page_for_second_dummy_community = CommunityPage.objects.create(
            title='About',
            page=about_second_dummy_community,
            community=second_community)
        self.assertEqual(len(Community.objects.all()), 2)
        self.assertEqual(len(Page.objects.all()), 3)
        self.assertEqual(len(CommunityPage.objects.all()), 3)
        self.assertEqual(about_page_for_second_dummy_community.page,
                         about_second_dummy_community)
        self.assertEqual(about_page_for_second_dummy_community.community,
                         second_community)
        second_dummy_community_about = Page.objects.get(
            communitypage=about_page_for_second_dummy_community)
        self.assertEqual(about_page_for_second_dummy_community,
                         second_dummy_community_about.communitypage)
        second_dummy_community_about = Page.objects.get(
            communitypage=about_page_for_second_dummy_community)
        self.assertEqual(about_second_dummy_community,
                         second_dummy_community_about)

    def test_group_permissions(self):
        groups = ["Content Contributor",
                  "Content Manager",
                  "User and Content Manager",
                  "Community Admin", ]
        permissions = [content_contributor_permissions,
                       content_manager_permissions,
                       user_content_manager_permissions,
                       community_admin_permissions, ]
        for i, group_name in enumerate(groups):
            group = Group.objects.get(name=group_name)
            group_permissions = [p.codename for p in
                                 list(group.permissions.all())]
            self.assertItemsEqual(group_permissions, permissions[i])


class DashboardFormsTestCase(TestCase):

    def setUp(self):
        auth_user = User.objects.create_user(username="foo", password="foobar")
        self.user = SysterUser(user=auth_user)
        self.user.save()
        self.community = Community(name='bar', community_admin=self.user)
        self.community.save()
        self.tag = Tag.objects.create(name='foo_tag')
        self.tag.save()

    def test_News_form(self):
        form_data = [
            {},
            {'title': 'news'},
            {'slug': 'foo'},
            {'content': 'This is dummy news'},
            {'title': 'foo', 'slug': 'foo'},
            {'title': 'foo',
             'slug': 'foo',
             'tags': self.tag},
            {'title': 'foo',
             'slug': 'foo',
             'is_public': True,
             'tags': [self.tag.id],
             'content': 'This is dummy news'},
            {'title': 'foo',
             'slug': 'foo',
             'is_public': True,
             'content': 'This is dummy news'},
        ]
        result = [False] * 6 + [True] * 2
        for i, data in enumerate(form_data):
            form = NewsForm(data=data)
            self.assertEqual(form.is_valid(), result[i])
