from django.db import models

from common.models import Post
from users.models import SystersUser


class Community(models.Model):
    """Model to represent Systers community or subcommunity"""
    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    order = models.IntegerField(unique=True, verbose_name="Order")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    mailing_list = models.EmailField(max_length=255, blank=True,
                                     verbose_name="Mailing list")
    members = models.ManyToManyField(SystersUser, blank=True, null=True,
                                     related_name='communities',
                                     verbose_name="Members")
    community_admin = models.ForeignKey(SystersUser, related_name='community',
                                        verbose_name="Community admin")
    parent_community = models.ForeignKey('self', blank=True, null=True,
                                         verbose_name="Parent community")
    website = models.URLField(max_length=255, blank=True,
                              verbose_name="Website")
    facebook = models.URLField(max_length=255, blank=True,
                               verbose_name="Facebook")
    googleplus = models.URLField(max_length=255, blank=True,
                                 verbose_name="Google+")
    twitter = models.URLField(max_length=255, blank=True,
                              verbose_name="Twitter")

    class Meta:
        verbose_name_plural = "Communities"

    def __unicode__(self):
        return self.name


class CommunityPage(Post):
    """Model to represent an arbitrary community page"""
    order = models.IntegerField(unique=True, verbose_name="Order")
    community = models.ForeignKey(Community, verbose_name="Community")
