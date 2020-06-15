from cities_light.models import Country, City
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from blog.models import News, Resource, ResourceType, Tag
from community.models import Community
from users.models import SystersUser


class CommunityNewsListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
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
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_community_news_list_view_with_news(self):
        """Test GET request to news list with a single existing community
        news."""
        News.objects.create(slug="bar", title="Bar",
                            author=self.systers_user,
                            content="Hi there!",
                            community=self.community)
        url = reverse('view_community_news_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, "Bar")
        self.assertContains(response, "Hi there!")

    def test_community_news_sidebar(self):
        """Test the presence or the lack of a news sidebar in the template"""
        url = reverse('view_community_news_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "News Actions")
        self.assertNotContains(response, "Add news")

        self.client.login(username="foo", password="foobar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/snippets/news_sidebar.html')
        self.assertContains(response, "News Actions")
        self.assertContains(response, "Add news")
        self.assertNotContains(response, "Edit current news")
        self.assertNotContains(response, "Delete current news")

        User.objects.create_user(username="baz", password="foobar")
        self.client.login(username="baz", password="foobar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "News Actions")
        self.assertNotContains(response, "Add news")


class CommunityNewsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=self.location,
                                                  admin=self.systers_user)
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
        self.assertTemplateUsed(response, 'blog/post.html')
        self.assertContains(response, "Bar")
        self.assertContains(response, "Hi there!")

    def test_multiple_communities_same_slug_news_view(self):
        """Test GET request to two news object with same slug, but belonging to
        two separate communities"""
        new_community = Community.objects.create(name="Super Unusual Name",
                                                 slug="bar",
                                                 order=2, location=self.location,
                                                 admin=self.systers_user)
        news1 = News.objects.create(slug="bar", title="Bar",
                                    author=self.systers_user,
                                    content="Hi there!",
                                    community=self.community)
        news2 = News.objects.create(slug="bar", title="New Bar!",
                                    author=self.systers_user,
                                    content="Hi there!",
                                    community=new_community)
        url = reverse('view_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.community.name)
        self.assertContains(response, news1.title)

        new_url = reverse("view_community_news", kwargs={'slug': 'bar',
                                                         'news_slug': 'bar'})
        response = self.client.get(new_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_community.name)
        self.assertContains(response, news2.title)

    def test_community_news_sidebar(self):
        """Test the presence or the lack of the news sidebar in the template"""
        self.client.login(username="foo", password="foobar")
        News.objects.create(slug="bar", title="Bar",
                            author=self.systers_user,
                            content="Hi there!",
                            community=self.community)
        url = reverse('view_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/snippets/news_sidebar.html')
        self.assertContains(response, "News Actions")
        self.assertContains(response, "Add news")
        self.assertContains(response, "Edit current news")
        self.assertContains(response, "Delete current news")


class AddCommunityNewsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

        self.client = Client()

    def test_get_add_community_news(self):
        """Test GET create new community news"""
        url = reverse('add_community_news', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/add_post.html')

        new_user = User.objects.create_user(username="bar", password="foobar")
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        group = Group.objects.get(name="Foo: Content Manager")
        new_user.groups.add(group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_add_community_news(self):
        """Test POST create new community news"""
        url = reverse('add_community_news', kwargs={'slug': 'foo'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data={"slug": "baz"})
        self.assertEqual(response.status_code, 200)

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponies"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        news = News.objects.get()
        self.assertEqual(news.title, 'Bar')
        self.assertEqual(news.author, self.systers_user)


class EditCommunityNewsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
        self.news = News.objects.create(slug="bar", title="Bar",
                                        author=self.systers_user,
                                        content="Hi there!",
                                        community=self.community)
        self.client = Client()

    def test_get_edit_community_news_view(self):
        """Test GET to edit community news"""
        url = reverse('edit_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_community_news_view(self):
        """Test POST to edit community news"""
        url = reverse('edit_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'foo'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_community_news', kwargs={'slug': 'foo',
                                                     'news_slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        data = {'slug': 'another',
                'title': 'Baz',
                'content': "Rainbows and ponies"}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)


class DeleteCommunityNewsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
        News.objects.create(slug="bar", title="Bar",
                            author=self.systers_user,
                            content="Hi there!",
                            community=self.community)
        self.client = Client()

    def test_get_delete_community_news_view(self):
        """Test GET to confirm deletion of news"""
        url = reverse("delete_community_news", kwargs={'slug': 'foo',
                                                       'news_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_community_news_view(self):
        """Test POST to delete a community news"""
        url = reverse("delete_community_news", kwargs={'slug': 'foo',
                                                       'news_slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertSequenceEqual(News.objects.all(), [])


class CommunityResourceListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
        self.client = Client()

    def test_community_news_list_view_no_resources(self):
        """Test GET request to resources list with an invalid community slug
        and with a valid community slug, but no resources"""
        url = reverse('view_community_resource_list', kwargs={'slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('view_community_resource_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_community_resource_list_view_with_resources(self):
        """Test GET request to resource list with a single existing community
        resource."""
        Resource.objects.create(slug="bar", title="Bar",
                                author=self.systers_user,
                                content="Hi there!",
                                community=self.community)
        url = reverse('view_community_resource_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, "Bar")
        self.assertContains(response, "Hi there!")

        resource_type = ResourceType.objects.create(name="abc")
        Resource.objects.create(slug="new", title="New",
                                author=self.systers_user,
                                content="New content!",
                                community=self.community,
                                resource_type=resource_type)
        missing_param_url = url + "?type=cba"
        response = self.client.get(missing_param_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Types")
        self.assertContains(response, "abc")
        self.assertContains(response, "Bar")
        self.assertContains(response, "New")

        existing_param_url = url + "?type=abc"
        response = self.client.get(existing_param_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Types")
        self.assertContains(response, "abc")
        self.assertNotContains(response, "Bar")
        self.assertContains(response, "New")

    def test_community_resource_sidebar(self):
        """Test the presence or the lack of a resource sidebar in the
        template"""
        url = reverse('view_community_resource_list', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Resource Actions")
        self.assertNotContains(response, "Add resource")

        self.client.login(username="foo", password="foobar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'blog/snippets/resources_sidebar.html')
        self.assertContains(response, "Resource Actions")
        self.assertContains(response, "Add resource")
        self.assertNotContains(response, "Edit current resource")
        self.assertNotContains(response, "Delete current resource")

        User.objects.create_user(username="baz", password="foobar")
        self.client.login(username="baz", password="foobar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Resource Actions")
        self.assertNotContains(response, "Add resource")


class CommunityResourceViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=self.location,
                                                  admin=self.systers_user)
        self.client = Client()

    def test_community_resource_view(self):
        """Test GET request to view a community resource"""
        url = reverse('view_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        Resource.objects.create(slug="bar", title="Bar",
                                author=self.systers_user,
                                content="Hi there!",
                                community=self.community)
        url = reverse('view_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post.html')
        self.assertContains(response, "Bar")
        self.assertContains(response, "Hi there!")

    def test_multiple_communities_same_slug_resource_view(self):
        """Test GET request to two resource objects with same slug, but
        belonging to two separate communities"""
        new_community = Community.objects.create(name="Super Unusual Name",
                                                 slug="bar",
                                                 order=2, location=self.location,
                                                 admin=self.systers_user)
        resource1 = Resource.objects.create(slug="bar", title="Bar",
                                            author=self.systers_user,
                                            content="Hi there!",
                                            community=self.community)
        resource2 = Resource.objects.create(slug="bar", title="New Bar!",
                                            author=self.systers_user,
                                            content="Hi there!",
                                            community=new_community)
        url = reverse('view_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.community.name)
        self.assertContains(response, resource1.title)

        new_url = reverse("view_community_resource",
                          kwargs={'slug': 'bar', 'resource_slug': 'bar'})
        response = self.client.get(new_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_community.name)
        self.assertContains(response, resource2.title)

    def test_community_resources_sidebar(self):
        """Test the presence or the lack of the resource sidebar in the
        template"""
        self.client.login(username="foo", password="foobar")
        Resource.objects.create(slug="bar", title="Bar",
                                author=self.systers_user,
                                content="Hi there!",
                                community=self.community)
        url = reverse('view_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'blog/snippets/resources_sidebar.html')
        self.assertContains(response, "Resource Actions")
        self.assertContains(response, "Add resource")
        self.assertContains(response, "Edit current resource")
        self.assertContains(response, "Delete current resource")


class AddCommunityResourceViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

        self.client = Client()

    def test_get_add_community_resource(self):
        """Test GET create new community resource"""
        url = reverse('add_community_resource', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/add_post.html')

        new_user = User.objects.create_user(username="bar", password="foobar")
        self.client.login(username='bar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        group = Group.objects.get(name="Foo: Content Manager")
        new_user.groups.add(group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_add_community_resource(self):
        """Test POST create new community resource"""
        url = reverse('add_community_resource', kwargs={'slug': 'foo'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data={"slug": "baz"})
        self.assertEqual(response.status_code, 200)

        data = {'slug': 'bar',
                'title': 'Bar',
                'content': "Rainbows and ponies"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        resource = Resource.objects.get()
        self.assertEqual(resource.title, 'Bar')
        self.assertEqual(resource.author, self.systers_user)


class EditCommunityResourceViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
        self.resource = Resource.objects.create(slug="bar", title="Bar",
                                                author=self.systers_user,
                                                content="Hi there!",
                                                community=self.community)
        self.client = Client()

    def test_get_edit_community_resource_view(self):
        """Test GET to edit community resource"""
        url = reverse('edit_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_community_resource_view(self):
        """Test POST to edit community resource"""
        url = reverse('edit_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'foo'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_community_resource',
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        data = {'slug': 'another',
                'title': 'Baz',
                'content': "Rainbows and ponies"}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)


class DeleteCommunityResourceViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
        Resource.objects.create(slug="bar", title="Bar",
                                author=self.systers_user,
                                content="Hi there!",
                                community=self.community)
        self.client = Client()

    def test_get_delete_community_resource_view(self):
        """Test GET to confirm deletion of a resource"""
        url = reverse("delete_community_resource",
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_community_resource_view(self):
        """Test POST to delete a community resource"""
        url = reverse("delete_community_resource",
                      kwargs={'slug': 'foo', 'resource_slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertSequenceEqual(Resource.objects.all(), [])


class AddTagViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_add_tag_view(self):
        """Test GET and POST requests to add a new tag"""
        url = reverse("add_tag", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        group = Group.objects.get(name="Foo: Content Contributor")
        self.systers_user.join_group(group)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.post(url, data={'name': 'Baz'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Tag.objects.get().name, "Baz")


class AddResourceTypeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_add_resourceType_view(self):
        """Test GET and POST requests to add a new resource type"""
        url = reverse("add_resource_type", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        group = Group.objects.get(name="Foo: Content Contributor")
        self.systers_user.join_group(group)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.post(url, data={'name': 'Baz'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(ResourceType.objects.get().name, "Baz")
