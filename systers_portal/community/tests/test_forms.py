from django.contrib.auth.models import User
from django.test import TestCase

from community.forms import CommunityForm, AddCommunityPageForm
from community.models import Community, CommunityPage
from users.models import SystersUser


class CommunityFormTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_community_form(self):
        """Test community form"""
        data = {'name': 'Bar',
                'slug': 'bar',
                'order': 1,
                'community_admin': self.systers_user}
        form = CommunityForm(data=data, instance=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.community.name, 'Bar')
        self.assertEqual(self.community.slug, 'bar')


class AddCommunityPageFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_add_community_page_form(self):
        """Test add CommunityPage form"""
        invalid_data = {'title': "something"}
        form = AddCommunityPageForm(data=invalid_data, author=self.user,
                                    community=self.community)
        self.assertFalse(form.is_valid())

        data = {'slug': 'foo',
                'title': 'Foo',
                'order': 1,
                'content': "Rainbows and ponies"}
        form = AddCommunityPageForm(data=data, author=self.user,
                                    community=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        resource = CommunityPage.objects.get()
        self.assertEqual(resource.title, 'Foo')
        self.assertEqual(resource.author, self.systers_user)
