from cities_light.models import Country, City
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from users.models import SystersUser
from community.models import Community


class CommunitiesProcessorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.client = Client()

    def test_communities_processor(self):
        """Test the rendering of all communities in the templates"""
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        Community.objects.create(name="Foo", slug="foo",
                                 order=1, location=location,
                                 admin=self.systers_user)
        Community.objects.create(name="Boo", slug="boo",
                                 order=2, location=location,
                                 admin=self.systers_user)
        index_url = reverse('index')
        response = self.client.get(index_url)
        self.assertContains(response, '<a role="menuitem" '
                                      'href="/community/foo/">Foo</a>')
        self.assertContains(response, '<a role="menuitem" '
                                      'href="/community/boo/">Boo</a>')
