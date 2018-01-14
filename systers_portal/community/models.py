from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db import models

from common.models import Post
from community.constants import COMMUNITY_ADMIN
from membership.constants import NOT_MEMBER, OK
from users.models import SystersUser


class Community(models.Model):
    """Model to represent Systers community or subcommunity"""
    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    order = models.IntegerField(unique=True, verbose_name="Order")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    mailing_list = models.EmailField(max_length=255, blank=True,
                                     verbose_name="Mailing list")
    members = models.ManyToManyField(SystersUser, blank=True,
                                     related_name='communities',
                                     verbose_name="Members")
    admin = models.ForeignKey(SystersUser, related_name='community',
                              verbose_name="Community admin")
    parent_community = models.ForeignKey('self', blank=True, null=True,
                                         verbose_name="Parent community")
    website = models.URLField(max_length=255, blank=True,
                              verbose_name="Website",
                              help_text="Enter URL starting with http(s)://")
    facebook = models.URLField(max_length=255, blank=True,
                               verbose_name="Facebook",
                               help_text="Enter URL starting with http(s)://")
    googleplus = models.URLField(max_length=255, blank=True,
                                 verbose_name="Google+",
                                 help_text="Enter URL starting with http(s)://")
    twitter = models.URLField(max_length=255, blank=True,
                              verbose_name="Twitter",
                              help_text="Enter URL starting with http(s)://")
    __original_name = None
    __original_admin = None

    class Meta:
        verbose_name_plural = "Communities"
        permissions = (
            ('add_community_systersuser', 'Add community Systers User'),
            ('change_community_systersuser', 'Change community Systers User'),
            ('delete_community_systersuser', 'Delete community Systers User'),
            ('add_community_news', 'Add community news'),
            ('change_community_news', 'Change community news'),
            ('delete_community_news', 'Delete community news'),
            ('add_community_resource', 'Add community resource'),
            ('change_community_resource', 'Change community resource'),
            ('delete_community_resource', 'Delete community resource'),
            ('add_community_page', 'Add community page'),
            ('change_community_page', 'Change community page'),
            ('delete_community_page', 'Delete community page'),
            ('approve_community_comment', 'Approve community comment'),
            ('delete_community_comment', 'Delete community comment'),
            ('approve_community_joinrequest', 'Approve community join '
                                              'request'),
        )

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Community, self).__init__(*args, **kwargs)
        self.__original_name = self.name
        if self.admin_id is not None:
            self.__original_admin = self.admin

    @property
    def original_name(self):
        return self.__original_name

    @property
    def original_admin(self):
        return self.__original_admin

    def get_absolute_url(self):
        """Absolute url to a Community main page"""
        return reverse('view_community_landing', kwargs={'slug': self.slug})

    def has_changed_name(self):
        """Check if community has a new name

        :return: True if community changed name, False otherwise
        """
        return self.name != self.original_name

    def has_changed_admin(self):
        """Check if community has a new admin

        :return: True if community changed admin, False otherwise
        """
        return self.admin != self.original_admin

    def add_member(self, systers_user):
        """Add community member

        :param systers_user: SystersUser objects
        """
        self.members.add(systers_user)

    def remove_member(self, systers_user):
        """Remove community member

        :param systers_user: SystersUser object
        :return:
        """
        self.members.remove(systers_user)

    def get_fields(self):
        """Get model fields of a Community object

        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                Community._meta.fields]

    def set_new_admin(self, new_admin):
        """Transfer the admin role from the old to the new admin

        :param new_admin: SystersUser object new admin of the community
        :return: OK if setting was successful, NOT_MEMBER if settings was
                 unsuccessful, since the new admin is not a member of the
                 community
        """
        if not new_admin.is_member(self):
            return NOT_MEMBER
        name = COMMUNITY_ADMIN.format(self.name)
        admin_group = Group.objects.get(name=name)
        self.admin.leave_group(admin_group)
        new_admin.join_group(admin_group)
        self.admin = new_admin
        self.save()
        return OK


class CommunityPage(Post):
    """Model to represent an arbitrary community page"""
    order = models.IntegerField(verbose_name="Order")
    community = models.ForeignKey(Community, verbose_name="Community")

    class Meta:
        unique_together = (('community', 'slug'), ('community', 'order'))

    def __str__(self):
        return "Page {0} of {1}".format(self.title, self.community)
