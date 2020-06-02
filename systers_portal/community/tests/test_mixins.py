from cities_light.models import Country, City
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.views.generic import TemplateView

from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage
from users.models import SystersUser


class CommunityMenuMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_get_context_data_no_community(self):
        """Test mixin with no community and no page_slug set"""
        class DummyView(CommunityMenuMixin, TemplateView):
            pass

        view = DummyView()
        self.assertRaises(ImproperlyConfigured, view.get_context_data)

    def test_get_context_data_no_pages(self):
        """Test mixin with a community set, but no page_slug set.
        Additionally Community has no pages."""
        class DummyView(CommunityMenuMixin, TemplateView):
            community = Community.objects.get()

        view = DummyView()
        context = view.get_context_data()
        self.assertQuerysetEqual(context['pages'], [])
        self.assertEqual(context['active_page'], 'news')

    def test_get_context_data_pages(self):
        """Test mixin with a community set, but no page_slug set.
        Community has 2 pages."""
        page1 = CommunityPage.objects.create(slug="page1", title="Page",
                                             order=1,
                                             author=self.systers_user,
                                             community=self.community)
        page2 = CommunityPage.objects.create(slug="page2", title="Page",
                                             order=2,
                                             author=self.systers_user,
                                             community=self.community)

        class DummyView(CommunityMenuMixin, TemplateView):
            def get_community(self):
                return Community.objects.get()

        view = DummyView()
        context = view.get_context_data()
        self.assertEqual(list(context["pages"]), [page1, page2])
        self.assertEqual(context['active_page'], 'page1')

    def test_get_context_data_with_page(self):
        """Test mixin with a community and a page_slug set to an existing
        CommunityPage slug."""
        page1 = CommunityPage.objects.create(slug="page1", title="Page",
                                             order=1,
                                             author=self.systers_user,
                                             community=self.community)

        class DummyView(CommunityMenuMixin, TemplateView):
            def get_community(self):
                return Community.objects.get()

            def get_page_slug(self):
                return 'page1'

        view = DummyView()
        context = view.get_context_data()
        self.assertEqual(list(context['pages']), [page1])
        self.assertEqual(context['active_page'], 'page1')

    def test_get_context_data_news(self):
        """Test mixin with a community and a page_slug set to news"""
        class DummyView(CommunityMenuMixin, TemplateView):
            community = Community.objects.get()
            page_slug = 'news'

        view = DummyView()
        context = view.get_context_data()
        self.assertEqual(context['active_page'], 'news')
