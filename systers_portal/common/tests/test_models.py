from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from blog.models import News
from common.models import Comment
from community.models import Community
from users.models import SystersUser


class CommentModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.
                                                  systers_user)

    def test_unicode(self):
        """Test Comment object str/unicode representation"""
        news = News.objects.create(slug="foonews", title="Bar",
                                   author=self.systers_user,
                                   content="Hi there!",
                                   community=self.community)
        related_object_type = ContentType.objects.get_for_model(news)
        comment = Comment.objects.create(author=self.systers_user, body="Bar",
                                         object_id=news.id,
                                         content_type=related_object_type)
        self.assertEqual(unicode(comment),
                         "Comment by foo to Bar of Foo Community")
