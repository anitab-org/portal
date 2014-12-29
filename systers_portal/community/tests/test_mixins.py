from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.views.generic import TemplateView

from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage
from users.models import SystersUser


class CommunityMenuMixinText(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_get_context_data_no_community(self):
        class DummyView(CommunityMenuMixin, TemplateView):
            pass

        view = DummyView()
        self.assertRaises(ImproperlyConfigured, view.get_context_data)

    def test_get_context_data_no_pages(self):
        class DummyView(CommunityMenuMixin, TemplateView):
            community = Community.objects.get()

        view = DummyView()
        context = view.get_context_data()
        self.assertQuerysetEqual(context['pages'], [])
        self.assertEqual(context['active_page'], 'news')

    def test_get_context_data_pages(self):
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
        page1 = CommunityPage.objects.create(slug="page1", title="Page",
                                             order=1,
                                             author=self.systers_user,
                                             community=self.community)

        class DummyView(CommunityMenuMixin, TemplateView):
            def get_community(self):
                return Community.objects.get()

            def get_page(self):
                return CommunityPage.objects.get()

        view = DummyView()
        context = view.get_context_data()
        self.assertEqual(list(context['pages']), [page1])
        self.assertEqual(context['active_page'], 'page1')
