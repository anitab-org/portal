from django.contrib.auth.models import User
from django.test import TestCase

from community.forms import CommunityForm
from community.models import Community
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
