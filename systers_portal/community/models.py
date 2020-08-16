from django.contrib.auth.models import Group
from django.urls import reverse
from django.db import models

from common.models import Post
from community.constants import (COMMUNITY_ADMIN,
                                 COMMUNITY_TYPES_CHOICES, COMMUNITY_CHANNEL_CHOICES,
                                 YES_NO_CHOICES)
from membership.constants import NOT_MEMBER, OK
from users.models import SystersUser
from cities_light.models import City


class Community(models.Model):
    """Model to represent Systers community or subcommunity"""
    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    order = models.IntegerField(unique=True, verbose_name="Order")
    location = models.ForeignKey(City, verbose_name="Location", default="",
                                 on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    mailing_list = models.EmailField(max_length=255, blank=True,
                                     verbose_name="Mailing list")
    members = models.ManyToManyField(SystersUser, blank=True,
                                     related_name='communities',
                                     verbose_name="Members")
    admin = models.ForeignKey(SystersUser, related_name='community',
                              verbose_name="Community admin", on_delete=models.CASCADE)
    parent_community = models.ForeignKey('self', blank=True, null=True,
                                         verbose_name="Parent community", on_delete=models.CASCADE)
    website = models.URLField(max_length=255, blank=True,
                              verbose_name="Website")
    facebook = models.URLField(max_length=255, blank=True,
                               verbose_name="Facebook")
    googleplus = models.URLField(max_length=255, blank=True,
                                 verbose_name="Google+")
    twitter = models.URLField(max_length=255, blank=True,
                              verbose_name="Twitter")
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


class RequestCommunity(models.Model):
    """Model to represent new community requests"""
    name = models.CharField(
        max_length=255, verbose_name="Proposed Community Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    order = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Order")
    location = models.ForeignKey(City, verbose_name="Location",
                                 default="", on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True,
                              verbose_name=" At what email address would you like to be contacted?")
    mailing_list = models.EmailField(max_length=255, blank=True,
                                     verbose_name="Mailing list of the community")
    parent_community = models.ForeignKey(Community, blank=True, null=True,
                                         verbose_name="Parent community", on_delete=models.CASCADE)
    website = models.URLField(max_length=255, blank=True,
                              verbose_name="Link to the website")
    facebook = models.URLField(max_length=255, blank=True,
                               verbose_name="Link to the community on Facebook")
    googleplus = models.URLField(max_length=255, blank=True,
                                 verbose_name="Link to the community on Google+")
    twitter = models.URLField(max_length=255, blank=True,
                              verbose_name="Link to the community on Twitter")

    is_member = models.CharField(default=None, max_length=25, choices=YES_NO_CHOICES,
                                 verbose_name="Are you a member of Systers?")
    email_id = models.EmailField(max_length=255, blank=True,
                                 verbose_name="What email have you used to sign up for Systers?")
    type_community = models.CharField(default=None, max_length=255, choices=COMMUNITY_TYPES_CHOICES,
                                      verbose_name="Type of Community")
    other_community_type = models.CharField(
        blank=True, max_length=255, verbose_name="Other type of community(Please specify)")
    community_channel = models.CharField(default=None, max_length=255,
                                         choices=COMMUNITY_CHANNEL_CHOICES,
                                         verbose_name="Online Community Channels")
    social_presence = models.CharField(null=True, max_length=255,
                                       verbose_name="Check off all the social media accounts you can manage\
                                    for your proposed community:")
    other_account = models.CharField(
        blank=True, max_length=25, verbose_name="Other social channel(Please specify)")
    demographic_target_count = models.TextField(blank=True, verbose_name="Who will it serve (\
                                                explain target demographics and number of people):")
    purpose = models.TextField(blank=True, verbose_name="Explain the purpose and\
                               need for this group or account:")
    is_avail_volunteer = models.CharField(default=None, max_length=25, choices=YES_NO_CHOICES,
                                          verbose_name="Do you have volunteers committed?")
    count_avail_volunteer = models.PositiveIntegerField(
        default=0, verbose_name="If yes, how many?")

    content_developer = models.TextField(blank=True, verbose_name="Explain the content of this group.\
                                         What service will this group provide (example: discussion,\
                                         linksharing, support)? Who will develop the content? What\
                                         kind of content will be shared in the group? How often\
                                         will moderators post/engage with users?")
    selection_criteria = models.TextField(blank=True,
                                          verbose_name="Will there be screening of new members of will this group be open to anyone?\
         If there will be screening,what will the criteria for membership be?")
    is_real_time = models.TextField(blank=True,
                                    verbose_name=" Will there be real-time meetings in addition to an online community?\
         (Example, at the Grace Hopper Celebration; regional meetings; etc)")
    user = models.ForeignKey(
        SystersUser, verbose_name="Created by", related_name="requestor", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, verbose_name="Approved")
    approved_by = models.ForeignKey(SystersUser, blank=True, null=True,
                                    verbose_name='Approved by', on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date created")

    def __str__(self):
        return self.name

    def get_fields(self):
        """Get model fields of a RequestCommunity object
        :return: list of tuples (fieldname, fieldvalue)
        """
        return [(field.name, getattr(self, field.name)) for field in
                RequestCommunity._meta.fields]

    def get_verbose_fields(self):
        """Get verbose names of RequestCommunity object's model fields
        :return: list of tuples (verbosefieldname, fieldvalue)
        """

        return [(field.verbose_name, getattr(self, field.name)) for field in
                RequestCommunity._meta.fields]


class CommunityPage(Post):
    """Model to represent an arbitrary community page"""
    order = models.IntegerField(verbose_name="Order")
    community = models.ForeignKey(Community, verbose_name="Community", on_delete=models.CASCADE)

    class Meta:
        unique_together = (('community', 'slug'), ('community', 'order'))

    def __str__(self):
        return "Page {0} of {1}".format(self.title, self.community)
