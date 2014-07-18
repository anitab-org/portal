import mock

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.http import Http404
from django.test import TestCase
from cms.models.pagemodel import Page
from cms.api import create_page
from allauth.account import signals
from guardian.shortcuts import get_perms
from south.signals import post_migrate

from dashboard.decorators import (membership_required, admin_required,
                                  authorship_required)
from dashboard.management import create_generic_group, permissions
from dashboard.models import (SysterUser, Community, News, Resource, Tag,
                              ResourceType, CommunityPage)
from dashboard.signals import *


class DashboardModelsTestCase(TestCase):
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

    def test_signal_registry(self):
        """Test if functions were registered as signal receivers"""
        signed_up_registered_funcs = [r[1]() for r in
                                      signals.user_signed_up.receivers]
        post_save_registered_funcs = [r[1]() for r in post_save.receivers]
        post_delete_registered_funcs = [r[1]() for r in post_delete.receivers]
        post_migrate_registered_funcs = [r[1]() for r in
                                         post_migrate.receivers]
        m2m_changed_registered_funcs = [r[1]() for r in m2m_changed.receivers]
        self.assertIn(create_syster_user, signed_up_registered_funcs)
        self.assertIn(create_community_groups, post_save_registered_funcs)
        self.assertIn(remove_community_groups, post_delete_registered_funcs)
        self.assertIn(create_generic_group, post_migrate_registered_funcs)
        self.assertIn(give_basic_access, m2m_changed_registered_funcs)

    def test_create_syster_user(self):
        """Test the creation of SysterUser object on user signup"""
        self.assertQuerysetEqual(SysterUser.objects.all(), [])
        request = {'user': self.auth_user}
        create_syster_user(self.test_create_syster_user, **request)
        users = User.objects.all()
        systerusers = SysterUser.objects.all()
        self.assertEqual(len(systerusers), len(users))
        self.assertEqual(len(users), 1)
        self.assertEqual(systerusers[0].user, users[0])

    def test_give_basic_access(self):
        """Test giving basic access to users"""
        self.assertEqual(list(self.auth_user.groups.all()), [])
        self.assertFalse(self.auth_user.is_staff)
        group = Group.objects.create(name="Foo group")
        self.auth_user.groups.add(group)
        self.auth_user.save()
        self.assertIn(group, self.auth_user.groups.all())
        self.assertTrue(self.auth_user.is_staff)
        self.auth_user.groups.remove(group)
        self.auth_user.save()
        self.assertEqual(list(self.auth_user.groups.all()), [])
        self.assertFalse(self.auth_user.is_staff)

    def test_create_community_groups(self):
        """Test creation of community specific groups"""
        systeruser = SysterUser.objects.create(user=self.auth_user)
        name = 'FooBar'
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())
        community = Community.objects.create(name=name,
                                             community_admin=systeruser)
        for key, group_name in generic_groups.items():
            self.assertTrue(Group.objects.filter(
                name=group_name.format(community.name)).exists())
        self.assertIn(Group.objects.get(
            name=generic_groups["community_admin"].format(name)),
            systeruser.user.groups.all())
        community.name = "BarFoo"
        systeruser2 = SysterUser.objects.create(
            user=User.objects.create(username='bar', password='foobar'))
        community.community_admin = systeruser2
        community.save()
        self.assertNotIn(Group.objects.get(
            name=generic_groups["community_admin"].format(community.name)),
            systeruser.user.groups.all())
        self.assertIn(Group.objects.get(
            name=generic_groups["community_admin"].format(community.name)),
            systeruser2.user.groups.all())
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())
            self.assertTrue(Group.objects.filter(
                name=group_name.format(community.name)).exists())

    def test_remove_community_groups(self):
        """Test removal of community specific groups"""
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name="Foo",
                                             community_admin=systeruser)
        community.delete()
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(community.name)).exists())

    def test_create_groups(self):
        name = "baz"
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())
        create_groups(name)
        for key, group_name in generic_groups.items():
            self.assertTrue(Group.objects.filter(
                name=group_name.format(name)).exists())

    def test_delete_groups(self):
        name = "bar"
        for key, group_name in generic_groups.items():
            Group.objects.create(name=group_name.format(name))
        delede_groups(name)
        for key, group_name in generic_groups.items():
            self.assertFalse(Group.objects.filter(
                name=group_name.format(name)).exists())

    def test_assign_permissions(self):
        name = "Foo"
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name=name,
                                             community_admin=systeruser)
        assign_permissions(community)
        for key, value in dashboard_group_permissions.items():
            group = Group.objects.get(name=generic_groups[key].format(name))
            group_permissions = [p.codename for p in
                                 list(group.permissions.all())]
            group_permissions += get_perms(group, community)
            self.assertItemsEqual(group_permissions, value)

    def test_grant_access_to_parent_community(self):
        systeruser1 = SysterUser.objects.create(user=self.auth_user)
        auth_user2 = User.objects.create(username='bar', password='foobar')
        systeruser2 = SysterUser.objects.create(user=auth_user2)
        community_a = Community.objects.create(name="A", slug='a',
                                               community_admin=systeruser1)
        community_b = Community.objects.create(name="B", slug='b',
                                               community_admin=systeruser2)
        group_a = Group.objects.get(name="Community Admin for A")
        group_a.user_set.add(self.auth_user)
        community_b.parent_community = community_a
        community_b.save()
        group_b = Group.objects.get(name="Community Admin for B")
        user_groups = self.auth_user.groups.all()
        self.assertIn(group_a, user_groups)
        self.assertIn(group_b, user_groups)

    def test_create_generic_group(self):
        self.assertTrue(Group.objects.filter(
            name="Generic permissions").exists())
        group = Group.objects.get(name="Generic permissions")
        group_permissions = [p.codename for p in
                             list(group.permissions.all())]
        self.assertItemsEqual(group_permissions, permissions)

    def test_join_leave_group(self):
        systeruser = SysterUser.objects.create(user=self.auth_user)
        community = Community.objects.create(name="Foo",
                                             community_admin=systeruser)
        self.assertRaises(Http404, join_group, systeruser, "No such group")
        self.assertRaises(Http404, leave_group, systeruser, "No such group")
        join_group(systeruser,
                   generic_groups["content_manager"].format(community.name))
        self.assertIn(Group.objects.get(
            name=generic_groups["content_manager"].format(community.name)),
            systeruser.user.groups.all())
        leave_group(systeruser,
                    generic_groups["content_manager"].format(community.name))
        self.assertNotIn(Group.objects.get(
            name=generic_groups["content_manager"].format(community.name)),
            systeruser.user.groups.all())


class DashboardDecoratorsTestCase(TestCase):
    def setUp(self):
        self.auth_user_foo = User.objects.create_user(username="foo",
                                                      password="foobar")
        self.user_foo = SysterUser(user=self.auth_user_foo)
        self.user_foo.save()
        self.auth_user_bar = User.objects.create_user(username="bar",
                                                      password="foobar")
        self.user_bar = SysterUser(user=self.auth_user_bar)
        self.user_bar.save()
        self.community = Community(community_admin=self.user_foo)
        self.community.save()
        self.community.members.add(self.user_foo)
        self.community.save()
        self.resource = Resource(community=self.community,
                                 author=self.user_foo)
        self.resource.save()

    def test_decorators(self):
        request = mock.MagicMock()
        view = mock.MagicMock(return_value='foo response')

        test_objects = [self.community, self.resource, ]
        mockup_tests = [
            {"user": self.auth_user_foo, "success": True},
            {"user": self.auth_user_bar, "success": False},
        ]
        tests = []
        for obj in test_objects:
            for mockup_test in mockup_tests:
                tests.append(mockup_test)
                tests[-1]["model"] = type(obj)
                tests[-1]["object"] = obj
        decorators = [membership_required, admin_required, authorship_required]
        for decorator in decorators:
            for test in tests:
                request.user = test["user"]
                request_kwargs = {"id": test["object"].id}
                decorated = decorator(test["model"], "id__exact", "id")
                wrapped = decorated(view)

                if test["success"]:
                    response = wrapped(request, **request_kwargs)
                    self.assertEqual(response, view.return_value)
                else:
                    self.assertRaises(PermissionDenied, wrapped, request,
                                      **request_kwargs)
