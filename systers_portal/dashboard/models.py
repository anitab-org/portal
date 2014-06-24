from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from cms.models.pagemodel import Page


class SysterUser(models.Model):
    """Profile model to store additional information about a user"""
    user = models.OneToOneField(User)
    country = CountryField(blank=True, null=True)
    blog_url = models.URLField(max_length=255, blank=True, null=True)
    homepage_url = models.URLField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='photos/',
                                        default='photos/dummy.jpeg',
                                        blank=True,
                                        null=True)

    def __unicode__(self):
        firstname = self.user.first_name
        lastname = self.user.last_name
        if firstname and lastname:
            return "{0} {1}".format(self.user.first_name, self.user.last_name)
        else:
            return self.user.username


class Community(models.Model):
    """Model to represent a Syster Community"""
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=True, null=True)
    mailing_list = models.EmailField(max_length=255, blank=True, null=True)
    resource_area = models.URLField(max_length=255, blank=True, null=True)
    members = models.ManyToManyField(SysterUser, blank=True, null=True)
    community_admin = models.ForeignKey(User)
    parent_community = models.ForeignKey('self', blank=True, null=True)
    website = models.URLField(max_length=30, blank=True, null=True)
    facebook = models.URLField(max_length=30, blank=True, null=True)
    googleplus = models.URLField(max_length=30, blank=True, null=True)
    twitter = models.URLField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    """Model to represent the tags a resource can have"""
    name = models.CharField(max_length=30, blank=False, null=False)

    def __unicode__(self):
        return self.name


class Resource_Type(models.Model):
    """Model to represent the types a resource can have"""
    name = models.CharField(max_length=30, blank=False, null=False)

    def __unicode__(self):
        return self.name


class News(models.Model):
    """Model to represent a News section on Community resource area"""
    title = models.CharField(max_length=255, blank=False, null=False)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(SysterUser)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    is_public = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return "{0} of {1} Community".format(self.title, self.community.name)


class CommunityPages(models.Model):
    """Model to represent community pages"""
    title = models.CharField(max_length=30, blank=False, null=False)
    page = models.OneToOneField(Page)
    community = models.ForeignKey(Community)

    def __unicode__(self):
        return "{0} of {1} Community".format(self.page, self.community.name)


class Resource(models.Model):
    """Model to represent a Resources section on Community resource area"""
    title = models.CharField(max_length=255, blank=False, null=False)
    community = models.ForeignKey(Community)
    author = models.ForeignKey(User)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=False)
    is_public = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    resource_type = models.ForeignKey(Resource_Type, blank=True, null=True)
    content = models.TextField()

    def __unicode__(self):
        return "{0} of {0} Community".format(self.title, self.community.name)
